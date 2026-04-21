"""
Automated PR analysis agent using the GitHub Copilot SDK.

Fetches pull requests merged in a GitHub repository (default: yesterday's),
passes them to a Copilot session with a custom skill, and writes the resulting
summary to the blog/ directory.

Usage:
    python pr_trigger.py [--repo owner/name] [--date YYYY-MM-DD]

Environment variables:
    GITHUB_TOKEN           GitHub token for the GitHub API (the built-in
                           Actions token works for public repo searches).
    COPILOT_TOKEN          GitHub PAT with Copilot scope for SDK auth.
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

# Load .env file if present (local development)
_env_file = pathlib.Path(__file__).parent / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

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
    next_day = (target_date + timedelta(days=1)).isoformat()
    query = f"repo:{repo} is:pr is:merged merged:>={date_str} merged:<{next_day}"
    url = (
        "https://api.github.com/search/issues"
        f"?q={urllib.parse.quote(query)}&per_page=15&sort=updated&order=desc"
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
            lines.append(f"  Description: {body[:250]}")
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

    copilot_token = os.environ.get("COPILOT_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not copilot_token:
        print("ERROR: Neither COPILOT_TOKEN nor GITHUB_TOKEN is set.")
        sys.exit(1)
    print(f"Using Copilot token: {'COPILOT_TOKEN' if os.environ.get('COPILOT_TOKEN') else 'GITHUB_TOKEN'}")

    config = SubprocessConfig(github_token=copilot_token)

    async with CopilotClient(config=config) as client:
        print("Copilot client started.")

        session: CopilotSession = await client.create_session(
            skill_directories=[SKILL_DIR],
            on_permission_request=lambda req: PermissionRequestResult(kind="approved"),
        )
        print("Copilot session created.")

        prompt = (
            f"Analyze the following pull requests merged on {target_date} "
            f"and produce a structured blog post following the pr-analyzer skill.\n\n"
            f"{pr_text}"
        )

        print("Sending prompt to Copilot …")
        try:
            reply = await session.send_and_wait(prompt, timeout=600.0)
            print(f"Reply received: type={reply.type if reply else None}")
        except Exception as exc:
            print(f"ERROR during send_and_wait: {exc}")
            reply = None

        content: str = ""
        if reply and reply.data:
            content = reply.data.content or reply.data.message or ""

        # Fallback: scan all accumulated messages for the longest assistant text
        if not content:
            try:
                messages = await session.get_messages()
                print(f"Scanning {len(messages)} accumulated message(s) …")
                best = ""
                for evt in reversed(messages):
                    if evt.type == SessionEventType.ASSISTANT_MESSAGE and evt.data:
                        text = evt.data.content or evt.data.message or ""
                        # Debug: show available non-None fields
                        if not best:
                            non_none = {
                                k: repr(v)[:80]
                                for k, v in vars(evt.data).items()
                                if v is not None
                            }
                            print(f"  DEBUG data fields: {non_none}")
                        if len(text) > len(best):
                            best = text
                content = best
            except Exception as exc:
                print(f"ERROR scanning messages: {exc}")

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
