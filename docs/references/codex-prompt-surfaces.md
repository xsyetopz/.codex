# Codex prompt surfaces

Checked 2026-07-12 against Codex CLI `0.144.1`, the official config schema/reference, and `openai/codex` commit `9e552e9d15ba52bed7077d5357f3e18e330f8f38`.

## Distinct surfaces

| Surface | Stock/default source | Request role and lifecycle |
| --- | --- | --- |
| Base model instructions | [`codex-rs/protocol/src/prompts/base_instructions/default.md`](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/protocol/src/prompts/base_instructions/default.md) when the selected model catalog does not provide another template | Resolved as session `base_instructions`; normally sent in the Responses request's top-level `instructions` field. `model_instructions_file` replaces this layer. |
| Developer instructions | No stock text: config deserializes to `None` when unset | Codex aggregates configured text with permissions, collaboration-mode, skills, plugin, and other runtime fragments into an input message whose role is `developer`. It is not a second top-level Responses API parameter. |
| Compaction prompt | [`codex-rs/prompts/templates/compact/prompt.md`](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/prompts/templates/compact/prompt.md) | Synthesized user input used by manual `/compact` and automatic local compaction. `compact_prompt` or `experimental_compact_prompt_file` overrides it. |
| Compaction summary prefix | [`codex-rs/prompts/templates/compact/summary_prefix.md`](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/prompts/templates/compact/summary_prefix.md) | Codex prefixes the generated summary before reinserting it into replacement history; the configurable compaction prompt does not replace this prefix. |
| Agent guidance | Global and project/subtree `AGENTS.md` files discovered at runtime | Injected as contextual user instructions, with closer files overriding broader files. This is additive to the three configurable prompt surfaces. |

## Loading and precedence

Current source resolves direct runtime overrides before configured values. For base instructions, a direct override wins over a non-empty `model_instructions_file`, which wins over the legacy inline `instructions` value. For compaction, a direct or inline `compact_prompt` wins over `experimental_compact_prompt_file`; if neither yields non-empty text, Codex uses the bundled summarization prompt.

Both file fields use absolute paths in the published schema. Root profile files layer over `config.toml`, so a profile may select its own `model_instructions_file` or `experimental_compact_prompt_file`. Identical profile declarations are intentionally omitted: profiles inherit the default files until an isolated eval supports a lane-specific variant.

## Local ownership

- `instructions/default.md`: current peer-programming base-instruction override, 8,375 bytes, SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`.
- `prompts/default-compact.md`: current compaction override, 589 bytes, SHA-256 `337310cae512938a109ac16a218ba77adbd603ea9f7d98549cd4b492a4b9d968`.
- `config.toml`: short root-specific `developer_instructions` plus absolute paths to those files.
- `speed.config.toml`, `build.config.toml`, and `deep.config.toml`: direct-session model/effort deltas; `promptlab.config.toml`: diagnostics-only detailed-summary, high-verbosity, and raw-event display overrides.
- `agents/hermes.toml`, `agents/hephaestus.toml`, and `agents/athena.toml`: independently discoverable custom subagent definitions.

For comparison, the inspected upstream hashes are:

- stock base instructions: `ac8ae107a0d72fe3476b430afb161ea4e67da2e446d778aefc44828160559807`;
- stock compaction prompt: `ab0c334d4faca17e3afbb9b16967c1b2fdcc7242a9a0880af57949fa236d6d07`;
- stock summary prefix: `e9b088e794a6bb9082ac053fcc760bd818d7e720ee4bcdc72c6e480de7b7cb0e`.

The local base override is therefore not assumed superior to stock. A future controlled pass should compare stock/catalog instructions, the current explicit contract, and golfed variants on representative cases. The stock prompt itself contains persistence and process language that may be redundant with the active harness, so source length alone is not a quality signal.

## Custom agents versus profiles

Official Codex documentation treats `~/.codex/agents/*.toml` as standalone custom-agent layers. Each must define `name`, `description`, and `developer_instructions`; model, effort, sandbox, MCP, and skills settings are optional overrides. The filename is conventional, while `name` is authoritative.

Profiles are separate direct-session overlays selected with `--profile`. This configuration therefore uses functional profile names (`speed`, `build`, `deep`) and Greek-deity agent names (`hermes`, `hephaestus`, `athena`) rather than making one file serve both contracts.

## Sources

- [Codex configuration reference](https://developers.openai.com/codex/config-reference#configtoml)
- [Codex subagents and custom-agent schema](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
- [Config resolution source](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/core/src/config/mod.rs)
- [Developer-context construction](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/core/src/session/mod.rs)
- [Compaction task source](https://github.com/openai/codex/blob/9e552e9d15ba52bed7077d5357f3e18e330f8f38/codex-rs/core/src/tasks/compact.rs)
