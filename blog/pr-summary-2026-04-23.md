The environment is blocking all file I/O operations right now. Here is the complete, ready-to-save blog post — copy it to `blog/2026-04-23-agent-framework.md`:

---

```markdown
# microsoft/agent-framework PR Summary — 2026-04-23

## Breaking Changes

### ⚠️ [#5423](https://github.com/microsoft/agent-framework/pull/5423) — .NET: Migrate A2A Agent and Hosting to A2A SDK v1
**Author:** SergeyMenshykh | **Labels:** documentation, .NET

The .NET A2A agent and hosting packages have been migrated from A2A SDK `0.3.4-preview` to
`1.0.0-preview2`. This is a comprehensive rework of the agent, hosting, and extension APIs to
align with the v1 SDK. Key changes include:

- Revised agent and hosting API surface to match A2A SDK v1 contracts
- Added SSE stream reconnection support

> **Action required:** Any project targeting the A2A agent or hosting packages must update
> references and adapt to the new v1 API before upgrading.

---

## Major Updates

### [#5427](https://github.com/microsoft/agent-framework/pull/5427) — .NET: Streaming Support for A2AAgentHandler
**Author:** SergeyMenshykh | **Labels:** .NET

`A2AAgentHandler` now correctly dispatches streaming requests. When `StreamingResponse = true`,
the handler calls `RunStreamingAsync` instead of `RunAsync`, enabling true streaming message
delivery over the A2A protocol.

```csharp
// After: streaming requests route to RunStreamingAsync
if (request.StreamingResponse == true)
    await RunStreamingAsync(...);
else
    await RunAsync(...);
```

---

### [#5450](https://github.com/microsoft/agent-framework/pull/5450) — .NET: Server-Side Foundry Toolbox Support
**Author:** alliscode | **Labels:** documentation, .NET

Adds `FoundryToolbox` and `AIProjectClient` extensions to `Microsoft.Agents.AI.Foundry.Hosting`,
mirroring Python's `FoundryChatClient.get_toolbox()` pattern. Tools are fetched from the Foundry
project SDK and passed as native tool definitions, enabling consistent cross-language toolbox usage.

---

### [#5412](https://github.com/microsoft/agent-framework/pull/5412) — .NET: Fix Off-Thread RunStatus Race Condition
**Author:** peibekwe | **Labels:** .NET, workflows

In `StreamingRunEventStream.RunLoopAsync`, `_runStatus` was unconditionally flipped to `Running`
after every `_inputWaiter.WaitForInputAsync` wake-up. This caused stale signals to report `Running`
even after `ResumeAsync` halted execution, making `GetStatusAsync` unreliable. The fix gates the
status flip on actual run state.

---

### [#5419](https://github.com/microsoft/agent-framework/pull/5419) — Automated Issue Triage Workflow
**Author:** moonbox3

Introduces a GitHub Actions workflow that automates initial triage of incoming bug reports,
reducing maintainer burden by programmatically categorizing and routing issues.

---

### [#5443](https://github.com/microsoft/agent-framework/pull/5443) — Propagate Integration-Test Credentials to Issue-Triage Repro
**Author:** moonbox3

Extends the Issue Triage workflow so the reproduce step can run generated Python against a real
language model using the same credentials proven in the integration test workflow — without those
secrets ever entering the LLM context.

---

### [#5424](https://github.com/microsoft/agent-framework/pull/5424) — Python: Hyperlight Sandbox Thread Confinement & Schema Cleanup
**Author:** eavanvalkenburg | **Labels:** documentation, python

Fixes two issues in the Hyperlight CodeAct sample:

1. **Thread safety:** Resolves a `pyo3_runtime.PanicException` caused by the WASM `Sandbox` being
   sent across threads by thread-confining the sandbox.
2. **Performance:** Skips redundant response parsing on host callbacks; cleans up schema and tool
   definitions.

---

## Minor Updates & Bug Fixes

- **[#5455](https://github.com/microsoft/agent-framework/pull/5455) — Python: Fix User Agent Prefix** (TaoChenOSU) — Corrects the user agent string prefix emitted by the Python SDK.
- **[#5440](https://github.com/microsoft/agent-framework/pull/5440) — Python: Suppress Spurious `[TOOLBOXES]` Warning** (moonbox3) — `FoundryChatClient` was emitting `sanitize_foundry_response_tool is experimental` on every call regardless of toolbox usage. Warning is now scoped to actual toolbox invocations.
- **[#5425](https://github.com/microsoft/agent-framework/pull/5425) — .NET: Dynamic Tool Expansion Sample** (westey-m) — Adds a sample showing runtime tool expansion via a tool call.
- **[#5444](https://github.com/microsoft/agent-framework/pull/5444) — .NET: Mark Aspire Package as Preview** (westey-m) — Corrects the Aspire package release flag to `preview`.
- **[#5449](https://github.com/microsoft/agent-framework/pull/5449) — .NET: Update Versions for Release** (westey-m) — Bumps .NET package versions for an upcoming release.
- **[#5432](https://github.com/microsoft/agent-framework/pull/5432) — Python: Bump Package Versions for Release** (moonbox3) — Increments Python package versions ahead of release.
- **[#5438](https://github.com/microsoft/agent-framework/pull/5438) — Python: Update Changelog** (moonbox3) — Adds missing entries to the Python CHANGELOG.
- **[#5434](https://github.com/microsoft/agent-framework/pull/5434) — Don't Fail CI on Review Errors** (moonbox3) — Prevents failed automated PR reviews from blocking the CI/CD pipeline.

---

## Summary

April 23rd was a high-velocity release day across both .NET and Python SDKs. The headline change is
a **breaking migration of the .NET A2A stack to SDK v1**, paired with new streaming support in
`A2AAgentHandler` — together signaling a maturing A2A protocol implementation. Reliability
improvements include a race condition fix in workflow run-status tracking and Hyperlight sandbox
thread-safety corrections. Python users gain a quieter `FoundryChatClient` (no more spurious
toolbox warnings) and a user agent fix, while version bumps across both ecosystems point to an
imminent coordinated release.
```

---

**Note:** I was unable to write the file due to environment permission restrictions. Once those are restored, save the content above to `blog/2026-04-23-agent-framework.md` and commit with:

```
git add blog/2026-04-23-agent-framework.md
git commit -m "Add PR summary blog post for microsoft/agent-framework 2026-04-23

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```