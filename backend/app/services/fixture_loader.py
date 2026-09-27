from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FixtureLoadError(Exception):
    """Raised when the fixture file cannot be loaded."""


def load_fixtures(path: str | Path) -> dict[str, Any]:
    """Load and validate the DOGFOOD fixture JSON file."""

    fixture_path = Path(path)

    if not fixture_path.exists():
        raise FixtureLoadError(
            f"Fixture file not found: {fixture_path}"
        )

    try:
        with fixture_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise FixtureLoadError(
            f"Invalid JSON in fixture file: {exc}"
        ) from exc

    if not isinstance(data, dict):
        raise FixtureLoadError(
            "Fixture root must be a JSON object."
        )

    required_sections = {
        "event",
        "tracks",
        "judges",
        "teams",
        "projects",
        "scores",
    }

    missing_sections = required_sections - data.keys()

    if missing_sections:
        raise FixtureLoadError(
            "Missing fixture sections: "
            + ", ".join(sorted(missing_sections))
        )

    return data


def get_event(fixtures: dict[str, Any]) -> dict[str, Any]:
    return fixtures["event"]


def get_tracks(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    return fixtures["tracks"]


def get_judges(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    return fixtures["judges"]


def get_teams(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    return fixtures["teams"]


def get_projects(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    return fixtures["projects"]


def get_scores(fixtures: dict[str, Any]) -> list[dict[str, Any]]:
    return fixtures["scores"]


def find_judge(
    fixtures: dict[str, Any],
    judge_id: str,
) -> dict[str, Any] | None:
    for judge in get_judges(fixtures):
        if judge["id"] == judge_id:
            return judge

    return None


def find_project(
    fixtures: dict[str, Any],
    project_id: str,
) -> dict[str, Any] | None:
    for project in get_projects(fixtures):
        if project["id"] == project_id:
            return project

    return None


def find_team(
    fixtures: dict[str, Any],
    team_id: str,
) -> dict[str, Any] | None:
    for team in get_teams(fixtures):
        if team["id"] == team_id:
            return team

    return None


def find_track(
    fixtures: dict[str, Any],
    track_id: str,
) -> dict[str, Any] | None:
    for track in get_tracks(fixtures):
        if track["id"] == track_id:
            return track

    return None