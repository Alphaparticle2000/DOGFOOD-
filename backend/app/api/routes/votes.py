from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.submission import Submission
from backend.app.models.vote import Vote
from backend.app.schemas.vote import (
    VoteCreate,
    VoteResponse,
    VoteCount,
)
from backend.app.services.audit import record_audit
from backend.app.services.vote_abuse import (
    check_rate_limit,
    calculate_vote_anomaly,
)


router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post(
    "",
    response_model=VoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def cast_vote(
    vote_in: VoteCreate,
    request: Request,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    submission = (
        db.query(Submission)
        .filter(Submission.id == vote_in.submission_id)
        .first()
    )

    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found.",
        )

    user_id = current_user["id"]

    # Rate-limit by authenticated user.
    try:
        check_rate_limit(str(user_id))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        )

    existing_vote = (
        db.query(Vote)
        .filter(
            Vote.submission_id == vote_in.submission_id,
            Vote.user_id == user_id,
        )
        .first()
    )

    if existing_vote:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already voted for this submission.",
        )

    ip_address = (
        request.client.host
        if request.client
        else None
    )

    user_agent = request.headers.get("user-agent")
    fingerprint = request.headers.get("x-browser-fingerprint")

    recent_vote_count = (
        db.query(Vote)
        .filter(Vote.user_id == user_id)
        .count()
    )

    same_ip_count = (
        db.query(Vote)
        .filter(Vote.ip_address == ip_address)
        .count()
        if ip_address
        else 0
    )

    same_fingerprint_count = (
        db.query(Vote)
        .filter(Vote.fingerprint == fingerprint)
        .count()
        if fingerprint
        else 0
    )

    anomaly = calculate_vote_anomaly(
        recent_vote_count=recent_vote_count,
        same_ip_count=same_ip_count,
        same_fingerprint_count=same_fingerprint_count,
    )

    vote = Vote(
        submission_id=vote_in.submission_id,
        user_id=user_id,
        ip_address=ip_address,
        user_agent=user_agent,
        fingerprint=fingerprint,
    )

    db.add(vote)
    db.flush()

    record_audit(
        db,
        actor_id=str(user_id),
        action="vote_cast",
        entity_type="vote",
        entity_id=str(vote.id),
        ip_address=ip_address,
        after_data={
            "submission_id": vote.submission_id,
            "user_id": str(vote.user_id),
            "anomaly_flag": anomaly,
            "ip_address": ip_address,
            "fingerprint": fingerprint,
        },
    )

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
        db.query(Vote)
        .filter(Vote.submission_id == submission_id)
        .count()
    )

    return VoteCount(
        submission_id=submission_id,
        votes=count,
    )