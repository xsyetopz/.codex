#!/usr/bin/env python3
"""Run a frozen Aider polyglot slice against one local Codex profile adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AIDER_ROOT = ROOT / ".tmp/aider-eval/aider"
BENCHMARKS = AIDER_ROOT / "tmp.benchmarks"
MANIFEST = ROOT / "docs/references/gpt-5.6-aider-cases.json"
NUMERICAL_MANIFEST = (
    ROOT / "docs/references/gpt-5.6-numerical-development-cases.json"
)
EXPECTED_AIDER_COMMIT = "5dc9490bb35f9729ef2c95d00a19ccd30c26339c"
MODEL_BY_PROFILE = {
    "base": "openai/codex-base",
    "speed": "openai/codex-speed",
    "build": "openai/codex-build",
    "deep": "openai/codex-deep",
}


def load_cases(case_set: str) -> list[str]:
    data = json.loads(MANIFEST.read_text())
    if case_set == "regression":
        return data["regression_cases"]
    if case_set == "holdout":
        return data["holdout_cases"]
    if case_set == "replacement_holdout":
        return data["replacement_holdout_cases"]
    if case_set == "exposed_failure":
        return data["exposed_replacement_failure_cases"]
    if case_set == "numerical":
        return data["numerical_development_cases"]
    if case_set == "all":
        return data["regression_cases"] + data["holdout_cases"]
    if case_set == "smoke":
        return ["rust/exercises/practice/acronym"]
    raise ValueError(case_set)


def materialize_numerical_cases() -> None:
    data = json.loads(NUMERICAL_MANIFEST.read_text())
    expected = data.get("content_sha256")
    unsigned = {key: value for key, value in data.items() if key != "content_sha256"}
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
    actual = hashlib.sha256(canonical.encode()).hexdigest()
    if actual != expected:
        raise RuntimeError("numerical development manifest hash mismatch")
    target = BENCHMARKS / "numerical-contract-development"
    for case in data["cases"]:
        relative = Path(case["path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RuntimeError(f"invalid numerical case path: {relative}")
        case_dir = target / relative
        scaffold = case.get("scaffold")
        if scaffold:
            source_relative = Path(scaffold["source"])
            if source_relative.is_absolute() or ".." in source_relative.parts:
                raise RuntimeError(f"invalid numerical scaffold path: {source_relative}")
            source_dir = BENCHMARKS / "polyglot-benchmark" / source_relative
            for name in scaffold["files"]:
                scaffold_relative = Path(name)
                if scaffold_relative.is_absolute() or ".." in scaffold_relative.parts:
                    raise RuntimeError(
                        f"invalid numerical scaffold file: {scaffold_relative}"
                    )
                source = source_dir / scaffold_relative
                destination = case_dir / scaffold_relative
                if source.is_dir():
                    shutil.copytree(source, destination, dirs_exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
        for name, content in case["files"].items():
            file_path = Path(name)
            if file_path.is_absolute() or ".." in file_path.parts:
                raise RuntimeError(f"invalid numerical file path: {file_path}")
            destination = case_dir / file_path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content)


def verify_prerequisites(proxy_url: str, expected_model: str) -> None:
    required = [
        AIDER_ROOT / "benchmark/benchmark.py",
        BENCHMARKS / "polyglot-benchmark",
        BENCHMARKS / "codex-model-settings.yml",
        MANIFEST,
        NUMERICAL_MANIFEST,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing benchmark prerequisites: " + ", ".join(missing))
    commit = subprocess.run(
        ["git", "-C", str(AIDER_ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    if commit.returncode or commit.stdout.strip() != EXPECTED_AIDER_COMMIT:
        raise SystemExit(
            "Aider checkout drift: "
            f"expected {EXPECTED_AIDER_COMMIT}, got {commit.stdout.strip() or commit.stderr.strip()}"
        )
    try:
        with urllib.request.urlopen(
            proxy_url.rstrip("/") + "/healthz", timeout=3
        ) as response:
            health = json.load(response)
            if health.get("status") != "ok":
                raise ValueError("unexpected health response")
            expected_alias = expected_model.rsplit("/", 1)[-1]
            if health.get("allowed_models") != [expected_alias]:
                raise ValueError(
                    "proxy lane lock mismatch: "
                    f"expected {[expected_alias]!r}, got {health.get('allowed_models')!r}"
                )
    except Exception as exc:
        raise SystemExit(f"Codex adapter is unavailable at {proxy_url}: {exc}") from exc


def render_benchmark_overlay(
    context_tests: bool,
    disable_auto_lint: bool,
    disable_summarization: bool,
    task_contract_addendum: bool,
    authoritative_test_context: bool,
    numerical_stability_addendum: bool,
    static_consistency_addendum: bool,
    value_semantics_addendum: bool,
    zero_canonicalization_addendum: bool,
    candidate_sidecar: Path | None,
    candidate_repair_on_failure: bool,
    request_timeout: float | None,
) -> Path:
    source = AIDER_ROOT / "benchmark/benchmark.py"
    text = source.read_text()
    replacements = []
    if request_timeout is not None:
        replacements.append(
            (
                "from aider.io import InputOutput\n\nBENCHMARK_DNAME",
                "from aider.io import InputOutput\n\n"
                f"models.request_timeout = {request_timeout!r}\n\nBENCHMARK_DNAME",
            )
        )
    if context_tests:
        replacements.extend(
            [
                (
                    '    fnames = []\n    config_file = testdir / ".meta/config.json"',
                    '    fnames = []\n    read_only_fnames = []\n    config_file = testdir / ".meta/config.json"',
                ),
                (
                    '    file_list = " ".join(fname.name for fname in fnames)',
                    '    for file_path in test_files:\n        test_file = testdir / Path(file_path)\n        if test_file.exists():\n            read_only_fnames.append(test_file)\n\n    file_list = " ".join(fname.name for fname in fnames)',
                ),
                (
                    "        fnames=fnames,\n        use_git=False,",
                    "        fnames=fnames,\n        read_only_fnames=read_only_fnames,\n        use_git=False,",
                ),
            ]
        )
    if disable_summarization:
        replacements.append(
            (
                "    dump(coder.ignore_mentions)",
                "    coder.summarizer.max_tokens = 1_000_000\n    dump(coder.ignore_mentions)",
            )
        )
    if authoritative_test_context:
        replacements.append(
            (
                "    dump(coder.ignore_mentions)",
                "    coder.gpt_prompts.read_only_files_prefix = (\n"
                "        \"Here are READ ONLY contract files. Treat every expected value, type, \"\n"
                "        \"diagnostic, boundary, serialization detail, and test input as \"\n"
                "        \"authoritative. Reconcile the implementation with all of them. \"\n"
                "        \"Do not edit these files!\\n\"\n"
                "    )\n"
                "    dump(coder.ignore_mentions)",
            )
        )
    if numerical_stability_addendum:
        replacements.append(
            (
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)",
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)\n"
                "    instructions += (\"\\nFinite-precision arithmetic is observable behavior. \"\n"
                "                     \"When equivalent expressions differ numerically, use an evaluation \"\n"
                "                     \"order or standard-library primitive that avoids cancellation, \"\n"
                "                     \"overflow, underflow, and avoidable rounding while preserving the \"\n"
                "                     \"stated mathematical contract.\")",
            )
        )
    if task_contract_addendum:
        replacements.append(
            (
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)",
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)\n"
                "    instructions += (\"\\nImplement stated algorithms and formulas in their \"\n"
                "                     \"stated operation order. Do not substitute an equivalent-looking \"\n"
                "                     \"shortcut when representation, ordering, padding, or floating-point \"\n"
                "                     \"behavior can differ. Trace supplied tests and examples before returning.\")",
            )
        )
    if static_consistency_addendum:
        replacements.append(
            (
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)",
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)\n"
                "    instructions += (\"\\nBefore returning, perform a static consistency pass \"\n"
                "                     \"across the complete edit: every referenced symbol exists, is \"\n"
                "                     \"visible from its use site, and has compatible types.\")",
            )
        )
    if value_semantics_addendum:
        replacements.append(
            (
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)",
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)\n"
                "    instructions += (\"\\nLanguage-level numeric representations are observable. \"\n"
                "                     \"Preserve signed zero and specified NaN or infinity behavior; \"\n"
                "                     \"do not substitute mathematically equivalent primitive values.\")",
            )
        )
    if zero_canonicalization_addendum:
        replacements.append(
            (
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)",
                "    instructions += prompts.instructions_addendum.format(file_list=file_list)\n"
                "    instructions += (\"\\nCanonicalize mathematical zero to +0 unless tests require -0.\")",
            )
        )
    if candidate_sidecar:
        container_sidecar = (
            Path("/aider") / candidate_sidecar.resolve().relative_to(AIDER_ROOT)
        )
        replacements.extend(
            [
                (
                    """    test_outcomes = []
    for i in range(tries):""",
                    f"""    test_outcomes = []
    selection_candidate_count = 1
    selection_selected_index = 0
    selection_test_runs = 0
    candidate_sidecar = Path({json.dumps(str(container_sidecar))})
    for i in range(tries):""",
                ),
                (
                    """        if errors:
            test_outcomes.append(False)""",
                    """        selection_test_runs += 1
        candidate_payload = (
            json.loads(candidate_sidecar.read_text())
            if candidate_sidecar.exists()
            else {}
        )
        candidates = candidate_payload.get("candidates", [])
        if candidates:
            selection_candidate_count = len(candidates)
        if errors and len(candidates) > 1:
            for candidate_index, candidate in enumerate(candidates[1:], 1):
                for file_path in solution_files:
                    destination = testdir / Path(file_path)
                    language_root = str(testdir).split("/exercises/practice/")[0]
                    original = (
                        original_dname
                        / Path(language_root).name
                        / "exercises"
                        / "practice"
                        / testdir.name
                        / file_path
                    )
                    if original.exists():
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy(original, destination)
                selection_start = time.time()
                coder.partial_response_content = candidate
                coder.apply_updates()
                dur += time.time() - selection_start
                response = candidate
                try:
                    errors = run_unit_tests(
                        original_dname, testdir, history_fname, test_files
                    )
                except subprocess.TimeoutExpired:
                    errors = "Tests timed out!"
                    timeouts += 1
                selection_test_runs += 1
                if not errors:
                    selection_selected_index = candidate_index
                    break
        if errors:
            test_outcomes.append(False)""",
                ),
                (
                    "        reasoning_effort=reasoning_effort,",
                    """        selection_candidate_count=selection_candidate_count,
        selection_selected_index=selection_selected_index,
        selection_test_runs=selection_test_runs,
        reasoning_effort=reasoning_effort,""",
                ),
            ]
        )
    if candidate_repair_on_failure:
        if not candidate_sidecar:
            raise RuntimeError("candidate repair requires a candidate sidecar")
        replacements.extend(
            [
                (
                    "    selection_test_runs = 0\n",
                    "    selection_test_runs = 0\n"
                    "    selection_repair_calls = 0\n"
                    "    selection_repair_candidate_count = 0\n"
                    "    selection_repair_selected_index = None\n"
                    "    selection_repair_test_runs = 0\n",
                ),
                (
                    """        if errors:
            test_outcomes.append(False)""",
                    """        if errors:
            for file_path in solution_files:
                destination = testdir / Path(file_path)
                language_root = str(testdir).split("/exercises/practice/")[0]
                original = (
                    original_dname
                    / Path(language_root).name
                    / "exercises"
                    / "practice"
                    / testdir.name
                    / file_path
                )
                if original.exists():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy(original, destination)
            coder.partial_response_content = candidates[0]
            coder.apply_updates()
            try:
                errors = run_unit_tests(
                    original_dname, testdir, history_fname, test_files
                )
            except subprocess.TimeoutExpired:
                errors = "Tests timed out!"
                timeouts += 1
            selection_test_runs += 1
            repair_base_files = {
                file_path: (testdir / Path(file_path)).read_bytes()
                for file_path in solution_files
                if (testdir / Path(file_path)).exists()
            }
            repair_message = errors + prompts.test_failures.format(
                file_list=file_list
            )
            repair_start = time.time()
            response = coder.run(with_message=repair_message, preproc=False)
            dur += time.time() - repair_start
            selection_repair_calls += 1
            repair_payload = (
                json.loads(candidate_sidecar.read_text())
                if candidate_sidecar.exists()
                else {}
            )
            repair_candidates = repair_payload.get("candidates", [])
            selection_repair_candidate_count = len(repair_candidates)
            try:
                errors = run_unit_tests(
                    original_dname, testdir, history_fname, test_files
                )
            except subprocess.TimeoutExpired:
                errors = "Tests timed out!"
                timeouts += 1
            selection_test_runs += 1
            selection_repair_test_runs += 1
            if not errors:
                selection_repair_selected_index = 0
            elif len(repair_candidates) > 1:
                for repair_index, repair_candidate in enumerate(
                    repair_candidates[1:], 1
                ):
                    for file_path, contents in repair_base_files.items():
                        destination = testdir / Path(file_path)
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        destination.write_bytes(contents)
                    selection_start = time.time()
                    coder.partial_response_content = repair_candidate
                    coder.apply_updates()
                    dur += time.time() - selection_start
                    response = repair_candidate
                    try:
                        errors = run_unit_tests(
                            original_dname, testdir, history_fname, test_files
                        )
                    except subprocess.TimeoutExpired:
                        errors = "Tests timed out!"
                        timeouts += 1
                    selection_test_runs += 1
                    selection_repair_test_runs += 1
                    if not errors:
                        selection_repair_selected_index = repair_index
                        break
        if errors:
            test_outcomes.append(False)""",
                ),
                (
                    "        selection_candidate_count=selection_candidate_count,\n",
                    "        selection_repair_calls=selection_repair_calls,\n"
                    "        selection_repair_candidate_count=selection_repair_candidate_count,\n"
                    "        selection_repair_selected_index=selection_repair_selected_index,\n"
                    "        selection_repair_test_runs=selection_repair_test_runs,\n"
                    "        selection_candidate_count=selection_candidate_count,\n",
                ),
            ]
        )
    if disable_auto_lint:
        replacements.append(
            (
                "        # auto_lint=False,  # disabled for code-in-json experiments",
                "        auto_lint=False,",
            )
        )
    for old, replacement in replacements:
        if text.count(old) != 1:
            raise RuntimeError(f"benchmark overlay source mismatch for {old!r}")
        text = text.replace(old, replacement)
    output = ROOT / ".tmp/aider-eval/generated/benchmark-stack-overlay.py"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text)
    return output


def render_chat_chunks_overlay() -> Path:
    source = AIDER_ROOT / "aider/coders/chat_chunks.py"
    text = source.read_text()
    old = (
        "            + self.readonly_files\n"
        "            + self.repo\n"
        "            + self.done\n"
        "            + self.chat_files\n"
        "            + self.cur\n"
    )
    new = (
        "            + self.repo\n"
        "            + self.done\n"
        "            + self.chat_files\n"
        "            + self.readonly_files\n"
        "            + self.cur\n"
    )
    if text.count(old) != 1:
        raise RuntimeError("chat chunk overlay source mismatch")
    output = ROOT / ".tmp/aider-eval/generated/chat-chunks-tests-near-request.py"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text.replace(old, new))
    return output


def build_command(args: argparse.Namespace, cases: list[str]) -> list[str]:
    proxy_base = args.proxy_url.rstrip("/") + "/v1"
    run_name = args.name or f"{args.profile}-{args.case_set}"
    inner = [
        "python3",
        "benchmark/benchmark.py",
        run_name,
        "--model",
        MODEL_BY_PROFILE[args.profile],
        "--edit-format",
        args.edit_format,
        "--threads",
        "1",
        "--tries",
        str(args.tries),
        "--keywords",
        ",".join(cases),
        "--exercises-dir",
        (
            "numerical-contract-development"
            if args.case_set == "numerical"
            else "polyglot-benchmark"
        ),
        "--read-model-settings",
        "/benchmarks/codex-model-settings.yml",
    ]
    if args.edit_format == "architect":
        inner.extend(
            [
                "--editor-model",
                MODEL_BY_PROFILE[args.profile],
                "--editor-edit-format",
                "whole",
            ]
        )
    command = [
        "docker",
        "run",
        "--rm",
        "--memory=12g",
        "--memory-swap=12g",
        "--add-host=host.docker.internal:host-gateway",
        "-v",
        f"{AIDER_ROOT}:/aider",
        "-v",
        f"{BENCHMARKS}:/benchmarks",
        "-e",
        "AIDER_DOCKER=1",
        "-e",
        "AIDER_BENCHMARK_DIR=/benchmarks",
        "-e",
        "OPENAI_API_KEY=local-eval",
        "-e",
        f"OPENAI_API_BASE={proxy_base.replace('127.0.0.1', 'host.docker.internal')}",
        "aider-benchmark",
        *inner,
    ]
    if (
        args.context_tests
        or args.disable_auto_lint
        or args.disable_summarization
        or args.task_contract_addendum
        or args.authoritative_test_context
        or args.numerical_stability_addendum
        or args.static_consistency_addendum
        or args.value_semantics_addendum
        or args.zero_canonicalization_addendum
        or args.candidate_sidecar
        or args.request_timeout is not None
    ):
        overlay = render_benchmark_overlay(
            args.context_tests,
            args.disable_auto_lint,
            args.disable_summarization,
            args.task_contract_addendum,
            args.authoritative_test_context,
            args.numerical_stability_addendum,
            args.static_consistency_addendum,
            args.value_semantics_addendum,
            args.zero_canonicalization_addendum,
            args.candidate_sidecar,
            args.candidate_repair_on_failure,
            args.request_timeout,
        )
        insert_at = command.index("aider-benchmark")
        command[insert_at:insert_at] = [
            "-v",
            f"{overlay}:/aider/benchmark/benchmark.py:ro",
        ]
    if args.context_tests_near_request:
        overlay = render_chat_chunks_overlay()
        insert_at = command.index("aider-benchmark")
        command[insert_at:insert_at] = [
            "-v",
            f"{overlay}:/aider/aider/coders/chat_chunks.py:ro",
        ]
    return command


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=sorted(MODEL_BY_PROFILE), required=True)
    parser.add_argument(
        "--case-set",
        choices=(
            "smoke",
            "regression",
            "holdout",
            "replacement_holdout",
            "exposed_failure",
            "numerical",
            "all",
        ),
        required=True,
    )
    parser.add_argument("--tries", type=int, default=2)
    parser.add_argument(
        "--edit-format",
        choices=("whole", "diff", "udiff", "architect"),
        default="whole",
    )
    parser.add_argument("--name")
    parser.add_argument("--proxy-url", default="http://127.0.0.1:18080")
    parser.add_argument(
        "--context-tests",
        action="store_true",
        help="Supply configured test files to Aider as read-only first-turn context",
    )
    parser.add_argument(
        "--numerical-stability-addendum",
        action="store_true",
        help="Append the general finite-precision decision rule",
    )
    parser.add_argument(
        "--static-consistency-addendum",
        action="store_true",
        help="Append the cross-file symbol and type consistency check",
    )
    parser.add_argument(
        "--value-semantics-addendum",
        action="store_true",
        help="Append the language-level numeric value semantics check",
    )
    parser.add_argument(
        "--zero-canonicalization-addendum",
        action="store_true",
        help="Append the ordinary-zero canonicalization rule",
    )
    parser.add_argument(
        "--authoritative-test-context",
        action="store_true",
        help="Label read-only tests as authoritative contract evidence",
    )
    parser.add_argument(
        "--task-contract-addendum",
        action="store_true",
        help="Append the general literal-contract check to the task message",
    )
    parser.add_argument(
        "--context-tests-near-request",
        action="store_true",
        help="Place read-only tests immediately before the current task message",
    )
    parser.add_argument(
        "--disable-auto-lint",
        action="store_true",
        help="Run tests directly after each edit without an Aider lint-repair turn",
    )
    parser.add_argument(
        "--disable-summarization",
        action="store_true",
        help="Prevent background chat-summary model calls during bounded runs",
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="Restrict this run to an exact path already present in the selected case set",
    )
    parser.add_argument("--candidate-sidecar", type=Path)
    parser.add_argument(
        "--candidate-repair-on-failure",
        action="store_true",
        help="Use one feedback call after every generated candidate fails locally",
    )
    parser.add_argument(
        "--request-timeout",
        type=float,
        help="Aider API request timeout in seconds for the benchmark process",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.tries < 1:
        parser.error("--tries must be positive")
    if args.request_timeout is not None and args.request_timeout <= 0:
        parser.error("--request-timeout must be positive")
    cases = load_cases(args.case_set)
    if args.case_set == "numerical":
        materialize_numerical_cases()
    if args.case:
        invalid = sorted(set(args.case) - set(cases))
        if invalid:
            parser.error(f"cases are outside {args.case_set}: {invalid}")
        cases = args.case
    verify_prerequisites(args.proxy_url, MODEL_BY_PROFILE[args.profile])
    command = build_command(args, cases)
    if args.dry_run:
        print(json.dumps({"cases": cases, "command": command}, indent=2))
        return
    result = subprocess.run(command, cwd=AIDER_ROOT, env=os.environ.copy(), check=False)
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
