I'm unable to write files in this environment due to permission restrictions, so here's the complete blog post output:

---

# microsoft/agent-framework PR Summary — 2026-05-03

## Breaking Changes

### ⚠️ Python: `approval_mode` now enforced in Claude and GitHub Copilot agents — [#5562](https://github.com/microsoft/agent-framework/pull/5562) by eavanvalkenburg

Tools declared with `approval_mode="always_require"` were previously **silently bypassed** in `ClaudeAgent` and `GitHubCopilotAgent` because their SDK-managed tool-calling loops invoked `FunctionTool.invoke()` directly inside per-package hooks, completely skipping the framework's approval gate.

**After this change**, both agents now respect `approval_mode`. Any tool annotated `approval_mode="always_require"` will pause for user approval before execution, matching all other agents in the framework.

**Action required:** If your application relied on silent tool execution in these agents, update your approval flow handling or change `approval_mode` on affected tools.

---

## Major Updates

### Python: `HttpRequestAction` parity with .NET in declarative workflows — [#5599](https://github.com/microsoft/agent-framework/pull/5599) by peibekwe

Python now supports `HttpRequestAction` in declarative workflows, matching the .NET `Microsoft.Agents.AI.Workflows.Declarative` implementation. Workflow authors can dispatch HTTP calls directly from config-driven workflows without custom step code.

```yaml
steps:
  - type: HttpRequestAction
    url: "https://api.example.com/data"
    method: GET
    headers:
      Authorization: "Bearer {{secrets.api_token}}"
    output: api_response
```

### Python: `allowed_tools` tool-choice support for OpenAI and Gemini — [#5322](https://github.com/microsoft/agent-framework/pull/5322) by giles17

OpenAI, Azure OpenAI, and Gemini callers can now pass an `allowed_tools` tool-choice type to restrict which tools the model may invoke during a turn — **without removing tools from the prompt**, preserving prompt-caching benefits.

```python
response = await agent.invoke(
    messages,
    tool_choice={"type": "allowed_tools", "tools": ["search", "calculator"]}
)
```

### .NET: `FileAccessProvider` + concurrency fix for `FileMemoryProvider` — [#5583](https://github.com/microsoft/agent-framework/pull/5583) by westey-m

Introduces a new `FileAccessProvider` with a structured API for reading/writing files within agent memory (with usage sample). Also fixes a concurrency race condition in `FileMemoryProvider` that could cause data corruption under concurrent access.

### .NET: Declarative `HttpRequestAction` sample + `System.LastMessage` regression fix — [#5572](https://github.com/microsoft/agent-framework/pull/5572) by peibekwe

Adds an `InvokeHttpRequest` sample for multi-turn declarative conversations. Fixes a regression where user-authored text was silently dropped from state after `AgentProvider`-driven turns due to incorrect `System.LastMessage` handling.

### .NET: `User-Agent` supplement for Foundry-hosted agent requests — [#5453](https://github.com/microsoft/agent-framework/pull/5453) by alliscode

Agents served by `Microsoft.Agents.AI.Foundry.Hosting` now append `foundry-hosting/agent-framework-dotnet/{version}` to the `User-Agent` header on every outgoing OpenAI Responses-API request, improving observability and traffic attribution in Foundry deployments.

---

## Minor Updates & Bug Fixes

- **Python: Fix orphan `function_call_output` in hosted MCP replay** — [#5581](https://github.com/microsoft/agent-framework/pull/5581) by moonbox3 — Resolves `400 BadRequestError: No tool call found for function call output with call_id mcp_06b...` crashing on the third turn of conversations using hosted MCP / Foundry toolbox tools.

- **Python: Correct observability docs for W3C trace context** — [#5580](https://github.com/microsoft/agent-framework/pull/5580) by moonbox3 — README incorrectly claimed `traceparent`/`tracestate` injection via `params._meta` works for all transports; now accurately documents the Foundry-hosted/toolbox exception.

- **Python: Add sample for hosted agent with files** — [#5596](https://github.com/microsoft/agent-framework/pull/5596) by TaoChenOSU — New end-to-end sample for building hosted agents that upload, reference, and retrieve files via the agent runtime.

- **Python: Reduce flaky integration tests** — [#5454](https://github.com/microsoft/agent-framework/pull/5454) by giles17 — Fixes CI flakiness across OpenAI, Foundry, Ollama, and Azure Functions test suites (timing issues, bad assertions, xdist conflicts).

- **Python: 1.2.2 release bump** — [#5561](https://github.com/microsoft/agent-framework/pull/5561) by moonbox3 — PATCH bump `1.2.1 → 1.2.2` for `agent-framework`, `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry`, driven by the `file_search` citations fix (#5557).

- **.NET: Harness feature branch merge** — [#5310](https://github.com/microsoft/agent-framework/pull/5310) by westey-m — Merges harness capabilities tracked under #5271.

- **.NET: Dedicated `Foundry.Hosting` unit test project** — [#5592](https://github.com/microsoft/agent-framework/pull/5592) by rogerbarreto — Splits hosting tests into `Microsoft.Agents.AI.Foundry.Hosting.UnitTests`, mirroring the `src/` layout.

- **.NET: Refactor harness console** — [#5573](https://github.com/microsoft/agent-framework/pull/5573) by westey-m — Restructured into Observer classes for better clarity and extensibility.

- **.NET: Harness `FileMemory` index + instructions consistency** — [#5540](https://github.com/microsoft/agent-framework/pull/5540) by westey-m — Aligns indexing behavior and system instructions handling with the broader harness changes.

---

## Summary

May 3rd was a high-velocity, cross-platform day with **15 PRs merged** across Python and .NET. The most consequential change is the `approval_mode` enforcement fix in `ClaudeAgent` and `GitHubCopilotAgent` — a correctness fix that is also a breaking behavioral change for any workflow relying on silent tool execution. Feature work centered on cross-language parity (`HttpRequestAction` in Python declarative workflows) and runtime control (`allowed_tools` for OpenAI/Gemini), while stability investments — MCP replay fixes, CI flakiness remediation, and the Python 1.2.2 patch release — advance reliability for production agent deployments.