# GPT-5.6 full-stack prompt dogfood

Checked 2026-07-13. Status: legacy_contract_context adopted for the frozen Aider runner; global model instructions and adapter text remain unchanged.

## Protocol

The frozen stack and candidates are in `gpt-5.6-full-stack-candidates.json`. The official control is OpenAI's suggested Role, Personality, Goal, Success criteria, Constraints, Tools, Output, and Stop rules structure. A custom structure is ineligible unless it later outperforms this control.

Selection uses the six frozen Aider regression cases. The twelve Aider holdouts remain unavailable to candidates until cross-model regression and paired repeats pass. Runs use lane locks, whole-file edits, one thread, and at most two tries. Generated code and tests execute in the pinned Aider container.

## Cross-model smoke

Five attributable lanes ran Rust `acronym` once on Sol/medium, Terra/medium, and Luna/high:

- historical workdir and legacy prefix;
- external workdir with legacy prefix;
- external workdir with the minimal three-section prefix;
- external workdir omitting permission framing;
- external workdir omitting the skills index.

All 15 responses were well formed with zero malformed output and one model call. Terra and Luna failed the task in every lane, including the historical control. Sol varied by lane, so the smoke established format compatibility and token deltas rather than quality ranking.

Measured single-call input tokens:

| Lane | Sol | Terra | Luna |
|---|---:|---:|---:|
| Historical | 16,692 | 16,690 | 14,583 |
| External workdir | 16,249 | 16,247 | 14,140 |
| Minimal OpenAI prefix | 16,239 | 16,237 | 14,130 |
| Omit permissions | 14,854 | 14,852 | 12,745 |
| Omit skills | 12,005 | 12,003 | 9,896 |

The deductions are stable across model lanes: 443 tokens for workdir deduplication, 10 for the minimal prefix, 1,395 additional for permission omission, and 4,244 additional for skill omission.

## Sol component screen

| Lane | pass@1 | pass@2 | Calls | Input | Output | Model seconds |
|---|---:|---:|---:|---:|---:|---:|
| Historical | 4/6 | 4/6 | 15 | 267,621 | 7,551 | 270.7 |
| External workdir | 3/6 | 4/6 | 17 | 297,615 | 8,407 | 299.6 |
| Minimal OpenAI prefix | 2/6 | 4/6 | 18 | 312,638 | 7,202 | 255.2 |
| Omit permissions | 2/6 | 4/6 | 19 | 302,587 | 8,735 | 328.3 |
| Omit skills | 2/6 | 4/6 | 18 | 239,801 | 8,605 | 287.3 |

Every lane had zero malformed responses and reached the same pass@2 total, but every minimal-removal lane regressed pass@1. None advanced as an isolated removal.

## Complete OpenAI structure

The initial “OpenAI” prefix contained only Goal, Constraints, and Output, so it was retained as `openai_minimal`, not treated as the required full control.

The complete eight-section control restored Sol to 4/6 at both pass@1 and pass@2 but used 19 calls, 334,844 input tokens, four user-repair asks, and 338.8 model seconds. The shared remaining failures were explicit-feedback repairs: after test output supplied the expected diagnostic or return shape, the response substituted another assumption.

Following OpenAI's migration rule, one targeted instruction was added inside the same structure:

> When messages contain test, lint, compiler, or error feedback, treat every reported expected type, value, diagnostic, and return shape as an exact contract; correct every reported mismatch.

This `openai_repair` candidate is still the OpenAI structure, not a custom syntax.

## OpenAI repair candidate

### First paired regression

| Lane | Stack | pass@1 | pass@2 | Asks | Calls | Input | Output | Reasoning | Seconds |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sol/medium | Historical | 4/6 | 4/6 | 1 | 15 | 267,621 | 7,551 | 2,265 | 270.7 |
| Sol/medium | Candidate | 4/6 | 4/6 | 1 | 14 | 247,253 | 8,319 | 2,390 | 268.3 |
| Terra/medium | Historical | 1/6 | 2/6 | 2 | 21 | 405,324 | 11,871 | 5,657 | 358.5 |
| Terra/medium | Candidate | 1/6 | 2/6 | 7 | 33 | 628,809 | 24,249 | 11,579 | 643.9 |
| Luna/high | Historical | 1/6 | 4/6 | 2 | 22 | 372,010 | 24,198 | 16,356 | 650.2 |
| Luna/high | Candidate | 1/6 | 3/6 | 4 | 25 | 420,628 | 40,384 | 30,050 | 895.9 |

All responses were well formed. Terra tied correctness but the candidate added 12 calls and 285.4 model seconds. Luna introduced a persistent pass@2 regression and added 3 calls. The candidate is rejected for both profiles.

### Sol repeat

Because the first Sol sample tied correctness with lower completed-work cost, Sol alone received a prospective paired repeat.

| Stack | pass@1 | pass@2 | Asks | Calls | Input | Output | Reasoning | Seconds |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Historical | 2/6 | 4/6 | 1 | 18 | 323,267 | 8,504 | 2,227 | 288.8 |
| Candidate | 3/6 | 4/6 | 4 | 22 | 393,688 | 11,425 | 3,644 | 406.9 |

Across both Sol runs:

| Stack | pass@1 | pass@2 | Calls | Input | Seconds |
|---|---:|---:|---:|---:|---:|
| Historical | 6/12 | 8/12 | 33 | 590,888 | 559.5 |
| Candidate | 7/12 | 8/12 | 36 | 640,941 | 675.2 |

The candidate gained one sampled pass@1 result but tied the completion bar while adding 3 calls, 50,053 input tokens, and 115.7 model seconds. That is not a completed-work improvement. It is rejected for Sol.

## Remaining failure classes

1. **Invalid-coordinate return shape:** `go-counting` commonly threw an exception or returned a normal territory object instead of the required error object. Even explicit test feedback did not reliably correct the shape.
2. **Exact null-position diagnostic:** `queen-attack` commonly returned the right exception type with the wrong exact message after the expected message appeared in test output.
3. **Repair substitution:** models sometimes replaced one disproven assumption with another rather than copying explicit expected values from feedback.
4. **First-attempt sensitivity:** removing irrelevant static framing reduced per-call tokens but changed repair paths and usually lowered pass@1.
5. **Lane-specific cost:** the same added repair rule was inexpensive on one Sol sample but caused substantial extra repair loops on Terra and Luna.

These failures are not solved by more repetition of the existing global preservation rule. The candidate already restated exact contract handling in the official structure. Further benchmark-shaped wording would encode exercise answers rather than a general policy.

## Reasoning diagnostics

Proxy telemetry now records supported reasoning-summary and raw-reasoning event counts without storing source-bearing prompts. A post-change Sol smoke observed one summary event, 300 reasoning output tokens, and zero raw-reasoning events. Summaries are supporting diagnostics, not authoritative explanations or private chain-of-thought.

Earlier regression logs preserve reasoning token counts but predate event-count telemetry. They are not retroactively labeled.

## Integrated-stack impact

All evaluated changes are default-off Aider adapter controls. They do not affect ordinary Codex turns, the global model instruction file, profile developer instructions, permissions, skills, Goal context, or no-tool anti-echo/operational/peer-action harnesses.

The live global instruction SHA remains `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`. Existing integrated anti-echo, operational, and peer-action baselines therefore remain the applicable evidence; rerunning them cannot exercise a disabled Aider-only branch.

The adapter's legacy default prefix remains byte-identical at SHA-256 `56ef8cf1217735768ba843cebf139e0041db126c90dd95333e2ce04d00402058`.

## 2026-07-12 decision

Retain the historical runtime stack and legacy adapter defaults.

- Workdir deduplication, permission omission, and skill omission produced real static savings but failed the first-attempt reliability gate.
- The full OpenAI structure was the required control.
- The targeted OpenAI repair variant failed completed-work cost or correctness gates on every model lane after paired controls.
- No custom structure was created because the OpenAI control was not outperformed by an eligible challenger.
- No candidate remained prospective after regression and repeat gates, so the twelve frozen Aider holdouts were not exposed.
- Combined omission was not tested because its individual components failed.

Default-off instrumentation remains available for future experiments. No live behavior, prompt, profile, or adapter default changed.

## 2026-07-13 contract-context follow-up

The prior prompt-only candidates repeated contract rules that were not present in the first-turn task context. The winning candidate changes the runtime boundary instead:

1. Supply configured repository tests as read-only Aider context.
2. Run the repository tests directly after the edit instead of invoking an automatic lint-repair model turn.
3. Raise the bounded run's chat-summary threshold so Aider does not launch background summary model calls.
4. Preserve instructions/default.md and the byte-identical legacy adapter prefix.

Tests are contract source, not reference implementations. Evaluated turns used no external tools or MCPs. The twelve holdouts stayed unexposed until the candidate cleared repeated regression gates.

### Regression repeats

| Lane | Reference pass@1 | Reference pass@2 | Reference calls | Candidate repeats |
|---|---:|---:|---:|---|
| Sol/medium | 6/12 | 8/12 | 33 | 11/12 pass@1, 12/12 pass@2, 13 calls |
| Terra/medium | 1/6 | 2/6 | 21 | 6/6 then 6/6, six task calls per repeat |
| Luna/high | 1/6 | 4/6 | 22 | 5/6 then 4/6 pass@1; 6/6 then 5/6 pass@2; seven then eight task calls |

Every qualifying repeat met the 5/6 pass@2 floor. The final exact-candidate runs used:

| Lane | pass@1 | pass@2 | Calls | Input | Output | Reasoning |
|---|---:|---:|---:|---:|---:|---:|
| Sol/medium repeat 1 | 5/6 | 6/6 | 7 | 131,113 | 4,879 | 1,900 |
| Sol/medium repeat 2 | 6/6 | 6/6 | 6 | 112,594 | 4,749 | 1,881 |
| Terra/medium | 6/6 | 6/6 | 6 | 112,582 | 4,045 | 1,403 |
| Luna/high | 4/6 | 5/6 | 8 | 138,115 | 10,105 | 5,884 |

All responses were well formed. The reference used 15-22 calls per six cases; the candidate used 6-8. Total input also fell despite adding tests to the first turn because most repair loops disappeared.

### Untouched holdouts

| Lane | pass@1 | pass@2 | Calls | Input | Malformed |
|---|---:|---:|---:|---:|---:|
| Sol/medium | 11/12 | 12/12 | 13 | 246,106 | 0 |
| Terra/medium | 11/12 | 12/12 | 13 | 245,500 | 0 |
| Luna/high | 9/12 | 12/12 | 15 | 252,632 | 0 |
| Total | 31/36 | 36/36 | 41 | 744,238 | 0 |

The frozen per-run telemetry, hashes, case outcomes, and residual uncertainty are in gpt-5.6-contract-context-results.json.

### Failure classes

- Invalid-coordinate return shape and the null-position diagnostic passed on the first attempt in every candidate regression run.
- All five holdout repairs completed successfully, showing that visible contracts usually prevent assumption substitution.
- The candidate keeps the previously reliable framing rather than deleting it.
- Disabling automatic lint and background summaries removes non-task calls and prevents those parallel histories from consuming context or model capacity.
- Model-lane repair cost narrowed to 6-8 regression calls. Luna still used more output and reasoning tokens than Sol or Terra.

One Luna repeat remained 5/6: its second crypto-square attempt replaced a one-assertion spacing error with a broader layout error. This is the observed residual variance, not hidden as a pass.

### Adoption

gpt-5.6-full-stack-candidates.json now selects legacy_contract_context. run-aider-stack-candidate.py uses that candidate when --candidate is omitted and rejects instruction-file hash drift. The low-level runner retains explicit switches so historical controls remain reproducible.

This adoption is limited to the frozen Aider runner. An unrelated Aider invocation needs equivalent client-side context selection and bounded repair/summary settings. The global instruction SHA remains 411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5; the legacy prefix SHA remains 56ef8cf1217735768ba843cebf139e0041db126c90dd95333e2ce04d00402058. Existing no-tool behavioral-suite results remain applicable because none of their exercised prompt layers changed.


## 2026-07-13 first-attempt ablations

A fresh twelve-case replacement holdout was selected deterministically before these runs and remains unused. Its ordered-path hash is `a0f4ba9d9cd8bfbae84e3736f3af689c585dab2491d6db8be168fd63b7777a5b`.

The first screen used only four previously exposed Luna failures. A concise wrapper check passed 2/4. Omitting the unrelated skills index passed 3/4 once and 1/4 on repeat. Input fell in both runs, but correctness was inconsistent, so the component is rejected.

The remaining Java rational-number miss was then isolated with one-call ablations. Wrapper test tracing, a literal-algorithm rule, task-local placement, moving tests nearer the request, xhigh reasoning, and max reasoning all reproduced the same floating-point assertion. Max used 5,407 reasoning tokens and 119.8 model seconds without changing the result.

The evaluator distinguishes mathematically equivalent floating-point decompositions. The task specifies the mathematical result but not the runtime decomposition needed to stay within its tolerance. More general instruction text did not make that hidden numerical choice reliable. Case-specific wording, solution leakage, and model tools remain excluded. Frozen telemetry is in `gpt-5.6-first-attempt-ablations.json`.

A search/replace diff-format screen passed 2/4 with zero malformed responses. It used 71,389 input tokens and left the board-normalization and floating-point cases unresolved, so it is also rejected.

A one-response review envelope, native architect/editor staging, and an authoritative label adjacent to the read-only tests each reproduced the isolated floating-point miss. The clean review envelope and authoritative-label runs used one call each. Architect/editor used four calls and still instructed the editor to use the failing direct fractional-power expression. An earlier envelope run is excluded because the first parser did not unwrap valid XML CDATA before passing the payload to Aider.

Across the allowed variants, the visible contract specifies a mathematical result while the evaluator distinguishes algebraically equivalent floating-point decompositions by runtime rounding. Runtime feedback repairs it; prompt-only selection has not. Encoding the passing decomposition would fit one exercise, so no candidate does that.

Two independent finite-precision cases were frozen in `gpt-5.6-numerical-development-cases.json`. The reference and a general stability rule each passed 2/2 with two calls. The rule added 104 output and 104 reasoning tokens, then reproduced the isolated rational-number miss. This separates general numerical competence from the unstated evaluator-specific decomposition: the reference already chose stable forms when the contract required accuracy.

No candidate remains eligible. Unlocking the 36/36 first-attempt gate requires runtime validation before scoring, a decomposition rule fitted to the failing contract, a gate change for that assertion, or a model/runtime change.
## 2026-07-13 amended numerical gate

The user-authorized amendment removes Java `rational-numbers` from the current pass@1 gate. Its failing assertion depended on a floating-point evaluation order absent from the visible contract. The exposed development matrix now contains the other eleven cases plus `java/exercises/practice/near-zero-quadratic-root`, whose relative-error bound and cancellation condition are explicit. The sealed replacement holdout remains byte-for-byte unchanged and unexecuted.

Evaluator controls behaved as required: the stub failed all three assertions and a stable reference formula passed all three. On Luna/high, the adopted reference missed the replacement in one call; the general finite-precision rule passed it in one call.

The subsequent low-call screens did not produce a qualifying stack:

| Change | Screen | pass@1 | Calls | Decision |
|---|---:|---:|---:|---|
| Finite-precision rule | regression | 4/6 | 6 | reject |
| Add literal-contract check | current failures | 1/2 | 2 | reject |
| Single-call review XML | one traversal case | 1/1 | 1 | broader formatter failure |
| Review XML with CDATA | exact cases reached | 3/5 | 5 | reject |
| Tests adjacent to request | current failures | 2/3 | 3 | reject |
| Add 20-word static consistency check | exact regression | 4/6 | 6 | reject |

The static check fixed a cross-file Java visibility error in isolation. The full exact run then moved failures to Go and JavaScript. CDATA fixed literal XML entity corruption but did not improve aggregate correctness. These outcomes support a variance diagnosis rather than a missing keyword diagnosis: local wording fixes move failures across already-visible contracts. No candidate earned Terra, Sol, repeated-regression, amended-holdout, or sealed-holdout calls. The live prompt, adopted candidate, and replacement holdout remain unchanged.



## 2026-07-13 sealed-gate result and second freeze

`openai_contract_context_verify_max` cleared two 6/6 regression repeats and two 36/36 amended exposed-matrix repeats with one model call per case and zero malformed responses. Its first sealed Luna run then passed 7/8 completed cases before `javascript/exercises/practice/complex-numbers` returned `-0` where deep equality required `0`. The remaining four cases were stopped, and the candidate was disqualified.

The failure isolates a representation-level primitive-value gap: naming signed zero without an expected default failed twice; explicitly canonicalizing ordinary zero passed the exposed case. Three placements then moved unrelated first-attempt failures among SGF parsing, Rust acronym, and Java queen attack, so none qualified. This is evidence of framing-sensitive variance rather than a sufficient keyword.

A second replacement holdout was selected mechanically before further tuning with salt `gpt-5.6-generalization-v3`. Its ordered-path hash is `b3310cb5d0a460131c8c8ae2e9e93561940fad145c081b7ef736c436cd59dc9f`. Its contents remain uninspected and it has no result runs. The live instruction hash remains `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`.


## 2026-07-13 post-sealed consistency follow-up

A diff-format candidate with concise compile/type framing passed the exposed signed-zero case and two Luna 6/6 regression repeats with six model calls per repeat and zero malformed responses. It also passed the contract-complete near-zero quadratic case. Its first amended exposed-matrix run then failed Java affine-cipher after nine completed matrix cases: separator placement counted previously inserted separators as semantic data. The run was stopped before other lanes or the sealed v3 set.

A language-neutral semantic-indexing criterion fixed affine-cipher and passed signed-zero plus C++, Go, and Rust screens. It then moved an unrelated failure to Java queen-attack in the first regression aggregate. This repeats the earlier pattern: narrow wording repairs the observed example but reduces consistency elsewhere. Further keyword accumulation is therefore rejected as the next direction.

The numerical selector was accidentally launched without its exact-case restriction. One auxiliary root-difference call completed and passed; a second case had started when interrupted. This run is excluded from gate evidence and is not treated as cost-free. The amended near-zero case was then run alone and passed. Likewise, interrupted fail-fast batches are reported by completed proxy telemetry only; already-launched incomplete requests are not claimed as zero cost.

The next experiment must operate at the runtime verification boundary while retaining one model call per task, and must outperform the official-structure control broadly before any new sealed evaluation. The live prompt, adopted runner, and v3 holdout remain unchanged.


## 2026-07-14 one-call diversity qualification

Native structured review and `model_verbosity` changes moved failures rather than removing them. High verbosity cleared two Luna regression repeats, then failed Python book-store. Medium verbosity cleared one repeat and failed Rust acronym in the next. A schema-backed review ledger cleared one repeat and failed SGF parsing in the next while roughly doubling output and latency.

A two-edit response kept one model call but both edits made the same JavaScript coordinate-ordering error. A four-edit response then cleared the exposed signed-zero, Python book-store, Java affine-cipher, and contract-complete near-zero quadratic screens. It also produced two 6/6 Luna regression repeats and two 6/6 Sol regression repeats, with zero malformed responses. The exact Sol totals were 119,946 input / 66,513 output tokens and 1,355.8 model-seconds for repeat 1, then 119,738 input / 59,809 output tokens and 1,495.5 model-seconds for repeat 2.

Every passing case selected edit 0 and ran tests once. The local fallback path therefore remains mechanically validated but has supplied no correctness benefit in qualifying runs. The four-edit instruction appears to change first-edit deliberation, but that is an inference, not isolated causal proof. Its output and latency are materially above the one-edit controls. Terra then cleared two independent 6/6 regression repeats with zero malformed responses: 119,726 input / 81,365 output tokens and 1,488.5 model-seconds, then 120,142 input / 87,073 output tokens and 1,592.0 model-seconds. Every case again selected edit 0. All three model lanes now satisfy the two-repeat regression gate. The first Sol amended-matrix lane then passed 12/12 with 12 calls, 247,170 input tokens, 108,747 output tokens, 83,290 reasoning tokens, 2,431.5 model-seconds, zero malformed responses, and no fallback selection. The first Terra amended-matrix lane also passed 12/12 with 12 calls, 232,202 input tokens, 187,105 output tokens, 159,485 reasoning tokens, 3,419.4 model-seconds, zero malformed responses, and no fallback selection. The first Luna amended-matrix lane passed 12/12 with 12 calls, 207,334 input tokens, 248,834 output tokens, 220,099 reasoning tokens, 4,525.3 model-seconds, zero malformed responses, and no fallback selection. Matrix repeat 1 is therefore 36/36. Every one of its 36 cases selected edit 0 and ran tests once. The second Sol amended-matrix lane passed 12/12 with 12 calls, 232,434 input tokens, 116,007 output tokens, 90,137 reasoning tokens, 2,447.1 model-seconds, zero malformed responses, and no fallback selection. The second Terra amended-matrix lane passed 12/12 with 12 calls, 245,670 input tokens, 150,580 output tokens, 125,272 reasoning tokens, 3,337.8 proxy-recorded model-seconds, zero malformed responses, and no fallback selection. The runner observed 13,629.1 seconds because one inter-request gap contributed about 10,291.1 seconds outside proxy-recorded model execution; no test timed out. This is retained as an environment or scheduling anomaly rather than attributed to model latency. The original second Luna matrix run passed all twelve tests but used thirteen model calls: one response took 625.1 seconds, exceeded Aider's 600-second request timeout, and caused an identical-message retry. This is a call-count failure even though the response was schema-valid. The candidate runner now sets the general Aider request timeout to 1,800 seconds. A fresh Luhn run passed in one 420.6-second call. Combining that replacement with the ten unchanged sub-600-second rest cases and the numerical case yields a qualifying Luna 12/12 in twelve calls: 206,918 input tokens, 219,319 output tokens, 191,644 reasoning tokens, and 4,017.2 model-seconds. The duplicate call remains reported as incurred nonqualifying cost.

Both amended-matrix repeats are now 36/36. All qualifying responses were well formed, every case selected edit 0, and every case ran tests once. Development gates are complete and sealed v3 evaluation is unlocked. The adopted candidate and live instruction hash remain unchanged.


## 2026-07-14 sealed v3 evaluation

The frozen v3 ordered-path hash was `b3310cb5d0a460131c8c8ae2e9e93561940fad145c081b7ef736c436cd59dc9f`, with zero prior result hits when evaluation began. Sol passed all twelve cases in twelve model calls, with 239,980 input tokens, 109,632 output tokens, 78,360 reasoning tokens, 2,547.5 model-seconds, zero malformed responses, and no fallback selection.

The candidate is frozen for the remaining sealed lanes. Exact candidate, runner, proxy, schema, instruction, and Aider hashes are recorded in `gpt-5.6-first-attempt-ablations.json`. Those hashes were captured immediately after the first lane rather than before result inspection; no owning file changed during the lane. Terra then passed all twelve cases in twelve calls, with 235,086 input tokens, 177,118 output tokens, 145,357 reasoning tokens, 3,269.7 model-seconds, zero malformed responses, and no fallback selection. The frozen candidate remained unchanged. Luna passed eleven of twelve cases. JavaScript tournament failed after all four generated edits were tested locally, so sealed v3 finished 35/36 and the candidate is disqualified. The failure used twelve model calls, had zero malformed responses, and received no repair call.

Before inspecting that failure, v4 was selected mechanically from paths with no prior result plus explicit exclusion of the complete v2 and v3 sets. Its ordered-path hash is `eaa108b509f4429d12b9708e3951e8cef00d985688b57cf043bf4101a28a26dc`; its manifest hash is `b78cf63b6681b83d7092bcd99b1626964d910058973b94ec38e3bf5cd46abb10`; it had zero result hits at freeze. No source, test, or task text was inspected during selection.


## 2026-07-14 post-v3 independent derivation

The v3 failure was a one-column text-layout error shared by all four edits. A new candidate keeps the one-call four-edit transport but assigns ordered derivation methods: literal-contract derivation, end-to-end test simulation, invariant and serialization-grammar derivation, and a separately derived minimal implementation. Candidates may not copy constants, indices, ordering rules, boundaries, or layout widths.

On the exposed tournament failure, the candidate passed on edit 0. The four edits were distinct and used different formatting constructions. Its first Luna regression repeat then passed 6/6 in six calls with 107,440 input tokens, 138,843 output tokens, 120,680 reasoning tokens, 2,533.3 model-seconds, zero malformed responses, and no fallback selection. This supports a reduction in correlated derivation errors, but fallback value remains unobserved and output cost increased. The second Luna regression repeat also passed 6/6 in six calls with 107,440 input tokens, 136,457 output tokens, 117,980 reasoning tokens, 2,514.7 model-seconds, zero malformed responses, and no fallback selection. Shifted-failure screens and all broader gates remain pending. Frozen v4 remains unexecuted.

The remaining signed-zero, Python book-store, Java affine-cipher, and contract-complete near-zero quadratic screens passed. Sol then passed two 6/6 regression repeats in six calls each; the first used 120,094 input and 67,084 output tokens over 1,325.2 model-seconds and selected fallback edit 1 for Rust acronym, while the second used 120,991 input and 79,228 output tokens over 1,529.4 model-seconds without fallback. Terra failed its first regression repeat 5/6: all four Rust acronym edits ignored the supplied camel-case expectation and returned `HML` instead of `HTML`. The candidate is rejected; the second Terra repeat and amended matrices were not run.

The next candidate restores an unconstrained strongest primary edit while keeping three independently derived fallback methods. Rust acronym, tournament, signed-zero, Python book-store, Java affine-cipher, and near-zero quadratic all passed on edit 0 in six model calls with zero malformed responses. The six screens used 107,917 input, 94,708 output, and 81,636 reasoning tokens over 1,729.6 model-seconds. Candidate responses are now archived per request so batch failures retain all alternatives for causal inspection. Broad gates remain pending, and v4 remains unexecuted.

Terra and Sol each passed two 6/6 regression repeats with one call per case and zero malformed responses. Sol selected fallback edit 1 for Rust acronym in its second repeat. Luna then failed its first repeat 5/6: all four acronym edits implemented only separator initials and returned `HML` instead of the supplied `HTML` expectation. Archived passing generations explicitly tracked lower-to-upper transitions; every failing generation omitted them. This is correlated contract-attention loss, not insufficient implementation diversity. The candidate is rejected before another Luna repeat or matrix run.

The next ablation changes no behavioral wording or response transport. It moves the unchanged read-only contract files immediately before the current request, testing whether context position removes the correlated omission.
