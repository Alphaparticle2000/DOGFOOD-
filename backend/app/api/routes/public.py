from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["Public API"])


@router.get("/health")
def public_health():
    return {
        "status": "ok",
        "service": "DOGFOOD Public API",
    }