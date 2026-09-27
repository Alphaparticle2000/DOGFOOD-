import pytest


def test_create_event_forbidden_for_participant(client, auth_headers):
    headers = {"Authorization": auth_headers(role="participant")["Authorization"]}
    payload = {
        "name": "Hackathon 2026",
        "description": "Annual hackathon",
        "is_active": True,
    }
    res = client.post("/api/events", json=payload, headers=headers)
    assert res.status_code == 403


def test_create_and_get_event_as_organizer(client, auth_headers):
    headers = {"Authorization": auth_headers(role="organizer")["Authorization"]}
    payload = {
        "name": "Dogfooding Hackathon",
        "description": "Internal test event",
        "is_active": True,
    }
    res = client.post("/api/events", json=payload, headers=headers)
    assert res.status_code == 201
    event = res.json()
    assert event["name"] == "Dogfooding Hackathon"
    event_id = event["id"]

    # Get event by id
    res_get = client.get(f"/api/events/{event_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == event_id


def test_create_and_list_tracks_in_event(client, auth_headers):
    headers = {"Authorization": auth_headers(role="admin")["Authorization"]}

    # 1. Create event
    event_res = client.post(
        "/api/events",
        json={"name": "Multi-Track Hackathon", "is_active": True},
        headers=headers,
    )
    assert event_res.status_code == 201
    event_id = event_res.json()["id"]

    # 2. Add tracks
    track_res1 = client.post(
        f"/api/events/{event_id}/tracks",
        json={"name": "AI / ML Track", "description": "Generative AI solutions"},
        headers=headers,
    )
    assert track_res1.status_code == 201
    track1 = track_res1.json()
    assert track1["name"] == "AI / ML Track"

    track_res2 = client.post(
        f"/api/events/{event_id}/tracks",
        json={"name": "FinTech Track", "description": "Finance and Web3"},
        headers=headers,
    )
    assert track_res2.status_code == 201

    # 3. List tracks
    tracks_list = client.get(f"/api/events/{event_id}/tracks").json()
    assert len(tracks_list) >= 2
    track_names = [t["name"] for t in tracks_list]
    assert "AI / ML Track" in track_names
    assert "FinTech Track" in track_names

    # 4. Check standalone track endpoint
    track_get = client.get(f"/api/tracks/{track1['id']}")
    assert track_get.status_code == 200
    assert track_get.json()["id"] == track1["id"]
