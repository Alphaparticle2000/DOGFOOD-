from pathlib import Path
from backend.app.services.fixture_loader import load_fixtures
from backend.app.services.judging import calculate_all_results
from backend.app.services.judging import calculate_all_results
def main():
    project_root = Path(__file__).resolve().parents[3]
    fixture_path = project_root / "fixtures.json"

    fixtures = load_fixtures(fixture_path)

    projects = fixtures["projects"]
    scores = fixtures["scores"]

    results = calculate_all_results(
        projects,
        scores,
    )
    print(f"Projects loaded: {len(projects)}")
    print(f"Scores loaded: {len(scores)}")
    print(f"Results calculated: {len(results)}")
    print()

    for result in results[:10]:
        print(
            f"{result['project']} | "
            f"judges={result['judge_count']} | "
            f"average={result['overall_average']}"
        )


if __name__ == "__main__":
    main()
