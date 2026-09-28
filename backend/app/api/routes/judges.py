from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import require_role
from backend.app.core.database import get_db
from backend.app.models.judge import Judge
from backend.app.models.event import Event
from backend.app.models.track import Track
from backend.app.models.user import User


router = APIRouter(prefix="/judges", tags=["Judges"])


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
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Track not found for this event.",
            )

    existing = (
        db.query(Judge)
        .filter(
            Judge.user_id == user_id,
            Judge.event_id == event_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already assigned as a judge for this event.",
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