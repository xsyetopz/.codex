#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "docs/references/gpt-5.6-representation-cases.json"


def render(k, c):
    x, w, v = c["classes"], c["workflow"], c["invariants"]
    if k == "markdown":
        return (
            "# Output policy\n\nClassify terms before drafting:\n"
            + f"- Contract terms: {x['contract']}.\n- Context terms: {x['context']}.\n\nProcedure:\n"
            + "".join(f"{i}. {s}.\n" for i, s in enumerate(w, 1))
            + "\nInvariants:\n"
            + "".join(f"- {s}.\n" for s in v)
            + f"\nStop condition: {c['stop']}.\nReturn only the requested user-facing sentence.\n"
        )
    if k == "pseudocode":
        return """POLICY
FOR EACH input term:
  IF term is identifier, API name, diagnostic, file path, or requested literal
  THEN class := CONTRACT
  ELSE class := CONTEXT
DRAFT current behavior and evidence in a neutral register
FOR EACH affected CONTRACT term: COPY it exactly
FOR EACH CONTEXT term:
  IF explicitly requested in output THEN KEEP it ELSE DELETE it
IF behavior was removed or renamed THEN describe intended current state only
REPEAT audit exact CONTRACT terms and absent unrequested CONTEXT terms
UNTIL both invariants hold
RETURN the requested user-facing sentence only
"""
    if k == "json":
        return (
            json.dumps(
                {
                    "policy": {
                        "classes": x,
                        "steps": w,
                        "invariants": v,
                        "stop": c["stop"],
                        "output": "requested user-facing sentence only",
                    }
                },
                indent=2,
            )
            + "\n"
        )
    if k == "dsp":
        return """TERM := CONTRACT<identifier|api|diagnostic|path|requested_literal> | CONTEXT<name|slogan|quality_qualifier|emotion|branding|incidental_jargon>
CLASSIFY input.* -> TERM
DRAFT := current_behavior + evidence @ neutral_register
DRAFT += exact(affected CONTRACT)
DRAFT -= CONTEXT where !explicit_output_request
STATE := intended_current_only after remove|rename
AUDIT := exact(affected CONTRACT) & absent(unrequested CONTEXT)
STOP when AUDIT
EMIT requested_user_sentence[1]
"""
    raise ValueError(k)


p = argparse.ArgumentParser()
p.add_argument(
    "--representation", choices=["markdown", "pseudocode", "json", "dsp"], required=True
)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
m = json.loads(M.read_text())
out = render(a.representation, m["semantic_contract"])
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(out)
