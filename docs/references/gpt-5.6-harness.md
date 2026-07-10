# GPT-5.6 Codex engineering-team harness

Checked 2026-07-10 against Codex CLI `0.144.1`, the live GPT-5.6 catalog fetched 2026-07-10, and `openai/codex` main commit `dc5ae378967cff0de2cfb30b98c52047ab978e3d`. Main advanced during the audit from `1f0566d3`; an exact path diff confirmed no changes to the audited prompt, Goal, feature, config, session, app-server, or multi-agent sources. Profile-v2 parsing was also checked against the installed `rust-v0.144.1` source.

## Design decision

TeamSTEPPS defines four shared skills rather than four job titles: communication, leading teams, mutual support, and situation monitoring. The engineering harness therefore places one translated teamwork protocol in `model-instructions.md` and uses narrow software roles derived from the guide's core, coordinating, contingency, ancillary/support, and cross-monitoring functions.

The translation keeps operational behavior and drops clinical simulation:

| TeamSTEPPS tool | Engineering contract |
| --- | --- |
| Brief | Establish objective, evidence, roster, ownership, dependencies, integration, validation, and stop conditions. |
| Closed Loop Communication | Named request, ambiguity check-back, confirmation or correction, evidence-backed completion, and root acknowledgment. |
| Call-out and SBAR | Broadcast critical state; frame urgent blockers as situation, background evidence, assessment, and recommendation/request. |
| STEP and Huddle | Scan product, team, environment, and progress; replan only when material evidence changes the plan. |
| IPASS handoff | Transfer issue state, summary, owned actions and results, risks/contingencies, and receiver synthesis. |
| Cross-monitoring and task assistance | Verify shared work, surface missed risk, and rebalance bounded work before overload causes conflict. |
| Two-challenge, CUS, DESC, and STAR | Escalate evidence-backed material risk, stop unsafe action after one repeated challenge, resolve conflict concretely, and review high-risk actions. |
| Debrief | After material collaboration or failure, record one evidence-backed process adjustment. |

The guide's patient, health, emotion, burnout, illness, fatigue, and psychological-safety language is not attributed to models. The functional beneficiary is the user's acceptance contract, product behavior, and repository integrity.

## Prompt ownership

- `model-instructions.md` is the sole shared execution and TeamSTEPPS-derived protocol. It and the standalone compaction prompt use OpenAI's published GPT-5.6 complex-prompt structure in order: Role, Personality, Goal, Success criteria, Constraints, Tools, Output, and Stop rules.
- `config.toml` adds only the default lead delta, compaction state, feature settings, and prompt-visible role registration.
- Each root `*.config.toml` contains one role delta and model/effort settings. It inherits the shared model instructions and compact prompt.
- `AGENTS.md` is a short global map with overview, read-next sources, command discovery, code/security, closer-scope precedence, and a compact code-discovery pointer. Workspace maps, local paths, and maintenance commands stay in `ARCHITECTURE.md`, this reference, and deterministic scripts.
- Exact duplicate prompt paragraphs are rejected by `scripts/check-prompt-budgets.py`.

Upstream `codex-rs/protocol/src/prompts/base_instructions/default.md` is a 275-line generic contract checklist, not the live GPT-5.6 catalog prompt. The replacement retains its material repository-instruction precedence, scope, progress, persistence, validation, and final-evidence duties while removing examples, repeated style scaffolding, and the upstream `apply_patch` mandate. Local Python-fu replaces that edit route once in the shared prompt.

## Role, effort, and usage contract

OpenAI states that additional weekly limits may apply and that usage varies with model, context, reasoning, tools, retrieval, and caching. Higher reasoning effort uses more tokens, Luna is the lowest-cost model, and Ultra explicitly trades higher token use for latency and capability. OpenAI positions Terra as the everyday balance, while Artificial Analysis reports Luna or Sol on the intelligence/cost Pareto frontier ahead of Terra in its tested effort levels. Because repeated turns compound cost in long-running Goals, standing profiles use Luna for routine work and Sol only for gated review or escalation. The independent benchmark is directional evidence, not a universal repository guarantee.

| Surface | Team function | Model | Effort | Dispatch rule |
| --- | --- | --- | --- | --- |
| no profile | Engineering lead and Goal steward | `gpt-5.6-luna` | `low` | Default single-agent root, including long-running Goals. |
| `explorer` | Ancillary support | `gpt-5.6-luna` | `low` | One explicit bounded lookup the root cannot answer cheaply. |
| `worker` | Core implementation | `gpt-5.6-luna` | `low` | One explicit disjoint implementation slice. |
| `reviewer` | Cross-monitor | `gpt-5.6-sol` | `low` | Explicit review or material risk only. |
| `responder` | Contingency team | `gpt-5.6-sol` | `medium` | Reproduced failure after one documented cheaper attempt. |
| `architect` | Technical decision support | `gpt-5.6-sol` | `high` | Rare root-only proof-grade escalation. |
| `orchestrator` | Coordinating team leader | `gpt-5.6-luna` | `medium` | Deliberately selected multi-agent burst with independent slices. |

Routine root, exploration, implementation, and orchestration stay on Luna. Sol low is reserved for independent review, Sol medium for reproduced contingency work, and Sol high for rare proof-grade architecture. Terra, Xhigh, Max, and Ultra remain deliberate per-session user choices but are absent from standing profiles. Duration alone never selects a higher tier.

Normal execution uses one agent. Multi-agent execution is capped at root plus two children. The 15-minute setting applies to CSV agent-job workers, not ordinary spawned threads; the root must bound and stop spawned work explicitly. Fast mode stays off, reasoning summaries are concise, the five-hour and weekly indicators remain visible, and the rate-limit model nudge is enabled. These controls reduce multiplicative contexts without inventing a weekly quota OpenAI does not publish.

The explorer, worker, reviewer, and responder files are each loaded by both `codex --profile NAME` and `[agents.NAME].config_file`. Architect and orchestrator are CLI profiles only. Old `quick-fix`, `build`, `debug`, and `think-hard` files and aliases remain absent.

## Goal and plan contract

A follow-up source audit checked Goal and slash-command behavior against `openai/codex` main commit `656a2d0905c9e0b9bdade1badab07ef6d42ca17c`. Slash commands are client-composer input, not model actions. Plan mode is host-selected; `update_plan` is a separate execution checklist and hard-fails in Plan mode with `update_plan is a TODO/checklist tool and is not allowed in Plan mode`.

Goals are stable, thread-scoped persisted state. The root has standing system/developer permission to call `create_goal` only when the user explicitly requests continued or autonomous work beyond an ordinary turn and supplies an auditable finish line. This satisfies the tool's explicit-request gate without treating ordinary tasks as Goals. Model tools remain `get_goal`, `create_goal`, and `update_goal`.

The model-facing `update_goal` schema exposes only `complete` and `blocked`, although Codex state and client APIs have a distinct `paused` status. For an explicit natural-language pause request, this harness uses `blocked` as a disclosed pause surrogate so automatic continuation stops immediately; this is a deliberate exception to the normal repeated-blocker threshold. Native clients should prefer Paused through their Goal controls or `thread/goal/set`. Only the root uses Goal tools. A deliberate resume starts a fresh blocked audit.

Automatic continuation occurs only while a Goal is Active, the thread is idle, no work or user input is pending, and the collaboration mode is not Plan. A continuation with no tool call is suppressed. Plan turns do not count toward Goal progress. Budget exhaustion is not completion. For Goals lasting hours or days, the root remains on Luna low, advances one verifiable milestone per continuation, batches and filters tool work, reuses cached context, and creates only short on-demand multi-agent bursts. Long duration is not evidence that Sol, Max, or Ultra is needed.

## Multi-agent contract

`multi_agent` and `goals` are stable and explicitly enabled. Live GPT-5.6 metadata selects multi-agent V2 for Sol and Terra and V1 for Luna. The config does not force the under-development V2 feature; it only sets V2 metadata visibility and the three-slot runtime shape used when the catalog selects V2.

Named role selection requires `features.multi_agent_v2.hide_spawn_agent_metadata = false`. The GPT-5.6 endpoint reserves `collaboration.spawn_agent` with an exact hidden-metadata schema, so exposing role metadata under that namespace is rejected. `tool_namespace = "team"` gives the configured role-aware schema a non-reserved namespace; a strict live canary returned `PROFILE_OK`. Three concurrent V2 slots include the root, leaving two child slots. V1 retains `agents.max_threads = 3` and `agents.max_depth = 1`.

Current V2 source exposes spawn tools at every depth and does not enforce `agents.max_depth`. The shared prompt therefore imposes one-hop delegation: only root spawns, and children never spawn even when tools remain visible. Root owns Goal status, total outcome, integration, and verification; child reports are evidence, not proof.

## Other feature decisions

Stable broad side-effect surfaces remain task-scoped: `apps`, `computer_use`, `personality`, and `secret_auth_storage` stay off globally. `workspace_dependencies` stays on. Under-development features remain unforced. Catalog-controlled `code_mode_only` and multi-agent version metadata are not duplicated as global feature toggles.

## Repository boundary

This directory is a live Codex home. `.gitignore` is default-deny. Public candidates include the shared prompt, role config layers, `AGENTS.md`, `ARCHITECTURE.md`, documentation, rules, and validation scripts. Private `config.toml`, credentials, histories, databases, sessions, caches, installed plugins/skills, OAuth state, and host paths remain ignored.

Before any commit, inspect:

```bash
git ls-files --cached --others --exclude-standard
```

## Validation record

The live runs below are the pre-optimization baseline that exposed the cost of standing high-effort and Ultra profiles; every run used `--strict-config`. After the usage rewrite, `python3 scripts/check-prompt-budgets.py` passes 267 checks, Python parses every TOML file, and `codex [--profile NAME] debug prompt-input` assembles the base and all six role layers without model inference. Codex 0.144.1 rejects `--strict-config` for its no-inference `features` and `debug` commands, so no unchanged live turns were spent merely to re-dogfood configuration. Live behavior of the new Luna/Sol ladder remains unverified.

| Run | Acceptance result | Input / cached / output / reasoning tokens |
| --- | --- | --- |
| base lead, Sol medium | Returned exact `BASE_OK`; no tools. | 14,798 / 0 / 6 / 0 |
| explorer, Terra low | Found the exact call path and percentage defect; no edit or artifact after the targeted fallback fix. | 45,977 / 36,096 / 663 / 51 |
| worker, Terra medium | Changed only `src/pricing.py` with Python; target test and `git diff --check` passed. | 61,583 / 44,800 / 733 / 85 |
| reviewer, Sol high | Found the bearer-token leak and missing assertion; no edits; ASCII severity labels after one targeted rerun. | 132,396 / 104,192 / 2,061 / 970 |
| responder, Sol xhigh | Reproduced `None.strip`, compared the contract, changed only `src/headers.py`, and passed the original test. | 81,543 / 61,440 / 1,646 / 645 |
| architect, Sol max | Chose request-scoped caching against every invariant; no edits and zero agent spawns. | 119,455 / 86,016 / 6,982 / 5,018 |
| orchestrator, Sol ultra | Briefed explorer/reviewer/worker, used disjoint ownership, waited for all, changed one file, reconciled the security finding, and passed two root-run tests. | 484,200 / 447,232 / 6,406 / 3,498 at root |

The Ultra state record confirms the exact configured children: explorer on Terra low, worker on Terra medium, and reviewer on Sol high. Their recorded token totals were 172,422, 85,630, and 71,749. No child created a descendant, confirming the prompt-enforced one-hop rule despite V2 exposing spawn tools. The root emitted a Brief, four completed waits, handoff acknowledgment, independent diff inspection, full-suite validation, and one synthesis.

Two same-case prompt reruns demonstrate targeted regression repair rather than prompt accretion. Explorer dropped from 140,379 input tokens with two failed graph calls and cache artifacts to 45,977 with two direct reads and a clean tree. The first Goal continuation reached `complete` but used four commands and a shell text write; after strengthening Python-fu, the same Goal used one Python write/verification command, produced exact bytes `474f414c5f4f4b0a`, reached `complete`, and cleared in 17 seconds with 1,560 Goal-accounted tokens.

The first role-aware V2 canary failed because the endpoint reserves `collaboration.spawn_agent` with an exact schema. Moving the visible-metadata tools to `team` returned `PROFILE_OK` and enabled the successful named-role Ultra run. These traces validate role boundaries and runtime composition; they are not a statistical claim that a higher effort always outperforms a lower one.

## Sources

- [TeamSTEPPS pocket guide](../teamstepps3-pocket-guide.md)
- [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)
- [GPT-5.6 prompt guidance](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance)
- [Global versus repository guidance](https://learn.chatgpt.com/docs/customization/overview#when-to-update-agentsmd)
- [Codex model selection](https://learn.chatgpt.com/docs/models)
- [Codex usage limits](https://learn.chatgpt.com/docs/pricing#what-are-the-usage-limits-for-my-plan)
- [OpenAI GPT-5.6 release](https://openai.com/index/gpt-5-6/)
- [Artificial Analysis GPT-5.6 benchmarks](https://artificialanalysis.ai/articles/gpt-5-6-has-landed)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference)
- [Codex base instructions](https://github.com/openai/codex/blob/dc5ae378967cff0de2cfb30b98c52047ab978e3d/codex-rs/protocol/src/prompts/base_instructions/default.md)
- [Codex feature registry](https://github.com/openai/codex/blob/dc5ae378967cff0de2cfb30b98c52047ab978e3d/codex-rs/features/src/lib.rs)
- [Current Goal tool definitions](https://github.com/openai/codex/blob/656a2d0905c9e0b9bdade1badab07ef6d42ca17c/codex-rs/ext/goal/src/spec.rs)
- [Current Goal statuses and client API](https://github.com/openai/codex/blob/656a2d0905c9e0b9bdade1badab07ef6d42ca17c/codex-rs/app-server-protocol/src/protocol/v2/thread.rs)
