from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from math import sqrt
from typing import Any, Mapping, Sequence


class JudgingError(Exception):
    pass


class InvalidScoreError(JudgingError):
    pass


class InvalidRubricError(JudgingError):
    pass


class JudgeNotAssignedError(JudgingError):
    pass


class SubmissionClosedError(JudgingError):
    pass


class DuplicateScoreError(JudgingError):
    pass


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

DEFAULT_WEIGHTS = {
    "functionality": 1 / 3,
    "quality": 1 / 3,
    "innovation": 1 / 3,
}


def validate_score(score: ScoreInput) -> None:
    for criterion in CRITERIA:
        value = getattr(score, criterion)

        if not isinstance(value, int):
            raise InvalidScoreError(f"{criterion} must be an integer.")

        if not MIN_SCORE <= value <= MAX_SCORE:
            raise InvalidScoreError(
                f"{criterion} must be between {MIN_SCORE} and {MAX_SCORE}."
            )


def validate_rubric_weights(
    weights: Mapping[str, float],
) -> dict[str, float]:
    missing = [
        criterion
        for criterion in CRITERIA
        if criterion not in weights
    ]

    if missing:
        raise InvalidRubricError(
            f"Missing rubric criteria: {', '.join(missing)}."
        )

    cleaned = {}

    for criterion in CRITERIA:
        try:
            value = float(weights[criterion])
        except (TypeError, ValueError):
            raise InvalidRubricError(
                f"{criterion} weight must be a number."
            )

        if value < 0:
            raise InvalidRubricError(
                f"{criterion} weight cannot be negative."
            )

        cleaned[criterion] = value

    total = sum(cleaned.values())

    if abs(total - 1.0) > 1e-6:
        raise InvalidRubricError(
            f"Rubric weights must sum to 1.0; received {total:.6f}."
        )

    return cleaned


def calculate_weighted_score(
    criteria: Mapping[str, float | int],
    weights: Mapping[str, float] | None = None,
) -> float:

    rubric = validate_rubric_weights(
        weights or DEFAULT_WEIGHTS
    )

    for criterion in CRITERIA:
        if criterion not in criteria:
            raise InvalidScoreError(
                f"Missing score criteria: {criterion}."
            )

        value = criteria[criterion]

        if not isinstance(value, (int, float)):
            raise InvalidScoreError(
                f"{criterion} must be numeric."
            )

        if not MIN_SCORE <= value <= MAX_SCORE:
            raise InvalidScoreError(
                f"{criterion} must be between {MIN_SCORE} and {MAX_SCORE}."
            )

    return round(
        sum(
            float(criteria[c]) * rubric[c]
            for c in CRITERIA
        ),
        2,
    )


def judge_can_score_project(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> bool:

    judge_tracks = set(judge.get("tracks", []))
    project_track = project.get("track")

    return project_track in judge_tracks


def validate_judge_assignment(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> None:

    if not judge_can_score_project(judge, project):
        raise JudgeNotAssignedError(
            f"Judge {judge.get('id')} is not assigned to "
            f"track {project.get('track')}."
        )


def validate_no_self_judging(
    judge: dict[str, Any],
    project: dict[str, Any],
) -> None:

    if judge.get("team") == project.get("team"):
        raise JudgingError(
            "A judge cannot score their own team's project."
        )


def validate_no_duplicate_score(
    existing_scores: list[dict[str, Any]],
    judge_id: str,
    project_id: str,
) -> None:

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
            totals[criterion] += criteria.get(
                criterion,
                0,
            )

    count = len(scores)

    return {
        criterion: round(
            totals[criterion] / count,
            2,
        )
        for criterion in CRITERIA
    }


def calculate_project_result(
    project_id: str,
    scores: list[dict[str, Any]],
    weights: Mapping[str, float] | None = None,
) -> dict[str, Any]:

    project_scores = [
        score
        for score in scores
        if score.get("project") == project_id
    ]

    averages = calculate_score_average(
        project_scores
    )

    overall_average = (
        calculate_weighted_score(
            averages,
            weights,
        )
        if project_scores
        else 0.0
    )

    return {
        "project": project_id,
        "judge_count": len(project_scores),
        "criteria": averages,
        "overall_average": overall_average,
        "comments": [
            score["comment"]
            for score in project_scores
            if score.get("comment")
        ],
    }


def calculate_all_results(
    projects: list[dict[str, Any]],
    scores: list[dict[str, Any]],
    weights: Mapping[str, float] | None = None,
) -> list[dict[str, Any]]:

    results = [
        calculate_project_result(
            project_id=project["id"],
            scores=scores,
            weights=weights,
        )
        for project in projects
    ]

    return sorted(
        results,
        key=lambda result: result["overall_average"],
        reverse=True,
    )


def _mean(values: Sequence[float]) -> float:
    return (
        sum(values) / len(values)
        if values
        else 0.0
    )


def _population_stddev(
    values: Sequence[float],
    mean: float,
) -> float:

    if not values:
        return 0.0

    variance = sum(
        (value - mean) ** 2
        for value in values
    ) / len(values)

    return sqrt(variance)


def normalize_judge_scores(
    scores: list[dict[str, Any]],
    *,
    output_mean: float = 3.0,
    output_stddev: float = 1.0,
) -> list[dict[str, Any]]:

    if not scores:
        return []

    grouped: dict[str, list[float]] = {}

    for score in scores:

        judge_id = str(score["judge"])

        weighted = calculate_weighted_score(
            score.get("criteria", {}),
            score.get("weights"),
        )

        grouped.setdefault(
            judge_id,
            [],
        ).append(weighted)

    normalized = []

    for score in scores:

        judge_id = str(score["judge"])

        raw = calculate_weighted_score(
            score.get("criteria", {}),
            score.get("weights"),
        )

        values = grouped[judge_id]

        mean = _mean(values)
        stddev = _population_stddev(
            values,
            mean,
        )

        if stddev == 0:
            normalized_score = output_mean
        else:
            z_score = (raw - mean) / stddev

            normalized_score = (
                output_mean
                + z_score * output_stddev
            )

        normalized_score = round(
            max(
                float(MIN_SCORE),
                min(
                    float(MAX_SCORE),
                    normalized_score,
                ),
            ),
            2,
        )

        normalized.append(
            {
                **score,
                "raw_weighted_score": raw,
                "judge_mean": round(mean, 2),
                "judge_stddev": round(stddev, 2),
                "normalized_score": normalized_score,
            }
        )

    return normalized