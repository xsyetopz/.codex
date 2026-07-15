# GPT-5.6 Codex configuration

Checked 2026-07-12 against Codex CLI `0.144.1`, the live model catalog fetched at `2026-07-12T05:30:01Z`, current official Codex documentation, the local `docs/codex` runtime studies, the curated `docs/reddit/codex` community sample, and open upstream issue `openai/codex#31814`.

## Resulting configuration

`config.toml` is the master user layer used by plain `codex`. It now defaults to `gpt-5.6-sol` at `medium`, matching the documented Power preset. Three functional direct-session profiles and three separately discovered Greek-deity custom agents replace six overlapping legacy profiles:

| Invocation / role | Function | Model | Effort | Selection rule |
| --- | --- | --- | --- | --- |
| plain `codex` | Lead and integration owner | `gpt-5.6-sol` | `medium` | Default for ambiguous end-to-end work. |
| `--profile speed` | Fast direct session | `gpt-5.6-luna` | `high` | Clear lookup, focused fix, test, transformation, or finishing pass. |
| `--profile build` | Everyday direct session | `gpt-5.6-terra` | `medium` | Multi-file implementation, broad scan, or supporting-document work. |
| `--profile deep` | Deliberate direct session | `gpt-5.6-sol` | `high` | High-blast-radius reasoning, architecture, security, failure recovery, or independent review. |
| `agent_type=hermes` | Bounded child executor | `gpt-5.6-luna` | `high` | One clear, self-contained delegated slice. |
| `agent_type=hephaestus` | Child workhorse | `gpt-5.6-terra` | `medium` | One multi-file, scan, or supporting-document slice. |
| `agent_type=athena` | Child escalation/reviewer | `gpt-5.6-sol` | `high` | One high-risk reasoning, recovery, or review slice. |

The objective's `gpt-5.5-terra` label is not a current model slug. Both the live catalog and official model page identify the balanced model as `gpt-5.6-terra`; `gpt-5.5` remains a separate previous-generation model.

## Why these efforts

Official guidance says Sol is the flagship for complex open-ended work, Terra is the everyday workhorse and natural starting point for work previously given GPT-5.5, and Luna is for clear repeatable work with a known good result. Medium balances speed and depth; High is for difficult multi-step work and edge cases. OpenAI recommends the lowest effort that works and says most tasks do not need Max or Ultra.

The community sample is real-world behavioral evidence and is necessarily workload-dependent. Several patterns recur across user experience:

- Sol medium is repeatedly recommended as the pleasant or capable main driver; Sol high is a high-stakes escalation. Sol xhigh, max, and ultra receive repeated quota-burn reports.
- Luna high/xhigh/max can be cost-effective for scoped implementation, but higher settings use more raw tokens, can meander, and can require more supervision. High is the conservative standing choice; Max stays an explicit one-off choice.
- Terra feedback is mixed. Some users find it broad and effective for exploration or everyday work; others report high token use or no Pareto advantage. Medium preserves its documented workhorse role without treating it as universally cheaper.
- Scope clarity and blast radius route better than difficulty alone: a hard isolated edit can stay on Luna, while a small auth, security, migration, or config change can justify Sol.

This is a practical default ladder, not a claim that one model/effort wins every repository. Adjust a profile after real workload evidence without duplicating the master config.

## CLI and profile layering

Installed CLI help, the local config-layer study, and official profile documentation agree:

1. Plain `codex` loads `$CODEX_HOME/config.toml`.
2. `codex --profile NAME` loads the same master file, then overlays `$CODEX_HOME/NAME.config.toml`; current direct profiles are `speed`, `build`, and `deep`.
3. Project config and CLI `-c` overrides have higher precedence.
4. A profile file therefore contains only values that differ from the master layer.
5. Custom agents are independently discovered from `$CODEX_HOME/agents/*.toml`; each declares `name`, `description`, and `developer_instructions` and is not a profile alias.

The three model-lane profiles and custom-agent files each contain only model, reasoning effort, plan-mode effort, and their own developer-instruction delta. The separate `promptlab` diagnostics profile changes summary/verbosity display controls without defining a model lane. They inherit `instructions/default.md`, `prompts/default-compact.md`, service tier, tools, MCP servers, permissions, features, UI settings, and unrelated defaults. A profile may override either absolute file path when a controlled eval supports a real lane-specific difference; duplicating identical paths in every profile would add configuration without changing behavior. The schema comment is editor metadata, not a duplicate runtime value.

## Prompt ownership and durable correction

`instructions/default.md` is the shared execution contract. `prompts/default-compact.md` is the file-backed compaction contract. Role files contain only role deltas until a controlled eval justifies a profile-specific instruction or compaction variant.

The contract now treats a complaint about recurring or model-inferred Codex behavior as a request to inspect the effective layers. When evidence supports a durable global fix, Codex should update the smallest owning file under `$CODEX_HOME`, validate the effective result, and report the change instead of requiring repeated prompt corrections. It must not turn a complaint into unrelated speculative cleanup.

Routing is explicit:

- choose `hermes`, `hephaestus`, or `athena` by function;
- never assume `task_name` selects the role;
- use `fork_turns = "none"` for self-contained work;
- use a small bounded turn count only when recent context is needed;
- use `"all"` only for genuine continuation;
- keep root plus at most two children and one delegation hop.

## Multi-agent V2 guard

The live catalog selects V2 for Sol and Terra and V1 for Luna. Upstream issue `#31814` remains open as of 2026-07-12: hidden V2 spawn metadata can remove explicit `agent_type`, model, effort, and service-tier routing, while a full-history fork can multiply token use.

The master config keeps:

```toml
[features.multi_agent_v2]
max_concurrent_threads_per_session = 3
tool_namespace = "team"
hide_spawn_agent_metadata = false
```

The non-reserved `team` namespace was previously validated against the GPT-5.6 endpoint. The prompt-level `fork_turns` rule handles the separate full-history default. This is a workaround, not a permanent upstream guarantee; recheck it when `#31814` closes or CLI defaults change.

## Validation

All configuration paths were validated after the rewrite:

- Python `tomllib` parsed `config.toml`, all three model profiles, and `promptlab.config.toml`.
- A deterministic contract audit confirmed the exact master model/effort, three functional profile files, three standalone Greek-deity agent files with required metadata, catalog-supported efforts, absence of the six legacy profiles, durable-correction and bounded-fork rules, Git allowlisting, and private-state ignores.
- `codex doctor --json` reported `config.load: ok`, current CLI `0.144.1`, model `gpt-5.6-sol`, reachable provider endpoints, and a successful Responses WebSocket handshake. Its overall status was `fail` only because this noninteractive validation shell sets `TERM=dumb`.
- `codex debug prompt-input` assembled the base plus `speed`, `build`, and `deep` profile layers. Standalone custom-agent discovery is validated separately from profile loading.
- `codex exec --strict-config --ephemeral --sandbox read-only` completed a no-tool contract canary for every direct lane: `BASE_OK`, `SPEED_OK`, `BUILD_OK`, and `DEEP_OK`.
- A fresh base session inspected its `spawn_agent` schema without calling tools and returned exactly `athena,hephaestus,hermes`, proving standalone custom-agent discovery after the split.
- `git diff --check` passed. `git check-ignore -v` shows the three model profiles and `promptlab` are public source exceptions while the private master `config.toml` remains ignored.

The bounded configuration canaries used read-only sandboxes, no tools, and exact short replies. They prove current CLI composition and endpoint acceptance, not statistical superiority for arbitrary workloads. Re-tune efforts from observed repository outcomes rather than adding more standing profiles.

## Sources

Official:

- [Codex models](https://learn.chatgpt.com/docs/models)
- [Codex configuration profiles](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference#configtoml)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)
- [Codex subagent model and reasoning guidance](https://learn.chatgpt.com/docs/agent-configuration/subagents#choosing-models-and-reasoning)
- [OpenAI Codex issue #31814](https://github.com/openai/codex/issues/31814)

Local source studies:

- [`docs/codex/studies/config-layer-stack-runtime-study.md`](../codex/studies/config-layer-stack-runtime-study.md)
- [`docs/codex/studies/reasoning-effort-selection-runtime-study.md`](../codex/studies/reasoning-effort-selection-runtime-study.md)
- [`docs/codex/studies/subagent-spawn-role-runtime-study.md`](../codex/studies/subagent-spawn-role-runtime-study.md)
- [`docs/codex/studies/model-instructions-request-lowering-study.md`](../codex/studies/model-instructions-request-lowering-study.md)

Community sample:

- [Sol/Terra/Luna early workflow guide](https://www.reddit.com/r/codex/comments/1utzi5w/gpt56_sol_vs_terra_vs_luna_my_early_guide_to/)
- [Sol medium main-driver discussion](https://www.reddit.com/r/codex/comments/1utuzrr/sol_medium_as_a_main_driver_tibos_recommendations/)
- [Luna max versus Sol medium discussion](https://www.reddit.com/r/codex/comments/1utrmty/luna_max_instead_of_sol_medium/)
- [Sol high default discussion](https://www.reddit.com/r/codex/comments/1us1d53/i_believe_sol_high_should_be_your_default_now/)
- [GPT-5.6 token-use and V2 routing report](https://www.reddit.com/r/codex/comments/1utumqd/for_anyone_experiencing_unusually_high_token/)
