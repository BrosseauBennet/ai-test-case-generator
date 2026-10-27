import json
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

MODEL = "claude-sonnet-5-5"

SYSTEM_PROMPT = """You are a senior QA engineer. Given a user story, write test cases.
Return ONLY a JSON array with no extra text. Write exactly 8 test cases:
3 positive, 3 negative, and 2 edge cases. Each test case has at most 5 steps.
Each item must have these keys:
"id", "title", "type" (one of: positive, negative, edge), "steps" (a list of strings), "expected_result"."""


def call_model(system: str, user: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    if message.stop_reason == "max_tokens":
        raise RuntimeError(
            "The response was cut off at max_tokens. "
            "Raise the limit or ask the model for less output."
        )
    return message.content[0].text


def generate_test_cases(user_story: str) -> list[dict]:
    text = call_model(SYSTEM_PROMPT, user_story).strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(text)


if __name__ == "__main__":
    story = " ".join(sys.argv[1:]) or (
        "As a shopper, I want to add items to my cart so that I can buy them later."
    )
    for case in generate_test_cases(story):
        print(f"[{case['type']}] {case['id']}: {case['title']}")
        for number, step in enumerate(case["steps"], 1):
            print(f"   {number}. {step}")
        print(f"   Expected: {case['expected_result']}\n")