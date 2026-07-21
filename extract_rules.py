"""Create a tutor-reviewable rules draft from lesson transcripts."""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)


PROJECT_ROOT = Path(__file__).parent
RAW_TRANSCRIPTS_DIR = PROJECT_ROOT / "data" / "transcripts" / "raw"
REVIEWED_TRANSCRIPTS_DIR = PROJECT_ROOT / "data" / "transcripts" / "reviewed"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "extract_rules_prompt.md"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "data" / "rules_draft.md"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a tutor-reviewable rules draft from lesson transcripts."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Markdown path to write (default: {DEFAULT_OUTPUT_PATH}).",
    )
    return parser.parse_args()


def select_transcript_directory() -> Path:
    if REVIEWED_TRANSCRIPTS_DIR.is_dir() and any(REVIEWED_TRANSCRIPTS_DIR.iterdir()):
        return REVIEWED_TRANSCRIPTS_DIR
    return RAW_TRANSCRIPTS_DIR


def load_transcripts() -> str:
    transcript_directory = select_transcript_directory()
    if not transcript_directory.is_dir():
        raise FileNotFoundError(
            "No transcript directory found. Add text transcripts to "
            f"{RAW_TRANSCRIPTS_DIR}."
        )

    sources = []
    for path in sorted(transcript_directory.rglob("*")):
        if not path.is_file() or path.name.startswith("."):
            continue
        content = path.read_text(encoding="utf-8").strip()
        if content:
            relative_path = path.relative_to(PROJECT_ROOT)
            sources.append(f"## Source: {relative_path}\n{content}")

    if not sources:
        raise ValueError(f"No non-empty transcripts found in {transcript_directory}.")
    return "\n\n".join(sources)


def load_extraction_prompt() -> str:
    if not PROMPT_PATH.is_file():
        raise FileNotFoundError(f"Missing extraction prompt: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8").strip()


def generate_draft(instructions: str, transcripts: str) -> str:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file.")

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    client = OpenAI()
    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=f"# Source transcripts\n\n{transcripts}",
        )
    except AuthenticationError as error:
        raise RuntimeError("OpenAI rejected the API key. Check OPENAI_API_KEY.") from error
    except RateLimitError as error:
        raise RuntimeError("The API request was rate-limited or has no quota.") from error
    except APIConnectionError as error:
        raise RuntimeError("Could not connect to the OpenAI API.") from error
    except APIError as error:
        raise RuntimeError(f"OpenAI API error: {error}") from error

    draft = response.output_text.strip()
    if not draft:
        raise RuntimeError("The extraction model returned an empty rules draft.")
    return draft


def main() -> None:
    args = parse_arguments()
    instructions = load_extraction_prompt()
    transcripts = load_transcripts()
    draft = generate_draft(instructions, transcripts)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(draft + "\n", encoding="utf-8")
    print(f"Tutor-reviewable rules draft written to {args.output}")
    print("Review it, then copy approved content into data/rules.md.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, RuntimeError, ValueError, UnicodeDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
