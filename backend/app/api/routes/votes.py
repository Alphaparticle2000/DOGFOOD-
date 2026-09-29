from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.submission import Submission
from backend.app.models.vote import Vote
from backend.app.schemas.vote import VoteCount, VoteCreate, VoteResponse
from backend.app.services.vote_abuse import (
    calculate_vote_anomaly,
    check_rate_limit,
)


router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def cast_vote(
    payload: VoteCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Cast a community vote.

    Community votes remain completely separate from official judging scores.
    """

    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")[:512]

    fingerprint = request.headers.get(
        "x-browser-fingerprint"
    )

    if fingerprint:
        fingerprint = fingerprint[:128]

    user_id = current_user.get("id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user ID is missing.",
        )

    # Rate-limit by authenticated identity.
    try:
        check_rate_limit(f"user:{user_id}")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        )

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

    # Abuse telemetry.
    recent_vote_count = (
        db.query(func.count(Vote.id))
        .filter(Vote.ip_address == client_ip)
        .scalar()
        or 0
    )

    same_fingerprint_count = 0

    if fingerprint:
        same_fingerprint_count = (
            db.query(func.count(Vote.id))
            .filter(Vote.fingerprint == fingerprint)
            .scalar()
            or 0
        )

    anomaly = calculate_vote_anomaly(
        recent_vote_count=recent_vote_count,
        same_ip_count=recent_vote_count,
        same_fingerprint_count=same_fingerprint_count,
    )

    # We don't silently destroy suspicious votes.
    # Store them and expose the anomaly to organizers later.
    vote = Vote(
        submission_id=payload.submission_id,
        user_id=user_id,
        ip_address=client_ip,
        user_agent=user_agent,
        fingerprint=fingerprint,
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
        or 0
    )

    return VoteCount(
        submission_id=submission_id,
        votes=count,
    )