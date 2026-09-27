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
    Extracts the user's role from Supabase JWT claims:
    Checks user_metadata, app_metadata, or the top-level role claim.
    """
    user_meta = payload.get("user_metadata") or {}
    app_meta = payload.get("app_metadata") or {}

    return (
        user_meta.get("role")
        or app_meta.get("role")
        or payload.get("role")
        or "participant"
    )
