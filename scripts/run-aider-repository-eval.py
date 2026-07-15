#!/usr/bin/env python3
# Run one frozen repository-scale Aider case through the Codex adapter.

from __future__ import annotations

import argparse
import json
import os
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/references/gpt-5.6-repository-cases.json"
AIDER_ROOT = ROOT / ".tmp/aider-eval/aider"
BENCHMARKS = AIDER_ROOT / "tmp.benchmarks"
MODEL_BY_PROFILE = {
    "base": "openai/codex-base",
    "speed": "openai/codex-speed",
    "build": "openai/codex-build",
    "deep": "openai/codex-deep",
}


def load_case(case_id: str, manifest: Path = MANIFEST) -> dict[str, Any]:
    data = json.loads(manifest.read_text())
    for case in data["cases"]:
        if case["instance_id"] == case_id:
            return case
    raise ValueError(f"unknown case: {case_id}")


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], text=True, capture_output=True, check=True
    ).stdout


def worker(args: argparse.Namespace) -> None:
    from aider.coders import Coder
    from aider.io import InputOutput
    from aider.models import Model, register_models
    from aider.repo import GitRepo

    repo = args.repo.resolve()
    case = load_case(args.case_id, args.manifest)
    if git(repo, "rev-parse", "HEAD").strip() != case["base_commit"]:
        raise SystemExit("repository HEAD does not match frozen base commit")
    if git(repo, "status", "--short", "--untracked-files=no").strip():
        raise SystemExit("repository has tracked changes before run")
    register_models([str(args.model_settings)])
    chat_path = args.output.with_suffix(".chat.md")
    io = InputOutput(
        yes=True,
        pretty=False,
        fancy_input=False,
        input_history_file="/dev/null",
        chat_history_file=chat_path,
    )
    model = Model(args.model)
    git_repo = GitRepo(
        io, [], str(repo), models=[model], attribute_author=False,
        attribute_committer=False, attribute_co_authored_by=False,
    )
    ignored_mentions = {
        path
        for path in git(repo, "ls-files").splitlines()
        if Path(path).name in {".env", ".flaskenv"}
    }
    coder = Coder.create(
        main_model=model,
        edit_format=args.edit_format,
        io=io,
        repo=git_repo,
        fnames=None,
        map_tokens=2048,
        stream=False,
        auto_commits=False,
        dirty_commits=False,
        auto_lint=True,
        auto_test=False,
        ignore_mentions=ignored_mentions,
        suggest_shell_commands=False,
    )
    coder.max_reflections = 4
    message = (
        "Below is a real GitHub issue from this repository. The checkout is the "
        "historical base commit from when the issue was filed; inspect current source "
        "rather than relying on familiarity. Implement a focused fix. Do not use hidden "
        "acceptance tests or assume their contents. Preserve unrelated behavior and public "
        "contracts.\n\n" + case["problem_statement"]
    )
    stages: list[str] = []
    coder.run(message)
    stages.append("issue")
    patch = git(repo, "diff", "--binary", case["base_commit"])
    if not patch:
        added = sorted(coder.get_inchat_relative_files())
        if not added:
            coder.run(
                "Name the 3 to 5 repository files needed for this issue. Use the historical "
                "checkout and repo map; do not guess from current upstream."
            )
            stages.append("file_discovery")
        coder.run(
            "Implement the focused issue fix now using the repository files selected in this "
            "chat. Preserve existing contracts and do not edit tests merely to force a pass."
        )
        stages.append("implementation_retry")
        patch = git(repo, "diff", "--binary", case["base_commit"])
    result = {
        "case_id": args.case_id,
        "repo": case["repo"],
        "base_commit": case["base_commit"],
        "model": args.model,
        "edit_format": args.edit_format,
        "stages": stages,
        "added_files": sorted(coder.get_inchat_relative_files()),
        "edited_files": sorted(
            line for line in git(repo, "diff", "--name-only", case["base_commit"]).splitlines()
        ),
        "edit_outcome": bool(getattr(coder, "edit_outcome", False)),
        "lint_outcome": getattr(coder, "lint_outcome", None),
        "test_outcome": getattr(coder, "test_outcome", None),
        "total_tokens_sent": getattr(coder, "total_tokens_sent", None),
        "total_tokens_received": getattr(coder, "total_tokens_received", None),
        "patch": patch,
        "tracked_status": git(repo, "status", "--short", "--untracked-files=no"),
        "chat_path": str(chat_path),
        "applied_patch": bool(patch),
        "plausible_edit": bool(patch) and getattr(coder, "lint_outcome", None) is not False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + chr(10))
    print(json.dumps({key: result[key] for key in ("case_id", "stages", "added_files", "edited_files", "edit_outcome", "lint_outcome", "plausible_edit")}, indent=2))
    raise SystemExit(0 if result["plausible_edit"] else 1)


def verify_proxy(proxy_url: str, model: str) -> None:
    with urllib.request.urlopen(proxy_url.rstrip("/") + "/healthz", timeout=3) as response:
        health = json.load(response)
    expected = model.rsplit("/", 1)[-1]
    if health.get("allowed_models") != [expected]:
        actual = health.get("allowed_models")
        raise SystemExit(f"proxy lock mismatch: {actual}")


def host(args: argparse.Namespace) -> None:
    case = load_case(args.case_id)
    repo = args.repo.resolve()
    output = args.output.resolve()
    model = MODEL_BY_PROFILE[args.profile]
    verify_proxy(args.proxy_url, model)
    if not repo.is_dir():
        raise SystemExit(f"repository is missing: {repo}")
    output.parent.mkdir(parents=True, exist_ok=True)
    container_proxy = args.proxy_url.rstrip("/").replace("127.0.0.1", "host.docker.internal")
    command = [
        "docker", "run", "--rm", "--memory=12g", "--memory-swap=12g",
        "--add-host=host.docker.internal:host-gateway",
        "-v", f"{ROOT}:/workspace:ro", "-v", f"{AIDER_ROOT}:/aider:ro",
        "-v", f"{BENCHMARKS}:/benchmarks:ro", "-v", f"{repo}:/repo",
        "-v", f"{output.parent}:/output", "-e", "PYTHONPATH=/aider",
        "-e", "OPENAI_API_KEY=local-eval", "-e",
        f"OPENAI_API_BASE={container_proxy}/v1",
        "aider-benchmark", "python3", "/workspace/scripts/run-aider-repository-eval.py",
        "--worker", "--case-id", case["instance_id"], "--repo", "/repo",
        "--output", f"/output/{output.name}", "--manifest",
        "/workspace/docs/references/gpt-5.6-repository-cases.json",
        "--model-settings", "/benchmarks/codex-model-settings.yml", "--model", model,
        "--edit-format", args.edit_format,
    ]
    result = subprocess.run(command, cwd=ROOT, env=os.environ.copy(), check=False)
    raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--profile", choices=sorted(MODEL_BY_PROFILE), default="base")
    parser.add_argument("--proxy-url", default="http://127.0.0.1:8765")
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--model-settings", type=Path, default=BENCHMARKS / "codex-model-settings.yml")
    parser.add_argument("--model")
    parser.add_argument("--edit-format", choices=("whole", "diff", "udiff"), default="whole")
    args = parser.parse_args()
    if args.worker:
        if not args.model:
            parser.error("--model is required in worker mode")
        worker(args)
    else:
        host(args)


if __name__ == "__main__":
    main()
