from typing import Any, Dict, List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.core.security import extract_user_role, verify_supabase_token

security_scheme = HTTPBearer(auto_error=True)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> Dict[str, Any]:
    """
    Validates Supabase Bearer JWT and extracts user payload.
    Raises 401 Unauthorized if invalid or expired.
    """
    token = credentials.credentials
    try:
        payload = verify_supabase_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired. Please sign in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing user ID (sub).",
            headers={"WWW-Authenticate": "Bearer"},
        )

    role = extract_user_role(payload)

    return {
        "id": user_id,
        "email": payload.get("email"),
        "role": role,
        "payload": payload,
    }


def require_role(allowed_roles: List[str]):
    """
    Dependency factory to enforce Role-Based Access Control (RBAC).
    Usage:
        @router.post("/judging", dependencies=[Depends(require_role(["judge", "admin"]))])
    """
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        user_role = current_user.get("role", "participant")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: User role '{user_role}' is not in allowed roles {allowed_roles}",
            )
        return current_user

    return role_checker
