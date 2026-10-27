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

I compared the generated cases against the manual test cases I wrote for [SauceDemo](https://github.com/BrosseauBennet/saucedemo-testing) across 1 run.

**What it caught that I missed**
- Five cases that weren't in my manual login set (TC-01 to TC-04):
  - TC002: submitting the form with the Enter key
  - TC003: session persists after a page refresh
  - TC005: login with a non-existent username (I only tested a wrong password)
  - TC007: username with leading/trailing spaces and different letter case
  - TC008: very long input and an SQL injection string
- It also raised a security point I hadn't considered: the error for an unknown username should be the same as for a wrong password, so attackers can't tell which usernames exist.

**What it missed**
- Locked-out or disabled accounts (my TC-03): none of the titles in any of three runs mention one, although it's a standard login scenario. The story doesn't mention account states, so this is a limit of generic input.
- Its basic cases mostly duplicated my own: valid login, wrong password, and empty fields map to my TC-01, TC-02, and TC-04.
- Password field masking appeared in two of three runs, so coverage of it is inconsistent rather than missing.

**Consistency between runs**
- I ran the same story three times. In the two runs I saved (`sample-runs/`), 5 of 8 case titles were identical.
- The remaining three covered the same themes but split them differently. For example, one run paired password masking with logout and re-login, and the other paired it with session persistence on refresh.
- Case ID format also varied between runs (`TC001` vs `TC-001`) because my prompt didn't specify one.
- Takeaway for testing: the output isn't reproducible, so it can't be treated as a fixed test plan.

**What it invented or got wrong**
- UI details it couldn't know: it called the button 'Log in', but on SauceDemo it's 'Login'.
- Expected results that differ from the real app: for empty fields, TC006 expects validation messages for both username and password, but SauceDemo shows only 'Username is required' (my TC-04).
- Requirements the story never stated: session persistence (TC003), identical error messages for unknown users and wrong passwords (TC005), and whitespace/case handling rules (TC007).
- Untestable expected results: TC007 accepts either outcome (trim and log in, or reject), so it can never fail and can't be automated as an assertion.
- Bundled tests: TC008 combines a 1000+ character input and an SQL injection string in one case, with an unclear "or".

**Takeaway:** The generator is a good source of edge cases I hadn't thought of, but it works from generic assumptions, so its expected results need checking against the real app before they go into a test plan.

## Problems I ran into

**Truncated output broke JSON parsing.** My first version capped the response at 2,000 tokens. The model returned more test cases than fit, the response was cut off mid-string, and `json.loads` failed with an unterminated string error. I fixed it by raising the limit, asking for a fixed number of cases with a cap on steps per case, and checking `stop_reason` so a cut-off response fails with a clear message instead of a confusing traceback.

## Known limitations

- Output varies from run to run, so results aren't reproducible.
- The model can invent requirements that aren't in the story, so generated cases need review.

## Planned next steps

- Validate output against a schema and retry on malformed responses
- Bug report generator
- Convert plain-English steps into Playwright tests
- Automated tests for this tool using mocked model responses
- CI workflow
