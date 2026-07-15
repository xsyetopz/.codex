# GPT-5.6 repository-scale dogfood

Checked 2026-07-12.

## Purpose

Extend prompt and profile evidence beyond Exercism-sized files into historical repository issues that require repo-map navigation, unfamiliar source inspection, multi-file reasoning, and realistic tests. SWE-bench issue statements and hidden acceptance tests are evaluation data, not prompt content; durable prompts must never receive instance-specific hints.

## Source custody

- Aider SWE-bench harness: `Aider-AI/aider-swe-bench` commit `6e98cd6c3b2cbcba12976d6ae1b07f847480cb74`.
- SWE-bench source: `SWE-bench/SWE-bench` commit `f7bbbb2ccdf479001d6467c9e34af59e44a840f9`.
- SWE-bench Lite test parquet: SHA-256 `f46f2e3f003f2552932393da4b223e1e0456a2c71eba8b73ae58f29646c1278b`.
- Aider runtime and proxy: the existing pinned Aider commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` and `aider-benchmark:latest` manifest `sha256:cbccb06e036b1eb0f753bfe8ef02ab265681afb5ac4091cc5f4eadef278bfd73`.
- Frozen cases: `docs/references/gpt-5.6-repository-cases.json`, SHA-256 `679828ea737c65ef797151d8651f9d741b86bcc38a992e65d9a3292998a57a6a`.

The historical Aider harness depends on a separate SWE-bench Docker testbed that is not installed. The generic Aider image is sufficient for adapter and navigation bring-up, but hidden acceptance scoring requires the official testbed or equivalent images.

## Case selection

Before model exposure, the slice froze the three lexicographically lowest values of `SHA-256("gpt-5.6-repo-dogfood-v1:" + instance_id)` across the 300 SWE-bench Lite test instances:

1. `pallets__flask-5063`
2. `scikit-learn__scikit-learn-14087`
3. `sphinx-doc__sphinx-8282`

Selection did not inspect gold patches, historical Aider success, expected files, or model outcomes. The durable manifest contains issue text, historical base commit, and named test sets, but omits gold and test patches.

## Flask adapter bring-up

The Flask repository was checked out exactly at `182ce3dd15dfa3537391c3efaf9c3ff407d134d4`. The issue text was passed unchanged except for a general historical-checkout warning and explicit prohibition on hidden-test assumptions. The live base prompt hash was `ac6189d36489abed3ab4f0b69a78c86ca614974bf6123ee66619f79e1a6144f8`.

The first repo-map turn correctly selected `src/flask/cli.py` and `tests/test_cli.py`. A later turn requested `tests/test_apps/helloworld/wsgi.py`. These were model-selected files, not oracle files.

The noninteractive CLI path then failed to produce an applied patch:

- literal `.env` and `.flaskenv` names in the issue output triggered Aider file-mention prompts;
- an explicit Aider ignore file removed those unrelated sensitive fixtures from subsequent repo maps;
- the model proposed focused `routes_command` and CLI-test changes, but whole-edit/file-expansion retries ended with no tracked source diff;
- the historical checkout was restored to a clean tracked state; no hidden acceptance test or gold patch was exposed.

Across accepted proxy requests, telemetry recorded 9 calls, 338,226 input tokens, 71,168 cached input tokens, 60,943 output tokens, 14,223 reasoning tokens, and 2,050.445 seconds of model-call time. The proxy recorded no adapter error and only the locked base alias.

Outcome: navigation evidence is positive, implementation outcome is **harness-invalid / no patch**, not a model or prompt pass/fail. The CLI orchestration consumed excessive tokens and interacted badly with Aider file-mention prompts. It must not be used for profile ranking or prompt adoption.

## Coder-API runner

`scripts/run-aider-repository-eval.py` replaces the invalid CLI path. The host side verifies the exact proxy lane lock and launches the pinned Aider image. The worker uses `InputOutput(yes=True)` and `Coder.create` directly with a 2,048-token repo map, whole-file edits, at most four reflections, no auto-commit, no automatic test command, ignored `.env` mentions, captured chat and patch, and one bounded implementation retry when discovery alone produces no diff.

The runner distinguishes an applied, lint-clean plausible patch from SWE-bench resolution. Aider’s final `edit_outcome` may remain false when an earlier whole-edit attempt failed even though a later bounded retry applied a patch; the authoritative applied-patch evidence is the Git diff plus validation.

## Flask valid baseline

The clean Coder-API execution used the same frozen issue and live base prompt. It required an issue turn plus one implementation retry, selected four files, and edited `src/flask/cli.py` and `tests/test_cli.py`. The resulting 4,334-character patch added domain sorting, domain display, and focused tests.

Telemetry recorded 5 accepted base calls, zero adapter errors, 167,487 input tokens, 18,944 cached input tokens, 31,499 output tokens, 5,758 reasoning tokens, and 769.285 seconds of model-call time.

Validation separated environment drift from task behavior:

- `pytest -q tests/test_cli.py::TestRoutes`: 6 passed;
- full `tests/test_cli.py`: 53 passed and 4 failed because contemporary Werkzeug and Click removed APIs expected by the historical checkout;
- after model completion, the frozen SWE-bench test patch was applied only in an isolated evaluation clone;
- hidden `test_subdomain` and `test_host`: 0 passed, 2 failed.

The hidden failures are substantive: the patch always labeled the new column `Domain`, while the acceptance contract requires `Subdomain` for subdomain rules and `Host` for host matching. The issue example used `Domain`, so the miss is plausible rather than evidence of benchmark leakage or a prompt omission.

Outcome: **plausible local patch, unresolved SWE-bench case**. Do not add `Host`/`Subdomain` wording to persistent prompts; the existing contract-preservation rule is already general, and one hidden semantic miss does not justify benchmark-shaped duplication.

## Next milestone

Calibrate a large-file Aider search/replace `diff` run on Sphinx after provider recovery, then run scikit-learn only if it yields an applied patch. Keep validation isolated from gold/test patches until after model completion. Pin official per-case test images if generic historical dependency environments cannot reproduce acceptance tests reliably.

## Sphinx format calibration

Sphinx’s selected source and test files total 4,434 lines. The repository runner now accepts an explicit `--edit-format` (`whole`, `diff`, or `udiff`) so edit-format calibration remains separate from model, effort, and prompt experiments.

Two attempts are excluded from task scoring:

1. **Whole-file:** three successful model calls; the model selected `sphinx/ext/autodoc/__init__.py` and `tests/test_ext_autodoc.py`, identified the relevant overloaded-signature behavior, then explicitly reported that the files were too large for safe whole-file reproduction. No patch was applied.
2. **Unified diff:** discovery succeeded and the implementation response proposed the relevant `show_annotation=False` changes, but emitted pseudo-hunks using `@@ ... @@`. Aider could not apply them. The repair phase then encountered provider overload: 2 successful requests followed by 27 failed Codex executions/HTTP 502 responses. No patch was applied.

The unified-diff attempt consumed 81,311 input, 2,311 output, and 192 reasoning tokens across its two successful calls. Failed overload retries reported no token usage. The checkout remains clean.

Outcome: **unscored harness/availability calibration**. Whole-file is structurally unsuitable for these files; unified-diff compliance was insufficient and its repair was interrupted by external service state. Neither result supports changing the persistent prompt or comparing effort levels.

The next Sphinx attempt will use Aider search/replace `diff` after service recovery. Scikit-learn remains unexposed until one large-file format produces an applied patch.

## Sphinx valid diff baseline

The recovered Aider search/replace `diff` run produced and applied a plausible patch to `sphinx/ext/autodoc/__init__.py` and `tests/test_ext_autodoc.py`. It set `show_annotation=False` for overloaded function, class, and method signatures when `autodoc_typehints` is `none` or `description`, and added a focused regression test. Telemetry recorded 4 successful calls, zero adapter failures, 116,327 input tokens, 17,664 cached input tokens, 1,827 output tokens, and 591 reasoning tokens.

Validation used the official pinned SWE-bench image `swebench/sweb.eval.x86_64.sphinx-doc_1776_sphinx-8282:latest` (digest `sha256:d2a39d34d5a72b717f61141ba06f7560a20447de66e9cf2b47e05647b394e874`). The model-added focused test passed, 1/1. The frozen acceptance test failed, 0/1: annotations were suppressed, but extra overload signature lines remained; at output index 5, `Bar(x, y)` appeared where `:module: target.overload` was expected, with seven additional items.

Outcome: **plausible local patch, unresolved SWE-bench case**. The local test asserted selected substrings and did not capture the exact-output contract. Do not add Sphinx-specific wording to persistent prompts from this single miss; the general exact-contract rule already exists.

## Next milestone

Run the frozen scikit-learn case with the validated Aider search/replace `diff` format. Keep its official test patch hidden until after model completion.

## scikit-learn valid diff baseline

The untouched Aider search/replace `diff` run produced and applied a plausible patch to `sklearn/linear_model/logistic.py` and `sklearn/linear_model/tests/test_logistic.py`. It correctly replaced the unresolved user setting `self.multi_class` with the locally resolved `multi_class` value and added a binary-auto regression test. Aider reported 86,593 sent and 691 received tokens. The proxy recorded 4 successful calls, zero failures, 120,279 input tokens, 26,112 cached input tokens, 1,371 output tokens, and 428 reasoning tokens; two calls were duplicate best-effort summarization attempts after the applied edit.

Validation used the official pinned SWE-bench image `swebench/sweb.eval.x86_64.scikit-learn_1776_scikit-learn-14087:latest` (digest `sha256:5d9fd1159824d0c8f0b96435e3e636951acb41f063198fc1e1881b922727be02`). The model-added test failed, 0/2. The frozen acceptance test passed 3/6: every elastic-net variant passed, while all three L2 variants still raised `TypeError`. The patch fixed the reported indexing branch, but left `l1_ratios_[best_indices_l1]`, which indexes a Python list with an array when the penalty is L2.

Outcome: **partial semantic fix, unresolved SWE-bench case**. The model identified one real cause but its own regression test immediately exposed the omitted adjacent failure. Do not add scikit-learn-specific wording to persistent prompts; one partial fix does not establish a general prompt defect.

## Repository baseline conclusion

All three frozen cases produced meaningful navigation and plausible edits, but none passed its complete hidden acceptance contract. Flask missed mode-dependent labels, Sphinx missed exact output shape, and scikit-learn fixed one branch condition but missed an adjacent array-indexing failure. These are useful real-world behavior observations, not a leaderboard claim. The repeated signal is incomplete local verification rather than missing task-specific knowledge. Preserve the current general requirements to inspect exact contracts and validate focused behavior; test wording and structure variants next before changing the live prompt.
