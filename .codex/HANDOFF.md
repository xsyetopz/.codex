# Session handoff

Updated: 2026-07-15
Goal state: cleared; this file is the sole continuation record
Repository: `/Users/krystian/.codex`

## Resume instruction

Read this file, verify the frozen hashes, then continue from **Pareto challenger qualification**. Do not rerun completed gates. Do not evaluate the frozen replacement holdout until one candidate has passed every development gate and its files have been hashed.

## Stop state

- Evaluation was interrupted at the user's request.
- No benchmark, proxy, or Docker workload remains active.
- The prior Goal was cleared before handoff. Work is incomplete and no candidate was adopted.
- The live instruction file and adopted runner remain unchanged.
- Evaluated model turns used no external tools or MCP assistance.

## Frozen invariants

- `instructions/default.md`: `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`
- Manifest `adopted_candidate`: `legacy_contract_context`
- Aider commit: `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`
- Replacement salt: `gpt-5.6-generalization-v4`
- Ordered-path SHA-256: `eaa108b509f4429d12b9708e3951e8cef00d985688b57cf043bf4101a28a26dc`
- Frozen-set result hits at stop: **0**
- `docs/references/gpt-5.6-full-stack-candidates.json`: `224e43bdc8a9eff2cf597fcc2a2229ba7eafe2ab6513cba21360b8cf8084d83a`
- `scripts/aider-codex-proxy.py`: `295f0f506fbbb2fb6adbd9be5ccb7db05bc61708c1a05de21f8040d2162567ea`
- `scripts/run-aider-profile-eval.py`: `5ea43553bd1448e0a82e137fe90d2e2d5a3dd7ede53bba15332b674e7ad14a3f`
- `scripts/run-aider-stack-candidate.py`: `0f5cb74c885d5db9d35d9a723ef66f26e9d2582b5585497e4592ed1ca31cd92e`

The whole manifest hash is not the holdout identity. Use the ordered-path hash.

## Continuation objective

Finish the general GPT-5.6 Codex/Aider prompt-and-context stack without exercise-specific rules. Preserve the adopted live stack until a candidate passes the development repeats, Pareto comparison, and untouched replacement holdout across Luna, Sol, and Terra. Minimize model calls first, then tokens and latency; keep malformed responses at zero and retain exact behavioral contracts. After adoption, apply the evidence to action-oriented agent profiles and prompt boundaries.

## Remaining finish line

1. Select a Pareto-efficient candidate using calls first, then tokens and latency.
2. Reach 100% on the untouched frozen set across all three lanes.
3. Keep malformed responses at zero and preserve exact contracts.
4. Only then change the live instruction and adopted runner.
5. Synchronize the evidence ledgers from raw results.

The numerical development gate is `java/exercises/practice/near-zero-quadratic-root`. Do not restore the underspecified assertion as a gate.

## Qualified backup

`openai_contract_context_verify_compile_zero_authoritative_diff_max_candidate_set_4_primary_independent_verified_repair`

Four initial edits; one feedback call with four repair edits only when all initial edits fail.

- Regression: 36/36 across two repeats per lane.
- Regression calls: 37; one repair.
- Amended exposed matrix: 72/72 across two repeats.
- Matrix calls: 73; one repair.
- Malformed responses: 0.
- Deterministic repair self-test passed.
- Candidate responses are archived in sidecar JSONL files.

Use this candidate for the frozen gate if the challenger is rejected.

## Pareto challenger qualification

`openai_contract_context_verify_compile_zero_authoritative_diff_max_candidate_set_2_verified_repair`

Two initial edits; one feedback call with two repair edits only when both initial edits fail.

Completed:

- Regression: 36/36 across two repeats per lane; 36 calls; no repairs; zero malformed.
- Luna amended repeat 1: holdout 11/11 with 12 calls and one repair; numerical 1/1 with one call and no repair.
- Numerical metrics: 16,042 prompt tokens; 8,864 completion tokens; 165.6 seconds.
- Interrupted Sol repeat: two successful cases, two calls, no repair, zero malformed:
  - `javascript/exercises/practice/book-store`
  - `javascript/exercises/practice/connect`
- Partial directory: `.tmp/aider-eval/aider/tmp.benchmarks/2026-07-15-15-18-05--goal-candidate-set-2-repair-base-amended-repeat-1-holdout`

The partial Sol run is cost evidence, not a qualifying repeat. Restart that lane cleanly.

### Stop rule

The backup needs 73 qualifying matrix calls. The challenger already used one repair, so its minimum is also 73. If another qualifying case invokes repair, reject the challenger immediately; it cannot win the primary metric. Do not finish a dominated candidate.

If it ties at 73 and passes, compare input, output, reasoning tokens, then latency. Keep interruption cost separate from clean candidate cost.

### Resume commands

Lane mapping: `speed` = Luna, `base` = Sol, `build` = Terra.

```sh
CANDIDATE=openai_contract_context_verify_compile_zero_authoritative_diff_max_candidate_set_2_verified_repair

python3 scripts/run-aider-stack-candidate.py \
  --candidate "$CANDIDATE" --profile base --case-set holdout --tries 1 \
  --name goal-candidate-set-2-repair-base-amended-repeat-1-holdout-restart

python3 scripts/run-aider-stack-candidate.py \
  --candidate "$CANDIDATE" --profile base --case-set numerical --tries 1 \
  --case java/exercises/practice/near-zero-quadratic-root \
  --name goal-candidate-set-2-repair-base-amended-repeat-1-near-zero

python3 scripts/run-aider-stack-candidate.py \
  --candidate "$CANDIDATE" --profile build --case-set holdout --tries 1 \
  --name goal-candidate-set-2-repair-build-amended-repeat-1-holdout

python3 scripts/run-aider-stack-candidate.py \
  --candidate "$CANDIDATE" --profile build --case-set numerical --tries 1 \
  --case java/exercises/practice/near-zero-quadratic-root \
  --name goal-candidate-set-2-repair-build-amended-repeat-1-near-zero
```

Run amended repeat 2 for all three lanes only if the stop rule has not fired.

## Frozen-set gate

Before its first call:

1. Select the challenger or backup.
2. Hash the candidate, manifest, proxy, runner, schemas, and live instruction.
3. Recheck that all twelve paths still have zero result hits.
4. Do not inspect task content or expected solutions.

Run the selected candidate with `--case-set replacement_holdout --tries 2` for `speed`, `base`, and `build`. Any failure exposes the set and disqualifies the candidate; freeze a new deterministic set before more tuning. Paths are in `docs/references/gpt-5.6-aider-cases.json`.

## Authorized configuration work

The user authorized evidence-based updates to global agents, action-oriented profiles, and main prompts. Current profiles:

- `speed.config.toml`: bounded lookups, focused fixes, tests, finishing.
- `build.config.toml`: ordinary multi-file implementation and repository scans.
- `deep.config.toml`: ambiguous or high-impact analysis, architecture, recovery, review.
- `promptlab.config.toml`: controlled evaluation only.

Do not modify `instructions/default.md` or the adopted runner before the frozen gate passes. Afterwards, audit profile names and boundaries together and avoid overlap. For very large repositories, use bounded discovery and at most two independent child workstreams with explicit ownership, integration evidence, and stop conditions; do not create a standing team.

## Owning files

Implementation:

- `scripts/aider-codex-proxy.py`
- `scripts/run-aider-profile-eval.py`
- `scripts/run-aider-stack-candidate.py`
- `docs/references/aider-candidate-set-response.schema.json`
- `docs/references/aider-candidate-set-4-response.schema.json`
- `docs/references/gpt-5.6-aider-cases.json`
- `docs/references/gpt-5.6-full-stack-candidates.json`

Evidence:

- `docs/references/gpt-5.6-first-attempt-ablations.json`
- `docs/references/gpt-5.6-full-stack-dogfood.md`
- `docs/references/gpt-5.6-full-stack-ledger.json`
- `docs/references/gpt-5.6-full-stack-ledger.md`

The narrative and ablation ledgers lag the newest results. Rebuild them from raw files before adoption.

## What the user must do on return

Say:

> Create a new long-running Goal from `.codex/HANDOFF.md` and resume from Pareto challenger qualification. Preserve the frozen holdout and stop if the challenger becomes call-dominated.
