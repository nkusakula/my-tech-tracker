I'm unable to write files in this environment, but here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-05-06

## ⚠️ Breaking Changes

### [#5584](https://github.com/microsoft/agent-framework/pull/5584) — Python: Restructure Agent Skills to Multi-Source Architecture
**Author:** SergeyMenshykh | **Labels:** documentation, python

The Python agent skills system has been **restructured** per [ADR-0021](https://github.com/microsoft/agent-framework/blob/main/docs/decisions/0021-agent-skills-design.md) to a **multi-source architecture**:

- Old single-source skill registration APIs are removed.
- Callers must migrate to the new multi-source registration pattern.
- See ADR-0021 and updated docs for migration guidance.

---

### [#5671](https://github.com/microsoft/agent-framework/pull/5671) — Python: Remove Bespoke Foundry Toolbox Helpers; Standardize on MCP
**Author:** moonbox3 | **Labels:** documentation, python

The hand-rolled Foundry toolbox surface has been **removed**. The following APIs no longer exist:

- `get_toolbox`, `fetch_toolbox`, `select_toolbox_tools`
- `get_toolbox_tool_name`, `get_toolbox_tool_type`, `FoundryHostedToolType`

Callers must migrate to **MCP (Model Context Protocol)** for toolbox consumption via `FoundryChatClient`.

---

## Major Updates

### [#5331](https://github.com/microsoft/agent-framework/pull/5331) — Python: Information-Flow Control Prompt Injection Defense (FIDES)
**Author:** eavanvalkenburg | **Labels:** documentation, python

Introduces **FIDES** — an information-flow control security layer merged from `feature/python-fides`:

- Tracks trust levels of data flowing through the agent pipeline.
- Detects and mitigates prompt injection attacks via policy enforcement.
- Critical addition for agents operating in adversarial or untrusted input environments.

---

### [#5650](https://github.com/microsoft/agent-framework/pull/5650) — Python: Notify Agent of External AgentModeProvider Mode Changes
**Author:** eavanvalkenburg | **Labels:** python

Follow-up to #5611. When a user changes agent mode externally (e.g., via `set_agent_mode` in a slash-command handler), the agent's chat history and internal state now correctly reflect the transition, preventing cross-turn behavioral confusion.

---

### [#5668](https://github.com/microsoft/agent-framework/pull/5668) — .NET: Overhaul Tool Approval Request/Response Handling
**Author:** alliscode | **Labels:** .NET

Significant improvements to human-in-the-loop tool approval flows:

- Function call details are now **preserved and correctly reconstructed** across HTTP turns.
- Internal implementation details are properly suppressed from the approval surface.

---

### [#5652](https://github.com/microsoft/agent-framework/pull/5652) — .NET: Bump MEAI to 10.5.1 + Foundry Per-Call `x-client-*` Header Support
**Author:** rogerbarreto | **Labels:** .NET

- Upgrades `Microsoft.Extensions.AI` `10.5.0` → `10.5.1`.
- **Replaces** the fragile `UserAgentResponsesClient` subclass with a clean **per-call `x-client-*` header pipeline** built on the new `OpenAIRequestPolicies` hook.

---

### [#5630](https://github.com/microsoft/agent-framework/pull/5630) — Python: InvokeMcpTool in Declarative Workflows (Parity with .NET)
**Author:** peibekwe | **Labels:** documentation, python

Adds Python `InvokeMcpTool` declarative workflow action — now workflow authors can dispatch MCP tool calls directly from **YAML definitions**, matching existing .NET support. Includes samples and docs.

---

### [#5598](https://github.com/microsoft/agent-framework/pull/5598) — .NET: Add `Foundry.Hosting.IntegrationTests`
**Author:** rogerbarreto | **Labels:** documentation, .NET

New integration test project that provisions **real Foundry hosted agents** and exercises them through `Microsoft.Agents.AI.Foundry.Hosting`, mirroring the structure of `Foundry.IntegrationTests`.

---

## Minor Updates & Bug Fixes

- **[#5172](https://github.com/microsoft/agent-framework/pull/5172)** — **Python/Bedrock:** `BedrockChatClient` no longer sends `toolConfig.toolChoice` when no tools are configured, preventing AWS `ValidationException`. *(Bahtya)*
- **[#5610](https://github.com/microsoft/agent-framework/pull/5610)** — **.NET:** Fixed YAML block scalar (`|` / `>`) parsing in file skill loaders — multi-line `description` fields in `SKILL.md` frontmatter now parse correctly. *(tejakusireddy)*
- **[#5635](https://github.com/microsoft/agent-framework/pull/5635)** — **.NET:** Fixed `QuestionExecutor` infinite loop after `GotoAction` re-entry in declarative workflows (e.g., `ConfirmInput` sample). *(peibekwe)*
- **[#5653](https://github.com/microsoft/agent-framework/pull/5653)** — **.NET:** Fixed JSON serialization of `MultiPartyConversation` during checkpointing — chat history was not persisted, causing deserialization failures on reload. *(lokitoth)*
- **[#5656](https://github.com/microsoft/agent-framework/pull/5656)** — **.NET:** Added missing Workflows "Shared" source files to the solution. *(lokitoth)*
- **[#5669](https://github.com/microsoft/agent-framework/pull/5669)** — **.NET:** Fixed flaky `HttpRequestAction` integration test by switching from unauthenticated GitHub REST API (prone to 429s) to authenticated ARM APIs. *(peibekwe)*
- **[#5660](https://github.com/microsoft/agent-framework/pull/5660)** — **.NET:** Added hosted agent observability sample under `dotnet/samples/04-hosting/FoundryHostedAgents/responses/`, matching the Python sample from #5608. *(rogerbarreto)*

---

## Summary

May 6, 2026 was a high-velocity day for `microsoft/agent-framework` with **15 PRs merged** across Python and .NET. The dominant theme was **security and architectural maturity**: FIDES prompt injection defense lands as a flagship Python security feature, and the skills system completes its breaking migration to multi-source architecture. On the .NET side, tool approval reliability, MEAI 10.5.1 adoption, and declarative workflow correctness received focused attention. Downstream consumers — especially Python callers using Foundry toolbox helpers or the old single-source skills API — should review the two breaking changes carefully before upgrading.