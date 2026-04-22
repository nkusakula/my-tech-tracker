It appears all shell/file tools are blocked in this environment right now. Here is the complete blog post — you can save it to `blog/2026-04-21-agent-framework-pr-summary.md`:

---

```markdown
# microsoft/agent-framework PR Summary — 2026-04-21

## Breaking Changes

### ⚠️ .NET: A2A Hosting Migrated to A2A SDK v1
[#5363](https://github.com/microsoft/agent-framework/pull/5363) by **SergeyMenshykh** | `.NET` `a2a`

The A2A hosting layer (`Microsoft.Agents.AI.Hosting.A2A` and
`Microsoft.Agents.AI.Hosting.A2A.AspNetCore`) has been fully migrated to
**A2A SDK v1**. This is a breaking change for consumers of the prior A2A SDK surface:

- **New `A2AAgentHandler`** — agent handling logic extracted into a dedicated class,
  replacing the previous inline approach.
- The public API for A2A hosting has changed; callers must update registration and
  handler wiring to target the new v1 abstractions.

> ⚠️ Consumers of `Microsoft.Agents.AI.Hosting.A2A` must update dependencies and
> adoption code to the A2A SDK v1 API before upgrading.

---

## Major Updates

### 🐍 Python: Foundry Hosted Agent V2
[#5379](https://github.com/microsoft/agent-framework/pull/5379) by **TaoChenOSU** | `python` `agents` `documentation`

Introduces a second-generation Foundry Hosted Agent implementation for Python,
advancing the hosted agent integration layer with improved compatibility and
capabilities for agents running on Azure AI Foundry infrastructure.

---

### 🐍 Python: `ground_truth` Support for Similarity Evaluator
[#5234](https://github.com/microsoft/agent-framework/pull/5234) by **chetantoshniwal** | `python`

Extends the evaluation framework with first-class `ground_truth` support:

- `expected_output` now included as `ground_truth` in Foundry JSONL dataset rows.
- `ground_truth` added to the item schema and data mapping for the similarity evaluator.
- `expected_output` parameter added to `evaluate_workflow`.
- Similarity Pattern 3 added to `evaluate_agent`.

Enables more robust correctness evaluation of agent outputs against known expected answers.

---

### 🟣 .NET: Hosted Agent Adapter
[#5406](https://github.com/microsoft/agent-framework/pull/5406) by **alliscode** | `.NET`
[#5408](https://github.com/microsoft/agent-framework/pull/5408) by **alliscode** | `.NET` `documentation`

Introduces a hosted agent adapter for .NET, removing hardcoded package versions and
internal feeds. Provides a clean integration point for connecting to hosted agent
services, with accompanying documentation.

---

### 🟣 .NET: Foundry Hosted Agents Support (WIP)
[#5312](https://github.com/microsoft/agent-framework/pull/5312) by **rogerbarreto** | `.NET` `workflows` `documentation`

Merges WIP support for Foundry Hosted Agents in .NET, laying the groundwork for
connecting .NET workflows to Azure AI Foundry-hosted agent endpoints. Includes
workflow and documentation updates.

---

### 🟣 .NET: Harness — Improved Prompts and FileSystem Store
[#5365](https://github.com/microsoft/agent-framework/pull/5365) by **westey-m** | `.NET`

Enhances the agent harness with improved prompts and adds a new `FileSystem` store
implementation, expanding local persistence options for developers building and
testing agents.

---

## Minor Updates & Bug Fixes

### Bug Fixes

- **[#5125](https://github.com/microsoft/agent-framework/pull/5125)** `python` —
  **Fix: Exclude null `file_id` from `input_image` payload** (by **Serjbory**)
  `Content.from_uri()` with a base64 data URI via `FoundryChatClient` (Responses API)
  triggered a `400 "data does not match expected schema"` error. Null `file_id` fields
  are now excluded.

- **[#5137](https://github.com/microsoft/agent-framework/pull/5137)** `python` —
  **Fix `OpenAIEmbeddingClient` to use `AsyncOpenAI` for `/openai/v1` endpoints**
  (by **chetantoshniwal**)
  The client incorrectly routed Azure `/openai/v1` requests through `AsyncAzureOpenAI`,
  injecting `/deployments/{model}/` into paths and causing `404` errors. Now correctly
  uses `AsyncOpenAI` for this endpoint.

- **[#5376](https://github.com/microsoft/agent-framework/pull/5376)** `.NET` `workflows` —
  **Declarative Workflows: Gracefully handle no-response from `InvokeAzureAgent`**
  (by **peibekwe**)
  Workflows with `InvokeAzureAgent` actions could crash with
  `InvalidOperationException: Sequence contains no elements` when no response was
  returned. Now handled gracefully.

- **[#5359](https://github.com/microsoft/agent-framework/pull/5359)** `.NET` `workflows`
  `agent orchestration` — **Fix: Duplicate `CallId`s breaking Handoff Message Filtering**
  (by **lokitoth**)
  Providers like Gemini that don't use `CallId` for simultaneous function call
  disambiguation produced duplicate IDs causing multi-turn filter failures.
  Now handled correctly.

### Tests & Coverage

- **[#5390](https://github.com/microsoft/agent-framework/pull/5390)** `.NET` `workflows` —
  **Expand Workflow Unit Test Coverage** (by **lokitoth**)
  Adds tests for `ChatForwardingExecutor`, `FunctionExecutor`, and failure when hosting
  a non-`ChatProtocol` workflow as an `AIAgent`. Removes dead code; suppresses coverage
  for the obsolete `HandoffsWorkflowBuilder`.

### Samples

- **[#4875](https://github.com/microsoft/agent-framework/pull/4875)** `python` —
  **Add `set_stop_loss` as second approval-required tool in `concurrent_builder_tool_approval`
  sample** (by **moonbox3**)
  Previously only `execute_trade` required approval. Adding `set_stop_loss` better
  demonstrates concurrent approval handling for multiple tools.

### Releases & Versioning

- **[#5364](https://github.com/microsoft/agent-framework/pull/5364)** `.NET` —
  **.NET package version bump to `1.2.0`** (by **lokitoth**)
  Minor version bump; date version component extracted for easier future updates.

- **[#5385](https://github.com/microsoft/agent-framework/pull/5385)** `python` `release` —
  **Python version bumps and CHANGELOG update** (by **moonbox3**)
  Bumps to `1.1.0` (stable), `1.0.0b260421` (beta), `1.0.0a260421` (alpha).

---

## Summary

April 21, 2026 was a high-velocity day across both .NET and Python, with 15 PRs merged
spanning new features, infrastructure upgrades, and targeted bug fixes. The dominant
themes are **hosted agent support** — Foundry Hosted Agent V2 in Python and the hosted
agent adapter in .NET — and the **A2A SDK v1 migration**, a breaking change for .NET
consumers of the A2A hosting layer. Python developers gain improved evaluation tooling
with `ground_truth` in the similarity evaluator. Downstream .NET users should review
the A2A SDK v1 migration guide before upgrading.
```

---

**Note:** All bash/file tools are currently returning permission errors in this environment, so the file could not be written to `blog/`. The content above is ready to paste directly into `blog/2026-04-21-agent-framework-pr-summary.md`.