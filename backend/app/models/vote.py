from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)

    submission_id = Column(
        Integer,
        ForeignKey(
            "submissions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    ip_address = Column(
        String(45),
        nullable=True,
        index=True,
    )

    user_agent = Column(
        String(512),
        nullable=True,
    )

    fingerprint = Column(
        String(128),
        nullable=True,
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    submission = relationship(
        "Submission",
        back_populates="votes",
    )

    user = relationship(
        "User",
        backref="votes_cast",
    )

    __table_args__ = (
        UniqueConstraint(
            "submission_id",
            "user_id",
            name="uq_vote_submission_user",
        ),
    )