from datetime import datetime
from pydantic import BaseModel


class VoteCreate(BaseModel):
    submission_id: int


class VoteResponse(BaseModel):
    id: int
    submission_id: int
    user_id: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class VoteCount(BaseModel):
    submission_id: int
    votes: int