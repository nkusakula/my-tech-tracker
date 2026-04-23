I'm unable to write files in this environment due to permission restrictions. Here is the complete blog post:

---

# microsoft/agent-framework PR Summary — 2026-04-22

## Breaking Changes

- ⚠️ [#5413](https://github.com/microsoft/agent-framework/pull/5413) **.NET: Split A2A endpoint mapping into protocol-specific methods** by `SergeyMenshykh`
  `MapA2A` has been replaced with `MapA2AHttpJson` and `MapA2AJsonRpc`. The `A2AProtocolBinding` flags enum is no longer the extension point. Callers must migrate to the appropriate method(s).

  ```csharp
  // Before
  app.MapA2A("/a2a");

  // After
  app.MapA2AHttpJson("/a2a/http");
  app.MapA2AJsonRpc("/a2a/rpc");
  ```

---

## Major Updates

### Python

- [#5384](https://github.com/microsoft/agent-framework/pull/5384) **Pass client `thread_id` as `session_id` in AG-UI `AgentSession`** by `moonbox3`
  `run_agent_stream()` was generating a fresh random UUID per request, discarding the client-supplied `thread_id`. `HistoryProvider` lookups keyed by `session_id` were therefore broken. The incoming `thread_id` is now used directly as `AgentSession.session_id`.

- [#5383](https://github.com/microsoft/agent-framework/pull/5383) **Propagate `thread_id` and `forwarded_props` through AG-UI to A2A `context_id`** by `moonbox3`
  When AG-UI fronts an A2A agent, `thread_id` is now forwarded as the A2A `context_id` and `forwarded_props` from the input payload are no longer silently dropped, restoring cross-protocol session continuity.

- [#5414](https://github.com/microsoft/agent-framework/pull/5414) **fix(foundry): reconcile toolbox hosted-tool payloads with Responses API** by `moonbox3`
  Fixes `400 Missing required parameter: 'tools[N].container'` when a Foundry toolbox with a `code_interpreter` tool is loaded via `FoundryChatClient.get_toolbox()` and passed to an `Agent`.

- [#5137](https://github.com/microsoft/agent-framework/pull/5137) **Fix `OpenAIEmbeddingClient` to use `AsyncOpenAI` for `/openai/v1` endpoints** by `chetantoshniwal`
  Routing through `AsyncAzureOpenAI` on the `/openai/v1` path caused 404s because Azure rewrites paths to `/deployments/{model}/`. The client now uses `AsyncOpenAI` on non-Azure-native paths.

- [#5234](https://github.com/microsoft/agent-framework/pull/5234) **feat(evals): add `ground_truth` support for similarity evaluator** by `chetantoshniwal`
  `ground_truth` / `expected_output` is now included in Foundry JSONL dataset rows and the item schema. `evaluate_workflow` gains an `expected_output` parameter; `evaluate_agent` adds a similarity Pattern 3.

- [#5125](https://github.com/microsoft/agent-framework/pull/5125) **fix: exclude null `file_id` from `input_image` payload** by `Serjbory`
  `Content.from_uri()` with a base64 data URI was including `"file_id": null`, triggering a `400` schema error from Foundry. Null `file_id` fields are now omitted.

- [#5342](https://github.com/microsoft/agent-framework/pull/5342) **Python: Flaky test report for CI/CD** by `giles17`
  New flaky-test reporting provides visibility into intermittently failing integration tests across CI runs, reducing noise and improving signal quality.

### .NET

- [#5312](https://github.com/microsoft/agent-framework/pull/5312) **.NET Foundry Hosted Agents Support** by `rogerbarreto`
  Adds Foundry-hosted agent support to the .NET SDK with workflows and documentation, enabling standard agent abstractions over Foundry-hosted endpoints.

---

## Minor Updates & Bug Fixes

- [#5382](https://github.com/microsoft/agent-framework/pull/5382) **Python: Fix `created_at=None` in final streamed response** by `moonbox3` — Propagates the timestamp from the `response.completed` event, eliminating noisy warnings in durabletask persistence.
- [#5404](https://github.com/microsoft/agent-framework/pull/5404) **.NET Harness: Improve path validation** by `westey-m` — Code consolidation and improved validation for file stores and file-based memory stores.
- [#5421](https://github.com/microsoft/agent-framework/pull/5421) **Python: Import naming and comment cleanup** by `eavanvalkenburg` — Minor documentation and naming fixes post-review.
- [#5387](https://github.com/microsoft/agent-framework/pull/5387) **Python: Fix dev status classifier in foundry hosting `pyproject.toml`** by `moonbox3` — Corrects alpha classifier from 4 to 3 (metadata only).
- [#5418](https://github.com/microsoft/agent-framework/pull/5418) **Add PR review GitHub workflow** by `moonbox3` — Automated PR review workflow for MAF team members.
- [#5430](https://github.com/microsoft/agent-framework/pull/5430) **Pin PR review workflow to specific release** by `moonbox3` — Supply-chain hardening follow-up to #5418.

---

## Summary

The 2026-04-22 batch was heavily Python-focused, resolving a cluster of session-continuity bugs across the AG-UI/A2A integration layer and multiple Foundry client `400` errors. The one breaking change is the .NET `MapA2A` split into protocol-specific methods — impactful but clearly scoped. The most significant feature additions are `ground_truth` support in the similarity evaluator and Foundry Hosted Agents for .NET, both of which expand the framework's evaluation and hosting story for downstream consumers.