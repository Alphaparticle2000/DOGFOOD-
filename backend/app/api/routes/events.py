from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.app.api.dependencies import require_role
from backend.app.core.database import get_db
from backend.app.models.event import Event
from backend.app.models.track import Track
from backend.app.schemas.event import EventCreate, EventResponse, EventUpdate
from backend.app.schemas.track import TrackCreate, TrackResponse

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("", response_model=List[EventResponse])
def list_events(
    active_only: bool = True,
    db: Session = Depends(get_db),
):
    """List hackathon events."""
    query = db.query(Event).options(joinedload(Event.tracks))
    if active_only:
        query = query.filter(Event.is_active == True)  # noqa: E712
    return query.order_by(Event.created_at.desc()).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    """Get single event with associated tracks."""
    event = (
        db.query(Event)
        .options(joinedload(Event.tracks))
        .filter(Event.id == event_id)
        .first()
    )
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return event


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def create_event(
    event_in: EventCreate,
    db: Session = Depends(get_db),
):
    """Create a new hackathon event (organizer/admin only)."""
    event = Event(**event_in.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.put(
    "/{event_id}",
    response_model=EventResponse,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def update_event(
    event_id: int,
    event_in: EventUpdate,
    db: Session = Depends(get_db),
):
    """Update hackathon event (organizer/admin only)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    for field, val in event_in.model_dump(exclude_unset=True).items():
        setattr(event, field, val)

    db.commit()
    db.refresh(event)
    return event


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    """Delete hackathon event (organizer/admin only)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    db.delete(event)
    db.commit()
    return None


# ------------------------------------------------------------------------------
# Tracks within an event
# ------------------------------------------------------------------------------

@router.get("/{event_id}/tracks", response_model=List[TrackResponse])
def list_event_tracks(
    event_id: int,
    db: Session = Depends(get_db),
):
    """List all tracks for a specific event."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return db.query(Track).filter(Track.event_id == event_id).all()


@router.post(
    "/{event_id}/tracks",
    response_model=TrackResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(["organizer", "admin"]))],
)
def create_event_track(
    event_id: int,
    track_in: TrackCreate,
    db: Session = Depends(get_db),
):
    """Add a track to an event (organizer/admin only)."""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )

    track = Track(event_id=event_id, **track_in.model_dump())
    db.add(track)
    db.commit()
    db.refresh(track)
    return track
