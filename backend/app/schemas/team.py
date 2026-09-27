from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from backend.app.schemas.user import UserProfileResponse


class TeamMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_id: int
    user_id: UUID
    is_lead: bool
    joined_at: Optional[datetime] = None
    user: Optional[UserProfileResponse] = None


class TeamMemberAdd(BaseModel):
    user_id: UUID
    is_lead: bool = False


class TeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Team name")
    event_id: int
    track_id: Optional[int] = None


class TeamCreate(TeamBase):
    pass


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    track_id: Optional[int] = None


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    event_id: int
    track_id: Optional[int] = None
    created_at: Optional[datetime] = None
    members: List[TeamMemberResponse] = []
