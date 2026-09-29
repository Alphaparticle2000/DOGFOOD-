from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

# Supabase and cloud providers often prefix postgres URIs with postgres://
# SQLAlchemy 1.4+ requires postgresql://, and default PostgreSQL driver in SQLAlchemy 2.0+ is psycopg (v3).
# We ensure postgresql+psycopg2:// is used if no explicit driver dialect is given for maximum reliability.
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

# Configure SQLAlchemy engine with pool_pre_ping for resilient cloud connections
engine = create_engine(
    database_url,
    pool_pre_ping=True,
    pool_recycle=300,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """FastAPI dependency to yield a database session and ensure clean close."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
