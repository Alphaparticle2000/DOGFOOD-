import pytest

from backend.app.services.judging import (
    InvalidRubricError,
    calculate_weighted_score,
    normalize_judge_scores,
    validate_rubric_weights,
)


def test_valid_rubric_weights():
    weights = {
        "functionality": 0.5,
        "quality": 0.3,
        "innovation": 0.2,
    }

    assert validate_rubric_weights(weights) == weights


def test_rubric_weights_must_sum_to_one():
    with pytest.raises(InvalidRubricError):
        validate_rubric_weights({
            "functionality": 0.5,
            "quality": 0.3,
            "innovation": 0.3,
        })


def test_rubric_weights_require_all_criteria():
    with pytest.raises(InvalidRubricError):
        validate_rubric_weights({
            "functionality": 0.5,
            "quality": 0.5,
        })


def test_weighted_score():
    criteria = {
        "functionality": 5,
        "quality": 3,
        "innovation": 4,
    }

    weights = {
        "functionality": 0.5,
        "quality": 0.2,
        "innovation": 0.3,
    }

    assert calculate_weighted_score(criteria, weights) == pytest.approx(4.3)


def test_normalize_judge_scores():
    scores = [
        {
            "judge": "j1",
            "submission_id": "p1",
            "criteria": {
                "functionality": 5,
                "quality": 5,
                "innovation": 5,
            },
        },
        {
            "judge": "j1",
            "submission_id": "p2",
            "criteria": {
                "functionality": 1,
                "quality": 1,
                "innovation": 1,
            },
        },
    ]

    result = normalize_judge_scores(scores)

    assert len(result) == 2
    assert result[0]["normalized_score"] == pytest.approx(4.0)
    assert result[1]["normalized_score"] == pytest.approx(2.0)


def test_normalization_single_score():
    scores = [
        {
            "judge": "j1",
            "submission_id": "p1",
            "criteria": {
                "functionality": 4,
                "quality": 4,
                "innovation": 4,
            },
        }
    ]

    result = normalize_judge_scores(scores)

    assert result[0]["normalized_score"] == pytest.approx(3.0)