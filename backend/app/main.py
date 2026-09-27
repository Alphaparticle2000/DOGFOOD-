from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import Base, engine, get_db
from backend.app.api.routes import api_router
import backend.app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist on startup (useful for dev / test environments)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ------------------------------------------------------------------------------
# CORS Middleware Configuration (enabling Himanshu's React / Vite client)
# ------------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """Liveness probe: verifies that the FastAPI server is running."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "environment": settings.APP_ENV,
    }


@app.get("/health/db", tags=["Health"])
def health_db_check(db: Session = Depends(get_db)):
    """Readiness probe: verifies active connectivity to Supabase PostgreSQL."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "detail": str(e),
        }


# Mount application domain routes under /api
app.include_router(api_router)
