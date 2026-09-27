from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=True)
    name = Column(String, nullable=False)

    event = relationship("Event", backref="teams")
    track = relationship("Track", backref="teams")
