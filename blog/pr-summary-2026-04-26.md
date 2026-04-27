I'm running into filesystem permission issues in this environment. Here is the complete blog post ready to save as `blog/2026-04-26-microsoft-agent-framework.md`:

---

# microsoft/agent-framework PR Summary — 2026-04-26

## Breaking Changes

None.

---

## Major Updates

### 🐍 Python: Functional Workflow API (Core)
**[#4238](https://github.com/microsoft/agent-framework/pull/4238)** — *moonbox3* · `python` `workflows` `documentation`

Introduces a `@workflow` / `@step` decorator-based API — no executor classes, no edge definitions, no builder patterns:

```python
@workflow
async def my_workflow(ctx: WorkflowContext) -> str:
    result = await step_one(ctx)
    return await step_two(ctx, result)

@step
async def step_one(ctx: WorkflowContext) -> str:
    ...
```

A foundational addition bridging single-agent use and the full graph API. Shipped in the 1.2.0 release.

---

### 🐍 Python: Agent Framework ↔ A2A Bridge
**[#2403](https://github.com/microsoft/agent-framework/pull/2403)** — *Shubham-Kumar-2000* · `python` `documentation`

Enables any Agent Framework agent to be exposed as an **A2A (Agent-to-Agent) hosted server**, including an event adapter that converts agent messages to the A2A protocol. Opens the framework to cross-vendor agent interoperability.

---

### 🐍 Python: OpenTelemetry Tracing for `GitHubCopilotAgent`
**[#5142](https://github.com/microsoft/agent-framework/pull/5142)** — *droideronline* · `python` `documentation`

Splits `GitHubCopilotAgent` into `RawGitHubCopilotAgent` (no telemetry) and `GitHubCopilotAgent` (wraps with `AgentTelemetry`), consistent with `ClaudeAgent` and `FoundryAgent`. OTel tracing now covers all three major backends.

---

### 🐍 Python: Surface `oauth_consent_request` Events in Foundry Clients
**[#5070](https://github.com/microsoft/agent-framework/pull/5070)** — *giles17* · `python`

Fixes a silent data-loss bug where the `oauth_consent_request` stream event was swallowed by the `case _:` catch-all when a Foundry MCP server required OAuth consent. Callers were never notified; the event is now properly surfaced.

---

### 🐍 Python: `FoundryAgent` Updated for Hosted Agent Sessions
**[#5447](https://github.com/microsoft/agent-framework/pull/5447)** — *eavanvalkenburg* · `python` `documentation`

Aligns `FoundryAgent` with Foundry's preview session APIs: lazy session creation and an updated hosted request payload shape. Users on hosted Foundry agents must upgrade to avoid broken session initialization.

---

### 🔷 .NET: Synchronous Results from Durable Workflow HTTP Trigger
**[#5321](https://github.com/microsoft/agent-framework/pull/5321)** — *kshyju* · `.NET` `documentation`

The workflow HTTP endpoint previously always returned `202 Accepted` (fire-and-forget). Callers can now pass `x-ms-wait-for-response: true` to block and receive the workflow result inline — a significant DX improvement for request/response style workflows.

---

### 🔷 .NET: Always-Approve Decorator for Tool Confirmations
**[#5451](https://github.com/microsoft/agent-framework/pull/5451)** — *westey-m* · `.NET`

Adds a decorator that persists a user's "always approve" preference for a tool call — scoped to specific parameters or the tool as a whole. Includes harness sample improvements and a related bug fix.

---

## Minor Updates & Bug Fixes

- **[#5425](https://github.com/microsoft/agent-framework/pull/5425)** **.NET: Dynamic tool expansion sample** — *westey-m* · New sample showing how to expand available tools dynamically via a tool call. (`documentation`, `.NET`)
- **[#5468](https://github.com/microsoft/agent-framework/pull/5468)** **Python: 1.1.1 → 1.2.0 version bump** — *moonbox3* · Releases `core`, `openai`, `foundry`, and root packages at 1.2.0, capturing the functional workflow API and `FunctionTool` `SKIP_PARSING` sentinel. (`python`, `lab`)
- **[#5478](https://github.com/microsoft/agent-framework/pull/5478)** **.NET: OpenTelemetry packages → 1.15.3** — *SergeyMenshykh* · Resolves `NU1902` CI failure from vulnerability `GHSA-g94r-2vxg-569j` in OTel 1.15.0. (`.NET`)
- **[#5446](https://github.com/microsoft/agent-framework/pull/5446)** **Python: Email security example cleanup** — *shrutitople* · Removes dead label-tracking methods; adds shared session to the email example. (`python`)
- **[#5459](https://github.com/microsoft/agent-framework/pull/5459)** **Python: Hosting server dependency upgrade + type improvements** — *TaoChenOSU* · Upgrades hosting server dep and expands type annotations. (`python`)
- **[#5389](https://github.com/microsoft/agent-framework/pull/5389)** **Python: Fix AG-UI reasoning role and multimodal parsing** — *moonbox3* · `ReasoningMessageStartEvent` now correctly emits `role="reasoning"`; multimodal media parsing follows spec. (`python`, `ag-ui`)
- **[#5455](https://github.com/microsoft/agent-framework/pull/5455)** **Python: Fix user-agent header prefix** — *TaoChenOSU* · Corrects a malformed user-agent prefix in outbound HTTP requests. (`python`)
- **[#5440](https://github.com/microsoft/agent-framework/pull/5440)** **Python: Suppress spurious `[TOOLBOXES]` warning** — *moonbox3* · `FoundryChatClient` no longer emits the `sanitize_foundry_response_tool is experimental` warning on every call when no toolbox is in use. (`python`, `agents`)

---

## Summary

April 26 was a high-velocity day for `microsoft/agent-framework` with 15 PRs merged across .NET and Python. The headline is Python-side: the **functional workflow API** lands in core (shipping in 1.2.0), an **A2A bridge** adds cross-vendor agent interoperability, and **OpenTelemetry tracing** reaches parity across all major agent backends. On .NET, durable workflows gain synchronous HTTP response support. Python consumers should upgrade to **1.2.0**; .NET users should update OpenTelemetry packages to clear the `NU1902` security advisory.

---

> ⚠️ Note: I encountered filesystem permission issues preventing me from writing to `blog/` directly. Please save the above content to `blog/2026-04-26-microsoft-agent-framework.md` and commit it.