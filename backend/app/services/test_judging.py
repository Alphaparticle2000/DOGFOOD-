from pathlib import Path
from backend.app.services.fixture_loader import load_fixtures
from backend.app.services.judging import calculate_all_results
from backend.app.services.judging import (
    ScoreInput,
    JudgingError,
    InvalidScoreError,
    JudgeNotAssignedError,
    DuplicateScoreError,
    SubmissionClosedError,
    validate_score,
    validate_judge_assignment,
    validate_no_duplicate_score,
    validate_no_self_judging,
    validate_submission,
    validate_submission_deadline,
    calculate_score_average,
    calculate_project_result,
    calculate_all_results,
)


PROJECT_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = PROJECT_ROOT / "fixtures.json"


def load_test_data():
    return load_fixtures(FIXTURE_PATH)


def test_valid_score():
    score = ScoreInput(
        functionality=5,
        quality=4,
        innovation=3,
        comment="Solid.",
    )
    validate_score(score)


def test_score_below_minimum():
    score = ScoreInput(
        functionality=0,
        quality=4,
        innovation=3,
    )

    try:
        validate_score(score)
    except InvalidScoreError:
        return

    raise AssertionError("Score below minimum was accepted.")


def test_score_above_maximum():
    score = ScoreInput(
        functionality=6,
        quality=4,
        innovation=3,
    )

    try:
        validate_score(score)
    except InvalidScoreError:
        return

    raise AssertionError("Score above maximum was accepted.")


def test_real_fixture_judge_assignment():
    fixtures = load_test_data()

    judge = next(
        judge
        for judge in fixtures["judges"]
        if judge["id"] == "jdg_01"
    )

    project = next(
        project
        for project in fixtures["projects"]
        if project["id"] == "prj_02"
    )

    validate_judge_assignment(judge, project)


def test_real_fixture_wrong_judge_assignment():
    fixtures = load_test_data()

    judge = next(
        judge
        for judge in fixtures["judges"]
        if judge["id"] == "jdg_01"
    )

    project = next(
        project
        for project in fixtures["projects"]
        if project["id"] == "prj_01"
    )

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

    raise AssertionError("Duplicate score was accepted.")


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

    assert result == {
        "functionality": 4.0,
        "quality": 4.0,
        "innovation": 4.0,
    }


def test_real_fixture_project_result():
    fixtures = load_test_data()

    result = calculate_project_result(
        "prj_01",
        fixtures["scores"],
    )

    assert result["project"] == "prj_01"
    assert result["judge_count"] > 0
    assert 1 <= result["overall_average"] <= 5


def test_all_fixture_results():
    fixtures = load_test_data()

    results = calculate_all_results(
        fixtures["projects"],
        fixtures["scores"],
    )

    assert len(results) == 41

    for result in results:
        assert result["project"].startswith("prj_")
        assert result["judge_count"] >= 0
        assert 0 <= result["overall_average"] <= 5


def test_results_are_sorted():
    fixtures = load_test_data()

    results = calculate_all_results(
        fixtures["projects"],
        fixtures["scores"],
    )

    averages = [
        result["overall_average"]
        for result in results
    ]

    assert averages == sorted(
        averages,
        reverse=True,
    )


def test_submission_before_deadline():
    fixtures = load_test_data()

    event = fixtures["event"]

    validate_submission_deadline(
        event,
        "2026-03-01T17:57:00Z",
    )


def test_submission_after_deadline():
    fixtures = load_test_data()

    event = fixtures["event"]

    try:
        validate_submission_deadline(
            event,
            "2026-03-01T18:01:00Z",
        )
    except SubmissionClosedError:
        return

    raise AssertionError(
        "Submission after the deadline was accepted."
    )


def test_self_judging_is_blocked():
    judge = {
        "id": "jdg_test",
        "team": "team_test",
        "tracks": ["track_test"],
    }

    project = {
        "id": "prj_test",
        "team": "team_test",
        "track": "track_test",
    }

    try:
        validate_no_self_judging(
            judge,
            project,
        )
    except JudgingError:
        return

    raise AssertionError(
        "Self-judging was allowed."
    )


def test_real_fixture_self_judging():
    fixtures = load_test_data()

    judge = fixtures["judges"][0]
    judge_team = judge.get("team")

    if not judge_team:
        return

    own_project = next(
        (
            project
            for project in fixtures["projects"]
            if project.get("team") == judge_team
        ),
        None,
    )

    if own_project is None:
        return

    try:
        validate_no_self_judging(
            judge,
            own_project,
        )
    except JudgingError:
        return

    raise AssertionError(
        "Real fixture judge was allowed to score "
        "their own team's project."
    )


def test_validate_submission_blocks_self_judging():
    judge = {
        "id": "jdg_test",
        "team": "team_test",
        "tracks": ["track_test"],
    }

    project = {
        "id": "prj_test",
        "team": "team_test",
        "track": "track_test",
    }

    score = ScoreInput(
        functionality=5,
        quality=5,
        innovation=5,
    )

    try:
        validate_submission(
            judge=judge,
            project=project,
            score=score,
            existing_scores=[],
        )
    except JudgingError:
        return

    raise AssertionError(
        "validate_submission allowed self-judging."
    )


def run_tests():
    tests = [
        test_valid_score,
        test_score_below_minimum,
        test_score_above_maximum,
        test_real_fixture_judge_assignment,
        test_real_fixture_wrong_judge_assignment,
        test_duplicate_score,
        test_score_average,
        test_real_fixture_project_result,
        test_all_fixture_results,
        test_results_are_sorted,
        test_submission_before_deadline,
        test_submission_after_deadline,
        test_self_judging_is_blocked,
        test_real_fixture_self_judging,
        test_validate_submission_blocks_self_judging,
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