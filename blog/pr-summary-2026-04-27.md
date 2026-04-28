I'm unable to write to the filesystem due to permission restrictions in this environment. Here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-04-27

## Breaking Changes

### ⚠️ [#5475](https://github.com/microsoft/agent-framework/pull/5475) — .NET: Support `string[]` arguments for file-based skill scripts
**Author:** SergeyMenshykh | **Labels:** `.NET`

File-based skill scripts invoking external CLI tools (e.g., `scripts/tool.py input.docx --output input.index`) previously forced arguments into a `Dictionary<string, object>`. The framework now accepts `string[]` directly, matching natural CLI argument conventions. **Any .NET code using Dictionary-based argument passing for file skill scripts must be updated.** Fixes [#5355](https://github.com/microsoft/agent-framework/issues/5355).

---

## Major Updates

### [#5530](https://github.com/microsoft/agent-framework/pull/5530) — Python: Hosted Declarative — Conversation History & Cross-Turn Context
**Author:** alliscode | **Labels:** `python`

Enhances declarative workflow agents to fully handle conversation history and message inputs, ensuring full cross-turn context is threaded correctly through agent-based workflow invocations.

---

### [#5524](https://github.com/microsoft/agent-framework/pull/5524) — Python: Hosted Declarative — `Message` List Workflow Triggers
**Author:** alliscode | **Labels:** `python`

Adds robust support for passing a list of `Message` objects as workflow triggers, allowing workflows to process a complete conversation history at invocation time:

```python
# Trigger a declarative workflow with full conversation history
await workflow.invoke(messages=[msg1, msg2, msg3])
```

---

### [#5321](https://github.com/microsoft/agent-framework/pull/5321) — .NET: Synchronous Results from Durable Workflow HTTP Trigger
**Author:** kshyju | **Labels:** `documentation`, `.NET`

Workflow HTTP endpoints previously always fire-and-forget (`202 Accepted`). Callers can now opt into a synchronous response by setting:

```http
x-ms-wait-for-response: true
```

The endpoint will block and return the final workflow result inline — ideal for short-lived workflows that don't need polling.

---

### [#2403](https://github.com/microsoft/agent-framework/pull/2403) — Python: Agent Framework ↔ A2A Bridge Support
**Author:** Shubham-Kumar-2000 | **Labels:** `documentation`, `python`, `requested-info`

Introduces a first-class bridge for running Agent Framework agents as A2A-hosted agent servers:
- **A2A event adapter** — translates Agent Framework messages to the A2A wire protocol
- **A2A server integration** — exposes agents as A2A-compliant endpoints
- Full end-to-end sample under `python/samples/04-hosting/a2a/`

---

### [#5447](https://github.com/microsoft/agent-framework/pull/5447) — Python: `FoundryAgent` Updated for Hosted Agent Sessions
**Author:** eavanvalkenburg | **Labels:** `documentation`, `python`

Realigns `FoundryAgent` with the Foundry preview session API: lazy session creation, updated hosted request payload shape, and refreshed sample flow. Teams using `FoundryAgent` against Azure AI Foundry should update to avoid runtime failures.

---

### [#5142](https://github.com/microsoft/agent-framework/pull/5142) — Python: OpenTelemetry Tracing for `GitHubCopilotAgent`
**Author:** droideronline | **Labels:** `documentation`, `python`

Adds OTel tracing following the layered pattern of `ClaudeAgent`/`FoundryAgent`:
- `RawGitHubCopilotAgent` — core logic, no OTel dependency
- `GitHubCopilotAgent(AgentTelemetry)` — span-instrumented wrapper

---

### [#5477](https://github.com/microsoft/agent-framework/pull/5477) — .NET: Configurable Todo, Mode, and FileMemory Providers
**Author:** westey-m | **Labels:** `.NET`

Exposes configuration hooks on the `Todo`, `Mode`, and `FileMemory` providers so users can supply custom instructions. Previously these were hardcoded and non-overridable.

---

### [#5451](https://github.com/microsoft/agent-framework/pull/5451) — .NET: Always-Approve Tool Helpers, Sample Improvements & Bug Fix
**Author:** westey-m | **Labels:** `.NET`

Adds a decorator that persists a user's "always approve" preference for a tool (either for specific parameter combinations or unconditionally), improves the approval harness sample, and fixes a bug in the approval flow.

---

## Minor Updates & Bug Fixes

- **[#5167](https://github.com/microsoft/agent-framework/pull/5167)** — **Python bug fix:** `AgentFrameworkException.__init__()` was overwriting `inner_exception` by unconditionally calling a second `super().__init__()`. Fixed so the inner exception is preserved. (by Bahtya)

- **[#5510](https://github.com/microsoft/agent-framework/pull/5510)** — **Python docs:** Added `requirements.txt` and `.env.example` to the `a2a/` sample, bringing it in line with every other sample under `04-hosting/`. (by moonbox3)

- **[#5446](https://github.com/microsoft/agent-framework/pull/5446)** — **Python docs:** Added shared session tracking to the `email_security_example` and removed dead `label_message()` / `get_message_label()` methods from `LabelTrackingFunctionMiddleware`. (by shrutitople)

- **[#5425](https://github.com/microsoft/agent-framework/pull/5425)** — **.NET docs:** New sample demonstrating dynamic runtime tool expansion via a tool call, per [#5326](https://github.com/microsoft/agent-framework/issues/5326). (by westey-m)

- **[#5478](https://github.com/microsoft/agent-framework/pull/5478)** — **.NET:** Bumped OpenTelemetry packages to 1.15.3 to resolve `NU1902` CI failures from known vulnerabilities (`GHSA-g94r-2vxg-569j`) in 1.15.0. (by SergeyMenshykh)

- **[#5468](https://github.com/microsoft/agent-framework/pull/5468)** — **Python:** Version bump 1.1.1 → 1.2.0 for `core`, `openai`, `foundry`, and root packages, formally releasing the functional workflow API and `FunctionTool` `SKIP_PARSING` sentinel. (by moonbox3)

---

## Summary

April 27 was a high-velocity day for `microsoft/agent-framework` with **15 PRs merged** spanning both Python and .NET. The dominant theme is **hosted and declarative agent maturity**: two PRs harden declarative workflow agents for multi-turn conversation histories, `FoundryAgent` is realigned to the preview session API, and the long-awaited A2A bridge lands full cross-agent protocol support. On the .NET side, durable workflow HTTP endpoints gain synchronous response capability and file-skill argument handling is corrected (breaking change). Python ships its 1.2.0 release simultaneously, formalizing the functional workflow API for all downstream consumers.