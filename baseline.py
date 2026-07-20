"""Answer a chemistry question without UnderStudy tutor-persona context."""

import os
import sys

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)


def get_question() -> str:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        try:
            question = input("Student question: ").strip()
        except EOFError as error:
            raise ValueError("Please provide a student question.") from error

    if not question:
        raise ValueError("Please provide a student question.")
    return question


def generate_baseline_answer(question: str) -> str:
    """Generate a generic chemistry-tutor answer with no UnderStudy context."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your local .env file.")

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    client = OpenAI()

    try:
        response = client.responses.create(
            model=model,
            instructions=(
                "You are a helpful chemistry tutor. Give a clear, accurate, "
                "age-appropriate answer to the student's question."
            ),
            input=question,
        )
    except AuthenticationError as error:
        raise RuntimeError(
            "OpenAI rejected the API key. Check OPENAI_API_KEY in your .env file."
        ) from error
    except RateLimitError as error:
        raise RuntimeError(
            "The API request was rate-limited or the project has no available quota."
        ) from error
    except APIConnectionError as error:
        raise RuntimeError(
            "Could not connect to the OpenAI API. Check your internet connection."
        ) from error
    except APIError as error:
        raise RuntimeError(f"OpenAI API error: {error}") from error

    return response.output_text


def main() -> None:
    question = get_question()
    print(generate_baseline_answer(question))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
