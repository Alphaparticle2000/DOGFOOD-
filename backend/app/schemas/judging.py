from pydantic import BaseModel, Field


class ScoreSubmission(BaseModel):
    functionality: int = Field(
        ge=1,
        le=5,
        description="Functionality score from 1 to 5.",
    )
    quality: int = Field(
        ge=1,
        le=5,
        description="Quality score from 1 to 5.",
    )
    innovation: int = Field(
        ge=1,
        le=5,
        description="Innovation score from 1 to 5.",
    )
    comment: str = Field(
        default="",
        max_length=2000,
        description="Optional judge feedback.",
    )


class ScoreResponse(BaseModel):
    message: str
    judge: str
    project: str
    criteria: dict[str, int]
    comment: str


class ProjectResultResponse(BaseModel):
    project: str
    judge_count: int
    criteria: dict[str, float]
    overall_average: float
    comments: list[str]