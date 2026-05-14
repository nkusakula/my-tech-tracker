The filesystem appears to be read-only in this environment. Here is the complete blog post ready for you to save to `blog/2026-05-13-agent-framework.md`:

---

# microsoft/agent-framework PR Summary — 2026-05-13

## ⚠️ Breaking Changes

### [#5740](https://github.com/microsoft/agent-framework/pull/5740) — Python: DevUI default CORS and access control tightened
**Author:** moonbox3 | **Labels:** python, devui

The DevUI server's out-of-the-box CORS and authentication defaults have been **tightened**. A bare `devui ./agents` invocation now enforces stricter access controls matching the typical local-development mental model. Callers who relied on the previous permissive defaults (e.g. wide-open CORS origins or unauthenticated access) will need to explicitly opt back in to the looser posture.

---

### [#5775](https://github.com/microsoft/agent-framework/pull/5775) — Python: Skill spec metadata extracted into `SkillFrontmatter`
**Author:** SergeyMenshykh | **Labels:** documentation, python

`Skill` subclass constructors previously accepted `name` and `description` as direct positional parameters. These metadata fields have been moved into a dedicated `SkillFrontmatter` object, aligned with the [agentskills.io specification](https://agentskills.io/specification). Any code constructing `Skill` subclasses must be updated:

```python
# Before
class MySkill(Skill):
    def __init__(self):
        super().__init__(name="my-skill", description="Does something")

# After
class MySkill(Skill):
    def __init__(self):
        super().__init__(frontmatter=SkillFrontmatter(name="my-skill", description="Does something"))
```

---

### [#5750](https://github.com/microsoft/agent-framework/pull/5750) — .NET: `OpenTelemetryAgent` auto-wires `IChatClient` with `OpenTelemetryChatClient`
**Author:** Copilot | **Labels:** .NET

`OpenTelemetryAgent` previously only instrumented the agent-level `invoke_agent` span; the underlying `IChatClient` was untouched, so model-level spans and usage metrics never flowed. This PR **auto-wires the `IChatClient` with `OpenTelemetryChatClient`** by default. Callers who already manually wrapped their `IChatClient` before passing it in may see **duplicate spans** and should remove the manual wrapping.

---

## Major Updates

### [#5690](https://github.com/microsoft/agent-framework/pull/5690) — Python: Fix duplicate item error for tool-using agents with service-side storage
**Author:** moonbox3 | **Labels:** documentation, python

Fixes [#3295](https://github.com/microsoft/agent-framework/issues/3295). When an agent used tools alongside any form of service-side storage (`RedisHistoryProvider`, `CosmosHistoryProvider`, sessions, or replaying workflows), the second conversation turn failed with a duplicate item error. This was a significant reliability regression for stateful tool-using agents in production.

---

### [#4866](https://github.com/microsoft/agent-framework/pull/4866) — Python: Fix MCP `message_handler` deadlock on `notifications/tools/list_changed`
**Author:** giles17 | **Labels:** python

When an MCP server sent a `notifications/tools/list_changed` notification during or after tool execution, `MCPTool.message_handler()` would **await `load_tools()`/`load_prompts()` directly**, deadlocking the running tool call. The fix dispatches the reload asynchronously so the handler returns immediately without blocking.

---

### [#5755](https://github.com/microsoft/agent-framework/pull/5755) — .NET: Workflow evaluations gain `ground_truth` / `expected_output` support
**Author:** alliscode | **Labels:** documentation, .NET, workflows

Adds support for passing a ground-truth value into workflow evaluations, unlocking reference-based evaluators such as Foundry's **Similarity evaluator**. Users can now specify `expected_output` alongside their evaluation input to drive richer automated quality checks.

---

### [#5808](https://github.com/microsoft/agent-framework/pull/5808) — .NET: Fix handoff role reassignment mutating shared conversation messages
**Author:** he-yufeng | **Labels:** .NET, workflows

Handoff logic was **mutating shared `ChatMessage` roles in place** when re-presenting context from other agents as user messages, causing state corruption when multiple agents shared the same conversation list. Messages are now copied before role reassignment. Unit and regression tests were added to prevent recurrence.

---

### [#5762](https://github.com/microsoft/agent-framework/pull/5762) — Python: ag-ui tool result display channel separated from agent context
**Author:** moonbox3 | **Labels:** documentation, python, ag-ui

Closes [#5760](https://github.com/microsoft/agent-framework/issues/5760). The ag-ui emitter previously sent one string to both `ToolCallResultEvent.content` (UI display) and `flow.tool_results[].content` (agent context), tightly coupling the two. They are now independent channels, enabling richer UI representations without polluting the agent's context window.

---

### [#5748](https://github.com/microsoft/agent-framework/pull/5748) — .NET: Fix `OpenAIResponsesAgentClient` ignoring `agentName` in endpoint path
**Author:** giles17 | **Labels:** .NET

`OpenAIResponsesAgentClient` hardcoded `/v1/` as its endpoint, silently ignoring `agentName`. OpenAI-compatible endpoints (e.g. LMGateway) that route by agent name were returning HTTP 400. Endpoint construction now correctly incorporates `agentName`.

---

### [#5782](https://github.com/microsoft/agent-framework/pull/5782) — .NET: Add `HarnessAgent` package
**Author:** westey-m | **Labels:** documentation, .NET

Introduces a new `HarnessAgent` NuGet package bundling a set of default agent capabilities into a ready-to-use harness, simplifying bootstrap for agents that need a standard capability baseline.

---

### [#5786](https://github.com/microsoft/agent-framework/pull/5786) — .NET / Python: Fix FoundryToolboxMcp sample; introduce `agent-framework-tools` package
**Author:** alliscode | **Labels:** documentation, python, .NET

Fixes the `FoundryToolboxMcp` .NET sample to use the correctly created toolbox instance. Also introduces a new Python package `agent-framework-tools` with built-in tools for the framework, focused initially on robust cross-platform shell command execution.

---

## Minor Updates & Bug Fixes

- **[#5831](https://github.com/microsoft/agent-framework/pull/5831) — .NET: DevUI logging refactored to `LoggerMessage` source generators** (alliscode) — Replaces inline `ILogger` calls with strongly-typed `[LoggerMessage]`-attributed methods in a new `DevUILog` class, fixing CA1873 build warnings.

- **[#5789](https://github.com/microsoft/agent-framework/pull/5789) — .NET: Version bump for release** (alliscode) — Routine version update in preparation for a release cut.

- **[#5717](https://github.com/microsoft/agent-framework/pull/5717) — .NET: CI hardening — split Functions tests, re-enable skipped integration tests** (giles17) — Splits long-running integration tests into a dedicated CI job and re-enables previously skipped tests to improve signal quality.

- **[#5533](https://github.com/microsoft/agent-framework/pull/5533) — Replace `merge-gatekeeper` Docker action with `github-script` polling** (moonbox3) — Removes the Go-image-building `upsidr/merge-gatekeeper@v1` action in favour of a lightweight `github-script` poller, reducing unnecessary CI overhead on `merge_group` events.

---

## Summary

The May 13 merge batch for `microsoft/agent-framework` was high-velocity and broad in scope, landing **three breaking changes** across Python (DevUI CORS hardening, `SkillFrontmatter` refactor) and .NET (automatic `OpenTelemetryChatClient` wiring in `OpenTelemetryAgent`). The dominant theme is **production reliability**: duplicate-item fixes for service-side storage, MCP deadlock prevention, and handoff mutation bugs all address real-world failure modes reported by downstream users. The new `HarnessAgent` package, `agent-framework-tools` Python library, and ground-truth evaluation support mark meaningful expansions to the framework's surface area that warrant immediate attention from library consumers.