I'm unable to write files in this environment due to permissions, but here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-05-12

## Breaking Changes

⚠️ **[#5752](https://github.com/microsoft/agent-framework/pull/5752) — Python: Migrate `agent-framework-a2a` to `a2a-sdk` v1.0** by *giles17*
**Labels:** documentation, python

The Python `agent-framework-a2a` package has been migrated from `a2a-sdk` **v0.3.x → v1.0**, aligning with the A2A protocol v1.0 release. Downstream consumers must upgrade their `a2a-sdk` dependency and review API surface changes. Mirrors the .NET migration in #5423; closes #5661.

---

## Major Updates

### .NET

**[#5743](https://github.com/microsoft/agent-framework/pull/5743) — Add A2A input-request content for human-in-the-loop scenarios** by *SergeyMenshykh*
**Labels:** documentation, .NET

Introduces first-class support for A2A agents returning an `input-required` task state. Two new content types:
- `A2AInputRequestContent` — wraps the requested `AIContent` from the remote agent.
- `A2AInputResponseContent` — wraps the user's reply to send back.

Enables structured human-in-the-loop flows over A2A without manually inspecting raw task states.

---

**[#5739](https://github.com/microsoft/agent-framework/pull/5739) — DevUI: configurable access controls for the DevUI HTTP surface** by *moonbox3*
**Labels:** documentation, .NET, devui

`Microsoft.Agents.AI.DevUI` previously exposed `/devui`, `/v1/entities`, and related endpoints with zero access control. This PR adds configurable authorization middleware, critical for any host reachable beyond `localhost`.

---

**[#5604](https://github.com/microsoft/agent-framework/pull/5604) — Feat: .NET Shell Tool** by *alliscode*
**Labels:** documentation, .NET

Adds a shell tool to the .NET built-in tool catalog, enabling agents to execute shell commands as part of their tool-use loop — bringing .NET to parity with Python-side capabilities.

---

**[#5778](https://github.com/microsoft/agent-framework/pull/5778) — Declare Magentic protocol messages** by *he-yufeng*
**Labels:** .NET, workflows

Formally declares the `ChatMessage` and `ResetChatSignal` messages that `MagenticOrchestrator` sends at runtime, and adds a protocol regression test to prevent silent contract drift. Fixes #5774.

---

**[#5718](https://github.com/microsoft/agent-framework/pull/5718) — Fix: Synthesized Handoff `FunctionResult` is never sent to agent** by *lokitoth*
**Labels:** .NET, workflows

Fixes a critical bug where the synthesized `FunctionResult` for a handoff was never delivered back into the agent loop, causing agents to stall silently after a handoff request.

---

**[#5763](https://github.com/microsoft/agent-framework/pull/5763) — Trigger issue triage on bug-labeled issues** by *moonbox3*

Issue Triage now fires automatically on bug-labeled issues rather than requiring manual `workflow_dispatch`, removing the maintainer gate and accelerating noise filtering.

---

### Python

**[#5762](https://github.com/microsoft/agent-framework/pull/5762) — Add ag-ui tool result display channel** by *moonbox3*
**Labels:** documentation, python, ag-ui

Separates the ag-ui emitter's UI display channel (`ToolCallResultEvent.content`) from the agent's data channel (`flow.tool_results[].content`), which were previously receiving the same string. Enables richer formatted UI output without polluting the agent's structured data feed. Closes #5760.

---

## Minor Updates & Bug Fixes

- **[#5717](https://github.com/microsoft/agent-framework/pull/5717)** (.NET) CI hardening: splits long-running integration tests into a dedicated job and re-enables previously skipped tests to improve signal quality. — *giles17*
- **[#5748](https://github.com/microsoft/agent-framework/pull/5748)** (.NET) Fix `OpenAIResponsesAgentClient` to include `agentName` in endpoint path; previously hardcoded to `/v1/`, causing HTTP 400 on LMGateway-style endpoints. — *giles17*
- **[#5709](https://github.com/microsoft/agent-framework/pull/5709)** (.NET) Align Anthropic Extensions AI version to fix `MissingMethodException` on `WebSearchToolResultContent.Results`. Related to #5707. — *danyalahmed1995*
- **[#5751](https://github.com/microsoft/agent-framework/pull/5751)** (.NET) Refactor harness console rendering with a framework-based approach; fixes resize failures and simplifies the rendering path. — *westey-m*
- **[#5753](https://github.com/microsoft/agent-framework/pull/5753)** (.NET) Remove Foundry Toolbox server-side tools support; the `HostedMcpToolboxAITool` + `FoundryToolboxService` path remains. Mirrors Python cleanup in #5671. — *alliscode*
- **[#5744](https://github.com/microsoft/agent-framework/pull/5744)** (.NET) Fix per-service input persistence on stream error; adds `PersistInputOnErrorAsync` to ensure chat history is written even on early enumerator disposal. — *alliscode*
- **[#5768](https://github.com/microsoft/agent-framework/pull/5768)** Propagate GitHub token to the issue-triage workflow's repro step, fixing a missing-credential gap. — *moonbox3*

---

## Summary

May 12th was a high-velocity day with 15 PRs merged across .NET and Python. The dominant theme was **protocol alignment and workflow robustness**: the Python A2A stack completed its breaking migration to `a2a-sdk` v1.0, .NET gained first-class human-in-the-loop A2A content types and DevUI access controls, and two significant workflow bugs (handoff result delivery, Magentic protocol declaration) were fixed. Python consumers of `agent-framework-a2a` **must** upgrade to `a2a-sdk` v1.0; .NET consumers should audit A2A and workflow-layer usages before updating.