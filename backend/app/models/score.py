from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)

    submission_id = Column(
        Integer,
        ForeignKey("submissions.id", ondelete="CASCADE"),
        nullable=False,
    )

    judge_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    functionality = Column(Integer, nullable=False)
    quality = Column(Integer, nullable=False)
    innovation = Column(Integer, nullable=False)

    comment = Column(String, nullable=True)

    # SHA-256 hash of the finalized scorecard.
    # 64 hexadecimal characters.
    scorecard_hash = Column(
        String(64),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    submission = relationship(
        "Submission",
        back_populates="scores",
    )

    judge = relationship(
        "User",
        backref="scores_given",
    )