# GPT-5.6 prompt-golf baseline

Checked 2026-07-12.

## Boundary

Aider does not impose a separate hard limit on standing instructions. Its official token-limit documentation says the provider owns the enforceable context and output limits; Aider estimates tokens and reports provider failures:

- https://aider.chat/docs/troubleshooting/token-limits.html
- https://aider.chat/docs/config/adv-model-settings.html

Aider's editing guidance also warns that instruction adherence often degrades above roughly 25,000 tokens of context:

- https://aider.chat/docs/troubleshooting/edit-errors.html

The pinned local harness is Aider commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`. Its model metadata configures every Codex alias with `max_input_tokens: 400000` and `max_output_tokens: 128000`. Aider's `check_tokens` warns when its estimate reaches the configured input limit; the API provider remains authoritative.

Therefore the optimization target is not fit under an Aider prompt-file limit. It is:

1. keep each complete Aider request safely below the provider window;
2. preserve headroom below the practical distraction region;
3. reduce repeated standing tokens without deleting explicit behavior.

## Current static payload

`instructions/default.md`:

| Measure | Value |
|---|---:|
| SHA-256 | `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5` |
| Bytes | 8,375 |
| Words | 1,168 |
| Lines | 76 |
| Measured Codex input-token delta versus a four-word minimal instruction | 1,534 |

The 1,534-token delta was identical for Sol/medium, Terra/medium, and Luna/high on the same frozen request. It is a direct runtime measurement, not a tokenizer estimate. The minimal comparison file is not a viable candidate; it failed the policy behavior on Terra and Luna.

The base profile adds a 35-word developer instruction. Build, Speed, and Deep add 51, 51, and 47 words respectively. Aider's adapter also adds a fixed 39-word edit-turn prefix before the compact JSON message array. These layers are separate from `instructions/default.md` and must not be silently counted as savings from editing that file.

## Observed Aider request size

Across the accepted master regression and repeated default holdout proxy logs:

| Measure | Codex input tokens per adapter call |
|---|---:|
| Calls | 57 |
| Minimum | 15,850 |
| Median | 16,985 |
| 90th percentile | 19,347 |
| Maximum | 23,267 |

All observed calls remained below 25,000. The static global instruction delta was about 6.69.7% of those complete requests. Compression can recover meaningful repeated headroom, but repository content, edit-format prompts, and repair history dominate total input.

Aider result-file `prompt_tokens` values aggregate multiple calls for a case and must not be mistaken for one request's context size.

## Optimization contract

A candidate is compared on a Pareto frontier:

- primary objective: no new correctness, authorization, contract, output-shape, or anti-echo regression;
- secondary objective: fewer measured input tokens;
- tertiary objectives: fewer bytes and words, no malformed output, and no unjustified latency or completion-token increase.

No candidate receives credit for brevity if it replaces an explicit rule with presumed model judgment. Synonyms are not automatically equivalent when they weaken authority, scope, stopping, preservation, or exact-output semantics.

Candidates are immutable during each run. Selection cases, holdouts, model efforts, scorer rules, and surrounding prompt remain fixed. A candidate that clears isolated tests must also beat the exact full-prompt baseline before adoption.
