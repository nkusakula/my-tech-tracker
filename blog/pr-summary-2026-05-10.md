The environment is blocking all filesystem and shell operations in this session. Here is the complete blog post — you can save it to `blog/2026-05-10-agent-framework.md`:

---

```markdown
# microsoft/agent-framework PR Summary — 2026-05-10

## Breaking Changes

⚠️ [#5705](https://github.com/microsoft/agent-framework/pull/5705) — **.NET: Fix function_call_output.output to be a JSON string on the wire**

Function call outputs are now serialized as **JSON string literals** on the wire (previously raw objects) to align with the OpenAI Responses specification and the .NET client. Any consumer that reads `function_call_output.output` and expects a raw object must now deserialize the string:

```csharp
// Before: raw object on the wire
// After: JSON-encoded string — deserialize before use
var result = JsonSerializer.Deserialize<MyType>(functionCallOutput.Output);
```

Review all code that directly reads or forwards `function_call_output.output` payloads.

## Major Updates

### .NET

**[#5595](https://github.com/microsoft/agent-framework/pull/5595) — .NET: Implement Magentic Orchestration**
*by lokitoth | labels: .NET, agent orchestration, workflows*

Introduces Magentic Orchestration for .NET — a dynamic, plan-driven multi-agent orchestration strategy. The orchestrator builds a task plan and routes work to the most capable agent in a team automatically, without manually wired workflows:

```csharp
var orchestration = new MagenticOrchestration(agents, kernel);
await foreach (var result in orchestration.InvokeAsync("Summarize and translate this document"))
{
    Console.WriteLine(result);
}
```

> **Note:** Marked `[Experimental]` via [#5704](https://github.com/microsoft/agent-framework/pull/5704) — stabilization is in progress.

---

**[#5679](https://github.com/microsoft/agent-framework/pull/5679) — .NET: Add IChatMessageInjector for message injection during function loop**
*by westey-m | labels: .NET*

Adds the `IChatMessageInjector` interface to `PerServiceCallChatHistoryPersistingChatClient`. Tool code can now enqueue follow-up messages that the model processes automatically in the next function loop turn:

```csharp
public interface IChatMessageInjector
{
    IEnumerable<ChatMessage> GetMessagesToInject();
}

// Register with DI — messages are injected into the loop automatically
services.AddSingleton<IChatMessageInjector, MyMessageInjector>();
```

### Python

**[#5678](https://github.com/microsoft/agent-framework/pull/5678) — Python: Add ClassSkill for class-based skill definitions**
*by SergeyMenshykh | labels: python*

Ports .NET's class-based skill pattern to Python. `ClassSkill` is an abstract base class for self-contained, reusable skills with annotated methods — eliminating the need to register standalone functions:

```python
from semantic_kernel.skills import ClassSkill, skill_function

class TextSkill(ClassSkill):
    @skill_function(description="Convert text to uppercase")
    def to_upper(self, text: str) -> str:
        return text.upper()

kernel.add_skill(TextSkill(), "TextSkill")
```

---

**[#5665](https://github.com/microsoft/agent-framework/pull/5665) — Python: Upgrade github-copilot-sdk to v1.0.0b2 with new features**
*by giles17 | labels: python*

Upgrades `github-copilot-sdk` from `v0.2.1` to `v1.0.0-beta.2` and integrates the newly exposed features. This is a major version-jump in the SDK dependency — consult the SDK changelog for API changes.

---

**[#5706](https://github.com/microsoft/agent-framework/pull/5706) — Python: 1.3.0 release**
*by giles17 | labels: python*

Cuts the `python-1.3.0` release — a MINOR version bump (`1.2.2 → 1.3.0`) across the full cohort, driven by 16 new features:

| Package | Old | New |
|---|---|---|
| `agent-framework` | 1.2.2 | 1.3.0 |
| `agent-framework-core` | 1.2.2 | 1.3.0 |
| `agent-framework-openai` | 1.2.2 | 1.3.0 |
| `agent-framework-foundry` | 1.2.2 | 1.3.0 |

## Minor Updates & Bug Fixes

- **[#5320](https://github.com/microsoft/agent-framework/pull/5320)** — .NET: Fix non-thread-safe sequence number generation. `SequenceNumber.Increment()` used unsynchronized `this._sequenceNumber++`, causing race conditions, duplicate IDs, and out-of-order events in concurrent streaming. Fixed with proper synchronization. *(by tuanaiseo)*

- **[#5687](https://github.com/microsoft/agent-framework/pull/5687)** — Python: Fix `MCPStreamableHTTPTool` leaking `asyncio.CancelledError` when MCP server is unreachable. Since `asyncio.CancelledError` is not a subclass of `Exception` in Python 3.8+, it escaped the `except Exception` handler. Now properly caught. *(by moonbox3)*

- **[#5677](https://github.com/microsoft/agent-framework/pull/5677)** — .NET: Fix `FoundryAgent` URL construction generating a project-level URL instead of an agent-level URL, causing 404s under strict routing (workaround for [Azure/azure-sdk-for-net#59011](https://github.com/Azure/azure-sdk-for-net/issues/59011)). *(by rogerbarreto)*

- **[#5704](https://github.com/microsoft/agent-framework/pull/5704)** — .NET: Mark Magentic Orchestration `[Experimental]` during stabilization period, consistent with Handoff Orchestration. *(by lokitoth)*

- **[#5515](https://github.com/microsoft/agent-framework/pull/5515)** — CI: Add .NET integration test report job (mirroring the Python report) and retry logic for flaky tests. *(by giles17)*

- **[#5703](https://github.com/microsoft/agent-framework/pull/5703)** — .NET: Version bump for release. *(by lokitoth)*

- **[#5695](https://github.com/microsoft/agent-framework/pull/5695)** — .NET: Add hyperlight project to the release solution filter. *(by westey-m)*

- **[#5689](https://github.com/microsoft/agent-framework/pull/5689)** — CI: Fix MSB3026 file-copy conflict during `dotnet-foundry-hosted-it` publish step. *(by rogerbarreto)*

- **[#5674](https://github.com/microsoft/agent-framework/pull/5674)** — .NET: Fix typo `sesionElement` → `sessionElement` in dotnet sample. *(by XiongHaoTrigger)*

## Summary

May 10 was a high-velocity shipping day for `agent-framework`, delivering Magentic Orchestration for .NET, `IChatMessageInjector` for dynamic message injection, Python's new `ClassSkill` abstraction, and the coordinated Python 1.3.0 minor release bundling 16 features. The one true breaking change is the wire-format shift in `function_call_output.output` to JSON string literals — downstream .NET consumers reading raw function call output payloads must audit and update their deserialization logic. Concurrency correctness (`SequenceNumber`) and MCP error propagation (`asyncio.CancelledError`) also received targeted fixes across both platforms.
```

---

**Key decisions made:**

| Section | PRs | Rationale |
|---|---|---|
| ⚠️ Breaking Changes | #5705 | Wire format change — behavioral contract broken for existing consumers |
| Major Updates | #5595, #5679, #5678, #5665, #5706 | Net-new APIs, significant architectural additions, coordinated release |
| Minor / Bug Fixes | #5320, #5687, #5677, #5704, #5515, #5703, #5695, #5689, #5674 | Correctness fixes, CI, experimental markers, version bumps, typos |