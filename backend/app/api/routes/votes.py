from collections import defaultdict
from time import monotonic
from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.api.dependencies import get_current_user
from backend.app.models.vote import Vote
from backend.app.models.submission import Submission
from backend.app.schemas.vote import VoteCreate, VoteResponse, VoteCount


router = APIRouter(prefix="/votes", tags=["Votes"])


# Simple process-local rate limiter.
# This is intentionally lightweight for the hackathon implementation.
_vote_requests: Dict[str, list[float]] = defaultdict(list)

RATE_LIMIT = 10
RATE_WINDOW_SECONDS = 60


def check_vote_rate_limit(ip: str) -> None:
    now = monotonic()

    timestamps = _vote_requests[ip]

    # Remove requests outside the window.
    _vote_requests[ip] = [
        timestamp
        for timestamp in timestamps
        if now - timestamp < RATE_WINDOW_SECONDS
    ]

    if len(_vote_requests[ip]) >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many vote requests. Please try again later.",
        )

    _vote_requests[ip].append(now)


@router.post("", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
def cast_vote(
    payload: VoteCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Cast one community vote for a submission.

    Community votes are stored separately from official judging scores.
    """

    client_ip = request.client.host if request.client else "unknown"

    check_vote_rate_limit(client_ip)

    submission = (
        db.query(Submission)
        .filter(Submission.id == payload.submission_id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found.",
        )

    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user ID is missing.",
        )

    existing_vote = (
        db.query(Vote)
        .filter(
            Vote.submission_id == payload.submission_id,
            Vote.user_id == user_id,
        )
        .first()
    )

    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already voted for this submission.",
        )

    user_agent = request.headers.get("user-agent")

    vote = Vote(
        submission_id=payload.submission_id,
        user_id=user_id,
        ip_address=client_ip,
        user_agent=user_agent,
    )

    db.add(vote)
    db.commit()
    db.refresh(vote)

    return vote


@router.get(
    "/submission/{submission_id}",
    response_model=VoteCount,
)
def get_vote_count(
    submission_id: int,
    db: Session = Depends(get_db),
):
    """
    Public community vote count.
    """

    submission = (
        db.query(Submission)
        .filter(Submission.id == submission_id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found.",
        )

    count = (
        db.query(func.count(Vote.id))
        .filter(Vote.submission_id == submission_id)
        .scalar()
    )

    return VoteCount(
        submission_id=submission_id,
        votes=count or 0,
    )