I'm unable to write files in this environment, but here is the fully structured blog post per the `pr-analyzer` skill:

---

# microsoft/agent-framework PR Summary — 2026-04-30

## Breaking Changes

> ⚠️ **[#5301](https://github.com/microsoft/agent-framework/pull/5301) — Python: Standardize orchestration terminal outputs as `AgentResponse`** (by moonbox3)
>
> **Scope:** `agent-framework-orchestrations` only (still experimental). Core `agent-framework` workflow code is non-breaking.
>
> `workflow.as_agent().run(prompt)` for `SequentialBuilder`, `GroupChatBuilder`, and related orchestrators now returns a unified `AgentResponse` instead of raw strings or ad-hoc types. Callers must update consumption:
>
> ```python
> # Before
> result: str = await workflow.as_agent().run("prompt")
>
> # After
> result: AgentResponse = await workflow.as_agent().run("prompt")
> print(result.content)
> ```
>
> A .NET port is tracked separately (`needs_port_to_dotnet`).

---

## Major Updates

### Python

- **[#5322](https://github.com/microsoft/agent-framework/pull/5322) — Support `allowed_tools` tool choice for OpenAI and Gemini** (by giles17)

  Adds the `allowed_tools` tool-choice type for OpenAI, Azure OpenAI, and Gemini providers. Restricts which tools the model may invoke at inference time *without* removing tools from the prompt — preserving prompt-caching benefits on long conversations.

  ```python
  response = await agent.run(
      prompt,
      tool_choice=AllowedTools(tools=["search", "lookup"])
  )
  ```

- **[#5531](https://github.com/microsoft/agent-framework/pull/5531) — Full conversation history forwarded to declarative workflow agents** (by alliscode)

  Hosted declarative workflow (DWF) agents now receive the complete message history — not just the latest user turn — when invoked through the agent framework. Enables multi-turn-aware workflows running inside agents.

- **[#5581](https://github.com/microsoft/agent-framework/pull/5581) — Fix hosted MCP replay producing orphan `function_call_output`** (by moonbox3)

  Resolves [#5546](https://github.com/microsoft/agent-framework/issues/5546). On the third turn of any conversation using a hosted MCP / Foundry tool, replay was emitting a `function_call_output` with no matching `function_call`:

  ```
  openai.BadRequestError: 400 - 'No tool call found for function call output with call_id mcp_06b...'
  ```

  The fix enforces correct ordering in the history submitted to the Responses API.

- **[#5557](https://github.com/microsoft/agent-framework/pull/5557) — Fix `file_search` citations breaking assistant history roundtrip** (by moonbox3)

  Closes [#5556](https://github.com/microsoft/agent-framework/issues/5556). Post RC5→1.0 Responses API migration, `SequentialBuilder`/`GroupChatBuilder` flows broke with a 400 whenever one agent used `file_search` and forwarded history downstream. Citation annotations were not being round-tripped correctly. This fix drives the `1.2.2` patch release.

### .NET

- **[#5453](https://github.com/microsoft/agent-framework/pull/5453) — Hosted-agent `User-Agent` supplement on Responses-API requests** (by alliscode)

  Agents served by `Microsoft.Agents.AI.Foundry.Hosting` now append `foundry-hosting/agent-framework-dotnet/{version}` to the outgoing `User-Agent` header alongside the existing Azure SDK string — enabling server-side telemetry and traffic attribution.

- **[#5572](https://github.com/microsoft/agent-framework/pull/5572) — Declarative `HttpRequestAction` sample + `System.LastMessage` regression fix** (by peibekwe)

  New `InvokeHttpRequest` sample demonstrating `HttpRequestAction` in a multi-turn declarative workflow. Also fixes a regression where user-authored text was silently dropped from state after `AgentProvider` processing (`System.LastMessage` now correctly preserves the user turn).

- **[#5583](https://github.com/microsoft/agent-framework/pull/5583) — Add `FileAccessProvider` + concurrency fix for `FileMemoryProvider`** (by westey-m)

  Introduces `FileAccessProvider` with an end-to-end sample. Also fixes a race condition in `FileMemoryProvider` that could cause data corruption or exceptions under concurrent read/write.

- **[#5592](https://github.com/microsoft/agent-framework/pull/5592) — Dedicated `Foundry.Hosting.UnitTests` project** (by rogerbarreto)

  Splits Foundry-hosting tests out of `Microsoft.Agents.AI.Foundry.UnitTests` into a new `Microsoft.Agents.AI.Foundry.Hosting.UnitTests` project, mirroring the `src/` directory structure and making ownership explicit.

---

## Minor Updates & Bug Fixes

- **[#5454](https://github.com/microsoft/agent-framework/pull/5454)** *(Python)* — Reduced flaky integration tests across OpenAI, Foundry, Ollama, and Azure Functions; fixed timing issues, incorrect assertions, infrastructure guards, and `pytest-xdist` conflicts. (by giles17)
- **[#5552](https://github.com/microsoft/agent-framework/pull/5552)** *(Python)* — Fixed telemetry spans not correctly nested during streaming responses. (by TaoChenOSU)
- **[#5555](https://github.com/microsoft/agent-framework/pull/5555)** *(Python)* — Updated package dependencies. (by moonbox3)
- **[#5561](https://github.com/microsoft/agent-framework/pull/5561)** *(Python)* — Cut the `python-1.2.2` patch release: `agent-framework`, `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry` bumped `1.2.1 → 1.2.2`, driven by the `file_search` citations fix. (by moonbox3)
- **[#5573](https://github.com/microsoft/agent-framework/pull/5573)** *(.NET)* — Refactored harness console into Observer-based components for improved readability and extensibility. (by westey-m)
- **[#5540](https://github.com/microsoft/agent-framework/pull/5540)** *(.NET)* — Improved consistency of file-memory index handling and agent instructions in the harness. (by westey-m)

---

## Summary

April 30th was a high-velocity day across both SDKs, with 15 PRs merged. The Python side shipped a **breaking orchestration API unification** (`AgentResponse`) alongside two critical runtime fixes — MCP replay corruption and `file_search` history roundtrip failures — that together triggered the `1.2.2` patch release. On the .NET side, headline additions include `FileAccessProvider`, a declarative `HttpRequestAction` sample, hosted-agent `User-Agent` attribution, and improved Foundry hosting test isolation. Teams consuming `agent-framework-orchestrations` in Python should migrate to `AgentResponse` immediately; all other changes are additive or fix-forward.