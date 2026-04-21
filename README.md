# my-tech-tracker

Automated tech-update tracker built with the **GitHub Copilot SDK** (Python).

Inspired by the blog post:
[Building Agents with GitHub Copilot SDK: A Practical Guide to Automated Tech Update Tracking](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/building-agents-with-github-copilot-sdk-a-practical-guide-to-automated-tech-upda/4488948)

## What it does

1. Fetches pull requests merged on a given date from a GitHub repository (default: `microsoft/agent-framework`).
2. Sends the PR list to a Copilot session that uses a custom **pr-analyzer** skill.
3. Saves a structured Markdown blog post to the `blog/` directory.
4. A GitHub Actions workflow runs this automatically Monday–Friday at 00:05 UTC.

## Project structure

```
my-tech-tracker/
├── pr_trigger.py                        # Main agent script
├── requirements.txt
├── blog/                                # Generated blog posts land here
└── .github/
    ├── skills/
    │   └── pr-analyzer/
    │       └── SKILL.md                 # Custom skill definition
    └── workflows/
        └── daily-pr-analysis.yml        # CI/CD automation
```

## Prerequisites

- Python 3.11+
- [GitHub Copilot CLI](https://github.com/github/copilot) installed globally (`npm install -g github/copilot`)
- A GitHub account with Copilot access
- `COPILOT_GITHUB_TOKEN` environment variable set to a token with **Copilot Requests: Read** permission

## Local setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your GitHub Copilot token
export COPILOT_GITHUB_TOKEN=ghp_...

# Run for yesterday's PRs (default repo: microsoft/agent-framework)
python pr_trigger.py

# Run for a specific repo and date
python pr_trigger.py --repo microsoft/semantic-kernel --date 2026-04-19
```

## CI/CD (GitHub Actions)

1. Add `COPILOT_GITHUB_TOKEN` as a repository secret.
2. The workflow (`daily-pr-analysis.yml`) runs automatically on weekdays.
3. You can also trigger it manually from the **Actions** tab with optional `repo` and `date` inputs.

## Customising the skill

Edit `.copilot_skills/pr-analyzer/SKILL.md` to adjust:
- Output format / sections
- Tone and target audience
- Rules for classifying PRs (breaking vs. major vs. minor)
