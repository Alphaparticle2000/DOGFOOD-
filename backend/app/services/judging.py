from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


class JudgingError(Exception):
    """Base exception for judging-related errors."""


class InvalidScoreError(JudgingError):
    """Raised when a submitted score is invalid."""


class JudgeNotAssignedError(JudgingError):
    """Raised when a judge is not assigned to the project's track."""


class SubmissionClosedError(JudgingError):
    """Raised when an action occurs after the submission deadline."""


class DuplicateScoreError(JudgingError):
    """Raised when a judge attempts to score the same project twice."""


@dataclass(frozen=True)
class ScoreInput:
    functionality: int
    quality: int
    innovation: int
    comment: str = ""


CRITERIA = (
    "functionality",
    "quality",
    "innovation",
)

MIN_SCORE = 1
MAX_SCORE = 5


def validate_score(score: ScoreInput) -> None:
    """
    Validate an individual judge's score.
    """

    for criterion in CRITERIA:
        value = getattr(score, criterion)

        if not isinstance(value, int):
            raise InvalidScoreError(
                f"{criterion} must be an integer."
            )

        if not MIN_SCORE <= value <= MAX_SCORE:
            raise InvalidScoreError(
                f"{criterion} must be between "
                f"{MIN_SCORE} and {MAX_SCORE}."
            )


def judge_can_score_project(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> bool:
    """
    Return True when the judge is assigned to the project's track.
    """

    judge_tracks = set(judge.get("tracks", []))
    project_track = project.get("track")

    return project_track in judge_tracks


def validate_judge_assignment(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> None:
    """
    Ensure that the judge is assigned to the project's track.
    """

    if not judge_can_score_project(judge, project):
        raise JudgeNotAssignedError(
            f"Judge {judge.get('id')} is not assigned to "
            f"track {project.get('track')}."
        )


def validate_no_self_judging(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> None:
    """
    Prevent a judge from scoring a project belonging to their own team.
    """

    if judge.get("team") == project.get("team"):
        raise JudgingError(
            "A judge cannot score their own team's project."
        )


def validate_no_duplicate_score(
    existing_scores: list[dict[str, Any]],
    judge_id: str,
    project_id: str,
) -> None:
    """
    Prevent the same judge from scoring the same project twice.
    """

    for score in existing_scores:
        if (
            score.get("judge") == judge_id
            and score.get("project") == project_id
        ):
            raise DuplicateScoreError(
                f"Judge {judge_id} has already scored "
                f"project {project_id}."
            )


def validate_submission(
    judge: dict[str, Any],
    project: dict[str, Any],
    score: ScoreInput,
    existing_scores: list[dict[str, Any]],
) -> None:
    """
    Run all validation required before accepting a score.
    """

    validate_judge_assignment(judge, project)

    validate_no_self_judging(judge, project)

    validate_no_duplicate_score(
        existing_scores,
        judge_id=judge["id"],
        project_id=project["id"],
    )

    validate_score(score)


def validate_submission_deadline(
    event: dict[str, Any],
    submitted_at: str,
) -> None:
    """
    Ensure a submission was made before the event submission deadline.
    """

    deadline = datetime.fromisoformat(
        event["submissions_close"].replace("Z", "+00:00")
    )

    submission_time = datetime.fromisoformat(
        submitted_at.replace("Z", "+00:00")
    )

    if submission_time > deadline:
        raise SubmissionClosedError(
            "Submission was made after the submission deadline."
        )


def calculate_score_average(
    scores: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calculate the average score for each judging criterion.
    """

    if not scores:
        return {
            criterion: 0.0
            for criterion in CRITERIA
        }

    totals = {
        criterion: 0
        for criterion in CRITERIA
    }

    for score in scores:
        criteria = score.get("criteria", {})

        for criterion in CRITERIA:
            totals[criterion] += criteria.get(criterion, 0)

    count = len(scores)

    return {
        criterion: round(totals[criterion] / count, 2)
        for criterion in CRITERIA
    }


def calculate_project_result(
    project_id: str,
    scores: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Produce the aggregated judging result for one project.
    """

    project_scores = [
        score
        for score in scores
        if score.get("project") == project_id
    ]

    averages = calculate_score_average(project_scores)

    overall_average = (
        sum(averages.values()) / len(CRITERIA)
        if project_scores
        else 0.0
    )

    return {
        "project": project_id,
        "judge_count": len(project_scores),
        "criteria": averages,
        "overall_average": round(overall_average, 2),
        "comments": [
            score["comment"]
            for score in project_scores
            if score.get("comment")
        ],
    }


def calculate_all_results(
    projects: list[dict[str, Any]],
    scores: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Calculate results for every project.
    """

    results = [
        calculate_project_result(
            project_id=project["id"],
            scores=scores,
        )
        for project in projects
    ]

    return sorted(
        results,
        key=lambda result: result["overall_average"],
        reverse=True,
    )



