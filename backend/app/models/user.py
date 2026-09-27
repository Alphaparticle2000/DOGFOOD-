from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base
import enum

class RoleEnum(str, enum.Enum):
    organizer = "organizer"
    judge = "judge"
    participant = "participant"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    supabase_id = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    name = Column(String)
