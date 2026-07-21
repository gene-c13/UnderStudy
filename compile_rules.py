"""Compile private tutor materials into an internal answer profile."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, AuthenticationError, OpenAI, RateLimitError


PROJECT_ROOT = Path(__file__).parent
RULES_PATH = PROJECT_ROOT / "data" / "rules.md"
EXAMPLES_DIR = PROJECT_ROOT / "data" / "build_examples"
PROFILE_PATH = PROJECT_ROOT / "data" / "internal" / "compiled_profile.md"
MAX_EXAMPLES = 4


def read_required_file(path: Path, description: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {description}: {path}\n"
            "Create the tutor materials from the templates before compiling."
        )
    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"The {description} is empty: {path}")
    return content


def load_examples() -> str:
    if not EXAMPLES_DIR.is_dir():
        raise FileNotFoundError(
            f"Missing build examples folder: {EXAMPLES_DIR}\n"
            "Create it and add tutor-written .md examples from templates/."
        )
    examples = []
    for path in sorted(EXAMPLES_DIR.glob("*.md"))[:MAX_EXAMPLES]:
        content = path.read_text(encoding="utf-8").strip()
        if content:
            examples.append(f"## Example: {path.stem}\n{content}")
    if not examples:
        raise ValueError("Add at least one non-empty build example before compiling.")
    return "\n\n".join(examples)


def compile_profile(rules: str, examples: str) -> str:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file.")
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    instructions = """You compile a tutor's private teaching materials into a private, structured profile for an answering system. Extract only what the tutor actually establishes. Do not invent content, pedagogy, marking rules, or response structures. Preserve uncertainty as an explicit gap rather than guessing.

Return Markdown with exactly these sections:
# Internal tutor profile
## Student-intent signals
## Response approaches established by the tutor
## Required and preferred vocabulary
## Prohibited or careful wording
## Topic map and reusable explanations
## Analogies and examples to reuse
## Misconceptions to pre-empt
## Syllabus boundaries
## Gaps requiring tutor input

This is internal reference, not a student response. Be concise, faithful, and specific. For each response approach, include recognition cues and a structure only if the tutor supplied them. The raw crash course is authoritative; build examples demonstrate how it is applied."""
    source = f"# Tutor crash course\n{rules}\n\n# Tutor build examples\n{examples}\n"
    client = OpenAI()
    try:
        response = client.responses.create(model=model, instructions=instructions, input=source)
    except AuthenticationError as error:
        raise RuntimeError("OpenAI rejected the API key. Check OPENAI_API_KEY.") from error
    except RateLimitError as error:
        raise RuntimeError("The API request was rate-limited or has no quota.") from error
    except APIConnectionError as error:
        raise RuntimeError("Could not connect to the OpenAI API.") from error
    except APIError as error:
        raise RuntimeError(f"OpenAI API error: {error}") from error
    profile = response.output_text.strip()
    if not profile:
        raise RuntimeError("The compiler returned an empty tutor profile.")
    return profile


def main() -> None:
    rules = read_required_file(RULES_PATH, "tutor rules file")
    examples = load_examples()
    profile = compile_profile(rules, examples)
    PROFILE_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROFILE_PATH.write_text(profile + "\n", encoding="utf-8")
    print(f"Internal tutor profile written to {PROFILE_PATH}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error
