from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import require_role, get_current_user
from backend.app.core.database import get_db
from backend.app.models.submission import Submission
from backend.app.models.team import Team
from backend.app.models.event import Event
from backend.app.schemas.submission import SubmissionCreate, SubmissionResponse, SubmissionUpdate

router = APIRouter(prefix="/submissions", tags=["Submissions"])


def _get_team_and_event(db: Session, team_id: int):
    team = db.query(Team).filter(Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )
    event = db.query(Event).filter(Event.id == team.event_id).first()
    return team, event


def _check_deadline(event: Optional[Event]):
    if event and event.submission_deadline:
        deadline = event.submission_deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > deadline:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Submission deadline has passed for this event.",
            )


@router.get("", response_model=List[SubmissionResponse])
def list_submissions(
    team_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """List submissions, optionally filtered by team."""
    query = db.query(Submission)
    if team_id is not None:
        query = query.filter(Submission.team_id == team_id)
    return query.order_by(Submission.submitted_at.desc()).all()


@router.get("/{submission_id}", response_model=SubmissionResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
):
    """Get a single submission by ID."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found",
        )
    return submission


@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(
    submission_in: SubmissionCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a submission — blocked once the event's submission deadline has passed."""
    team, event = _get_team_and_event(db, submission_in.team_id)
    _check_deadline(event)

    submission = Submission(**submission_in.model_dump())
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.put("/{submission_id}", response_model=SubmissionResponse)
def update_submission(
    submission_id: int,
    submission_in: SubmissionUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a submission — blocked if locked or past deadline."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found",
        )

    if submission.is_locked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission is locked and cannot be edited.",
        )

    _, event = _get_team_and_event(db, submission.team_id)
    _check_deadline(event)

    for field, val in submission_in.model_dump(exclude_unset=True).items():
        setattr(submission, field, val)

    db.commit()
    db.refresh(submission)
    return submission


@router.delete(
    "/{submission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def delete_submission(
    submission_id: int,
    db: Session = Depends(get_db),
):
    """Delete a submission (organizer/admin only)."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found",
        )
    db.delete(submission)
    db.commit()
    return None


@router.post(
    "/{submission_id}/lock",
    response_model=SubmissionResponse,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def lock_submission(
    submission_id: int,
    db: Session = Depends(get_db),
):
    """Lock a submission so it can no longer be edited (organizer/admin only)."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Submission with ID {submission_id} not found",
        )
    submission.is_locked = True
    db.commit()
    db.refresh(submission)
    return submission