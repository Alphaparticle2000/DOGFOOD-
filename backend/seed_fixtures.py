from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.core.database import SessionLocal
from backend.app.models.event import Event
from backend.app.models.track import Track
from backend.app.models.user import User, RoleEnum
from backend.app.models.team import Team
from backend.app.models.team_member import TeamMember
from backend.app.models.judge import Judge
from backend.app.models.submission import Submission
from backend.app.models.score import Score


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures.json"


def parse_dt(value: str | None):
    if not value:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )


def main():
    with FIXTURES.open("r", encoding="utf-8") as f:
        data = json.load(f)

    db = SessionLocal()

    try:
        # Clear existing fixture data.
        db.query(Score).delete()
        db.query(Judge).delete()
        db.query(TeamMember).delete()
        db.query(Submission).delete()
        db.query(Team).delete()
        db.query(Track).delete()
        db.query(Event).delete()

        # -------------------------
        # Event
        # -------------------------
        event_data = data["event"]

        event = Event(
            name=event_data["name"],
            description="Seeded from fixtures.json",
            submission_deadline=parse_dt(
                event_data["submissions_close"]
            ),
            is_active=True,
        )

        db.add(event)
        db.flush()

        # -------------------------
        # Tracks
        # -------------------------
        track_map = {}

        for item in data["tracks"]:
            track = Track(
                event_id=event.id,
                name=item["name"],
            )

            db.add(track)
            db.flush()

            track_map[item["id"]] = track.id

        # -------------------------
        # Users
        # -------------------------
        user_map = {}

        # Judges
        for item in data["judges"]:
            user = db.query(User).filter(
                User.email == item["email"]
            ).first()

            if not user:
                user = User(
                    email=item["email"],
                    name=item["name"],
                    role=RoleEnum.judge,
                )
                db.add(user)
                db.flush()

            user_map[item["email"]] = user.id

        # Participants from team members
        participant_emails = set()

        for team in data["teams"]:
            participant_emails.update(team["members"])

        for email in participant_emails:
            if email not in user_map:
                user = db.query(User).filter(
                    User.email == email
                ).first()

                if not user:
                    user = User(
                        email=email,
                        name=email.split("@")[0],
                        role=RoleEnum.participant,
                    )
                    db.add(user)
                    db.flush()

                user_map[email] = user.id

        # -------------------------
        # Teams
        # -------------------------
        team_map = {}

        for item in data["teams"]:
            team = Team(
                event_id=event.id,
                name=item["name"],
            )

            db.add(team)
            db.flush()

            team_map[item["id"]] = team.id

            for index, email in enumerate(item["members"]):
                member = TeamMember(
                    team_id=team.id,
                    user_id=user_map[email],
                    is_lead=(index == 0),
                )
                db.add(member)

        db.flush()

        # -------------------------
        # Assign team tracks from projects
        # -------------------------
        project_map = {}

        for item in data["projects"]:
            team = db.query(Team).filter(
                Team.id == team_map[item["team"]]
            ).first()

            if team is None:
                raise RuntimeError(
                    f"Team not found: {item['team']}"
                )

            team.track_id = track_map[item["track"]]

            submission = Submission(
                team_id=team.id,
                title=item["title"],
                description=item.get("summary"),
                repo_url=item.get("repo_url"),
                submitted_at=parse_dt(item.get("submitted_at")),
                is_locked=True,
            )

            db.add(submission)
            db.flush()

            project_map[item["id"]] = submission.id

        # -------------------------
        # Judges
        # -------------------------
        for item in data["judges"]:
            user_id = user_map[item["email"]]

            for fixture_track_id in item["tracks"]:
                judge = Judge(
                    user_id=user_id,
                    event_id=event.id,
                    track_id=track_map[fixture_track_id],
                )

                db.add(judge)

        db.flush()

        # -------------------------
        # Scores
        # -------------------------
        for item in data["scores"]:
            judge_data = next(
                j for j in data["judges"]
                if j["id"] == item["judge"]
            )

            judge_user_id = user_map[judge_data["email"]]

            score = Score(
                submission_id=project_map[item["project"]],
                judge_id=judge_user_id,
                functionality=item["criteria"]["functionality"],
                quality=item["criteria"]["quality"],
                innovation=item["criteria"]["innovation"],
                comment=item.get("comment"),
            )

            db.add(score)

        db.commit()

        print("FIXTURES SEEDED SUCCESSFULLY")
        print(f"Event: {event.id} - {event.name}")
        print(f"Tracks: {len(track_map)}")
        print(f"Teams: {len(team_map)}")
        print(f"Projects: {len(project_map)}")
        print(f"Judges: {len(data['judges'])}")
        print(f"Scores: {len(data['scores'])}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()