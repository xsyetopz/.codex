# GPT-5.6 compaction prompt dogfood

Checked 2026-07-12.

## Scope

This suite measures whether `prompts/default-compact.md` preserves continuation-critical facts while dropping disposable transcript noise. It is a synthetic no-tool prompt contract, not native Codex `/compact` lifecycle execution. Native manual and automatic compaction also include Codex history normalization, the bundled summary prefix, world state, hooks, and replacement-history behavior; this harness does not prove those layers.

## Frozen cases and runner

- Cases: `docs/references/gpt-5.6-compaction-cases.json` version 5, SHA-256 `64bac37c46bd74728789d6297deafa147ae4b664af0e8324def3a3609d0f45da`.
- Runner: `scripts/run-compaction-contract-eval.py`.
- Model lane: `gpt-5.6-sol`, fixed medium reasoning, eight isolated ephemeral read-only calls.
- Scoring: every continuation-critical exact canary must remain; every disposable raw-log canary must be absent.

The cases cover active goals and acceptance criteria, decisions with rationale, exact files and validation commands, blockers and authorization boundaries, unverified claims, explicit non-goals, analysis-only scope, milestones, invariants, and next actions.

## Control calibration

Five control versions were evaluated before any candidate prompt exposure:

1. v1 incorrectly forbade canceled-decision and negative-constraint markers. The prompt correctly retained them as useful non-goals.
2. v2 restricted forbidden values to raw-log markers, but one marker remained embedded in a potentially contradictory compiler dump.
3. v3 changed that marker to a stack address; the model still retained it to explain why the dump did not invalidate validation.
4. v4 made the dump explicitly redundant, but its central placement still made it salient.
5. v5 placed every disposable raw-log canary in the same trailing-noise shape. This is the frozen candidate gate.

These are scoring-control corrections, not candidate tuning: no alternative compact prompt was evaluated before v5 froze.

## Live baseline

The live prompt is 589 bytes, 87 words, SHA-256 `337310cae512938a109ac16a218ba77adbd603ea9f7d98549cd4b492a4b9d968`.

Version 5 baseline passed 8/8: all required canaries remained and all trailing raw-log canaries were dropped. This establishes a preservation gate for prompt golfing. It does not establish compression ratio, long-transcript behavior, prompt-injection resistance, or native history replacement correctness.

## Acceptance gate

A candidate must pass 8/8 on the frozen suite with no missing or leaked canary, reduce static prompt size, and receive a repeat before adoption. Native lifecycle or long-transcript coverage must be added before making broad compaction-quality claims.

## Compact Golf 01: rejected

Candidate `prompts/golf-01-compact-contract.md` compressed the same stated contract to 524 bytes and 69 words (65 bytes and 18 words fewer), SHA-256 `7b311a16477ec1cd49ecee37c9bf7bbea537323054134cbb7e70a589d054fc1c`.

On its first frozen v5 run, it passed 7/8. All required continuation facts remained, but `files_validation` retained disposable canary `RAW-DROP-FILES-903`; the live baseline had dropped it. The candidate used 124,013 input tokens versus 124,141 for the baseline, exactly 128 fewer across eight calls, but input reduction cannot compensate for a failed preservation/deletion contract.

The candidate is rejected without a repeat or live adoption. This single sampled failure does not establish which wording caused the leak; it enforces the predeclared 8/8 gate. The candidate file was removed and `prompts/default-compact.md` remains unchanged.

## Next milestone

Add long-transcript and native lifecycle coverage before another compaction golf. The current synthetic suite proves only exact continuation-canary behavior in isolated prompt calls.

## Native local compaction probe

`scripts/run-native-compaction-probe.py` exercises the installed Codex CLI `0.144.1` app-server rather than simulating the compact prompt as ordinary user text. It:

1. initializes an experimental stdio client;
2. starts an ephemeral Sol/medium, read-only, no-approval thread with the live `experimental_compact_prompt_file`;
3. records a turn containing six continuation canaries plus one already-summarized raw-log canary;
4. starts manual compaction through `thread/compact/start`;
5. waits for a completed `contextCompaction` item and idle thread status;
6. starts a continuation turn that must recover the six exact facts without naming them; and
7. scores the returned handoff.

The probe disables `remote_compaction_v2` deliberately. The configurable local compact prompt is the surface under test; the remote endpoint is a different compaction implementation and would not isolate this file.

The accepted live run passed:

- terminal compaction status: `idle`;
- completed native `contextCompaction` items: 1;
- required canaries recovered: 6/6;
- disposable raw-log canaries leaked: 0/1;
- compact prompt hash: `337310cae512938a109ac16a218ba77adbd603ea9f7d98549cd4b492a4b9d968`.

The continuation preserved the active goal, acceptance marker, exact file, exact validation command, authorization boundary, and next action. The thread was ephemeral, so the probe left no persisted rollout.

### Protocol findings

The installed app-server returns `thread/compact/start` as an asynchronous acknowledgment. In this stdio path, a benign `thread/read` request is used to wake the queued operation; waiting only for `thread/compacted` stalled. Completion is therefore established from the completed `contextCompaction` item plus terminal thread status, not from that optional notification.

Ephemeral threads reject `thread/read` with `includeTurns: true`, so scoring uses live `item/completed` events. Earlier diagnostic attempts that raced a continuation against compaction reached `systemError`; they are excluded because the accepted probe serializes on the native compaction barrier. These protocol corrections changed orchestration only, not the prompt, transcript canaries, or scoring rule.

This adds native local lifecycle evidence but remains a short transcript. Long-history replacement, automatic threshold compaction, tool-call normalization, world-state reinjection, and remote compaction remain unverified.
