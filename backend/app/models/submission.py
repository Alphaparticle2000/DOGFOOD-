from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    repo_url = Column(String)
    demo_url = Column(String)
    is_locked = Column(Boolean, default=False)
    submitted_at = Column(DateTime, server_default=func.now())

    team = relationship("Team", backref="submissions")
