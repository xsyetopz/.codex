# ARCHITECTURE.md

This workspace is a personal Codex home, not an application repository.

## Stable domains

- `instructions/default.md` is the shared execution, Goal, coordination, escalation, validation, and handoff contract; profiles may select narrower instruction variants only after eval evidence.
- `config.toml` owns private runtime settings; Codex discovers standalone spawnable roles from `agents/*.toml`.
- Root `speed.config.toml`, `build.config.toml`, and `deep.config.toml` are thin direct-session profile layers; `promptlab.config.toml` is a diagnostics-only profile for summary and raw-event experiments. `agents/hermes.toml`, `agents/hephaestus.toml`, and `agents/athena.toml` are separate standalone subagent layers.
- `AGENTS.md` is global and contains only cross-repository scope and code-discovery defaults; local workspace facts remain here and in `docs/`.
- `docs/references/gpt-5.6-harness.md` records external source decisions and validation evidence.
- `docs/references/codex-prompt-surfaces.md` maps stock and overridden base, developer, compaction, and AGENTS.md prompt layers to current Codex source.
- `hooks.json` and `hooks/pretooluse-agent-commit-attribution.py` enforce active-model commit trailers for Codex-run Git commands; `docs/references/agent-commit-attribution.md` records scope and validation.
- `docs/references/gpt-5.6-aider-dogfood.md` owns the prompt-eval protocol; `docs/references/gpt-5.6-full-stack-dogfood.md` and `docs/references/gpt-5.6-contract-context-results.json` own full-stack candidate decisions and frozen metrics. `scripts/aider-codex-proxy.py`, `scripts/run-aider-profile-eval.py`, and `scripts/run-aider-stack-candidate.py` provide the local adapter and runner. Generated benchmark sources and raw results stay under ignored `.tmp/`.
- `docs/references/gpt-5.6-first-attempt-ablations.json` records frozen first-attempt screens and causal decisions.
- `docs/references/gpt-5.6-numerical-development-cases.json` freezes independent finite-precision fixtures materialized by the Aider runner.
- `docs/references/gpt-5.6-operational-cases.json` and `scripts/run-prompt-contract-eval.py` provide structured no-tool checks for authorization, delegation, escalation, handoff, risk, and completion behavior.
- `docs/references/gpt-5.6-repository-dogfood.md` records frozen repository-scale Aider cases; `docs/references/gpt-5.6-promptcraft-dogfood.md` and `scripts/run-promptcraft-eval.py` own wording, structure, effort, and cross-model prompt experiments.
- `docs/references/gpt-5.6-enterprise-peer-dogfood.md`, its frozen case manifest, and `scripts/run-enterprise-peer-eval.py` own enterprise peer-programming prompt validation.
- `docs/references/gpt-5.6-anti-echo-dogfood.md`, its frozen case manifest, and `scripts/run-anti-echo-eval.py` own lexical-echoing, register-mirroring, and contract-token validation.
- `docs/references/gpt-5.6-model-reading-dogfood.md` records the cross-model instruction-form matrix and reasoning-visibility limits.
- `rules/` and `scripts/` contain deterministic policy and contract checks.

## Invariants

- Shared protocol text occurs once. `instructions/` owns model-instruction variants and `prompts/` owns compaction prompts; profile files contain only measured deltas and inherit defaults otherwise.
- The root owns total outcome, Goal status, integration, and final validation.
- Delegation is one hop even when multi-agent V2 exposes spawn tools to children.
- Each concurrent writer owns disjoint files or worktrees.
- Goal completion is evidence-based; a turn, handoff, usage limit, or token budget does not prove completion. Long duration alone does not justify higher effort or a standing child team.
- The base CLI session uses Sol at medium effort. Hermes uses Luna/high for clear bounded work, Hephaestus uses Terra/medium for everyday multi-file work and broad scans, and Athena uses Sol/high only for deliberate high-risk escalation.
- Live GPT-5.6 catalog metadata selects the multi-agent runtime. Configuration exposes named role metadata without forcing V2 on globally.
- The Git boundary remains default-deny for credentials, conversations, databases, sessions, caches, and host state.
