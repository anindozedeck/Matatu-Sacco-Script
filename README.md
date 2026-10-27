# Matatu SACCO Q&A

A small command-line assistant for answering common member questions for a
matatu SACCO in Thika. It uses the Anthropic API to respond to questions about
membership fees, monthly contributions, and meeting schedules.

## Requirements

- Python 3.10 or later
- An Anthropic API key
- Internet access when running the assistant

## Setup

Install the required Python packages:

```powershell
python -m pip install anthropic python-dotenv
```

Create a `.env` file in the project directory and add your API key:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Keep your API key private. Do not commit the `.env` file.

## Run

Start the interactive assistant:

```powershell
python Day11_exercise.py
```

Enter a member's question at the prompt. Type `quit` or `exit` to stop.

Run six sample question variations:

```powershell
python Day11_exercise.py --test
```

## Demo information

The script's system prompt currently uses these example details:

- One-time membership fee: KSh 5,000
- Monthly membership contribution: KSh 1,500, due by the 5th
- Regular members' meeting: first Saturday of the month at 10:00 AM at the
  SACCO office in Thika

These are demo values, not verified SACCO information. Update them in
`SYSTEM_PROMPT` in `Day11_exercise.py` and confirm the details with the SACCO
before sharing the assistant with members.

The assistant cannot access member accounts or payment records, so it directs
balance questions to the treasurer or secretary rather than guessing.

## API usage

Each question sent to the assistant uses the Anthropic API and may incur
charges according to your account and model pricing. The `--test` option sends
six API requests.
