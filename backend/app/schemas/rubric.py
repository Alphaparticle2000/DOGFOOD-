from pydantic import BaseModel, Field, field_validator

from backend.app.services.judging import validate_rubric_weights


class RubricCreate(BaseModel):
    event_id: int

    track_id: int | None = None

    name: str = Field(
        min_length=1,
        max_length=255,
    )

    criteria_weights: dict[str, float]

    is_active: bool = True

    @field_validator("criteria_weights")
    @classmethod
    def validate_weights(
        cls,
        value: dict[str, float],
    ) -> dict[str, float]:
        return validate_rubric_weights(value)


class RubricResponse(BaseModel):
    id: int
    event_id: int
    track_id: int | None
    name: str
    criteria_weights: dict[str, float]
    is_active: bool

    class Config:
        from_attributes = True