The filesystem appears restricted in this environment. Here is the complete blog post produced per the `pr-analyzer` skill:

---

# microsoft/agent-framework PR Summary — 2026-05-07

## Breaking Changes

⚠️ **[#5705](https://github.com/microsoft/agent-framework/pull/5705) — .NET: Fix `function_call_output.output` serialization to JSON string on the wire** (by alliscode)

All function call outputs are now wrapped as **JSON string literals** on the wire to comply with the OpenAI Responses specification and the .NET client contract. Any integration that reads raw `function_call_output.output` values off the wire must update its parsing logic accordingly.

---

## Major Updates

### 🆕 [#5595](https://github.com/microsoft/agent-framework/pull/5595) — .NET: Implement Magentic Orchestration (by lokitoth)

Introduces **Magentic Orchestration** — a dynamic, plan-driven multi-agent system that assembles task-solving agent teams via intelligent planning and routes around the workflow dynamically based on available team capabilities. A major addition to the orchestration surface alongside the existing Handoff model.

> ⚠️ Marked `[Experimental]` via [#5704](https://github.com/microsoft/agent-framework/pull/5704) — API changes expected before GA.

---

### 🆕 [#5678](https://github.com/microsoft/agent-framework/pull/5678) — Python: Add `ClassSkill` for class-based skill definitions (by SergeyMenshykh)

Ports .NET's class-based skill feature to Python. `ClassSkill` is an abstract base class for self-contained, reusable skill units — one of 16 features driving the `python-1.3.0` release:

```python
from agent_framework import ClassSkill

class MySkill(ClassSkill):
    def my_method(self, arg: str) -> str:
        """Skill method exposed to the agent."""
        return f"processed: {arg}"
```

---

### 🆕 [#4953](https://github.com/microsoft/agent-framework/pull/4953) — .NET: Support reasoning events in AGUI (by jeffinsibycoremont)

Adds **7 new reasoning event types** to the .NET AGUI protocol layer, allowing agents to surface intermediate reasoning steps to front-end consumers. Addresses issues #2619 and #2558.

---

### ⬆️ [#5665](https://github.com/microsoft/agent-framework/pull/5665) — Python: Upgrade `github-copilot-sdk` to v1.0.0-beta.2 (by giles17)

Upgrades from `v0.2.1` → `v1.0.0-beta.2` and implements all newly exposed SDK capabilities, keeping the Python integration current with the latest Copilot SDK release.

---

### ⬆️ [#5699](https://github.com/microsoft/agent-framework/pull/5699) — .NET: Update GitHub Copilot SDK to 1.0.0-beta.2 (by lokitoth)

Mirrors the Python upgrade for .NET. The prior reference was months old and was also triggering a NuGet warning-as-error, blocking clean CI builds.

---

### ✨ [#5685](https://github.com/microsoft/agent-framework/pull/5685) — Python: Add `base_url` to `AnthropicClient` and `RawAnthropicClient` (by moonbox3)

Enables pointing the Anthropic client at custom endpoints (e.g., Azure AI Foundry), mirroring the upstream Anthropic SDK:

```python
client = AnthropicClient(base_url="https://my-foundry-endpoint.azure.com/")
```

---

## Minor Updates & Bug Fixes

- **[#5320](https://github.com/microsoft/agent-framework/pull/5320)** — .NET: Fix race condition in `SequenceNumber.Increment()` (by tuanaiseo) — `this._sequenceNumber++` was unsynchronized; concurrent streaming could produce duplicate/out-of-order IDs. Now uses proper synchronization to guarantee monotonic sequencing.
- **[#5687](https://github.com/microsoft/agent-framework/pull/5687)** — Python: Fix `MCPStreamableHTTPTool` leaking `asyncio.CancelledError` when MCP server is unreachable (by moonbox3) — `CancelledError` is not an `Exception` subclass in Python 3.8+; adds an explicit `BaseException` catch to prevent unexpected task cancellation propagation.
- **[#5704](https://github.com/microsoft/agent-framework/pull/5704)** — .NET: Mark Magentic Orchestration `[Experimental]` (by lokitoth) — Communicates stabilization-in-progress status consistently with how Handoff Orchestration was handled at launch.
- **[#5515](https://github.com/microsoft/agent-framework/pull/5515)** — .NET/Python: Add .NET integration test report to CI (by giles17) — Adds a `dotnet-integration-test-report` CI job mirroring the Python one, plus retry logic for flaky tests.
- **[#5689](https://github.com/microsoft/agent-framework/pull/5689)** — .NET: Fix MSB3026 file-lock conflict in `Foundry.Hosting` publish step (by rogerbarreto) — Resolves CI failure where `Microsoft.Agents.AI.Abstractions.dll` could not be copied during the `dotnet-foundry-hosted-it` publish job.
- **[#5674](https://github.com/microsoft/agent-framework/pull/5674)** — .NET: Fix typo `sesionElement` → `sessionElement` in `01-get-started` sample (by XiongHaoTrigger).
- **[#5706](https://github.com/microsoft/agent-framework/pull/5706)** — Python: Bump packages to 1.3.0 (by giles17) — MINOR bump for `agent-framework`, `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry`: `1.2.2 → 1.3.0`.
- **[#5703](https://github.com/microsoft/agent-framework/pull/5703)** — .NET: Version bump for release (by lokitoth).

---

## Summary

May 7, 2026 was a high-velocity release day for `microsoft/agent-framework`, anchored by two simultaneous releases: **Python 1.3.0** (16 new features including `ClassSkill` and GitHub Copilot SDK v1 beta) and a **.NET release** delivering **Magentic Orchestration**, AGUI reasoning events, and a matching Copilot SDK upgrade. The single item demanding immediate downstream attention is the **wire-format breaking change** in `function_call_output.output` serialization ([#5705](https://github.com/microsoft/agent-framework/pull/5705)), which affects any .NET integration reading raw function call outputs. Concurrency and error-handling fixes (#5320, #5687) round out a well-balanced day of stability improvements across both SDK surfaces.

---

> ℹ️ *Note: The blog file could not be written to `blog/` due to filesystem permissions in this environment. The content above can be saved manually as `blog/2026-05-07-agent-framework.md`.*