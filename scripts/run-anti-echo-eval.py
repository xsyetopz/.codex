#!/usr/bin/env python3
"""Run frozen natural-prose anti-echo promptcraft cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "docs/references/gpt-5.6-anti-echo-cases.json"


def render_instructions(clauses: list[str]) -> str:
    return (
        "# Communication contract\n\n"
        + "\n".join(f"- {clause}" for clause in clauses)
        + "\n\nReturn only the requested user-facing sentence.\n"
    )


def parse_jsonl(stdout: str) -> tuple[str, dict[str, int], list[str], list[str]]:
    message = None
    usage: dict[str, int] = {}
    reasoning_summaries: list[str] = []
    raw_reasoning: list[str] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message":
                message = item.get("text")
            elif item.get("type") == "reasoning":
                text = item.get("text")
                if isinstance(text, str):
                    reasoning_summaries.append(text)
                content = item.get("content")
                if isinstance(content, str):
                    raw_reasoning.append(content)
        elif event.get("type") == "turn.completed":
            usage = {
                key: int(value) for key, value in (event.get("usage") or {}).items()
            }
    if not isinstance(message, str):
        raise ValueError("Codex returned no final agent message")
    return message.strip(), usage, reasoning_summaries, raw_reasoning


def score(case: dict[str, Any], actual: str) -> dict[str, Any]:
    folded = actual.casefold()
    missing = [group for group in case["required"] if not any(term.casefold() in folded for term in group)]
    echoed = [term for term in case["forbidden"] if term.casefold() in folded]
    words = re.findall(r"\b[\w.-]+\b", actual)
    return {
        "passed": not missing and not echoed and len(words) <= case["max_words"],
        "missing_required": missing,
        "echoed_forbidden": echoed,
        "word_count": len(words),
        "max_words": case["max_words"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--variant", choices=["baseline", "positive", "negative", "balanced", "contract_aware", "classify_terms", "strict_context", "explicit_output_only", "filter_pass"]
    )
    group.add_argument("--instructions-file", type=Path)
    parser.add_argument("--model", default="gpt-5.6-sol")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--reasoning-summary", choices=["auto", "concise", "detailed", "none"], default="detailed")
    parser.add_argument("--verbosity", choices=["low", "medium", "high"], default="low")
    parser.add_argument("--show-raw-reasoning", action="store_true")
    parser.add_argument("--case-ids", help="Comma-separated frozen case IDs")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(CASES_PATH.read_text())
    if args.instructions_file:
        instructions_source = args.instructions_file.resolve()
        if not instructions_source.is_file():
            parser.error("--instructions-file must exist")
        rendered = instructions_source.read_text()
        variant_name = "file"
    else:
        rendered = render_instructions(data["variants"][args.variant])
        variant_name = args.variant
    selected_cases = data["cases"]
    if args.case_ids:
        requested = args.case_ids.split(",")
        by_id = {case["id"]: case for case in selected_cases}
        missing_ids = [case_id for case_id in requested if case_id not in by_id]
        if missing_ids:
            parser.error(f"unknown --case-ids: {missing_ids}")
        selected_cases = [by_id[case_id] for case_id in requested]
    records = []
    with tempfile.TemporaryDirectory() as directory:
        instructions_path = Path(directory) / "instructions.md"
        instructions_path.write_text(rendered)
        for case in selected_cases:
            command = [
                "codex",
                "exec",
                "--strict-config",
                "--ephemeral",
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--json",
                "-c",
                f"model={json.dumps(args.model)}",
                "-c",
                f"model_reasoning_effort={json.dumps(args.effort)}",
                "-c",
                f"model_reasoning_summary={json.dumps(args.reasoning_summary)}",
                "-c",
                f"model_verbosity={json.dumps(args.verbosity)}",
                "-c",
                "hide_agent_reasoning=false",
                "-c",
                f"show_raw_agent_reasoning={str(args.show_raw_reasoning).lower()}",
                "-c",
                f"model_instructions_file={json.dumps(str(instructions_path))}",
                "-",
            ]
            started = time.monotonic()
            process = subprocess.run(
                command,
                input=case["prompt"],
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
            actual, usage, reasoning_summaries, raw_reasoning = parse_jsonl(process.stdout)
            result = score(case, actual)
            records.append(
                {
                    "case_id": case["id"],
                    "actual": actual,
                    **result,
                    "usage": usage,
                    "reasoning_summaries": reasoning_summaries,
                    "raw_reasoning": raw_reasoning,
                    "elapsed_seconds": elapsed,
                }
            )
            print(f"{case['id']}: {'PASS' if result['passed'] else 'FAIL'}")
    output = {
        "cases_sha256": hashlib.sha256(CASES_PATH.read_bytes()).hexdigest(),
        "variant": variant_name,
        "model": args.model,
        "effort": args.effort,
        "reasoning_summary": args.reasoning_summary,
        "verbosity": args.verbosity,
        "show_raw_reasoning": args.show_raw_reasoning,
        "rendered_instructions": rendered,
        "rendered_instructions_sha256": hashlib.sha256(
            rendered.encode()
        ).hexdigest(),
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
