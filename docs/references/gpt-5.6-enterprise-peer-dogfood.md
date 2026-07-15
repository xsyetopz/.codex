# GPT-5.6 enterprise peer-programming promptcraft

Checked 2026-07-12 against Codex CLI `0.144.1`.

## Objective

Improve the shared GPT-5.6 instructions as an enterprise peer-programming contract without adding repository answers or replacing evidence with corporate ceremony. The target behavior is risk-proportional engineering: routine edits remain direct, while changes involving compatibility, authorization, sensitive data, persistence, migrations, concurrency, distributed state, billing, deployment, or recovery receive the evidence their failure modes require.

## Prior findings

Earlier controlled promptcraft established:

- concise positive wording is more reliable than negative-only wording on Sol;
- balanced positive and negative boundaries transfer better to Terra;
- XML and Markdown-plus-XML add tokens without improving exact behavior;
- higher effort does not repair ambiguous authorization or missing context;
- community experience is real-world behavioral evidence, while controlled runs isolate causes;
- three repository cases repeatedly failed through incomplete exact-contract or adjacent-path validation, not missing benchmark-specific knowledge.

Those findings rule out decorative structure, blanket prohibitions, and benchmark-shaped hints. They support a lifecycle organized around framing, tracing, implementation, skeptical review, independent validation, and concise reporting.

## Frozen enterprise suite

`gpt-5.6-enterprise-peer-cases.json` was frozen at SHA-256 `a9c755c5c0f88f9e6b64cdeccef5fac4f0d7b1d996cf4183ff76f3bfcd42cb32` before either prompt saw the cases. Eight no-tool cases cover:

1. direct handling of a routine private fix;
2. public API compatibility;
3. destructive and mixed-version migration planning;
4. administrative authorization and tenant isolation;
5. billing idempotency, retries, transactions, and concurrency;
6. rolling cache-protocol compatibility, observability, rollback, and recovery;
7. rejection of a self-confirming test; and
8. escalation of a dismissed credential-logging risk.

`scripts/run-enterprise-peer-eval.py` locks Sol medium, strict schema output, read-only execution, isolated calls, and exact action scoring.

## Candidate design

The accepted candidate restructures the prompt around an explicit enterprise engineering loop:

1. frame observable behavior and relevant stakeholders or promises;
2. trace owning code, callers, tests, configuration, data flow, and adjacent branches;
3. scale planning to the actual production risk;
4. implement in the owning architecture;
5. review the diff skeptically across relevant failure modes;
6. validate external behavior with independent positive, negative, and adjacent cases plus operational evidence when implicated; and
7. report compatibility, operational impact, caveats, and unverified behavior.

Enterprise controls are conditional. A private typo does not require a migration plan; a shared protocol rollout does require compatibility, observability, rollback, and recovery evidence.

## Results

### Operational safety

The accepted candidate scored 8/8 twice on the existing frozen operational suite. It preserved analysis-only scope, destructive confirmation, work-alone and bounded-delegation rules, handoff verification, environment repair, risk escalation, and evidence-based completion.

Two attempted compressions were rejected:

- the 6,917-byte form lost the operational grouping needed to classify rolling protocol readiness;
- the 7,024-byte form restored operational readiness but produced a new single-workstream allocation failure.

The rejected files were removed. Their artifacts remain under ignored `.tmp/aider-eval/` for auditability.

### Enterprise behavior

The previous live prompt scored 7/8 twice. Both runs classified a rolling cache-format deployment only as a migration concern and missed the more specific requirement for deployment compatibility, metrics, alerting, rollback, and recovery.

The accepted candidate scored 8/8 twice and consistently selected the operational-evidence boundary. This repeated result is the material adoption signal.

### Coding behavior

Because the local benchmark image had been evicted, it was rebuilt from pinned Aider source commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`. The rebuilt arm64 image ID was `sha256:e72ae53d4782b01bf9db2844d768003c603a1955c32925f2763a59ad365ef2a1`; the same environment was used for both sides of the controlled comparison.

On the frozen six-language regression slice, both the previous live prompt and accepted candidate solved the same four cases: C++ crypto-square, Go tree-building, Python SGF parsing, and Rust acronym. Both failed Java queen-attack and JavaScript go-counting after two tries. There was no case regression or improvement.

The previous prompt used 156,575 Aider prompt tokens and 5,915 completion tokens. The candidate used 158,396 prompt tokens and 6,148 completion tokens: 1.2% more input and 3.9% more output. Correctness outranks this modest cost increase for the explicit enterprise objective.

## Adoption

`instructions/default.md` now contains the accepted enterprise peer-programming contract:

- 7,623 bytes;
- 1,055 words;
- SHA-256 `9398b1ff7253f1f15b2433eaffec90405137a00e5d10487e4ba88451c6cc94db`.

The rewrite adds 1,418 bytes over the previous live prompt. It is not a successful size golf; it is a validated capability trade: unchanged frozen coding and operational behavior, plus repeated improvement on production rollout reasoning.

The compact prompt, profiles, agents, hooks, and configuration ownership remain unchanged.

## Lexical-echoing follow-up

A subsequent user correction identified lexical echoing and register mirroring in the adopted framing itself. The role label was neutralized, and a dedicated 17-case suite produced a contract-token classification plus final contextual-token deletion pass. The current live prompt is 8,375 bytes with SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`; see `gpt-5.6-anti-echo-dogfood.md`. The earlier hash remains the historical enterprise-pass artifact, not current ownership.
