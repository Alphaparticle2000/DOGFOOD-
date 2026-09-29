import uuid


def test_get_current_user_me_auto_provisions(client, auth_headers):
    uid = str(uuid.uuid4())
    headers = auth_headers(role="participant", user_id=uid)
    token_headers = {"Authorization": headers["Authorization"]}

    res = client.get("/api/users/me", headers=token_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["id"] == uid
    assert data["role"] == "participant"


def test_update_user_profile(client, auth_headers):
    uid = str(uuid.uuid4())
    headers = auth_headers(role="participant", user_id=uid)
    token_headers = {"Authorization": headers["Authorization"]}

    # Update profile
    payload = {
        "name": "Jane Doe",
        "bio": "Fullstack builder",
        "avatar_url": "https://avatar.url/jane.png",
    }
    res = client.put("/api/users/me", json=payload, headers=token_headers)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Jane Doe"
    assert data["bio"] == "Fullstack builder"
    assert data["avatar_url"] == "https://avatar.url/jane.png"


def test_get_current_user_unauthorized(client):
    res = client.get("/api/users/me")
    assert res.status_code == 401
