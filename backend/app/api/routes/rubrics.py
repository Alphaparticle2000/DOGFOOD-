from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from backend.app.api.dependencies import require_role
from backend.app.core.database import get_db
from backend.app.models.event import Event
from backend.app.models.rubric import Rubric
from backend.app.models.track import Track
from backend.app.schemas.rubric import (
    RubricCreate,
    RubricResponse,
)


router = APIRouter(
    prefix="/rubrics",
    tags=["Rubrics"],
)


@router.post(
    "",
    response_model=RubricResponse,
    status_code=201,
)
def create_rubric(
    data: RubricCreate,
    current_user=Depends(
        require_role(
            ["organizer", "admin"]
        )
    ),
    db: Session = Depends(get_db),
):

    event = (
        db.query(Event)
        .filter(
            Event.id == data.event_id
        )
        .first()
    )

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    if data.track_id is not None:

        track = (
            db.query(Track)
            .filter(
                Track.id == data.track_id,
                Track.event_id == data.event_id,
            )
            .first()
        )

        if not track:
            raise HTTPException(
                status_code=404,
                detail="Track not found for this event.",
            )

    rubric = Rubric(
        event_id=data.event_id,
        track_id=data.track_id,
        name=data.name,
        criteria_weights=data.criteria_weights,
        is_active=data.is_active,
    )

    db.add(rubric)
    db.commit()
    db.refresh(rubric)

    return rubric


@router.get(
    "/event/{event_id}",
    response_model=list[RubricResponse],
)
def get_event_rubrics(
    event_id: int,
    track_id: int | None = None,
    db: Session = Depends(get_db),
):

    query = (
        db.query(Rubric)
        .filter(
            Rubric.event_id == event_id,
            Rubric.is_active.is_(True),
        )
    )

    if track_id is not None:
        query = query.filter(
            (Rubric.track_id == track_id)
            | (Rubric.track_id.is_(None))
        )

    return query.order_by(
        Rubric.id.desc()
    ).all()