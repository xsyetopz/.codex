#!/usr/bin/env python3
"""Run frozen wording, structure, and effort promptcraft comparisons."""

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
CASES_PATH = ROOT / "docs/references/gpt-5.6-promptcraft-cases.json"
DECISIONS = [
    "answer_only",
    "ask_confirmation",
    "verify_first",
    "repair_context",
    "preserve_contract",
    "stop_supported",
]
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["case_id", "decision", "act", "complete", "literal"],
    "properties": {
        "case_id": {"type": "string"},
        "decision": {"type": "string", "enum": DECISIONS},
        "act": {"type": "boolean"},
        "complete": {"type": "boolean"},
        "literal": {"type": "string"},
    },
}
DECISION_SEMANTICS = [
    "answer_only: answer or compare without changing state",
    "ask_confirmation: request confirmation before destructive action",
    "verify_first: obtain direct evidence before integration or completion",
    "repair_context: fix a missing environmental prerequisite rather than increasing effort",
    "preserve_contract: implement while preserving the exact stated contract",
    "stop_supported: stop when implementation and all required validation are complete",
]


def render_instructions(clauses: list[str], structure: str) -> str:
    semantics = DECISION_SEMANTICS
    if structure == "markdown":
        return ("# Classification contract\n\n## Rules\n\n" +
                "\n".join(f"- {clause}" for clause in clauses) +
                "\n\n## Decisions\n\n" +
                "\n".join(f"- `{item.split(chr(58), 1)[0]}`:{item.split(chr(58), 1)[1]}" for item in semantics) + "\n")
    rules = "\n".join(f"  <rule>{clause}</rule>" for clause in clauses)
    decisions = "\n".join(
        f"  <decision id=\"{item.split(chr(58), 1)[0]}\">{item.split(chr(58), 1)[1].strip()}</decision>"
        for item in semantics
    )
    xml = f"<classification_contract>\n<rules>\n{rules}\n</rules>\n<decisions>\n{decisions}\n</decisions>\n</classification_contract>\n"
    if structure == "xml":
        return xml
    return "# Classification contract\n\nUse the following exact contract.\n\n" + xml


def render_prompt(case: dict[str, Any], structure: str) -> str:
    if structure == "markdown":
        return "## Scenario `{}`\n\n{}\n\nRequired literal: `{}`\n".format(case["id"], case["scenario"], case["expected"]["literal"])
    xml = ("<scenario id=\"{}\">".format(case["id"]) +
           case["scenario"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") +
           "<required_literal>" + case["expected"]["literal"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") +
           "</required_literal></scenario>\n")
    return xml if structure == "xml" else "## Scenario\n\n" + xml


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
            usage = {key: int(value) for key, value in (event.get("usage") or {}).items()}
    if not isinstance(message, str):
        raise ValueError("Codex returned no final agent message")
    actual = json.loads(message)
    if not isinstance(actual, dict):
        raise ValueError("Codex final message is not an object")
    return actual, usage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wording", choices=["positive", "negative", "balanced"], required=True)
    parser.add_argument("--structure", choices=["markdown", "xml", "mdx_xml"], default="markdown")
    parser.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max", "ultra"], default="medium")
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(CASES_PATH.read_text())
    clauses = data["wording_variants"][args.wording]
    rendered = render_instructions(clauses, args.structure)
    records = []
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        instructions_path = temp / "instructions.md"
        schema_path = temp / "schema.json"
        instructions_path.write_text(rendered)
        schema_path.write_text(json.dumps(SCHEMA))
        for case in data["cases"]:
            command = [
                "codex", "exec", "--strict-config", "--ephemeral",
                "--sandbox", "read-only", "--skip-git-repo-check",
                "--output-schema", str(schema_path), "--json",
                "-c", f"model={json.dumps(args.model)}",
                "-c", f"model_reasoning_effort={json.dumps(args.effort)}",
                "-c", f"model_instructions_file={json.dumps(str(instructions_path))}", "-",
            ]
            started = time.monotonic()
            process = subprocess.run(command, input=render_prompt(case, args.structure), text=True,
                                     capture_output=True, check=False, cwd=ROOT)
            elapsed = round(time.monotonic() - started, 3)
            if process.returncode:
                raise SystemExit("{}: Codex exited {}: {}".format(case["id"], process.returncode, process.stderr[-500:]))
            actual, usage = parse_jsonl(process.stdout)
            expected = {"case_id": case["id"], **case["expected"]}
            passed = actual == expected
            records.append({"case_id": case["id"], "expected": expected, "actual": actual,
                            "passed": passed, "usage": usage, "elapsed_seconds": elapsed})
            print("{}: {}".format(case["id"], "PASS" if passed else "FAIL"))
    output = {
        "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
        "wording": args.wording, "structure": args.structure, "effort": args.effort,
        "model": args.model, "rendered_instructions": rendered,
        "rendered_instructions_sha256": hashlib.sha256(rendered.encode()).hexdigest(),
        "passed": sum(record["passed"] for record in records), "total": len(records),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n")
    print("aggregate: {}/{}".format(output["passed"], output["total"]))
    raise SystemExit(0 if output["passed"] == output["total"] else 1)


if __name__ == "__main__":
    main()
