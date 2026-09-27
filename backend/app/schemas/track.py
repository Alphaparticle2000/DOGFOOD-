from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TrackBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name of the hackathon track")
    description: Optional[str] = Field(None, description="Detailed track criteria or topic")


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class TrackResponse(TrackBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_id: int
