# Codex Prompt-Layer Architecture

## Purpose

This document records the verified behavior of Codex instruction overrides and
the approved architecture for Skizzles-managed instructions. It is an
implementation guide for maintainers, not a claim that the generic upstream
prompt is the active prompt for every model.

## Status and scope

### Confirmed from source at the provenance commit**

- `model_instructions_file` is a supported replacement for the selected model's
  built-in base instructions. It is not merely an appended instruction file.
- `developer_instructions` is a separate developer-message contribution; it does
  not replace the base instructions.
- `compact_prompt` is used only for history compaction, where Codex synthesizes
  it as the compaction task's user input.
- Permissions, skills, collaboration state, environment context, extensions, and
  plugins are injected dynamically. A custom base file does not by itself remove
  these contributions.
- The installed configuration currently selects `gpt-5.6-sol`, sets
  `model_instructions_file` to
  `/Users/krystian/.codex/instructions/skizzles-base.md`, and has non-empty
  inline `developer_instructions` and `compact_prompt` values. The validated
  runtime is `codex-cli 0.144.5`; the generic base prompt at tag `rust-v0.144.5`
  is byte-identical to the pinned main-branch baseline used for the local
  derivation.

### Applied architecture**

- Maintain `/Users/krystian/.codex/instructions/skizzles-base.md` as the pinned
  local base-instructions file derived from the upstream generic `default.md`
  baseline.
- `model_instructions_file` is set to that reviewed local file as a complete
  base-instruction replacement.
- Skizzles-specific operating policy is stored in non-empty inline
  `developer_instructions`, not in the base replacement.
- Non-empty inline `compact_prompt` supplies a short continuation-state
  contract, not a general operating prompt.
- Keep permissions, skill discovery, collaboration-mode guidance, and runtime
  environment data dynamically injected by Codex.

### Open operational question**

The active file path and settings are recorded above. This document
intentionally does not duplicate the full prompt bodies, which are configuration
and policy artifacts rather than developer-facing reference content.

## Verified instruction behavior

### `model_instructions_file`

Codex reads a non-empty `model_instructions_file` into `base_instructions`; a
relative path is resolved against the effective configuration working directory.
The base chosen for a session has this source-order priority:

1. an explicit `base_instructions` override, including the value loaded from
   `model_instructions_file`;
2. base instructions persisted in resumed conversation history; or
3. the selected model's instructions from model metadata.

The relevant loader code reads the file and supplies it as `base_instructions`;
session creation then applies the priority above. This means a file replaces the
model metadata's base instructions for a new session, while a resumed session
can retain its persisted base unless an explicit override is present.

The configuration schema carries an explicit warning: users are strongly
discouraged from setting this field because departing from Codex-sanctioned
instructions will likely degrade model performance. Treat the replacement as a
versioned compatibility surface and validate it against real tasks before broad
rollout.

### `developer_instructions`

`developer_instructions` is carried independently into session configuration and
is added to the aggregated developer-message sections when non-empty. It is
appended after permissions instructions and before personality and skill
instructions in the observed assembly path. It therefore adds owner policy
without substituting the selected base instructions.

The user manual describes this setting as additional instructions injected
before `AGENTS.md`. That documentation describes the high-level ordering
contract; source inspection establishes that it remains a distinct
developer-message contribution rather than a base-model replacement.

Use this layer for durable, machine-owner policy such as task scope, engineering
evidence requirements, authority boundaries, and communication constraints. Do
not freeze runtime permission facts, installed-skill catalogs, or multi-agent
state into it.

### `compact_prompt`

Codex uses `compact_prompt` only when it runs a history-compaction task. If the
configured value is absent, it uses the built-in summarization prompt. The
configured text is synthesized as a user input for that task; it is not the
ordinary user prompt and does not change normal turn behavior.

Use this layer to preserve the state required to continue work after compaction:
objective, accepted decisions, file ownership, current evidence, outstanding
validation, blockers, and next actions. Require it to discard stale transcript
detail and sensitive values. It should not restate a complete base or developer
policy.

## Base prompt versus `codex-rs/prompts`

The upstream generic base prompt is stored at
`codex-rs/protocol/src/prompts/base_instructions/default.md`. Codex resolves the
actual selected-model baseline through model metadata, so that generic file must
not be represented as the literal active instruction text for `gpt-5.6-sol`
without inspecting the selected model catalog.

`codex-rs/prompts` is a different crate. Its exports include compaction,
apply-patch, permissions, review, realtime, and goal prompt helpers. These are
operation-specific templates and are not the selected model's base instructions.
Changing or copying an operation-specific template is not a substitute for
managing `model_instructions_file`.

## Dynamic contributions retained by the architecture

At turn setup, Codex conditionally renders permissions instructions from the
active permission profile and approval policy. It can then add configured
developer instructions, personality guidance, and the available-skills catalog.
Context contributors can add further developer, user, or isolated developer
sections.

Separately, world-state construction includes `AGENTS.md`, collaboration-mode
state, environment state, app availability, plugin state, and extension
contributions according to enabled settings. The exact content can vary with the
current session, configured features, installed plugins, task graph,
permissions, and environment.

Skizzles is enabled as a plugin in the current configuration. Its skills,
including Fourth Wall, must remain runtime-discovered rather than being copied
into a static replacement base prompt. This preserves harness updates and avoids
stale orchestration instructions.

## Applied file and policy split

| Layer | Responsibility | Content boundary | | --- | --- | --- | | Local
base-instructions file | Full replacement baseline for the selected model |
Preserve the upstream operational mechanics needed for Codex execution:
instruction hierarchy, repository rules, tool use, planning, implementation,
validation, and response discipline. Make only reviewed changes. | |
`developer_instructions` | Skizzles owner policy | State global operating
constraints, evidence standards, authority limits, and communication rules. Keep
it concise and compatible with dynamic harness instructions. | |
`compact_prompt` | Durable continuation summary | Ask for compact, factual
continuity state and explicit unresolved work. Do not carry general policy,
installed-skill text, or transient runtime data. | | Dynamic Codex injection |
Per-session facts and capabilities | Leave permissions, approvals, skills,
collaboration state, environment context, `AGENTS.md`, plugins, and extension
contributions to Codex. |

This split minimizes the risk of replacing an evolving model baseline while
still allowing stable local policy and compaction behavior. It also avoids
duplicating the dynamic information whose truth depends on the current run.

## Update procedure

When changing the applied policy:

1. Record the upstream Codex commit and source path used for the local base
   baseline.
2. Compare the local base file with the pinned upstream baseline and identify
   every intentional divergence.
3. Review the developer and compaction layers independently; neither should
   recreate the base prompt or dynamic runtime sections.
4. Apply the reviewed configuration change in the owning layer, then start a
   fresh session. A resumed session may retain persisted base instructions when
   no explicit override is supplied.
5. Exercise representative implementation, review, skill-discovery, permission,
   collaboration, and compaction workflows.
6. Update this document's provenance when rebasing the baseline or when Codex
   changes these semantics.

## Rollback

The applied prompt-policy receipt is
`/Users/krystian/.skizzles/host-wiring.json` under `promptPolicy`. If behavior
regresses, use that receipt to identify the applied wiring, then remove or
disable `model_instructions_file` first to return new sessions to the selected
model's built-in instructions. Independently clear `developer_instructions` and
`compact_prompt` if their policy or compaction behavior is implicated. Start a
new session to avoid relying on persisted history state, then rerun the
validation matrix below. Preserve the prior files long enough to identify the
failing divergence; do not silently substitute a generic upstream file for an
unverified model-specific baseline.

## Validation plan

After applying the architecture and after each material update, verify:

- **Base selection:** a fresh session reports/behaves consistently with the
  local base replacement; a fresh session without the setting returns to the
  selected model metadata baseline.
- **Developer layer:** configured owner policy appears alongside, rather than in
  place of, permissions and skill instructions.
- **Dynamic context:** active permissions, installed Skizzles skills,
  `AGENTS.md`, collaboration hints, and environment context remain available.
- **Compaction:** force or observe a compaction event and verify that the
  configured compact prompt governs the generated continuation summary without
  appearing as normal-turn policy.
- **Regression coverage:** run the repository's existing prompt/compaction
  evaluations where available, plus a representative live implementation task
  and a multi-agent task.
- **Rollback:** remove each setting in an isolated run and confirm the
  corresponding behavior returns to default without configuration parse errors.

## MultiAgentV2 validation boundary

On `codex-cli 0.144.5`, `codex exec --json` is not a sufficient record of
MultiAgentV2 spawning. The V2 spawn handler emits `SubAgentActivity`; the Exec
JSON mapper exposes `CollabAgentToolCall` items but drops other thread items. V2
wait events also use an empty `receiver_thread_ids` list because they wait on
mailbox activity rather than a named child set. Consequently, an empty wait
event and the absence of a spawn item in public Exec JSON do not prove that no
child ran.

Validate a fresh multi-agent session without `--ephemeral`, obtain the thread ID
from `thread.started`, and inspect the matching persisted rollout under
`$CODEX_HOME/sessions`. Acceptance requires a raw namespaced `spawn_agent`
function call, its matching `function_call_output`, an authored child completion
message, and the expected parent result. The 2026-07-17 canary produced all four
for `/root/qa__canary` and returned `CANARY_OK`; the parent rollout is
`/Users/krystian/.codex/sessions/2026/07/17/rollout-2026-07-17T23-28-59-019f71c4-a02c-7113-9958-38ae4c19388e.jsonl`.

For the installed version, use `fork_turns = "none"` or a positive count when
supplying explicit model or reasoning overrides. The installed handler rejects
the older full-history/default-`all` combination with those overrides. If public
Exec JSON must expose V2 spawning, the upstream owning surface is the Exec event
mapper or the V2 spawn event representation, not the local prompt stack.

## Provenance

All source links below are pinned to `bc5c9161b46feddc13282652fd2cfdf1e5bab4a9`
so future upstream changes do not alter the evidence cited here. Local source
inspection used the checkout at `/tmp/openai-codex-main` at that exact commit
and the current Codex manual cache on 2026-07-17.

- [Configuration fields and performance
  warning](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/config/src/config_toml.rs#L221-L244)
- [File loading and default injection
  flags](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/core/src/config/mod.rs#L3702-L3734)
- [Base-instruction priority and session
  configuration](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/core/src/session/mod.rs#L596-L647)
- [Developer-message, permissions, and skills
  assembly](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/core/src/session/mod.rs#L3193-L3303)
- [Collaboration and dynamic world-state
  assembly](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/core/src/session/world_state.rs#L26-L94)
- [Compaction prompt execution
  path](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/core/src/compact.rs#L92-L120)
- [Generic upstream base
  prompt](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/protocol/src/prompts/base_instructions/default.md)
- [`codex-rs/prompts` operation-template
  exports](https://github.com/openai/codex/blob/bc5c9161b46feddc13282652fd2cfdf1e5bab4a9/codex-rs/prompts/src/lib.rs#L1-L25)
- [0.144.5 MultiAgentV2 tool
  registration](https://github.com/openai/codex/blob/87db9bc18ba5bc82c1cb4e4381b44f693ee35623/codex-rs/core/src/tools/spec_plan.rs#L762-L813)
- [0.144.5 V2 spawn activity
  emission](https://github.com/openai/codex/blob/87db9bc18ba5bc82c1cb4e4381b44f693ee35623/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs#L113-L152)
- [0.144.5 Exec JSON thread-item
  mapping](https://github.com/openai/codex/blob/87db9bc18ba5bc82c1cb4e4381b44f693ee35623/codex-rs/exec/src/event_processor_with_jsonl_output.rs#L234-L310)
- [0.144.5 mailbox-wide V2 wait
  events](https://github.com/openai/codex/blob/87db9bc18ba5bc82c1cb4e4381b44f693ee35623/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs#L77-L115)
