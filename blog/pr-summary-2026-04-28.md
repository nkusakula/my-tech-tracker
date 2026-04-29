It seems the filesystem is fully locked in this environment. Here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-04-28

## ⚠️ Breaking Changes

### [#5301](https://github.com/microsoft/agent-framework/pull/5301) — Python: Standardize orchestration terminal outputs as `AgentResponse`
**Author:** moonbox3 | **Labels:** `python`, `needs_port_to_dotnet`

Orchestration terminal outputs in the `agent-framework-orchestrations` package have been unified under a single `AgentResponse` type. Previously, `.run(prompt)` on `SequentialBuild` and other orchestrators returned varying shapes (dict, tuple, or string); they now always return `AgentResponse`.

> **Scope:** Scoped to the still-experimental `agent-framework-orchestrations` package only. Core `agent-framework` workflow code is non-breaking.

**Migration:**
```python
# Before — shape varied by orchestrator
result = await workflow.as_agent().run("Summarize this")
text = result["output"]

# After — always AgentResponse
result = await workflow.as_agent().run("Summarize this")
text = result.content
```

---

## 🚀 Major Updates

### [#5531](https://github.com/microsoft/agent-framework/pull/5531) — Python: Conversation history in hosted declarative workflow agents
**Author:** alliscode | **Labels:** `python`

Declarative workflow agents triggered via the hosted agent surface now receive the **full conversation history**, not just the latest user turn. Multi-turn context was previously silently dropped, causing workflows that rely on prior messages to behave incorrectly. Input initialization now propagates the complete message history into the workflow context at invocation time.

---

### [#5474](https://github.com/microsoft/agent-framework/pull/5474) — .NET: `HttpRequestAction` support in declarative workflows
**Author:** peibekwe | **Labels:** `.NET`, `workflows`

Workflow authors can now issue HTTP requests directly from YAML and pipe responses into variables or the conversation — no custom C# required. The shape mirrors existing action types (`InvokeFunctionTool`, `InvokeAgentAction`).

```yaml
actions:
  - type: HttpRequestAction
    method: GET
    url: "https://api.example.com/data"
    output_variable: api_response
```

---

### [#4829](https://github.com/microsoft/agent-framework/pull/4829) — Python: New `agent-framework-azure-ai-contentunderstanding` package
**Author:** yungshinlintw | **Labels:** `python`, `documentation`

A new first-party package bridges **Azure Content Understanding** with Agent Framework via a `BaseContextProvider`. File attachments (PDF, images, audio, video) are intercepted, analyzed by Azure CU, and the extracted content is injected into the agent context before the LLM call. Closes [#4942](https://github.com/microsoft/agent-framework/issues/4942).

```python
from agent_framework_azure_ai_contentunderstanding import AzureCUContextProvider

agent = ChatCompletionAgent(
    ...,
    context_providers=[AzureCUContextProvider(endpoint="...", api_key="...")]
)
```

---

### [#5518](https://github.com/microsoft/agent-framework/pull/5518) — .NET: Subagents provider and sample
**Author:** westey-m | **Labels:** `.NET`, `documentation`

A new provider enables .NET agents to **delegate tasks to sub-agents and follow up asynchronously**, unlocking fan-out / coordinator patterns. An accompanying sample demonstrates the full delegation lifecycle.

---

## 📦 Minor Updates & Maintenance

- **[#5536](https://github.com/microsoft/agent-framework/pull/5536)** — Python 1.2.1 release bump: `1.2.0 → 1.2.1`; 21 beta packages stamped `1.0.0b260428`, 3 alpha packages stamped `1.0.0a260428`. *(moonbox3)*
- **[#5228](https://github.com/microsoft/agent-framework/pull/5228)** — Dependabot: bump `prek` `0.3.8 → 0.3.9`
- **[#5126](https://github.com/microsoft/agent-framework/pull/5126)** — Dependabot: bump `vite` `7.1.12 → 7.3.2` (chatkit-integration)
- **[#5127](https://github.com/microsoft/agent-framework/pull/5127)** — Dependabot: bump `vite` `7.1.12 → 7.3.2` (devui)
- **[#5492](https://github.com/microsoft/agent-framework/pull/5492)** — Dependabot: bump `pytest` `9.0.2 → 9.0.3` (devui)
- **[#5461](https://github.com/microsoft/agent-framework/pull/5461)** — Dependabot: bump `pytest` `9.0.2 → 9.0.3` (ag-ui)
- **[#4936](https://github.com/microsoft/agent-framework/pull/4936)** — Dependabot: bump `picomatch` `4.0.3 → 4.0.4`
- **[#5227](https://github.com/microsoft/agent-framework/pull/5227)** — Dependabot: relax `rich` upper bound to `<16.0.0`
- **[#5484](https://github.com/microsoft/agent-framework/pull/5484)** — Dependabot: bump `postcss` `8.5.6 → 8.5.10`
- **[#5286](https://github.com/microsoft/agent-framework/pull/5286)** — Dependabot: bump `python-multipart` `0.0.22 → 0.0.26`

---

## Summary

April 28 was a high-velocity day spanning both Python and .NET. The most urgent change for downstream consumers is the **breaking `AgentResponse` unification** in the experimental orchestrations package. Beyond that, four significant features landed: multi-modal file understanding via Azure CU, declarative HTTP actions in .NET workflows, full conversation-history propagation for hosted DWF agents, and a new .NET subagents delegation provider — collectively pushing the framework further toward production-ready multi-agent and declarative workflow scenarios.

---

> **Note:** I was unable to write the file to disk due to environment filesystem restrictions. You can paste the above directly into `blog/2026-04-28-microsoft-agent-framework.md`.