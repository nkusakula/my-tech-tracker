I'm encountering filesystem permission issues in this environment, so I'll present the blog post directly here:

---

# microsoft/agent-framework PR Summary — 2026-05-04

## Breaking Changes

> ⚠️ None identified in today's merged PRs.

---

## Major Updates

### 🧠 [#5613](https://github.com/microsoft/agent-framework/pull/5613) — Python: Experimental Memory Harness Context Provider
**Author:** eavanvalkenburg | **Labels:** python

Adds an experimental **memory harness context provider** to the Python core, completing the Python-side of the Agent Harness feature. The .NET counterpart shipped earlier via [#5310](https://github.com/microsoft/agent-framework/pull/5310) and follow-ups #5404, #5365, #5540. This provider enables agents to plug in memory backends via the harness abstraction, alongside the sibling mode (#5611) and todo (#5612) context providers.

---

### 🏗️ [#5310](https://github.com/microsoft/agent-framework/pull/5310) — .NET: Harness Feature Branch
**Author:** westey-m | **Labels:** documentation, .NET

A significant architectural addition: the **Agent Harness** for .NET, providing a structured host/execution context with pluggable context providers (memory, mode, todo). This is the foundational .NET implementation that the Python work in #5613 mirrors.

---

### ✅ [#5562](https://github.com/microsoft/agent-framework/pull/5562) — Python: Enforce `approval_mode` in Claude and GitHub Copilot Agents
**Author:** eavanvalkenburg | **Labels:** python, agents

Closes a silent policy gap: tools declared with `approval_mode="always_require"` were **silently executed** by `ClaudeAgent` and `GitHubCopilotAgent` because their SDK-managed loops called `FunctionTool.invoke()` directly, bypassing the framework's approval gate. The fix enforces approval checks consistently across all agent implementations.

> **Impact:** Workflows relying on the prior (incorrect) pass-through behavior for Claude or GitHub Copilot agents will now correctly pause for approval.

---

### 🌐 [#5589](https://github.com/microsoft/agent-framework/pull/5589) — .NET: Declarative Workflow MCP Approval Support
**Author:** alliscode | **Labels:** .NET, workflows

Adds conversion of **MCP approval request/response items** to `ChatMessage` objects in declarative workflows, with session state bag mapping and robust argument parsing — enabling correct interop between approval workflows and MCP-based tool hosts.

---

### 🔌 [#5599](https://github.com/microsoft/agent-framework/pull/5599) — Python: `HttpRequestAction` in Declarative Workflows
**Author:** peibekwe | **Labels:** documentation, python

Achieves Python parity with .NET's `Microsoft.Agents.AI.Workflows.Declarative`: workflow authors can now dispatch HTTP calls directly from declarative workflow definitions in Python.

---

### 🔊 [#5619](https://github.com/microsoft/agent-framework/pull/5619) — Python: GPT-5 Verbosity Option + Foundry `agent_reference` Restored
**Author:** moonbox3 | **Labels:** documentation, python

Two fixes from GPT-5/Foundry testing: (1) the new `verbosity` parameter for GPT-5 family models is now passed through correctly on both the Responses and Chat Completions APIs; (2) `agent_reference` for Foundry-hosted deployments was regressed and is now restored.

---

### 🐛 [#5462](https://github.com/microsoft/agent-framework/pull/5462) — Python: Fix `background=True` + Tools Infinite-Retrieve Loop
**Author:** he-yufeng | **Labels:** python

Fixes [#5394](https://github.com/microsoft/agent-framework/issues/5394). Combining `background=True` with local function tools caused an **infinite retrieve loop** — polling the same completed response on every iteration without ever POSTing tool results — until `max_iterations` was exhausted. The fix correctly detects the completed background run state and routes tool results to the POST path.

---

### 📡 [#5608](https://github.com/microsoft/agent-framework/pull/5608) & [#5596](https://github.com/microsoft/agent-framework/pull/5596) — Python: New Hosted Agent Samples
**Author:** TaoChenOSU | **Labels:** documentation, python, samples

Two new end-to-end samples: one demonstrating a **hosted agent with observability** (tracing/telemetry for Foundry deployments), and one covering **file attachments** with hosted agents.

---

## Minor Updates & Bug Fixes

- **[#5617](https://github.com/microsoft/agent-framework/pull/5617)** *(eavanvalkenburg)* — Adds missing test coverage for empty-message pruning in `_replace_approval_contents_with_results` (requested in review of [#5331](https://github.com/microsoft/agent-framework/pull/5331)).
- **[#5509](https://github.com/microsoft/agent-framework/pull/5509)** *(moonbox3)* — Adds `redis[asyncio]` to `requirements.txt` for the two streaming samples that import `redis.asyncio` but previously omitted the dependency.
- **[#5622](https://github.com/microsoft/agent-framework/pull/5622)** *(aishsawant0202-tech)* — Fixes stale `@ai_function` → `@tool` reference in the workflows README; the rename happened in `python-1.0.0b260128` and caused `ImportError` for new users.
- **[#5580](https://github.com/microsoft/agent-framework/pull/5580)** *(moonbox3)* — Corrects observability docs to clarify that W3C `traceparent`/`tracestate` injection via `params._meta` does **not** apply to Foundry hosted/toolbox MCP tools.
- **[#5508](https://github.com/microsoft/agent-framework/pull/5508)** *(moonbox3)* — Docs: recommends `uv venv` and documents a workaround for the `python -m venv` hang on Windows with Microsoft Store Python 3.13.
- **[#5534](https://github.com/microsoft/agent-framework/pull/5534)** *(chetantoshniwal)* — Main README enhanced with 1.0 feature highlights, a Table of Contents, and reduced redundancy.

---

## Summary

The May 4, 2026 batch for `microsoft/agent-framework` is dominated by two themes: **agent harness cross-language parity** and **approval workflow correctness**. The experimental memory harness context provider ([#5613](https://github.com/microsoft/agent-framework/pull/5613)) brings Python in line with the already-shipped .NET harness ([#5310](https://github.com/microsoft/agent-framework/pull/5310)), while [#5562](https://github.com/microsoft/agent-framework/pull/5562) closes a real security/policy gap where `approval_mode="always_require"` was silently bypassed in Claude and GitHub Copilot agents. The `background=True` + tools infinite-loop fix ([#5462](https://github.com/microsoft/agent-framework/pull/5462)) is the most impactful bug fix of the day — consumers using that combination should upgrade promptly.