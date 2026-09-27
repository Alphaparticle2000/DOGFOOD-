from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import require_role
from backend.app.core.database import get_db
from backend.app.models.track import Track
from backend.app.schemas.track import TrackResponse, TrackUpdate

router = APIRouter(prefix="/tracks", tags=["Tracks"])


@router.get("/{track_id}", response_model=TrackResponse)
def get_track(
    track_id: int,
    db: Session = Depends(get_db),
):
    """Get single track by ID."""
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track with ID {track_id} not found",
        )
    return track


@router.put(
    "/{track_id}",
    response_model=TrackResponse,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def update_track(
    track_id: int,
    track_in: TrackUpdate,
    db: Session = Depends(get_db),
):
    """Update track details (organizer/admin only)."""
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track with ID {track_id} not found",
        )

    for field, val in track_in.model_dump(exclude_unset=True).items():
        setattr(track, field, val)

    db.commit()
    db.refresh(track)
    return track


@router.delete(
    "/{track_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def delete_track(
    track_id: int,
    db: Session = Depends(get_db),
):
    """Delete a track (organizer/admin only)."""
    track = db.query(Track).filter(Track.id == track_id).first()
    if not track:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track with ID {track_id} not found",
        )
    db.delete(track)
    db.commit()
    return None
