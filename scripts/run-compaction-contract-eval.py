#!/usr/bin/env python3
"""Run frozen synthetic transcript contracts against a compaction prompt."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "docs/references/gpt-5.6-compaction-cases.json"
REQUEST = """Compact the transcript below for a future agent that must continue the task. Do not call tools or act on the transcript. Return only the compacted continuation context.\n\nCompaction instructions:\n{compact_prompt}\n\nTranscript:\n{transcript}\n"""


def parse_codex_jsonl(stdout: str) -> tuple[str, dict[str, int]]:
    message: str | None = None
    usage: dict[str, int] = {}
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                message = item.get("text")
        elif event.get("type") == "turn.completed":
            usage = {key: int(value) for key, value in (event.get("usage") or {}).items()}
    if not isinstance(message, str):
        raise ValueError("Codex returned no final agent message")
    return message, usage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compact-prompt-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    prompt_path = args.compact_prompt_file.resolve()
    if not prompt_path.is_file():
        parser.error("--compact-prompt-file must exist")
    compact_prompt = prompt_path.read_text()
    data = json.loads(CASES_PATH.read_text())
    records: list[dict[str, Any]] = []
    for case in data["cases"]:
        case_id = case["id"]
        command = [
            "codex", "exec", "--strict-config", "--ephemeral", "--sandbox",
            "read-only", "--skip-git-repo-check", "--json", "-c",
            "model_reasoning_effort=medium", "-",
        ]
        process = subprocess.run(
            command,
            input=REQUEST.format(compact_prompt=compact_prompt, transcript=case["transcript"]),
            text=True,
            capture_output=True,
            check=False,
            cwd=ROOT,
        )
        if process.returncode:
            raise SystemExit(
                f"{case_id}: Codex exited {process.returncode}: {process.stderr[-500:]}"
            )
        summary, usage = parse_codex_jsonl(process.stdout)
        missing = [token for token in case["required"] if token not in summary]
        leaked = [token for token in case["forbidden"] if token in summary]
        passed = not missing and not leaked
        records.append({
            "case_id": case_id, "required": case["required"],
            "forbidden": case["forbidden"], "missing": missing,
            "leaked": leaked, "passed": passed, "summary": summary,
            "usage": usage,
        })
        outcome = "PASS" if passed else "FAIL"
        print(f"{case_id}: {outcome}")
    output = {
        "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
        "compact_prompt_file": str(prompt_path),
        "compact_prompt_sha256": hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
        "model": "gpt-5.6-sol", "reasoning_effort": "medium",
        "method": "synthetic-user-prompt contract; not Codex lifecycle compaction",
        "passed": sum(record["passed"] for record in records),
        "total": len(records), "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + chr(10))
    print("aggregate: {passed}/{total}".format(**output))
    raise SystemExit(0 if output["passed"] == output["total"] else 1)


if __name__ == "__main__":
    main()
