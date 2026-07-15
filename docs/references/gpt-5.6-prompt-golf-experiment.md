# GPT-5.6 prompt-golf experiment

Completed 2026-07-12.

## Decision

Retain `instructions/default.md` unchanged at SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`.

No candidate met the combined correctness, explicit-contract, and completed-work efficiency gate. The smallest candidates crossed a behavioral cliff on Terra and Luna. The only candidate that survived paired behavioral screening saved 61 static input tokens but increased Aider calls, total input, and latency, so adopting it would optimize the file rather than the work.

## Boundary and controls

Aider has no separate hard standing-instruction limit. Provider context limits are authoritative. The pinned harness configures 400,000 input tokens; observed accepted baseline calls were below the roughly 25,000-token distraction region discussed in Aider's editing guidance.

- Baseline and boundary: `gpt-5.6-prompt-golf-baseline.md`
- Frozen atomic contracts and suites: `gpt-5.6-prompt-golf-contracts.json`
- Deterministic anchor audit: `scripts/audit-prompt-golf-contracts.py`
- Aider harness commit: `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`
- Efforts: Sol/medium, Terra/medium, Luna/high
- No-tool runs used immutable full instruction files, isolated calls, low verbosity, supported detailed summaries, and raw-reasoning probes.
- Raw reasoning events were zero. Summaries were diagnostic observations, not private chain-of-thought.
- Aider used a lane-locked Sol/medium proxy, whole-file format, one thread, and two tries.

Official references:

- https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6
- https://aider.chat/docs/troubleshooting/token-limits.html
- https://aider.chat/docs/troubleshooting/edit-errors.html

## Static frontier

Every candidate passed the same explicit 12-group contract-anchor audit as the baseline. Static coverage did not predict runtime reliability.

| Candidate | Bytes | Words | Measured input tokens saved/call | First anti-echo pass |
|---|---:|---:|---:|---:|
| Baseline | 8,375 | 1,168 | 0 | 49/51 |
| Conservative | 7,172 | 981 | 205 | 42/51 |
| Balanced | 5,976 | 768 | 421 | 45/51 |
| Aggressive | 5,452 | 662 | 508 | 42/51 |
| Hybrid restoring original anti-echo wording | 6,258 | 822 | not separately probed | 46/51 |
| Delegation-only | 8,159 | 1,128 | 61 | 47/51 |

The broad candidates were rejected immediately for new frozen-case failures. Restoring the anti-echo paragraph alone did not restore behavior, demonstrating interaction with surrounding instructions.

## Paired full-prompt evaluation

The delegation-only candidate changed one low-frequency group; every other byte remained the live integrated prompt.

### Anti-echo, two passes

| Full prompt | Pass 1 | Pass 2 | Combined |
|---|---:|---:|---:|
| Baseline | 49/51 | 43/51 | 92/102 |
| Candidate | 47/51 | 49/51 | 96/102 |

Failures varied between passes. No candidate-only failure repeated across both passes, so the candidate advanced rather than being selected from one favorable sample.

Across the two passes, deterministic standing-input savings were 6,222 tokens. Candidate output increased from 5,786 to 6,767 tokens and measured model time from 581.7s to 597.8s. No malformed output occurred. Diagnostic summary events were 70 baseline and 74 candidate; raw events were zero.

### Operational contracts

| Full prompt | Sol | Terra | Luna | Total |
|---|---:|---:|---:|---:|
| Baseline | 8/8 | 7/8 | 7/8 | 22/24 |
| Candidate | 8/8 | 7/8 | 7/8 | 22/24 |

### Peer-action selection

| Full prompt | Sol | Terra | Luna | Total |
|---|---:|---:|---:|---:|
| Baseline | 7/8 | 8/8 | 7/8 | 22/24 |
| Candidate | 7/8 | 8/8 | 8/8 | 23/24 |

The candidate tied or improved these sampled correctness totals and remained structurally valid.

## Aider regression gate

The first baseline launch used a relative instruction path that resolved under the proxy work directory and produced only adapter failures. It was interrupted, excluded, and rerun with an absolute immutable path. The accepted paired runs had zero adapter failures.

| Measure | Baseline | Candidate |
|---|---:|---:|
| pass@1 | 3/6 | 3/6 |
| pass@2 | 4/6 | 4/6 |
| Malformed responses | 0 | 0 |
| Exhausted contexts | 0 | 0 |
| User-repair asks | 1 | 1 |
| Accepted model calls | 15 | 17 |
| Codex input tokens | 266,763 | 302,566 |
| Cached input tokens | 162,560 | 173,312 |
| Output tokens | 7,907 | 8,148 |
| Reasoning output tokens | 2,888 | 2,359 |
| Model-call time | 280.350s | 340.104s |
| Aider prompt tokens | 177,300 | 177,449 |
| Aider completion tokens | 6,760 | 6,551 |

The same correctness required two more calls, 35,803 more Codex input tokens, and 59.754 more model seconds. Those increases dwarf a 61-token per-call static reduction. Different repair paths prevent claiming that delegation wording caused the cost, but the predeclared gate does not permit adopting a candidate whose measured completed work is materially worse.

The candidate ceased to be a prospective winner at this gate. Untouched Aider holdouts were not exposed to a rejected candidate.

## Pareto conclusion

- Large compression (205508 tokens/call) is dominated because it regressed frozen behavior.
- The 61-token candidate is not dominated statically, but is dominated operationally in the paired Aider run.
- The live prompt is the only evaluated point preserving the best verified combination of explicitness, correctness, and completed-work efficiency.
- Prompt size is not the objective function. Minimum completed-work cost under behavioral constraints is.
- Future attempts should change one instruction group at a time and require paired service-drift controls. Good targets are duplicated runtime-injected instructions or adapter framing, not further semantic contraction of this global file.

## Artifacts

Immutable candidates remain under `instructions/candidates/` as rejected experimental evidence. Generated raw results remain under ignored `.codex-evals/prompt-golf/` and pinned Aider results under `.tmp/aider-eval/`. The live prompt was never replaced.
