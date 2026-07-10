# ARCHITECTURE.md

This workspace is a personal Codex home, not an application repository.

## Stable domains

- `model-instructions.md` is the single shared execution, Goal, coordination, escalation, validation, and handoff contract.
- `config.toml` owns private runtime settings and registers spawnable roles.
- Root `*.config.toml` role files are canonical configuration layers. The same explorer, worker, reviewer, and responder file is loaded by both `--profile NAME` and `[agents.NAME].config_file`.
- Architect and orchestrator are root-only profiles; they are not registered as child roles.
- `AGENTS.md` is global and contains only cross-repository scope and code-discovery defaults; local workspace facts remain here and in `docs/`.
- `docs/references/gpt-5.6-harness.md` records external source decisions and validation evidence.
- `rules/` and `scripts/` contain deterministic policy and contract checks.

## Invariants

- Shared protocol text occurs once; role files contain only role deltas. Standalone shared and compaction prompts follow the published GPT-5.6 section order.
- The root owns total outcome, Goal status, integration, and final validation.
- Delegation is one hop even when multi-agent V2 exposes spawn tools to children.
- Each concurrent writer owns disjoint files or worktrees.
- Goal completion is evidence-based; a turn, handoff, usage limit, or token budget does not prove completion. Long duration alone does not justify higher effort or a standing child team.
- Routine and long-running work defaults to Luna; Sol is gated to material review, reproduced contingency work, or proof-grade architecture.
- Live GPT-5.6 catalog metadata selects the multi-agent runtime. Configuration exposes named role metadata without forcing V2 on globally.
- The Git boundary remains default-deny for credentials, conversations, databases, sessions, caches, and host state.
