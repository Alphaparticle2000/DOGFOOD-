import uuid
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.event import Event
from backend.app.models.team import Team
from backend.app.models.team_member import TeamMember
from backend.app.models.track import Track
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.team import (
    TeamMemberAdd,
    TeamCreate,
    TeamResponse,
    TeamUpdate,
)

router = APIRouter(prefix="/teams", tags=["Teams"])


def _ensure_user_exists(db: Session, current_user: Dict[str, Any]) -> User:
    """Ensure user exists in public.users, provisioning if needed."""
    user_uuid = uuid.UUID(str(current_user["id"]))
    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        role_str = current_user.get("role", "participant")
        try:
            role_enum = RoleEnum(role_str)
        except ValueError:
            role_enum = RoleEnum.participant

        user = User(
            id=user_uuid,
            email=current_user.get("email") or f"{user_uuid}@supabase.user",
            name=current_user.get("payload", {}).get("user_metadata", {}).get("full_name"),
            role=role_enum,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


def _is_team_lead_or_admin(team: Team, user_id: uuid.UUID, user_role: str) -> bool:
    """Check if the user is the leader of the team or an admin/organizer."""
    if user_role in ("admin", "organizer"):
        return True
    return any(m.user_id == user_id and m.is_lead for m in team.members)


@router.get("", response_model=List[TeamResponse])
def list_teams(
    event_id: Optional[int] = Query(None, description="Filter teams by event ID"),
    track_id: Optional[int] = Query(None, description="Filter teams by track ID"),
    db: Session = Depends(get_db),
):
    """List teams with optional event and track filters."""
    query = (
        db.query(Team)
        .options(
            joinedload(Team.members).joinedload(TeamMember.user)
        )
    )
    if event_id is not None:
        query = query.filter(Team.event_id == event_id)
    if track_id is not None:
        query = query.filter(Team.track_id == track_id)

    return query.order_by(Team.created_at.desc()).all()


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db),
):
    """Get single team with full member roster."""
    team = (
        db.query(Team)
        .options(
            joinedload(Team.members).joinedload(TeamMember.user)
        )
        .filter(Team.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )
    return team


@router.post("", response_model=TeamResponse, status_code=status.HTTP_201_CREATED)
def create_team(
    team_in: TeamCreate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new team for an event.
    Automatically assigns the authenticated user as the team lead.
    """
    # 1. Verify event exists and is active
    event = db.query(Event).filter(Event.id == team_in.event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {team_in.event_id} not found",
        )
    if not event.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create team: this event is not active",
        )

    # 2. Verify track if provided
    if team_in.track_id is not None:
        track = db.query(Track).filter(
            Track.id == team_in.track_id,
            Track.event_id == team_in.event_id,
        ).first()
        if not track:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Track ID {team_in.track_id} is not part of event {team_in.event_id}",
            )

    # 3. Ensure user exists
    user = _ensure_user_exists(db, current_user)

    # 4. Check if user already in a team for this event
    existing_membership = (
        db.query(TeamMember)
        .join(Team)
        .filter(Team.event_id == team_in.event_id, TeamMember.user_id == user.id)
        .first()
    )
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already a member of a team in this event",
        )

    # 5. Create team and add user as lead
    team = Team(
        name=team_in.name,
        event_id=team_in.event_id,
        track_id=team_in.track_id,
    )
    db.add(team)
    db.flush()

    lead_member = TeamMember(
        team_id=team.id,
        user_id=user.id,
        is_lead=True,
    )
    db.add(lead_member)
    db.commit()

    return (
        db.query(Team)
        .options(joinedload(Team.members).joinedload(TeamMember.user))
        .filter(Team.id == team.id)
        .first()
    )


@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id: int,
    team_in: TeamUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update team details (team lead or admin/organizer only)."""
    team = (
        db.query(Team)
        .options(joinedload(Team.members))
        .filter(Team.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    user_uuid = uuid.UUID(str(current_user["id"]))
    user_role = current_user.get("role", "participant")
    if not _is_team_lead_or_admin(team, user_uuid, user_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team leads or organizers can update team details",
        )

    if team_in.track_id is not None:
        track = db.query(Track).filter(
            Track.id == team_in.track_id,
            Track.event_id == team.event_id,
        ).first()
        if not track:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Track ID {team_in.track_id} is not valid for this event",
            )

    for field, val in team_in.model_dump(exclude_unset=True).items():
        setattr(team, field, val)

    db.commit()
    return (
        db.query(Team)
        .options(joinedload(Team.members).joinedload(TeamMember.user))
        .filter(Team.id == team.id)
        .first()
    )


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team(
    team_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a team (team lead or admin/organizer only)."""
    team = (
        db.query(Team)
        .options(joinedload(Team.members))
        .filter(Team.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    user_uuid = uuid.UUID(str(current_user["id"]))
    user_role = current_user.get("role", "participant")
    if not _is_team_lead_or_admin(team, user_uuid, user_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team leads or organizers can delete a team",
        )

    db.delete(team)
    db.commit()
    return None


# ------------------------------------------------------------------------------
# Team Members Management
# ------------------------------------------------------------------------------

@router.post("/{team_id}/members", response_model=TeamResponse)
def add_team_member(
    team_id: int,
    member_in: TeamMemberAdd,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Add a member to the team (team lead or admin/organizer only)."""
    team = (
        db.query(Team)
        .options(joinedload(Team.members))
        .filter(Team.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    user_uuid = uuid.UUID(str(current_user["id"]))
    user_role = current_user.get("role", "participant")
    if not _is_team_lead_or_admin(team, user_uuid, user_role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only team leads or organizers can add members",
        )

    # Verify user to add exists
    target_user = db.query(User).filter(User.id == member_in.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {member_in.user_id} not found",
        )

    # Check if target user is already in a team for this event
    existing = (
        db.query(TeamMember)
        .join(Team)
        .filter(Team.event_id == team.event_id, TeamMember.user_id == member_in.user_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already registered in a team for this event",
        )

    new_member = TeamMember(
        team_id=team.id,
        user_id=member_in.user_id,
        is_lead=member_in.is_lead,
    )
    db.add(new_member)
    db.commit()

    return (
        db.query(Team)
        .options(joinedload(Team.members).joinedload(TeamMember.user))
        .filter(Team.id == team.id)
        .first()
    )


@router.delete("/{team_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_team_member(
    team_id: int,
    user_id: uuid.UUID,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove a member from team (team lead, admin, or the user themselves)."""
    team = (
        db.query(Team)
        .options(joinedload(Team.members))
        .filter(Team.id == team_id)
        .first()
    )
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with ID {team_id} not found",
        )

    caller_uuid = uuid.UUID(str(current_user["id"]))
    caller_role = current_user.get("role", "participant")

    is_self = caller_uuid == user_id
    is_lead_or_admin = _is_team_lead_or_admin(team, caller_uuid, caller_role)

    if not (is_self or is_lead_or_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove this member",
        )

    member = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == user_id)
        .first()
    )
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found in this team",
        )

    db.delete(member)
    db.commit()
    return None
