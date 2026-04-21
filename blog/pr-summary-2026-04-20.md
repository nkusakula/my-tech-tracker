I'm unable to write to the filesystem in this environment, so here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-04-20

## Breaking Changes

None.

---

## Major Updates

### 🟦 .NET: Hosted Agents Toolbox Support
**[#5368](https://github.com/microsoft/agent-framework/pull/5368)** by `alliscode` | Labels: `.NET`

Adds Foundry Toolbox (MCP proxy) integration to `AgentFrameworkResponseHandler` in `Microsoft.Agents.AI.Foundry`. Supports two configuration modes:

- **Host-configured (eager/startup):** Toolboxes wired at startup for all requests.
- **Client-selectable (per-request/lazy):** Clients activate specific toolboxes per request.

Developers building hosted agents on Foundry can now route tool calls through MCP proxies without custom middleware.

---

### 🟦 .NET: Hosted Agent Adapter
**[#5374](https://github.com/microsoft/agent-framework/pull/5374)** · **[#5371](https://github.com/microsoft/agent-framework/pull/5371)** by `alliscode` | Labels: `.NET`

Introduces a hosted agent adapter for the .NET SDK (#5371 fixed the build; #5374 shipped the version bump). Enables .NET agents to be exposed and consumed as hosted (remote) agents in the framework's orchestration model.

---

### 🟦 .NET: Add a File Memory Provider
**[#5315](https://github.com/microsoft/agent-framework/pull/5315)** by `westey-m` | Labels: `.NET`

Introduces a file-backed memory provider for .NET agents — a foundational building block for agents that need to persist and recall memories across sessions without an external database.

---

### 🐍 Python: Add Support for Foundry Toolboxes
**[#5346](https://github.com/microsoft/agent-framework/pull/5346)** by `moonbox3` | Labels: `python`, `agents`

`FoundryChatClient` gains two new helpers:
- `get_toolbox()` — retrieves a named Foundry Toolbox.
- `select_toolbox_tools()` — selects specific tools from a toolbox for a session.

`normalize_tools` in the core package now flattens `ToolboxVersionObject` and generic tool-collection wrappers, so toolbox tools integrate seamlessly with existing patterns.

---

### 🐍 Python: Foundry Hosted Agent V2
**[#5379](https://github.com/microsoft/agent-framework/pull/5379)** by `TaoChenOSU` | Labels: `python`, `agents`

Second-generation Foundry-hosted agent integration for Python, aligned with the V2 Foundry agent hosting model.

---

### 🐍 Python: Expose `forwardedProps` via Session Metadata
**[#5264](https://github.com/microsoft/agent-framework/pull/5264)** by `moonbox3` | Labels: `python`

`forwardedProps` from AG-UI requests were previously parsed but silently dropped. They are now propagated through session metadata, accessible to agents, tools, and workflows:

```python
metadata = context.session_metadata
forwarded = metadata.get("forwardedProps", {})
invocation_source = forwarded.get("invocationSource")
```

Users can remove custom workarounds previously needed to thread request-level context (e.g., CopilotKit flags) into tools.

---

### 🐍 Python: Add Search Tool Content for OpenAI Responses
**[#5302](https://github.com/microsoft/agent-framework/pull/5302)** by `eavanvalkenburg` | Labels: `python`

The Python OpenAI chat client previously dropped web-search and file-search built-in tool calls/results from the framework content model. This change preserves them as first-class content items. Developers building search-augmented agents no longer need to parse raw provider responses to access search results.

---

## Minor Updates & Bug Fixes

- **[#5359](https://github.com/microsoft/agent-framework/pull/5359)** 🐛 `.NET` — **Fix: Duplicate CallIds break Handoff Message Filtering** (`lokitoth`): Providers like Gemini don't use `CallId` to disambiguate simultaneous function calls, producing duplicate CallIds that broke multi-turn message filtering. Fixed. Labels: `.NET`, `agent orchestration`, `workflows`

- **[#5365](https://github.com/microsoft/agent-framework/pull/5365)** `.NET` — **Harness: Improve prompts and add FileSystem store** (`westey-m`): Better default prompts and a FileSystem-backed store for local dev/testing.

- **[#4875](https://github.com/microsoft/agent-framework/pull/4875)** 🐍 `python` — **Add second approval-required tool to concurrent_builder sample** (`moonbox3`): Adds `set_stop_loss` alongside `execute_trade` to better showcase concurrent multi-tool approval workflows.

- **[#5378](https://github.com/microsoft/agent-framework/pull/5378)** 🐍 `python` — **Add more types** (`TaoChenOSU`): Expands type annotations across the Python SDK.

- **[#5372](https://github.com/microsoft/agent-framework/pull/5372)** 🐍 `python` — **Improve samples** (`TaoChenOSU`): General Python sample quality improvements.

- **[#5385](https://github.com/microsoft/agent-framework/pull/5385)** 🐍 `python` — **Bump versions for release; update CHANGELOG** (`moonbox3`): Ships `1.1.0` (stable), `1.0.0b260421` (beta), `1.0.0a260421` (alpha).

- **[#5367](https://github.com/microsoft/agent-framework/pull/5367)** `.NET` — **Bump preview version to `260420.1`; fix AgentServer deps** (`alliscode`): Version `0.0.1-preview.260420.1`, `Azure.AI.AgentServer.Core` `beta.21` → `beta.22`.

---

## Summary

April 20 was a high-velocity day for `microsoft/agent-framework`, defined by a coordinated cross-platform push to ship **Foundry Toolbox (MCP proxy) integration** in both .NET and Python, a new **.NET hosted agent adapter**, and a **Python Foundry hosted agent V2**. Two meaningful Python developer experience gaps were closed — the silent drop of `forwardedProps` and the loss of OpenAI built-in search results from the content model — while a new .NET file memory provider adds persistent memory without an external store. A targeted bug fix addresses Gemini-triggered handoff filtering failures in multi-turn agent orchestration.