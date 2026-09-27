import pytest
from backend.app.core.security import extract_user_role


def test_extract_user_role_supabase_default():
    """Verify that a user with Supabase's default 'authenticated' role resolves to 'participant'."""
    payload = {
        "sub": "test-uuid-1",
        "email": "user@example.com",
        "role": "authenticated",
    }
    assert extract_user_role(payload) == "participant"


def test_extract_user_role_user_metadata():
    """Verify that a custom role in user_metadata is correctly extracted."""
    payload = {
        "sub": "test-uuid-2",
        "email": "judge@example.com",
        "role": "authenticated",
        "user_metadata": {"role": "judge"},
    }
    assert extract_user_role(payload) == "judge"


def test_extract_user_role_app_metadata():
    """Verify that admin role in app_metadata takes priority."""
    payload = {
        "sub": "test-uuid-3",
        "email": "admin@example.com",
        "role": "authenticated",
        "app_metadata": {"role": "admin"},
        "user_metadata": {"role": "participant"},
    }
    assert extract_user_role(payload) == "admin"
