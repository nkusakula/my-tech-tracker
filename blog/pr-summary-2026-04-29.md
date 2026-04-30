I'm experiencing permission issues with file system access in this session. Here is the complete blog post output per the pr-analyzer skill format:

---

# microsoft/agent-framework PR Summary — 2026-04-29

## ⚠️ Breaking Changes

### [#5301](https://github.com/microsoft/agent-framework/pull/5301) — Python: Standardize orchestration terminal outputs as `AgentResponse`
**Author:** moonbox3 | **Labels:** python, needs_port_to_dotnet

All terminal outputs from `SequentialBuilder` and `GroupChatBuilder` orchestrations now return a unified `AgentResponse` object instead of raw strings or varied types. Scoped to the still-experimental `agent-framework-orchestrations` package — core workflow code is unaffected.

```python
# Before
result: str = await workflow.as_agent().run(prompt)

# After
result: AgentResponse = await workflow.as_agent().run(prompt)
print(result.value)
```

Any code pattern-matching or directly assigning terminal results to `str` must be updated.

---

## Major Updates

### [#5474](https://github.com/microsoft/agent-framework/pull/5474) — .NET: Add `HttpRequestAction` support to declarative workflows
**Author:** peibekwe | **Labels:** .NET, workflows

End-to-end support for `HttpRequestAction` in declarative YAML workflows. Authors can now issue HTTP requests directly from YAML and pipe responses into variables or the conversation — no custom C# code required for common HTTP integrations.

```yaml
actions:
  - type: HttpRequestAction
    url: "https://api.example.com/data"
    method: GET
    output_variable: "$api_response"
```

### [#5572](https://github.com/microsoft/agent-framework/pull/5572) — .NET: Declarative `HttpRequestAction` sample + `System.LastMessage` regression fix
**Author:** peibekwe | **Labels:** .NET, workflows

Ships the companion `InvokeHttpRequest` sample for multi-turn `HttpRequestAction` usage. Also fixes a regression where user-authored text was silently dropped from state after `AgentProv` processing — `System.LastMessage` now correctly preserves the user turn.

### [#5322](https://github.com/microsoft/agent-framework/pull/5322) — Python: Support OpenAI and Gemini `allowed_tools` tool choice
**Author:** giles17 | **Labels:** python

Adds `allowed_tools` tool-choice support for OpenAI, Azure OpenAI, and Gemini providers. Callers restrict which tools the model may invoke at inference time without removing tools from the prompt, preserving prompt-caching benefits.

```python
response = await agent.invoke(
    prompt,
    tool_choice=ToolChoice(type="allowed_tools", allowed_tools=["search", "calculator"]),
)
```

### [#5518](https://github.com/microsoft/agent-framework/pull/5518) — .NET: Add subagents provider and sample
**Author:** westey-m | **Labels:** documentation, .NET

New provider enabling async task delegation to sub-agents with deferred follow-up, plus a runnable sample. Expands the .NET multi-agent orchestration surface.

### [#4829](https://github.com/microsoft/agent-framework/pull/4829) — Python: New `agent-framework-azure-ai-contentunderstanding` package
**Author:** yungshinlintw | **Labels:** documentation, python

New first-party package bridging Azure Content Understanding with the Agent Framework via `BaseContextProvider`. File attachments (PDF, images, audio, video) are automatically intercepted, processed through Azure CU, and injected into agent context. Closes #4942.

### [#5531](https://github.com/microsoft/agent-framework/pull/5531) — Python: Full conversation history in declarative workflow agents
**Author:** alliscode | **Labels:** python

Declarative workflow agents now receive the complete message history (not just the latest user turn) when triggered via an agent. Critical for multi-turn hosted/remote DWF deployments.

---

## Minor Updates & Bug Fixes

- **[#5557](https://github.com/microsoft/agent-framework/pull/5557)** *(moonbox3)* — Python: Fix `file_search` citations breaking assistant history roundtrip in multi-agent Responses API flows (400 errors). Fixes #5556. Shipped in 1.2.2.
- **[#5552](https://github.com/microsoft/agent-framework/pull/5552)** *(TaoChenOSU)* — Python: Fix streaming spans not correctly nested — observability/tracing correctness fix.
- **[#5540](https://github.com/microsoft/agent-framework/pull/5540)** *(westey-m)* — .NET: File-memory index and instructions consistency improvements.
- **[#5561](https://github.com/microsoft/agent-framework/pull/5561)** *(moonbox3)* — Python: 1.2.2 patch release (`agent-framework`, `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry`: `1.2.1 → 1.2.2`).
- **[#5536](https://github.com/microsoft/agent-framework/pull/5536)** *(moonbox3)* — Python: 1.2.1 patch release (`1.2.0 → 1.2.1`); beta packages stamped `1.0.0b260428`, alpha packages `1.0.0a260428`.
- **[#5555](https://github.com/microsoft/agent-framework/pull/5555)** *(moonbox3)* — Python: General package dependency updates.
- **[#5228](https://github.com/microsoft/agent-framework/pull/5228)** *(dependabot[bot])* — Bump `prek` `0.3.8 → 0.3.9`.
- **[#5126](https://github.com/microsoft/agent-framework/pull/5126)** *(dependabot[bot])* — Bump `vite` `7.1.12 → 7.3.2` in the ChatKit integration frontend.

---

## Summary

April 29 was a high-velocity, dual-SDK day for `microsoft/agent-framework`. The headline theme is **declarative workflow expansion**: `HttpRequestAction` reaches full end-to-end support in .NET (YAML authoring, runtime, and sample), and Python's hosted DWF agents gain complete conversation-history awareness. On the Python side, the experimental `agent-framework-orchestrations` package ships a breaking unification of orchestration return types to `AgentResponse`, and two rapid patch releases (1.2.1 and 1.2.2) were cut — the latter addressing a critical `file_search` citation bug affecting all multi-agent Responses API flows. **Python users on multi-agent workflows with `file_search` should upgrade to ≥ 1.2.2 immediately; consumers of the orchestrations package must migrate terminal-result handling to `AgentResponse`.**