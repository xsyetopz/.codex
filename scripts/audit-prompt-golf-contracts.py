#!/usr/bin/env python3
"""Deterministically audit prompt-golf candidates for explicit contract anchors."""

from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/references/gpt-5.6-prompt-golf-contracts.json"
PATTERNS = {
    "scope_authority": [
        r"(current )?request.{0,20}scope",
        r"prior context|earlier context",
        r"evidence",
        r"permission",
        r"within authority|only within authority",
    ],
    "edit_authority": [
        r"do not edit|without a change request|without editing",
        r"edit.{0,60}validat|make.{0,60}validat",
        r"confirm",
        r"destruct",
        r"external write",
        r"material (scope )?(expansion|expand)",
    ],
    "preservation": [
        r"preserve unrelated",
        r"api",
        r"diagnostic",
        r"exception",
        r"return shape",
        r"whitespace",
        r"punctuation",
    ],
    "evidence": [
        r"inspect exact",
        r"owner|owning",
        r"caller",
        r"test",
        r"incomplete",
        r"official source",
        r"community experience.{0,30}(real-world|evidence)",
    ],
    "anti_echo": [
        r"classif",
        r"contract",
        r"context",
        r"copy(?:ing)? affected.{0,50}exact",
        r"not explicitly requested",
        r"remov|delet",
        r"intended current state",
    ],
    "engineering_loop": [
        r"frame",
        r"trace",
        r"rollback",
        r"speculative cleanup",
        r"idempoten",
        r"negative",
        r"required (type|type/lint)",
        r"report result|lead with the result",
    ],
    "stopping": [
        r"stop",
        r"requested outcome|core request",
        r"optional work|optional detail",
        r"manufacture.{0,10}certainty",
    ],
    "completion": [
        r"visible outcome|user-visible outcome",
        r"preserv(?:e|ed) (?:source )?contracts|preserved contracts|source contracts.{0,40}preserved",
        r"required validation",
        r"material risk",
        r"uncertainty",
        r"(does not prove|not proof|proves nothing)",
    ],
    "goals": [
        r"root.{0,80}(alone )?(changes|change).{0,20}goal status",
        r"every criterion",
        r"explicit",
        r"pause",
        r"blocked-status surrogate",
        r"shared finite budgets",
    ],
    "delegation": [
        r"work alone",
        r"two children",
        r"one hop",
        r"children do not delegate|no child delegation",
        r"exclusive ownership",
        r"root verif",
        r"challenge.{0,80}repeat once",
        r"escalat",
    ],
    "tools_edits": [
        r"smallest relevant tool",
        r"prerequisite",
        r"programmatic",
        r"deterministic",
        r"direct calls",
        r"fallback",
        r"python 3",
        r"read-only roles leave no artifacts",
        r"slash commands",
    ],
    "communication": [
        r"before multi-step tool",
        r"one short",
        r"major (phase )?changes",
        r"final",
        r"lead with evidence|lead with the result",
        r"caveat",
        r"exactly what unlocks|what unlocks progress",
    ],
}


def audit(path: Path) -> dict:
    text = path.read_text().casefold()
    groups = {}
    for group, patterns in PATTERNS.items():
        missing = [p for p in patterns if re.search(p, text, re.DOTALL) is None]
        groups[group] = {"passed": not missing, "missing_patterns": missing}
    return {
        "path": str(path),
        "passed": all(v["passed"] for v in groups.values()),
        "groups": groups,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("paths", nargs="+", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    manifest = json.loads(MANIFEST.read_text())
    expected = {x["id"] for x in manifest["atomic_contracts"]}
    if set(PATTERNS) != expected:
        raise SystemExit(
            f"contract audit mismatch: expected={sorted(expected)} actual={sorted(PATTERNS)}"
        )
    result = {"manifest": str(MANIFEST), "results": [audit(x) for x in a.paths]}
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(result, indent=2) + "\n")
    for item in result["results"]:
        print(f"{item['path']}: {'PASS' if item['passed'] else 'FAIL'}")
        for group, data in item["groups"].items():
            if not data["passed"]:
                print(f"  {group}: {data['missing_patterns']}")
    raise SystemExit(0 if all(x["passed"] for x in result["results"]) else 1)


if __name__ == "__main__":
    main()
