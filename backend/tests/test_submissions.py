import uuid
from datetime import datetime, timedelta, timezone


def _admin_hdr(auth_headers):
    return {"Authorization": auth_headers(role="admin")["Authorization"]}


def _participant(auth_headers):
    uid = str(uuid.uuid4())
    hdr = {"Authorization": auth_headers(role="participant", user_id=uid)["Authorization"]}
    return uid, hdr


def _make_event(client, admin_hdr, deadline):
    res = client.post(
        "/api/events",
        json={
            "name": f"Submission Test Event {uuid.uuid4().hex[:8]}",
            "is_active": True,
            "submission_deadline": deadline.isoformat(),
        },
        headers=admin_hdr,
    )
    assert res.status_code == 201
    return res.json()["id"]


def _make_team(client, member_hdr, event_id):
    res = client.post(
        "/api/teams",
        json={"name": f"Team {uuid.uuid4().hex[:8]}", "event_id": event_id},
        headers=member_hdr,
    )
    assert res.status_code == 201
    return res.json()["id"]


def test_submission_requires_login(client):
    res = client.post("/api/submissions", json={"team_id": 1, "title": "No token"})
    assert res.status_code == 401


def test_submission_lifecycle_and_access_rules(client, auth_headers):
    admin_hdr = _admin_hdr(auth_headers)
    future = datetime.now(timezone.utc) + timedelta(days=7)
    event_id = _make_event(client, admin_hdr, future)

    _, member_hdr = _participant(auth_headers)
    _, outsider_hdr = _participant(auth_headers)
    team_id = _make_team(client, member_hdr, event_id)

    payload = {"team_id": team_id, "title": "My Project", "repo_url": "https://example.com/repo"}

    # A logged-in user who is not on the team is rejected
    res = client.post("/api/submissions", json=payload, headers=outsider_hdr)
    assert res.status_code == 403

    # A team member can create
    res = client.post("/api/submissions", json=payload, headers=member_hdr)
    assert res.status_code == 201
    sub = res.json()
    assert sub["team_id"] == team_id
    assert sub["title"] == "My Project"
    assert sub["is_locked"] is False
    sub_id = sub["id"]

    # Public list and get need no token
    res = client.get(f"/api/submissions?team_id={team_id}")
    assert res.status_code == 200
    assert any(s["id"] == sub_id for s in res.json())
    assert client.get(f"/api/submissions/{sub_id}").status_code == 200

    # Outsider cannot edit, member can
    res = client.put(f"/api/submissions/{sub_id}", json={"title": "Hacked"}, headers=outsider_hdr)
    assert res.status_code == 403
    res = client.put(f"/api/submissions/{sub_id}", json={"title": "Renamed"}, headers=member_hdr)
    assert res.status_code == 200
    assert res.json()["title"] == "Renamed"

    # Only organizer/admin can lock
    res = client.post(f"/api/submissions/{sub_id}/lock", headers=member_hdr)
    assert res.status_code == 403
    res = client.post(f"/api/submissions/{sub_id}/lock", headers=admin_hdr)
    assert res.status_code == 200
    assert res.json()["is_locked"] is True

    # Locked submissions cannot be edited
    res = client.put(f"/api/submissions/{sub_id}", json={"title": "Too late"}, headers=member_hdr)
    assert res.status_code == 400
    assert "locked" in res.json()["detail"].lower()

    # Only organizer/admin can delete
    res = client.delete(f"/api/submissions/{sub_id}", headers=member_hdr)
    assert res.status_code == 403
    res = client.delete(f"/api/submissions/{sub_id}", headers=admin_hdr)
    assert res.status_code == 204
    assert client.get(f"/api/submissions/{sub_id}").status_code == 404


def test_submission_rejected_after_deadline(client, auth_headers):
    admin_hdr = _admin_hdr(auth_headers)
    past = datetime.now(timezone.utc) - timedelta(days=1)
    event_id = _make_event(client, admin_hdr, past)

    _, member_hdr = _participant(auth_headers)
    team_id = _make_team(client, member_hdr, event_id)

    res = client.post(
        "/api/submissions",
        json={"team_id": team_id, "title": "Late entry"},
        headers=member_hdr,
    )
    assert res.status_code == 400
    assert "deadline" in res.json()["detail"].lower()