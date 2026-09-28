from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session\

from backend.app.api.dependencies import (
    get_current_user,
    require_role,
)
from backend.app.models.rubric import Rubric
from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.judge import Judge
from backend.app.models.score import Score
from backend.app.models.submission import Submission
from backend.app.models.team_member import TeamMember
from backend.app.schemas.judging import ScoreSubmission, ScoreResponse
from backend.app.services.judging import (
    ScoreInput,
    validate_score,
    InvalidScoreError,
)


router = APIRouter(prefix="/judging", tags=["Judging"])


@router.post(
    "/submissions/{submission_id}/score",
    response_model=ScoreResponse,
    status_code=status.HTTP_201_CREATED,
)
def score_submission(
    submission_id: int,
    score_in: ScoreSubmission,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # ---------------------------------------------------------
    # 1. Parse authenticated user ID
    # ---------------------------------------------------------
    try:
        judge_user_id = UUID(current_user["id"])
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authenticated user ID.",
        )

    # ---------------------------------------------------------
    # 2. Find submission
    # ---------------------------------------------------------
    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found.",
        )

    # ---------------------------------------------------------
    # 3. Get team
    # ---------------------------------------------------------
    team = submission.team

    if not team:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission is not associated with a team.",
        )

    # ---------------------------------------------------------
    # 4. Submission must be locked before judging
    # ---------------------------------------------------------
    if not submission.is_locked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission must be locked before it can be judged.",
        )

    # ---------------------------------------------------------
    # 5. Find judge assignment for this user + event
    # ---------------------------------------------------------
    judge = (
        db.query(Judge)
        .filter(
            Judge.user_id == judge_user_id,
            Judge.event_id == team.event_id,
        )
        .first()
    )

    if not judge:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not assigned as a judge for this event.",
        )

    # ---------------------------------------------------------
    # 6. Check track assignment
    #
    # NULL track_id = judge can judge all tracks in the event.
    # Otherwise, judge must be assigned to this team's track.
    # ---------------------------------------------------------
    if judge.track_id is not None and judge.track_id != team.track_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not assigned to this submission's track.",
        )

    # ---------------------------------------------------------
    # 7. Prevent self-judging
    # ---------------------------------------------------------
    team_membership = (
        db.query(TeamMember)
        .filter(
            TeamMember.team_id == team.id,
            TeamMember.user_id == judge_user_id,
        )
        .first()
    )

    if team_membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Judges cannot score their own team's submission.",
        )

    # ---------------------------------------------------------
    # 8. Prevent duplicate scoring
    # ---------------------------------------------------------
    existing_score = (
        db.query(Score)
        .filter(
            Score.submission_id == submission.id,
            Score.judge_id == judge_user_id,
        )
        .first()
    )

    if existing_score:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already scored this submission.",
        )

    # ---------------------------------------------------------
    # 9. Validate score using the judging service
    # ---------------------------------------------------------
    score_input = ScoreInput(
        functionality=score_in.functionality,
        quality=score_in.quality,
        innovation=score_in.innovation,
        comment=score_in.comment,
    )

    try:
        validate_score(score_input)
    except InvalidScoreError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )

    # ---------------------------------------------------------
    # 10. Save score
    # ---------------------------------------------------------
    score = Score(
        submission_id=submission.id,
        judge_id=judge_user_id,
        functionality=score_in.functionality,
        quality=score_in.quality,
        innovation=score_in.innovation,
        comment=score_in.comment,
    )

    db.add(score)
    db.commit()
    db.refresh(score)

    # ---------------------------------------------------------
    # 11. Return API response
    # ---------------------------------------------------------
    return ScoreResponse(
        message="Score submitted successfully.",
        judge=str(judge_user_id),
        project=str(submission.id),
        criteria={
            "functionality": score.functionality,
            "quality": score.quality,
            "innovation": score.innovation,
        },
        comment=score.comment or "",
    ) 
import csv
import io

from fastapi.responses import StreamingResponse

from backend.app.models.rubric import Rubric
from backend.app.services.judging import (
    DEFAULT_WEIGHTS,
    calculate_weighted_score,
    normalize_judge_scores,
)

@router.get(
    "/events/{event_id}/results",
)
def get_judging_results(
    event_id: int,
    current_user: Dict[str, Any] = Depends(
        require_role(["organizer", "admin", "judge"])
    ),
    db: Session = Depends(get_db),
):

    submissions = (
        db.query(Submission)
        .join(Submission.team)
        .filter(
            Submission.is_locked.is_(True),
            Submission.team.has(
                event_id=event_id
            ),
        )
        .all()
    )

    results = []

    for submission in submissions:

        scores = (
            db.query(Score)
            .filter(
                Score.submission_id
                == submission.id
            )
            .all()
        )

        rubric = (
            db.query(Rubric)
            .filter(
                Rubric.event_id == event_id,
                Rubric.is_active.is_(True),
                (
                    Rubric.track_id
                    == submission.team.track_id
                )
                | Rubric.track_id.is_(None),
            )
            .order_by(
                Rubric.track_id.desc()
            )
            .first()
        )

        weights = (
            rubric.criteria_weights
            if rubric
            else DEFAULT_WEIGHTS
        )

        if not scores:
            results.append(
                {
                    "submission_id": submission.id,
                    "title": submission.title,
                    "judge_count": 0,
                    "weighted_average": 0.0,
                    "normalized_average": 0.0,
                }
            )
            continue

        score_dicts = []

        for score in scores:

            criteria = {
                "functionality": score.functionality,
                "quality": score.quality,
                "innovation": score.innovation,
            }

            score_dicts.append(
                {
                    "id": score.id,
                    "judge": str(score.judge_id),
                    "project": str(submission.id),
                    "criteria": criteria,
                    "weights": weights,
                    "comment": score.comment or "",
                }
            )

        normalized = normalize_judge_scores(
            score_dicts
        )

        weighted_average = round(
            sum(
                item["raw_weighted_score"]
                for item in normalized
            )
            / len(normalized),
            2,
        )

        normalized_average = round(
            sum(
                item["normalized_score"]
                for item in normalized
            )
            / len(normalized),
            2,
        )

        results.append(
            {
                "submission_id": submission.id,
                "title": submission.title,
                "judge_count": len(scores),
                "weighted_average": weighted_average,
                "normalized_average": normalized_average,
            }
        )

    results.sort(
        key=lambda x: x["normalized_average"],
        reverse=True,
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        result["rank"] = index

    return {
        "event_id": event_id,
        "results": results,
    }


@router.get(
    "/events/{event_id}/export.csv",
)
def export_judging_csv(
    event_id: int,
    current_user: Dict[str, Any] = Depends(
        require_role(["organizer", "admin"])
    ),
    db: Session = Depends(get_db),
):

    submissions = (
        db.query(Submission)
        .join(Submission.team)
        .filter(
            Submission.is_locked.is_(True),
            Submission.team.has(
                event_id=event_id
            ),
        )
        .all()
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow(
        [
            "submission_id",
            "title",
            "judge_id",
            "functionality",
            "quality",
            "innovation",
            "weighted_score",
            "comment",
            "created_at",
        ]
    )

    for submission in submissions:

        scores = (
            db.query(Score)
            .filter(
                Score.submission_id
                == submission.id
            )
            .all()
        )

        rubric = (
            db.query(Rubric)
            .filter(
                Rubric.event_id == event_id,
                Rubric.is_active.is_(True),
                (
                    Rubric.track_id
                    == submission.team.track_id
                )
                | Rubric.track_id.is_(None),
            )
            .order_by(
                Rubric.track_id.desc()
            )
            .first()
        )

        weights = (
            rubric.criteria_weights
            if rubric
            else DEFAULT_WEIGHTS
        )

        for score in scores:

            criteria = {
                "functionality": score.functionality,
                "quality": score.quality,
                "innovation": score.innovation,
            }

            weighted = calculate_weighted_score(
                criteria,
                weights,
            )

            writer.writerow(
                [
                    submission.id,
                    submission.title,
                    str(score.judge_id),
                    score.functionality,
                    score.quality,
                    score.innovation,
                    weighted,
                    score.comment or "",
                    score.created_at,
                ]
            )

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=event_{event_id}_judging.csv"
            )
        },
    )