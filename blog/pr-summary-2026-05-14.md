The file system appears to be locked down in this environment — I can't write to any path. Here is the complete blog post output directly:

---

# microsoft/agent-framework PR Summary — 2026-05-14

## ⚠️ Breaking Changes

- **[#5850](https://github.com/microsoft/agent-framework/pull/5850) — Python: Support `list[str]` arguments for file-based skill scripts** *(SergeyMenshykh)*
  Broadens the `args` parameter type from `dict[str, Any] | None` to also accept `list[str]`, porting .NET PR #5475. Callers relying on the old strict `dict`-only contract must verify compatibility. Fixes #5714 and #5712.

- **[#5840](https://github.com/microsoft/agent-framework/pull/5840) — Python: DevUI improvements** *(moonbox3)*
  Reworks DevUI startup handling, CLI help text, and package guidance so local opt-out behavior stays local and shared-host usage is explicit. The changed CLI surface and opt-out semantics are a breaking change for existing DevUI integrations.

- **[#5872](https://github.com/microsoft/agent-framework/pull/5872) — Python: Bump packages for 1.4.0 release** *(giles17)*
  Cuts the `python-1.4.0` release (`agent-framework`, `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry`: `1.3.0 → 1.4.0`), driven by **two breaking changes** in the experimental Skills API. Consumers pinned to `1.3.x` must review migration notes before upgrading.

---

## Major Updates

### Python

- **[#5849](https://github.com/microsoft/agent-framework/pull/5849) — Fix A2A v1.0 non-streaming response and sample runtime issues** *(giles17)*
  Fixes two regressions from the A2A SDK v1.0 migration (#5752): (1) non-streaming path now correctly accumulates individual `StreamResponse` events rather than expecting full `Task` objects; (2) sample runtime wiring updated to match the v1.0 SDK contract.

- **[#5815](https://github.com/microsoft/agent-framework/pull/5815) — Forward MCP tool call metadata** *(he-yufeng)*
  Caches per-tool metadata from `MCP tools/list` and forwards it through `MCP tools/call` while preserving OpenTelemetry trace context injection. Adds a regression test for direct `MCPTool.call_tool()` calls that bypass `FunctionTool`.

- **[#5851](https://github.com/microsoft/agent-framework/pull/5851) — Reject path-traversal context IDs in Foundry Hosting Checkpoint Storage** *(Copilot)*
  Closes a path-traversal vulnerability where caller-supplied `previous_response_id` values containing `../` sequences could escape the checkpoint storage root via `os.path.join`. All context IDs are now validated and sanitised before path construction.

### .NET

- **[#5799](https://github.com/microsoft/agent-framework/pull/5799) — Allow naming handoff workflows** *(he-yufeng)*
  Adds `WithName` and `WithDescription` fluent methods to `HandoffWorkflowBuilder`, propagating metadata to the underlying `WorkflowBuilder`. Covers both direct metadata and DI-keyed hosting registration.

  ```csharp
  var workflow = new HandoffWorkflowBuilder()
      .WithName("CustomerSupportHandoff")
      .WithDescription("Routes customer queries to the appropriate support agent.")
      .Build();
  ```

- **[#5829](https://github.com/microsoft/agent-framework/pull/5829) — Sample: Foundry Toolbox tools in declarative workflows** *(peibekwe)*
  New declarative workflow sample showing how to embed Foundry Toolbox tools and wire them to an agent conversation. Also updates `DefaultMcpToolHandler` to accommodate the Foundry Toolbox calling convention.

- **[#5833](https://github.com/microsoft/agent-framework/pull/5833) — Add Magentic E2E workflow coverage** *(Copilot)*
  Completes the Magentic E2E test plan (`MagenticE2E_TestPlan.md`), exercising all user-visible branches of the Magentic orchestrator and providing a regression safety net for multi-agent coordination scenarios.

- **[#5880](https://github.com/microsoft/agent-framework/pull/5880) — Workflow improvements** *(moonbox3)*
  General improvements to workflow execution behavior across both Python and .NET stacks.

---

## Minor Updates & Bug Fixes

- **[#5826](https://github.com/microsoft/agent-framework/pull/5826) — .NET: Workflow Builder specialized edge tests + allocation fix** *(Copilot)*
  `WorkflowBuilderExtensions.ForwardMessage` / `ForwardExcept` were allocating an intermediate `List<ExecutorBinding>` on every single-target call. Eliminated the unnecessary allocation and added targeted edge-case tests.

- **[#5837](https://github.com/microsoft/agent-framework/pull/5837) — .NET: Re-enable previously-flaky ObservabilityTests and WorkflowRunActivityStopTests** *(Copilot)*
  Closes #4398. Un-skips `CreatesWorkflowEndToEndActivities_WithCorrectName_OffThreadAsync` and the broader `ObservabilityTests` / `WorkflowRunActivityStopTests` suites after resolving the underlying race condition.

- **[#5835](https://github.com/microsoft/agent-framework/pull/5835) — .NET: Fix flaky `InputWaiter_WaitForInputAsync_BlocksUntilSignaledAsync`** *(Copilot)*
  The `InputWaiter` implementation was correct; the test's "did not complete before signal" assertion was racy under load. Tightened test timing logic to make the invariant reliable.

- **[#5811](https://github.com/microsoft/agent-framework/pull/5811) — .NET: Harness console refactoring** *(westey-m)*
  Promotes the App Component to the top-level unit of the harness console, following a more established reactive pattern. Improves configurability and reusability of the shared console infrastructure.

- **[#5844](https://github.com/microsoft/agent-framework/pull/5844) — Python: Bump `agent-framework-ag-ui` to `1.0.0rc1`** *(moonbox3)*
  Promotes the AG-UI package to release candidate stage, signalling readiness for broader integration testing.

---

## Summary

The 2026-05-14 merge wave for `microsoft/agent-framework` was high-velocity, landing 15 PRs across both stacks. The dominant themes were **security hardening** (path-traversal fix in Foundry Hosting Checkpoint Storage), **protocol compliance** (A2A v1.0 fixes, MCP metadata forwarding), and **workflow ergonomics** (handoff naming, Foundry Toolbox declarative samples, complete Magentic E2E coverage). Downstream Python consumers should treat this as a **breaking release** — the `1.4.0` tag ships two Skills API breaking changes and a revamped DevUI CLI that require review before upgrading.