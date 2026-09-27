from judging import (
    ScoreInput,
    InvalidScoreError,
    JudgeNotAssignedError,
    DuplicateScoreError,
    validate_score,
    validate_judge_assignment,
    validate_no_duplicate_score,
    calculate_score_average,
    calculate_project_result,
)


def test_valid_score():
    score = ScoreInput(
        functionality=5,
        quality=4,
        innovation=3,
        comment="Solid project.",
    )

    validate_score(score)


def test_invalid_score():
    score = ScoreInput(
        functionality=6,
        quality=4,
        innovation=3,
    )

    try:
        validate_score(score)
    except InvalidScoreError:
        return

    raise AssertionError("Invalid score was accepted.")


def test_judge_assignment():
    judge = {
        "id": "jdg_01",
        "tracks": ["trk_03"],
    }

    project = {
        "id": "prj_02",
        "track": "trk_03",
    }

    validate_judge_assignment(judge, project)


def test_wrong_judge_assignment():
    judge = {
        "id": "jdg_01",
        "tracks": ["trk_03"],
    }

    project = {
        "id": "prj_01",
        "track": "trk_04",
    }

    try:
        validate_judge_assignment(judge, project)
    except JudgeNotAssignedError:
        return

    raise AssertionError(
        "Judge was allowed to score an unassigned track."
    )


def test_duplicate_score():
    existing_scores = [
        {
            "judge": "jdg_01",
            "project": "prj_02",
        }
    ]

    try:
        validate_no_duplicate_score(
            existing_scores,
            "jdg_01",
            "prj_02",
        )
    except DuplicateScoreError:
        return

    raise AssertionError(
        "Duplicate score was accepted."
    )


def test_score_average():
    scores = [
        {
            "criteria": {
                "functionality": 5,
                "quality": 4,
                "innovation": 3,
            }
        },
        {
            "criteria": {
                "functionality": 3,
                "quality": 4,
                "innovation": 5,
            }
        },
    ]

    result = calculate_score_average(scores)

    assert result["functionality"] == 4.0
    assert result["quality"] == 4.0
    assert result["innovation"] == 4.0


def test_project_result():
    scores = [
        {
            "judge": "jdg_01",
            "project": "prj_01",
            "criteria": {
                "functionality": 5,
                "quality": 4,
                "innovation": 3,
            },
            "comment": "Solid.",
        },
        {
            "judge": "jdg_02",
            "project": "prj_01",
            "criteria": {
                "functionality": 3,
                "quality": 4,
                "innovation": 5,
            },
            "comment": "Runs clean.",
        },
    ]

    result = calculate_project_result(
        "prj_01",
        scores,
    )

    assert result["project"] == "prj_01"
    assert result["judge_count"] == 2
    assert result["overall_average"] == 4.0
    assert len(result["comments"]) == 2


def run_tests():
    tests = [
        test_valid_score,
        test_invalid_score,
        test_judge_assignment,
        test_wrong_judge_assignment,
        test_duplicate_score,
        test_score_average,
        test_project_result,
    ]

    passed = 0

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
        passed += 1

    print()
    print(f"{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    run_tests()