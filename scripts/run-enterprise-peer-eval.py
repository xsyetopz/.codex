#!/usr/bin/env python3
"""Run frozen enterprise peer-programming action-selection cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "docs/references/gpt-5.6-enterprise-peer-cases.json"
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["case_id", "decision", "act"],
    "properties": {
        "case_id": {"type": "string"},
        "decision": {
            "type": "string",
            "enum": [
                "proceed_direct",
                "inspect_contract",
                "require_migration_plan",
                "verify_authorization",
                "verify_concurrency",
                "require_operational_evidence",
                "strengthen_test",
                "escalate_risk",
            ],
        },
        "act": {"type": "boolean"},
    },
}
PROMPT = """Classify the next peer-programming action using only the supplied scenario.
Do not call tools, modify state, or perform the described change.
Choose the most specific decision. Set act true only when the implementation can proceed directly now.
Return only the schema-matching JSON object.

Scenario ID: {case_id}
Scenario:
{scenario}
"""


def parse_jsonl(stdout: str) -> tuple[dict[str, Any], dict[str, int]]:
    message = None
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
            usage = {
                key: int(value) for key, value in (event.get("usage") or {}).items()
            }
    if not isinstance(message, str):
        raise ValueError("Codex returned no final agent message")
    actual = json.loads(message)
    if not isinstance(actual, dict):
        raise ValueError("Codex final message is not an object")
    return actual, usage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instructions-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="medium")
    args = parser.parse_args()
    instructions = args.instructions_file.resolve()
    if not instructions.is_file():
        parser.error("--instructions-file must exist")
    data = json.loads(CASES_PATH.read_text())
    records = []
    with tempfile.TemporaryDirectory() as directory:
        schema_path = Path(directory) / "schema.json"
        schema_path.write_text(json.dumps(SCHEMA))
        for case in data["cases"]:
            command = [
                "codex",
                "exec",
                "--strict-config",
                "--ephemeral",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--output-schema",
                str(schema_path),
                "--json",
                "-c",
                f"model={json.dumps(args.model)}",
                "-c",
                f"model_reasoning_effort={json.dumps(args.effort)}",
                "-c",
                f"model_instructions_file={json.dumps(str(instructions))}",
                "-",
            ]
            started = time.monotonic()
            process = subprocess.run(
                command,
                input=PROMPT.format(
                    case_id=case["id"], scenario=case["scenario"]
                ),
                text=True,
                capture_output=True,
                check=False,
                cwd=ROOT,
            )
            elapsed = round(time.monotonic() - started, 3)
            if process.returncode:
                raise SystemExit(
                    f"{case['id']}: Codex exited {process.returncode}: "
                    f"{process.stderr[-500:]}"
                )
            actual, usage = parse_jsonl(process.stdout)
            expected = {"case_id": case["id"], **case["expected"]}
            passed = actual == expected
            records.append(
                {
                    "case_id": case["id"],
                    "expected": expected,
                    "actual": actual,
                    "passed": passed,
                    "usage": usage,
                    "elapsed_seconds": elapsed,
                }
            )
            print(f"{case['id']}: {'PASS' if passed else 'FAIL'}")
    output = {
        "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
        "instructions_file": str(instructions),
        "instructions_sha256": hashlib.sha256(instructions.read_bytes()).hexdigest(),
        "model": args.model,
        "effort": args.effort,
        "passed": sum(record["passed"] for record in records),
        "total": len(records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(f"aggregate: {output['passed']}/{output['total']}")
    raise SystemExit(0 if output["passed"] == output["total"] else 1)


if __name__ == "__main__":
    main()
