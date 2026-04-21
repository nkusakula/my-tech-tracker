"""
Automated PR analysis agent using the GitHub Copilot SDK.

Fetches pull requests merged in a GitHub repository (default: yesterday's),
passes them to a Copilot session with a custom skill, and writes the resulting
summary to the blog/ directory.

Usage:
    python pr_trigger.py [--repo owner/name] [--date YYYY-MM-DD]

Environment variables:
    GITHUB_TOKEN           GitHub token for both the GitHub API and Copilot SDK
                           auth (the built-in Actions token works for API calls;
                           Copilot access requires a token with copilot scope).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

from copilot.client import CopilotClient, SubprocessConfig
from copilot.session import (
    CopilotSession,
    PermissionRequest,
    PermissionRequestResult,
)
from copilot.generated.session_events import SessionEvent, SessionEventType

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = pathlib.Path(__file__).parent
SKILL_DIR = str(ROOT / ".github" / "skills")
BLOG_DIR = ROOT / "blog"
BLOG_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------

def _github_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    headers: dict[str, str] = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_merged_prs(repo: str, target_date: date) -> list[dict]:
    """Return a list of PR dicts merged on *target_date* (UTC) in *repo*."""
    date_str = target_date.isoformat()
    query = f"repo:{repo} is:pr is:merged merged:{date_str}"
    url = (
        "https://api.github.com/search/issues"
        f"?q={urllib.parse.quote(query)}&per_page=50&sort=updated&order=desc"
    )

    req = urllib.request.Request(url, headers=_github_headers())
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    return data.get("items", [])


def format_pr_list(prs: list[dict], repo: str) -> str:
    """Format raw PR items into a prompt-friendly text block."""
    if not prs:
        return "No pull requests were merged."

    lines = [f"Merged PRs for {repo}:\n"]
    for pr in prs:
        lines.append(
            f"- #{pr['number']} [{pr['title']}]({pr['html_url']})"
            f" by {pr.get('user', {}).get('login', 'unknown')}"
            f" | labels: {', '.join(l['name'] for l in pr.get('labels', []))}"
        )
        body = (pr.get("body") or "").strip()
        if body:
            # Trim very long PR bodies
            lines.append(f"  Description: {body[:400]}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main agent logic
# ---------------------------------------------------------------------------

async def run(repo: str, target_date: date) -> None:
    print(f"Fetching PRs merged on {target_date} in {repo} …")
    try:
        prs = fetch_merged_prs(repo, target_date)
    except Exception as exc:  # noqa: BLE001
        print(f"Warning: could not fetch PRs from GitHub API: {exc}")
        prs = []

    pr_text = format_pr_list(prs, repo)
    print(f"  Found {len(prs)} PR(s).\n")

    token = os.environ.get("GITHUB_TOKEN")
    config = SubprocessConfig(github_token=token) if token else None

    client = CopilotClient(config=config)
    await client.start()

    session: CopilotSession = await client.create_session(
        skill_directories=[SKILL_DIR],
        on_permission_request=lambda req: PermissionRequestResult(kind="approved"),
    )

    prompt = (
        f"Analyze the following pull requests merged on {target_date} "
        f"and produce a structured blog post following the pr-analyzer skill.\n\n"
        f"{pr_text}"
    )

    print("Sending prompt to Copilot …")
    reply = await session.send_and_wait(prompt, timeout=300.0)

    content: str = ""
    if reply and reply.type == SessionEventType.ASSISTANT_MESSAGE:
        content = reply.data.message or ""

    # Fallback: scan all accumulated messages for assistant reply
    if not content:
        for evt in reversed(session.get_messages()):
            if (
                evt.type == SessionEventType.ASSISTANT_MESSAGE
                and evt.data
                and evt.data.message
            ):
                content = evt.data.message
                break

    if not content:
        print("No response received from Copilot.")
        sys.exit(1)

    out_path = BLOG_DIR / f"pr-summary-{target_date}.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"\nBlog post written to: {out_path}")
    print("\n--- Preview (first 500 chars) ---")
    print(content[:500])


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a PR summary blog post.")
    parser.add_argument(
        "--repo",
        default="microsoft/agent-framework",
        help="GitHub repository in owner/name format (default: microsoft/agent-framework)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Target date YYYY-MM-DD (default: yesterday UTC)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    target = (
        date.fromisoformat(args.date)
        if args.date
        else date.today() - timedelta(days=1)
    )
    asyncio.run(run(repo=args.repo, target_date=target))
