from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.track import TrackResponse


class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the hackathon event")
    description: Optional[str] = Field(None, description="Event description and guidelines")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    is_active: bool = True


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    submission_deadline: Optional[datetime] = None
    is_active: Optional[bool] = None


class EventResponse(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    tracks: List[TrackResponse] = []
