# AI Test Case Generator

Python tools that use the Claude API to turn QA inputs, starting with user stories, into structured test cases, plus notes on how I verified the output.

## What it does

`generate_tests.py` takes a user story and returns test cases as JSON: a title, a type (positive, negative, or edge), steps, and an expected result.

```bash
python generate_tests.py "As a user, I want to log in with a username and password so that I can see my account."
```

## Setup

Requires Python 3.11 or newer and an Anthropic API key.

```bash
git clone https://github.com/BrosseauBennet/ai-test-case-generator.git
cd ai-test-case-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your key (it is gitignored):

```
ANTHROPIC_API_KEY=your-key-here
```

## How I verified the output

I compared the generated cases against the manual test cases I wrote for [SauceDemo](https://github.com/BrosseauBennet/saucedemo-testing) across [number] runs.

**What it caught that I missed**
- [Example, with case ID or title]

**What it missed**
- [Example from your manual cases that never appeared]

**What it invented or got wrong**
- [Example: a rule or UI element the story never mentioned]

**Consistency between runs**
- [Same story, different output? How much did the cases differ?]

**Takeaway:** [One sentence, for example: useful as a brainstorming starting point, but every case needs human review before it goes into a test plan.]

## Problems I ran into

**Truncated output broke JSON parsing.** My first version capped the response at 2,000 tokens. The model returned more test cases than fit, the response was cut off mid-string, and `json.loads` failed with an unterminated string error. I fixed it by raising the limit, asking for a fixed number of cases with a cap on steps per case, and checking `stop_reason` so a cut-off response fails with a clear message instead of a confusing traceback.

## Known limitations

- Output varies from run to run, so results aren't reproducible.
- The model can invent requirements that aren't in the story, so generated cases need review.
- [Add anything else you noticed.]

## Planned next steps

- Validate output against a schema and retry on malformed responses
- Bug report generator
- Convert plain-English steps into Playwright tests
- Automated tests for this tool using mocked model responses
- CI workflow
