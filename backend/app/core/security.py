from typing import Any, Dict, Optional
import jwt
from backend.app.core.config import settings

ALGORITHM = "HS256"


def verify_supabase_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and validates a Supabase Auth JWT using the project's SUPABASE_JWT_SECRET.
    Returns the decoded payload if valid, otherwise raises jwt.PyJWTError.
    """
    if not settings.SUPABASE_JWT_SECRET:
        # In local dev without secret configured, decode without verification only if in debug mode
        if settings.DEBUG:
            return jwt.decode(token, options={"verify_signature": False})
        raise ValueError("SUPABASE_JWT_SECRET is not configured on the server.")

    # Supabase uses HS256 with the secret
    payload = jwt.decode(
        token,
        settings.SUPABASE_JWT_SECRET,
        algorithms=[ALGORITHM],
        audience="authenticated",
    )
    return payload


def extract_user_role(payload: Dict[str, Any]) -> str:
    """
    Extracts the user's role from Supabase JWT claims.
    Prioritizes app_metadata and user_metadata custom roles.
    Ignores the generic Supabase internal role 'authenticated'.
    Defaults to 'participant'.
    """
    user_meta = payload.get("user_metadata") or {}
    app_meta = payload.get("app_metadata") or {}

    custom_role = app_meta.get("role") or user_meta.get("role")
    if custom_role:
        return custom_role

    top_role = payload.get("role")
    if top_role and top_role != "authenticated":
        return top_role

    return "participant"

