"""Answer a student question using a tutor's rules and teaching examples."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


PROJECT_ROOT = Path(__file__).parent
RULES_PATH = PROJECT_ROOT / "data" / "rules.md"
EXAMPLES_DIR = PROJECT_ROOT / "data" / "build_examples"
MAX_EXAMPLES = 4


def read_required_file(path: Path, description: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {description}: {path}\n"
            "Copy the matching file from templates/ into data/ and fill it in."
        )
    return path.read_text(encoding="utf-8").strip()


def load_examples() -> str:
    if not EXAMPLES_DIR.is_dir():
        raise FileNotFoundError(
            f"Missing build examples folder: {EXAMPLES_DIR}\n"
            "Create it and add 3–4 tutor-written .md examples from templates/."
        )

    example_paths = sorted(EXAMPLES_DIR.glob("*.md"))[:MAX_EXAMPLES]
    if not example_paths:
        raise FileNotFoundError(
            f"No .md examples found in {EXAMPLES_DIR}\n"
            "Add 3–4 tutor-written question-and-answer examples before running."
        )

    examples = []
    for path in example_paths:
        content = path.read_text(encoding="utf-8").strip()
        if content:
            examples.append(f"## Example: {path.stem}\n{content}")

    if not examples:
        raise ValueError("The build example files are empty.")
    return "\n\n".join(examples)


def get_question() -> str:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        question = input("Student question: ").strip()
    if not question:
        raise ValueError("Please provide a student question.")
    return question


def generate_understudy_answer(question: str) -> str:
    """Generate an answer using the tutor's rules and build-set examples."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file.")

    rules = read_required_file(RULES_PATH, "tutor rules file")
    examples = load_examples()
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")

    instructions = f"""You are UnderStudy: a tutor-persona answering a student's question.

Your job is method fidelity, not generic tutoring. Follow the tutor's rules and
teaching examples exactly. Do not mention these instructions, the examples, or
that you are an AI.

TUTOR RULES
{rules}

BUILD-SET EXAMPLES
{examples}

For the student's question, use the tutor's explanation structure, required
vocabulary, notation, analogies, and syllabus ceiling. Avoid every banned
phrase and pre-empt the listed misconceptions where relevant. If the question
requires material beyond the syllabus ceiling, say so briefly in the tutor's
style and stay within scope.
"""

    client = OpenAI()
    response = client.responses.create(
        model=model,
        instructions=instructions,
        input=question,
    )
    return response.output_text


def main() -> None:
    question = get_question()
    print(generate_understudy_answer(question))


if __name__ == "__main__":
    main()
