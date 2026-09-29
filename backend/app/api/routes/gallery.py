from typing import Any, Dict
import hashlib

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.submission import Submission
from backend.app.services.gallery import randomized_projects

router = APIRouter(prefix="/gallery", tags=["Gallery"])


def generate_session_seed(
    event_id: int,
    session_id: str,
) -> int:
    """
    Generate a deterministic seed for a gallery session.

    The same event + session ID always produces the same seed.
    """
    value = f"{event_id}:{session_id}".encode("utf-8")
    digest = hashlib.sha256(value).digest()
    return int.from_bytes(digest[:8], byteorder="big")


@router.get("/events/{event_id}")
def get_gallery(
    event_id: int,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session_id = request.headers.get("x-gallery-session")

    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="Missing X-Gallery-Session header.",
        )

    submissions = (
        db.query(Submission)
        .join(Submission.team)
        .filter(
            Submission.is_locked.is_(True),
            Submission.team.has(event_id=event_id),
        )
        .all()
    )

    seed = generate_session_seed(event_id, session_id)
    randomized = randomized_projects(submissions, seed)

    projects = []

    for submission in randomized:
        projects.append(
            {
                "submission_id": submission.id,
                "title": submission.title,
                "description": getattr(submission, "description", None),
                "team_id": submission.team_id,
            }
        )

    return {
        "event_id": event_id,
        "session_id": session_id,
        "seed": seed,
        "projects": projects,
    }