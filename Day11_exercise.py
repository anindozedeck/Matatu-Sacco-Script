import argparse
import os
import sys

import anthropic
from dotenv import load_dotenv


SYSTEM_PROMPT = """
You are a helpful, clear WhatsApp assistant for a matatu SACCO in Thika.
Answer briefly and politely. Use Kenyan shillings (KSh).

For this demo, the SACCO's standard details are:
- Membership fee: KSh 5,000, paid once when joining.
- Monthly membership contribution: KSh 1,500, due by the 5th of each month.
- Next regular members' meeting: the first Saturday of the month at 10:00 AM
  at the SACCO office in Thika.

These are example details for the script. Do not describe them as verified
official SACCO information; advise members to confirm with the secretary.
You cannot access member accounts or payment records. Never guess or invent
someone's personal balance. Explain that the member should check with the
treasurer or secretary using the SACCO's private member channel.
If a question is outside these details, say you don't have that information
and direct the member to the secretary.
"""

TEST_QUESTIONS = [
    "Could you check what I still owe the SACCO?",
    "How much is left on my account?",
    "When are we meeting next?",
    "Is there a date for our next members' meeting?",
    "What should I pay to join?",
    "How much are monthly contributions?",
]


def answer_question(client: anthropic.Anthropic, question: str) -> str:
    message = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description="Answer common Matatu SACCO questions using AI."
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Send six example question variations to the AI and show its answers.",
    )
    args = parser.parse_args()

    load_dotenv()
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY is missing. Add it to your .env file and try again.")
        return

    client = anthropic.Anthropic()
    questions = TEST_QUESTIONS if args.test else None

    if questions is None:
        print("SACCO Q&A is ready. Type 'quit' to exit.")
        while True:
            question = input("\nMember's question: ").strip()
            if question.lower() in {"quit", "exit"}:
                break
            if not question:
                continue
            try:
                print("\n" + answer_question(client, question))
            except anthropic.APIConnectionError:
                print("The API is unavailable. Check your internet connection and try again.")
            except anthropic.AuthenticationError:
                print("The API key is invalid or expired. Check your .env file.")
            except anthropic.RateLimitError:
                print("The API is busy. Please wait a minute and try again.")
            except anthropic.APIStatusError as error:
                print(f"The API returned an error (HTTP {error.status_code}).")
            except anthropic.APIError as error:
                print(f"An API error occurred: {error}")
        return

    for question in questions:
        print(f"\nMember: {question}")
        try:
            print(f"Assistant: {answer_question(client, question)}")
        except anthropic.APIConnectionError:
            print("Test could not reach the API. Check your internet connection.")
        except anthropic.AuthenticationError:
            print("Test could not authenticate. Check your .env file.")
        except anthropic.RateLimitError:
            print("Test was rate limited. Wait a minute before trying again.")
        except anthropic.APIStatusError as error:
            print(f"API error (HTTP {error.status_code}); this question could not be tested.")
        except anthropic.APIError as error:
            print(f"API error; this question could not be tested: {error}")


if __name__ == "__main__":
    main()