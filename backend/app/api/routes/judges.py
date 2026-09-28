from typing import Any, Dict

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from backend.app.api.dependencies import (
    get_current_user,
    require_role,
)
from backend.app.core.database import get_db
from backend.app.models.judge import Judge
from backend.app.models.event import Event
from backend.app.models.track import Track
from backend.app.models.submission import Submission
from backend.app.models.score import Score
from backend.app.models.team_member import TeamMember
from backend.app.models.user import User


router = APIRouter(
    prefix="/judges",
    tags=["Judges"],
)


@router.post(
    "/assign",
    status_code=status.HTTP_201_CREATED,
)
def assign_judge(
    user_id: str,
    event_id: int,
    track_id: int | None = None,
    current_user: Dict[str, Any] = Depends(
        require_role(["organizer", "admin"])
    ),
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    event = (
        db.query(Event)
        .filter(Event.id == event_id)
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    if track_id is not None:

        track = (
            db.query(Track)
            .filter(
                Track.id == track_id,
                Track.event_id == event_id,
            )
            .first()
        )

        if not track:
            raise HTTPException(
                status_code=404,
                detail="Track not found for this event.",
            )

    existing = (
        db.query(Judge)
        .filter(
            Judge.user_id == user_id,
            Judge.event_id == event_id,
        )
        .all()
    )

    # Same assignment already exists.
    if any(
        judge.track_id == track_id
        for judge in existing
    ):
        raise HTTPException(
            status_code=409,
            detail="Judge is already assigned to this event/track.",
        )

    # Event-wide assignment conflicts with everything.
    if any(
        judge.track_id is None
        for judge in existing
    ):
        raise HTTPException(
            status_code=409,
            detail="Judge already has an event-wide assignment.",
        )

    # New event-wide assignment conflicts with existing tracks.
    if track_id is None and existing:
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot create an event-wide assignment "
                "while track assignments already exist."
            ),
        )

    judge = Judge(
        user_id=user_id,
        event_id=event_id,
        track_id=track_id,
    )

    db.add(judge)
    db.commit()
    db.refresh(judge)

    return {
        "message": "Judge assigned successfully.",
        "judge_id": judge.id,
        "user_id": str(judge.user_id),
        "event_id": judge.event_id,
        "track_id": judge.track_id,
    }


@router.get(
    "/me/progress",
)
def judge_progress(
    current_user: Dict[str, Any] = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    user_id = current_user["id"]

    assignments = (
        db.query(Judge)
        .filter(
            Judge.user_id == user_id
        )
        .all()
    )

    if not assignments:
        raise HTTPException(
            status_code=403,
            detail="You are not assigned as a judge.",
        )

    assigned = 0
    completed = 0

    for assignment in assignments:

        query = (
            db.query(Submission)
            .join(
                Submission.team
            )
            .filter(
                Submission.is_locked.is_(True),
                Submission.team.has(
                    event_id=assignment.event_id
                ),
            )
        )

        if assignment.track_id is not None:
            query = query.filter(
                Submission.team.has(
                    track_id=assignment.track_id
                )
            )

        submissions = query.all()

        for submission in submissions:

            # Own team cannot be judged.
            own_team = (
                db.query(TeamMember)
                .filter(
                    TeamMember.team_id
                    == submission.team_id,
                    TeamMember.user_id
                    == user_id,
                )
                .first()
            )

            if own_team:
                continue

            assigned += 1

            score = (
                db.query(Score)
                .filter(
                    Score.submission_id
                    == submission.id,
                    Score.judge_id
                    == user_id,
                )
                .first()
            )

            if score:
                completed += 1

    remaining = max(
        assigned - completed,
        0,
    )

    percentage = (
        round(
            completed / assigned * 100,
            2,
        )
        if assigned
        else 0.0
    )

    return {
        "assigned": assigned,
        "completed": completed,
        "remaining": remaining,
        "completion_percentage": percentage,
    }