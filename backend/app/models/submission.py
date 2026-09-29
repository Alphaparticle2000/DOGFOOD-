from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.core.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String, nullable=True)
    demo_url = Column(String, nullable=True)
    is_locked = Column(Boolean, default=False, nullable=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    team = relationship("Team", back_populates="submissions")
    comments = relationship("Comment", back_populates="submission", cascade="all, delete-orphan")
    scores = relationship("Score", back_populates="submission", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="submission", cascade="all, delete-orphan")
