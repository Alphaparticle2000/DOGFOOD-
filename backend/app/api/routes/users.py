import uuid
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.core.database import get_db
from backend.app.models.user import User, RoleEnum
from backend.app.schemas.user import UserProfileResponse, UserProfileUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get profile for currently authenticated Supabase user.
    Auto-provisions the user in public.users if they don't yet exist.
    """
    user_uuid = uuid.UUID(str(current_user["id"]))
    user = db.query(User).filter(User.id == user_uuid).first()

    if not user:
        # Auto-provision public user profile from verified Supabase token claims
        role_str = current_user.get("role", "participant")
        try:
            role_enum = RoleEnum(role_str)
        except ValueError:
            role_enum = RoleEnum.participant

        user = User(
            id=user_uuid,
            email=current_user.get("email") or f"{user_uuid}@supabase.user",
            name=current_user.get("payload", {}).get("user_metadata", {}).get("full_name")
            or current_user.get("payload", {}).get("user_metadata", {}).get("name"),
            role=role_enum,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


@router.put("/me", response_model=UserProfileResponse)
def update_current_user_profile(
    profile_data: UserProfileUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Update profile details for currently authenticated user.
    """
    user_uuid = uuid.UUID(str(current_user["id"]))
    user = db.query(User).filter(User.id == user_uuid).first()

    if not user:
        # If user record doesn't exist yet, call get profile logic to provision
        role_str = current_user.get("role", "participant")
        try:
            role_enum = RoleEnum(role_str)
        except ValueError:
            role_enum = RoleEnum.participant

        user = User(
            id=user_uuid,
            email=current_user.get("email") or f"{user_uuid}@supabase.user",
            role=role_enum,
        )
        db.add(user)

    update_dict = profile_data.model_dump(exclude_unset=True)
    for field, val in update_dict.items():
        setattr(user, field, val)

    db.commit()
    db.refresh(user)
    return user
