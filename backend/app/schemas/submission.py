from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class SubmissionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    team_id: int


class SubmissionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None


class SubmissionResponse(SubmissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team_id: int
    is_locked: bool
    submitted_at: Optional[datetime] = None
