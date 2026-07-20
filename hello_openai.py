"""Verify that this project can make a basic OpenAI API request."""

import os

from dotenv import load_dotenv
from openai import OpenAI


def main() -> None:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to a local .env file before running this script."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-5.6-sol")
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input="Reply with exactly: UnderStudy API connection successful.",
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
