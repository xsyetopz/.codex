# GPT-5.6 full-stack prompt ledger

Checked 2026-07-12.

## Official control

The required control is OpenAI's GPT-5.6 suggested structure:

1. Role
2. Personality
3. Goal
4. Success criteria
5. Constraints
6. Tools
7. Output
8. Stop rules

Each section stays short; detail is added only when it changes behavior. OpenAI also recommends removing one repeated or irrelevant group at a time, keeping safe-action and approval policy in one place, exposing only relevant tools, and counting a resource reduction only when existing evaluations still pass.

Source: https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6

The Codex manual helper was attempted first but rejected its response because the required `x-content-sha256` header was absent. That unverified manual response is excluded. The GPT-5.6 guide was fetched through the configured OpenAI Developer Docs MCP.

## Measured stack

`codex debug prompt-input` produced exact model-visible input snapshots for base, Build, Deep, and Speed. Base instructions are sent separately through `model_instructions_file`, so the ledger records their known immutable file hash and measured runtime delta.

| Layer | Role | Characters | Words | Condition |
|---|---|---:|---:|---|
| Base instructions | API instructions | 8,375 bytes | 1,168 | Always |
| Permissions | developer | 5,647 | 878 | Default |
| Base profile delta | developer | 300 | 40 | Base |
| Skills index | developer | 18,406 | 2,052 | 43 enabled skills |
| Multi-agent common | developer | 1,842 | 288 | Sol/Terra snapshots |
| Multi-agent mode | developer | 186 | 20 | Sol/Terra snapshots |
| Global `AGENTS.md` | user | 2,024 | n/a | Always |
| Duplicate project copy | user | 2,018 | n/a | Workdir under `$CODEX_HOME` |
| Environment | user | 371-387 | n/a | Always |
| Goal continuation | user | variable | n/a | Active Goal turns |
| Aider messages | user JSON | variable | n/a | Each edit request |
| Legacy adapter prefix | user prefix | 277 | 44 | Legacy |
| Minimal OpenAI prefix | user prefix | 235 | 34 | Partial early control |
| Full OpenAI prefix | user prefix | 942 | 129 | Required eight-section control |
| OpenAI repair prefix | user prefix | 1,214 | 168 | Full control plus measured-gap rule |

The live base instruction file remains SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5` and adds 1,534 measured input tokens over a four-word minimal instruction.

## Confirmed duplication

### Workdir duplication

Running the proxy under `/Users/krystian/.codex/.tmp/...` makes Codex inject the same canonical `AGENTS.md` as both global and project guidance. Moving the no-filesystem Aider proxy workdir to its existing default, `/private/tmp/aider-codex-proxy`, removes 2,002 model-visible characters without changing the Aider messages or base instructions.

### Irrelevant Aider framing

The adapter explicitly prohibits tool calls and states that all task context is in the messages. Nevertheless, baseline Aider calls receive:

- 5,647 characters explaining permission escalation for tools;
- 18,406 characters listing 43 skills;
- 2,028 characters of multi-agent guidance on Sol/Terra.

Permissions and skill listings are independently suppressible. Multi-agent prompt injection did not respond to the tested feature overrides and remains a runtime-owned layer.

### Repeated policy

Autonomy appears in the base prompt, profile delta, and permission compiler. Delegation appears in the base prompt, profile delta, multi-agent common text, and multi-agent mode. Repository discovery appears in the base prompt and `AGENTS.md`, with the latter duplicated under `$CODEX_HOME`. Completion protocol appears in the base prompt and every active Goal continuation.

Runtime-owned safety or capability text is not deleted merely because it overlaps. The first candidates target framing that is provably irrelevant to the Aider no-tool boundary.

## Candidate controls

`scripts/aider-codex-proxy.py` now exposes independent, default-off switches:

- `--adapter-structure openai`
- `--omit-permissions`
- `--omit-skills`

Its default behavior is unchanged. Health and telemetry report each selection. The initial three-section prefix is retained as `openai_minimal`. The mandatory control uses all eight suggested sections; `openai_repair` adds one measured-gap rule without changing that structure. No custom structure exists.

Exact prompt-input snapshots show:

| Candidate | Characters | Words | Static reduction |
|---|---:|---:|---:|
| Historical workdir baseline | 30,807 | 3,832 | n/a |
| External workdir only | 28,805 | 3,561 | 2,002 chars |
| Omit permissions after workdir fix | 23,158 | 2,683 | 7,649 chars |
| Omit skills after workdir fix | 10,399 | 1,509 | 20,408 chars |
| Omit both after workdir fix | 4,752 | 631 | 26,055 chars |

These are static candidates, not accepted improvements. Each must pass paired Aider regression and holdouts with correctness, malformed output, calls, tokens, latency, and repair behavior measured. Combined removal is tested only after its components pass.

Machine-readable ledger: `gpt-5.6-full-stack-ledger.json`.
