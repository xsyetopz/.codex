#!/usr/bin/env python3
"""Run one frozen Aider stack candidate through a lane-locked local proxy."""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/references/gpt-5.6-full-stack-candidates.json"
PROXY = ROOT / "scripts/aider-codex-proxy.py"
RUNNER = ROOT / "scripts/run-aider-profile-eval.py"
KEY = "local-eval"


def wait_health(
    url: str, expected: str, instance_id: str, timeout: float = 10.0
) -> None:
    deadline = time.monotonic() + timeout
    last: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url + "/healthz", timeout=1) as response:
                data = json.load(response)
            if data.get("instance_id") != instance_id:
                raise ValueError(f"proxy instance mismatch: {data}")
            if data.get("allowed_models") != [expected]:
                raise ValueError(f"lane mismatch: {data}")
            return
        except Exception as exc:
            last = exc
            time.sleep(0.1)
    raise RuntimeError(f"proxy health timeout: {last}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--candidate", help="Defaults to the manifest adopted_candidate")
    p.add_argument("--profile", choices=["base", "build", "speed"], required=True)
    p.add_argument(
        "--case-set",
        choices=[
            "smoke",
            "regression",
            "holdout",
            "replacement_holdout",
            "exposed_failure",
            "numerical",
            "all",
        ],
        required=True,
    )
    p.add_argument("--tries", type=int, required=True)
    p.add_argument("--port", type=int, default=18080)
    p.add_argument("--name")
    p.add_argument(
        "--case",
        action="append",
        default=[],
        help="Restrict the run to exact paths in the selected case set",
    )
    a = p.parse_args()
    data = json.loads(MANIFEST.read_text())
    candidate_name = a.candidate or data.get("adopted_candidate")
    if candidate_name not in data["candidates"]:
        p.error("unknown candidate and no valid adopted_candidate")
    c = data["candidates"][candidate_name]
    instructions_path = ROOT / data["base_instructions"]["path"]
    actual_instructions_hash = hashlib.sha256(
        instructions_path.read_bytes()
    ).hexdigest()
    expected_instructions_hash = data["base_instructions"]["sha256"]
    if actual_instructions_hash != expected_instructions_hash:
        p.error(
            "base instruction drift: "
            f"expected {expected_instructions_hash}, got {actual_instructions_hash}"
        )
    alias = data["profiles"][a.profile]["alias"]
    workdir = Path(c["workdir"])
    if not workdir.is_absolute():
        workdir = ROOT / workdir
    workdir.mkdir(parents=True, exist_ok=True)
    out = ROOT / ".tmp/aider-eval/full-stack"
    out.mkdir(parents=True, exist_ok=True)
    stem = a.name or f"{candidate_name}-{a.profile}-{a.case_set}"
    log = out / f"{stem}-proxy.jsonl"
    candidate_sidecar = (
        ROOT / ".tmp/aider-eval/aider/tmp.candidate-sidecars" / f"{stem}.json"
    )
    if candidate_sidecar.exists():
        candidate_sidecar.unlink()
    candidate_archive = candidate_sidecar.with_suffix(
        candidate_sidecar.suffix + ".jsonl"
    )
    if candidate_archive.exists():
        candidate_archive.unlink()
    instance_id = uuid.uuid4().hex
    command = [
        sys.executable,
        str(PROXY),
        "--host",
        "127.0.0.1",
        "--port",
        str(a.port),
        "--workdir",
        str(workdir),
        "--log",
        str(log),
        "--concurrency",
        "1",
        "--instructions-file",
        str(instructions_path.resolve()),
        "--adapter-structure",
        c["adapter_structure"],
        "--allow-model",
        alias,
        "--api-key",
        KEY,
        "--instance-id",
        instance_id,
    ]
    if c["omit_permissions"]:
        command.append("--omit-permissions")
    if c["omit_skills"]:
        command.append("--omit-skills")
    reasoning_effort = c.get("reasoning_effort")
    if reasoning_effort:
        command.extend(["--reasoning-effort", reasoning_effort])
    model_verbosity = c.get("model_verbosity")
    if model_verbosity:
        command.extend(["--model-verbosity", model_verbosity])
    response_protocol = c.get("response_protocol", "plain")
    if response_protocol != "plain":
        command.extend(["--response-protocol", response_protocol])
    if response_protocol.startswith("candidate_set_"):
        command.extend(["--candidate-sidecar", str(candidate_sidecar)])
    context_tests = c.get("context_tests", False)
    context_tests_near_request = c.get("context_tests_near_request", False)
    task_contract_addendum = c.get("task_contract_addendum", False)
    authoritative_test_context = c.get("authoritative_test_context", False)
    numerical_stability_addendum = c.get("numerical_stability_addendum", False)
    static_consistency_addendum = c.get("static_consistency_addendum", False)
    value_semantics_addendum = c.get("value_semantics_addendum", False)
    zero_canonicalization_addendum = c.get("zero_canonicalization_addendum", False)
    disable_auto_lint = c.get("disable_auto_lint", False)
    disable_summarization = c.get("disable_summarization", False)
    proxy = subprocess.Popen(
        command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    url = f"http://127.0.0.1:{a.port}"
    try:
        wait_health(url, alias, instance_id)
        run = [
            sys.executable,
            str(RUNNER),
            "--profile",
            a.profile,
            "--case-set",
            a.case_set,
            "--tries",
            str(a.tries),
            "--edit-format",
            c.get("edit_format", "whole"),
            "--name",
            stem,
            "--proxy-url",
            url,
        ]
        if response_protocol.startswith("candidate_set_"):
            run.extend(["--candidate-sidecar", str(candidate_sidecar)])
        if c.get("candidate_repair_on_failure", False):
            run.append("--candidate-repair-on-failure")
        if context_tests:
            run.append("--context-tests")
        if context_tests_near_request:
            run.append("--context-tests-near-request")
        if task_contract_addendum:
            run.append("--task-contract-addendum")
        if authoritative_test_context:
            run.append("--authoritative-test-context")
        if numerical_stability_addendum:
            run.append("--numerical-stability-addendum")
        if static_consistency_addendum:
            run.append("--static-consistency-addendum")
        if value_semantics_addendum:
            run.append("--value-semantics-addendum")
        if zero_canonicalization_addendum:
            run.append("--zero-canonicalization-addendum")
        if disable_auto_lint:
            run.append("--disable-auto-lint")
        if disable_summarization:
            run.append("--disable-summarization")
        request_timeout = c.get("request_timeout")
        if request_timeout is not None:
            run.extend(["--request-timeout", str(request_timeout)])
        for case in a.case:
            run.extend(["--case", case])
        result = subprocess.run(run, cwd=ROOT, env=os.environ.copy(), check=False)
        raise SystemExit(result.returncode)
    finally:
        proxy.terminate()
        try:
            proxy.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proxy.kill()
            proxy.wait()
        stderr = proxy.stderr.read() if proxy.stderr else ""
        if proxy.returncode not in (0, -15) and stderr:
            print(stderr[-1000:], file=sys.stderr)


if __name__ == "__main__":
    main()
