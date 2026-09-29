from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from backend.app.core.database import Base


class Rubric(Base):
    __tablename__ = "rubrics"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )

    track_id = Column(
        Integer,
        ForeignKey("tracks.id", ondelete="CASCADE"),
        nullable=True,
    )

    name = Column(String, nullable=False)

    criteria_weights = Column(JSON, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    event = relationship("Event")

    track = relationship("Track")

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "track_id",
            "name",
            name="uq_rubric_event_track_name",
        ),
    )