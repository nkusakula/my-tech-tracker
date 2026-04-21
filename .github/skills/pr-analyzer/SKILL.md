---
name: pr-analyzer
description: Analyze merged pull requests and generate a structured technical summary blog post.   
---
# PR Analyzer Skill

## Purpose
Analyze merged pull requests from a GitHub repository and produce a structured
technical summary blog post.

## Input
A list of pull requests merged within a given date range, including:
- PR title, number, URL
- Author and merge date
- Description / body
- Labels
- Code diff summary (if available)

## Output Format
Generate a Markdown blog post with the following structure:

```
# [Repository] PR Summary — {YYYY-MM-DD}

## Breaking Changes
List any PRs that introduce breaking changes (API removals, behavioral changes,
deprecations). Highlight these prominently with ⚠️ markers.

## Major Updates
List significant new features, enhancements, or architectural changes.
Include code snippets where relevant to illustrate the change.

## Minor Updates & Bug Fixes
Summarize smaller improvements, documentation updates, and bug fixes in a
concise bullet list.

## Summary
A 2–3 sentence overall assessment of the day's activity: velocity, theme,
and impact for downstream users.
```

## Rules
1. Breaking Changes MUST be listed first, even if there are none (write "None").
2. Extract and include relevant code snippets for Major Updates when the diff
   shows a clear API or behavior change.
3. Keep the tone technical and informative — target audience is developers
   consuming the library.
4. If no PRs were merged, output a single line: "No pull requests merged today."
5. Use the PR number and URL as a reference link for each item, e.g.
   `[#123](https://github.com/org/repo/pull/123)`.
6. Do not include internal/bot PRs (e.g., Dependabot version bumps) in
   Breaking Changes or Major Updates — list them under Minor Updates only.
