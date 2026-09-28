from fastapi import APIRouter

from backend.app.api.routes.users import router as users_router
from backend.app.api.routes.events import router as events_router
from backend.app.api.routes.tracks import router as tracks_router
from backend.app.api.routes.teams import router as teams_router
from backend.app.api.routes.judging import router as judging_router
from backend.app.api.routes.judges import router as judges_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(events_router)
api_router.include_router(tracks_router)
api_router.include_router(teams_router)
api_router.include_router(judging_router)
api_router.include_router(judges_router)

__all__ = ["api_router"]
