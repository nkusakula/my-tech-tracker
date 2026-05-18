The filesystem appears to be read-only in this environment. Here is the complete blog post — you can save it to `blog/2026-05-17-microsoft-agent-framework.md`:

---

# microsoft/agent-framework PR Summary — 2026-05-17

## Breaking Changes

⚠️ [#5872](https://github.com/microsoft/agent-framework/pull/5872) **Python: bump package versions for 1.4.0 release** — by giles17 | labels: `documentation`, `python`, `lab`

The Python `1.4.0` release introduces **two breaking changes** to the experimental skills API. The following packages received a MINOR version bump (`1.3.0 → 1.4.0`):

- `agent-framework`
- `agent-framework-core`
- `agent-framework-openai`
- `agent-framework-foundry`

Consumers of the experimental skills API should review the release notes carefully before upgrading, as behavioral compatibility is not guaranteed across this boundary.

---

## Major Updates

### 🔒 Security: Path-Traversal Fix in Foundry Hosting Checkpoint Storage

[#5851](https://github.com/microsoft/agent-framework/pull/5851) **Python: Reject path-traversal context ids in Foundry Hosting Checkpoint Storage** — by Copilot | labels: `python`, `workflows`

`ResponsesHostServer._handle_workflow_agent` previously derived a checkpoint directory from caller-supplied values (`previous_response_id`, `conversation_id`, `response_id`) via `os.path.join(...)` without sanitisation, opening a path-traversal attack vector. This PR adds validation to reject any context id containing traversal sequences (e.g. `../`), ensuring checkpoint paths stay within the intended storage root.

---

### 🐛 Python: GitHubCopilotAgent Now Forwards Dynamically-Registered Tools

[#5780](https://github.com/microsoft/agent-framework/pull/5780) **Python: Fix GitHubCopilotAgent to include tools added by ContextProvider.before_run in session creation** — by giles17 | labels: `python`

`SkillsProvider.before_run` registers tools such as `load_skill` via `context.extend_tools()`, but `GitHubCopilotAgent` only forwarded constructor-supplied tools (`self._tools`) when creating or resuming Copilot sessions. This caused dynamically-added tools to be silently unavailable. The fix ensures the full resolved tool list (including those added by context providers) is forwarded during session creation and resumption.

---

### 🐛 Python: A2A v1.0 Non-Streaming Response & Sample Runtime Fixes

[#5849](https://github.com/microsoft/agent-framework/pull/5849) **Python: Fix A2A v1.0 non-streaming response and sample runtime issues** — by giles17 | labels: `documentation`, `python`

Addresses two regressions introduced by the A2A SDK v1.0 migration (#5752):

1. **Non-streaming empty response** — In v1.0 the stream yields individual `StreamResponse` events rather than full `Task` objects with accumulated history. `A2AExecutor` was not accumulating these events, producing an empty non-streaming response.
2. **Sample runtime issues** — Several sample scripts broke due to interface changes in the v1.0 SDK.

---

### ✨ Python: MCP Tool Call Metadata Forwarding

[#5815](https://github.com/microsoft/agent-framework/pull/5815) **Python: forward MCP tool call metadata** — by he-yufeng | labels: `python`

- Caches per-tool metadata returned by `MCP tools/list`.
- Passes that metadata back on `MCP tools/call` while still layering in OpenTelemetry trace context.
- Adds a regression test for direct `MCPTool.call_tool()` calls that bypass the `FunctionTool` wrapper.

---

### 🐛 Python: YAML Block Scalar Support in SKILL.md Frontmatter

[#5863](https://github.com/microsoft/agent-framework/pull/5863) **Python: Parse YAML block scalars in SKILL.md frontmatter** — by SergeyMenshykh | labels: `python`

Fixes [#5713](https://github.com/microsoft/agent-framework/issues/5713). The `_extract_frontmatter()` parser previously only matched single-line `key: value` pairs, silently truncating multi-line values that used YAML block scalar indicators (`|` literal, `>` folded, and chomping modifiers `-`/`+`). The parser now correctly handles block scalars in SKILL.md frontmatter.

---

### ✨ .NET: Observer for OpenAIWebSearch Tool

[#5894](https://github.com/microsoft/agent-framework/pull/5894) **.NET: Add observer for OpenAIWebSearch** — by westey-m | labels: `.NET`

Adds an observer to the console samples that surfaces richer detail for calls to the `OpenAIResponses` `web_search` tool, improving developer visibility into web search invocations during local development and debugging.

---

### 🐛 .NET: Fix Store-False Helper (Factory Replacement vs. Appending)

[#5895](https://github.com/microsoft/agent-framework/pull/5895) **.NET: Fix bug in store-false helper to ensure addition rather than replacement** — by westey-m | labels: `.NET`

Using `AsIChatClientWithStoredOutputDisabled` previously caused any other raw-representation factory to be **replaced** when using `ResponsesClient`, whereas `ProjectClient` correctly **appended**. This PR aligns `ResponsesClient` behaviour to append, making factory composition consistent across both client types.

---

### ✨ .NET: Hosted-MemoryAgent Sample with Isolation Key Plumbing

[#5702](https://github.com/microsoft/agent-framework/pull/5702) **.NET: Add Hosted-MemoryAgent sample with isolation key plumbing** — by rogerbarreto | labels: `documentation`, `.NET`

Closes #5692. Adds a `Hosted-MemoryAgent` sample demonstrating `FoundryMemoryProvider` running inside a Foundry hosted agent, with per-end-user memory scoping via platform isolation headers. Includes the framework hooks required to plumb isolation keys through the agent lifecycle.

---

### ✨ Python: New Foundry Hosted Agent Samples (RAG, Skills, Memory)

[#5822](https://github.com/microsoft/agent-framework/pull/5822) **Python: New Foundry Hosted Agents samples: RAG, Skills, and Memory** — by TaoChenOSU | labels: `documentation`, `python`, `samples`

Adds three new end-to-end Python samples for Foundry Hosted Agents covering:
- **RAG** — retrieval-augmented generation patterns
- **Skills** — skill registration and invocation
- **Memory** — stateful memory across agent turns

---

### 🧪 .NET: Magentic End-to-End Workflow Test Coverage

[#5833](https://github.com/microsoft/agent-framework/pull/5833) **.NET: Add Magentic E2E workflow coverage** — by Copilot | labels: `.NET`, `agent orchestration`, `workflows`

Completes the Magentic orchestrator end-to-end test plan (`MagenticE2E_TestPlan.md`). Covers all user-visible branches of the Magentic orchestrator including happy-path orchestration, error propagation, and edge-case termination conditions.

---

### ✨ Workflow Improvements

[#5880](https://github.com/microsoft/agent-framework/pull/5880) **Workflow improvements** — by moonbox3

General workflow improvements to the agent framework's workflow execution layer.

---

## Minor Updates & Bug Fixes

- [#5800](https://github.com/microsoft/agent-framework/pull/5800) **.NET: fix: avoid AGUI tool result message id collisions** (by he-yufeng | `.NET`) — Generates a separate fallback message id for tool-result-only updates; keeps assistant text and tool-call parent events on the shared assistant fallback id. Adds a regression test covering null provider `MessageId` with text, tool call, and tool result events.

- [#5838](https://github.com/microsoft/agent-framework/pull/5838) **.NET: add AgentSession StateBag edge case coverage** (by challaravinath | `.NET`) — Expands `AgentSession.StateBag` test coverage to include empty initial state, independent multi-key storage, and value overwrite behaviour.

- [#5837](https://github.com/microsoft/agent-framework/pull/5837) **.NET: Re-enable previously-flaky ObservabilityTests and WorkflowRunActivityStopTests** (by Copilot | `.NET`) — Closes #4398. Re-enables `CreatesWorkflowEndToEndActivities_WithCorrectName_OffThreadAsync` and related test suites that had been marked `[Fact(Skip = ...)]` due to intermittent failures.

---

## Summary

May 17 was a high-velocity day for `microsoft/agent-framework`, with 15 PRs merged spanning both the .NET and Python SDKs. The headline event is the **Python 1.4.0 release** (⚠️ two breaking changes in the experimental skills API), accompanied by a cluster of correctness and security fixes — notably a **path-traversal vulnerability patch** in Foundry Hosting checkpoint storage, a `GitHubCopilotAgent` tool-forwarding fix, and A2A v1.0 non-streaming response handling. On the .NET side, an `OpenAIWebSearch` observer, a store-false factory composition bug fix, and completion of Magentic E2E test coverage round out a day that emphasises reliability, security hardening, and developer experience across both ecosystems.

---

> **Note:** The environment is currently read-only so the file could not be saved to `blog/`. You can paste the above into `blog/2026-05-17-microsoft-agent-framework.md` manually.