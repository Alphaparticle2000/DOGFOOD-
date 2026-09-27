import uuid
import pytest


def test_team_create_and_membership_lifecycle(client, auth_headers):
    admin_hdr = {"Authorization": auth_headers(role="admin")["Authorization"]}

    # 1. Create an event and track
    event_res = client.post(
        "/api/events",
        json={"name": "Team LifeCycle Event", "is_active": True},
        headers=admin_hdr,
    )
    assert event_res.status_code == 201
    event_id = event_res.json()["id"]

    track_res = client.post(
        f"/api/events/{event_id}/tracks",
        json={"name": "DevOps Track"},
        headers=admin_hdr,
    )
    assert track_res.status_code == 201
    track_id = track_res.json()["id"]

    # 2. Participant 1 creates a team
    user1_id = str(uuid.uuid4())
    user1_info = auth_headers(role="participant", user_id=user1_id)
    user1_hdr = {"Authorization": user1_info["Authorization"]}

    team_res = client.post(
        "/api/teams",
        json={"name": "Team Alpha", "event_id": event_id, "track_id": track_id},
        headers=user1_hdr,
    )
    assert team_res.status_code == 201
    team = team_res.json()
    assert team["name"] == "Team Alpha"
    assert len(team["members"]) == 1
    assert team["members"][0]["user_id"] == user1_id
    assert team["members"][0]["is_lead"] is True
    team_id = team["id"]

    # 3. Participant 1 cannot create another team in same event
    dup_res = client.post(
        "/api/teams",
        json={"name": "Team Beta", "event_id": event_id},
        headers=user1_hdr,
    )
    assert dup_res.status_code == 400
    assert "already a member" in dup_res.json()["detail"]

    # 4. User 1 (team lead) adds Participant 2 to the team
    user2_id = str(uuid.uuid4())
    user2_info = auth_headers(role="participant", user_id=user2_id)
    # First provision user2 in public.users
    client.get("/api/users/me", headers={"Authorization": user2_info["Authorization"]})

    add_res = client.post(
        f"/api/teams/{team_id}/members",
        json={"user_id": user2_id, "is_lead": False},
        headers=user1_hdr,
    )
    assert add_res.status_code == 200
    updated_team = add_res.json()
    assert len(updated_team["members"]) == 2

    # 5. List teams filtered by event
    list_res = client.get(f"/api/teams?event_id={event_id}")
    assert list_res.status_code == 200
    teams = list_res.json()
    assert any(t["id"] == team_id for t in teams)

    # 6. Participant 2 removes themselves from team
    del_mem_res = client.delete(
        f"/api/teams/{team_id}/members/{user2_id}",
        headers={"Authorization": user2_info["Authorization"]},
    )
    assert del_mem_res.status_code == 204

    # 7. Verify roster is back to 1 member
    team_check = client.get(f"/api/teams/{team_id}").json()
    assert len(team_check["members"]) == 1
