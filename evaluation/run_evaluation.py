import json
from pathlib import Path


def load_questions(path: str = "evaluation/datasets/questions.json") -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    questions = load_questions()
    print(f"Loaded {len(questions)} evaluation questions.")
    print("Execution against the live API will be added after the benchmark is populated.")
    print("No accuracy or faithfulness numbers are claimed until a real run is recorded.")


if __name__ == "__main__":
    main()
