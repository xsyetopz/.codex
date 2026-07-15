#!/usr/bin/env python3
"""OpenAI-compatible chat adapter that routes Aider benchmark turns through Codex profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

PROFILE_BY_MODEL = {
    "codex-base": None,
    "codex-speed": "speed",
    "codex-build": "build",
    "codex-deep": "deep",
}
MAX_BODY_BYTES = 8 * 1024 * 1024
REVIEW_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs/references/aider-reviewed-response.schema.json"
)
CANDIDATE_SET_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs/references/aider-candidate-set-response.schema.json"
)
CANDIDATE_SET_4_SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs/references/aider-candidate-set-4-response.schema.json"
)
ADAPTER_PREFIXES = {
    "legacy": """Produce one assistant response for this Aider code-edit turn.

Return only the content Aider should apply. Follow the requested edit format exactly. Do not add a wrapper or preliminary commentary. Do not call tools; all task context is in the messages below.

Messages (JSON):
""",
    "legacy_preflight": """Produce one assistant response for this Aider code-edit turn.

Return only the content Aider should apply. Follow the requested edit format exactly. Do not add a wrapper or preliminary commentary. Do not call tools; all task context is in the messages below.

Before returning, check the proposed implementation against every supplied test and exact observable contract. Resolve each mismatch without changing the tests.

Messages (JSON):
""",
    "legacy_trace": """Produce one assistant response for this Aider code-edit turn.

Return only the content Aider should apply. Follow the requested edit format exactly. Do not add a wrapper or preliminary commentary. Do not call tools; all task context is in the messages below.

Stop rule: Trace the proposed implementation against every supplied test and stated example. Return only after each expected value, operation order, boundary, and output byte matches. Do not change tests or substitute an equivalent-looking contract.

Messages (JSON):
""",
    "legacy_literal": """Produce one assistant response for this Aider code-edit turn.

Return only the content Aider should apply. Follow the requested edit format exactly. Do not add a wrapper or preliminary commentary. Do not call tools; all task context is in the messages below.

Implement stated algorithms literally: preserve operation order, representation, ordering, and padding instead of substituting equivalent-looking behavior. Before returning, trace supplied tests and examples against the edit.

Messages (JSON):
""",
    "legacy_reviewed_xml": """Produce one assistant response for this Aider code-edit turn.

Use only the supplied messages and do not call tools. Before finalizing, review the proposed edit against every supplied contract, test, example, boundary, and exact observable value. Correct every mismatch found.

Return exactly two XML elements and no text outside them:
<review>A concise verification record; no source code.</review>
<final>The complete content Aider should apply, in the requested edit format, with no wrapper or commentary.</final>

Messages (JSON):
""",
    "legacy_reviewed_cdata": """Produce one assistant response for this Aider code-edit turn.

Use only the supplied messages and do not call tools. Before finalizing, review the proposed edit against every supplied contract, test, example, boundary, and exact observable value. Correct every mismatch found.

Return exactly two XML elements and no text outside them. Put the complete source payload inside CDATA so code characters remain literal:
<review>A concise verification record; no source code.</review>
<final><![CDATA[The complete content Aider should apply, in the requested edit format, with no wrapper or commentary.]]></final>

Messages (JSON):
""",
    "openai_minimal": """Goal: Return one assistant response for Aider to apply.

Constraints: Use only the supplied messages. Do not call tools.

Output: Follow the requested edit format exactly. Return no wrapper or preliminary commentary.

Messages (JSON):
""",
    "openai": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, and return shapes unless the request changes them.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, check requested behavior, boundaries, observable contracts, and consistency across all supplied files.

Messages (JSON):
""",
    "openai_verify": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_compile": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_structured": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Return one object matching the supplied schema. verification records the checked contracts and concrete evidence. final contains only the complete requested Aider edit format, with no wrapper or commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_candidate_set": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Return one object matching the supplied schema. candidates contains exactly two independently derived, complete edits in the requested Aider format. Each candidate must satisfy all success criteria without wrappers or commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_candidate_set_4": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Return one object matching the supplied schema. candidates contains exactly four independently derived, complete edits in the requested Aider format. Each candidate must satisfy all success criteria without wrappers or commentary. Use materially different control flow, state representation, and helper structure; independently derive exact ordering and boundaries for each candidate.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_candidate_set_4_independent": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.
- Do not copy derived constants, indices, ordering logic, boundaries, or layout widths between candidates.

Tools: None.

Output: Return one object matching the supplied schema. candidates contains exactly four complete edits in the requested Aider format, ordered by independent derivation method:
1. Derive directly from every literal contract and expected example.
2. Simulate each supplied test from input through observable output.
3. Derive invariants, state transitions, boundaries, and serialization grammar before implementing.
4. Build a minimal independent implementation with separately derived constants and helpers.
Use materially different control flow, state representation, and helper structure. For textual output, each method must independently account for every character position, payload width, delimiter, and line boundary.

Stop rules: Before returning, reconcile each expected result with each complete edit. If two candidates use the same derived constant or layout rule, re-derive one rather than copying it.

Messages (JSON):
""",
    "openai_verify_candidate_set_4_primary_independent": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.
- Candidates 2-4 independently derive constants, indices, ordering, boundaries, and layout; they do not copy those decisions from another candidate.

Tools: None.

Output: Return one object matching the supplied schema. candidates contains exactly four complete edits in the requested Aider format, ordered as follows:
1. Produce the strongest complete implementation after tracing every supplied test.
2. Independently simulate each supplied test from input through observable output, then implement.
3. Independently derive invariants, state transitions, boundaries, and serialization grammar, then implement.
4. Build a minimal independent implementation with separately derived constants and helpers.
Use materially different control flow, state representation, and helper structure. For textual output, each method independently accounts for every character position, payload width, delimiter, and line boundary.

Stop rules: Before returning, reconcile every supplied test's expected result with each complete edit. Re-derive any shared boundary or layout decision rather than copying it.

Messages (JSON):
""",
    "openai_verify_compile_sequence": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- The complete edit compiles and type-checks; every inferred declaration is resolvable at its definition.
- Derive indices and boundaries from semantic elements, excluding inserted presentation characters.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_value_verify": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- Match every supplied equality assertion under the language's actual primitive-value semantics, including signed zero, NaN, and infinity.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions, ordering, and representation-level primitive values through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_value_canonical": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- Match every supplied equality assertion under the language's actual primitive-value semantics.
- When a mathematical result is zero and the contract expects ordinary zero, return +0; retain -0 only when required. Preserve specified NaN and infinity behavior.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions, ordering, and representation-level primitive values through every supplied test; reconcile each expected result with the complete edit.

Messages (JSON):
""",
    "openai_verify_zero_stop": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, return shapes, and ordering unless the request changes them.
- Satisfy every supplied test without changing tests.
- Return a complete, applicable edit with no placeholders.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, trace state transitions and ordering through every supplied test; reconcile each expected result with the complete edit. Canonicalize mathematical zero to +0 unless tests require -0.

Messages (JSON):
""",
    "openai_repair": """Role: Software engineer producing one Aider code-edit response.

Personality: Direct and precise; no conversational preface.

Goal: Complete the requested code change from the supplied messages.

Success criteria:
- Implement every requested behavior, including stated boundary and failure cases.
- Preserve exact public APIs, diagnostics, exception types, and return shapes unless the request changes them.
- Return a complete, applicable edit with no placeholders.
- When messages contain test, lint, compiler, or error feedback, treat every reported expected type, value, diagnostic, and return shape as an exact contract; correct every reported mismatch.

Constraints:
- Use only the supplied messages; do not call tools.
- Do not invent observable contracts. When a contract is unspecified, preserve the existing public surface.

Tools: None.

Output: Follow the requested edit format exactly. Return only content Aider should apply, with no wrapper or preliminary commentary.

Stop rules: Before returning, check requested behavior, boundaries, observable contracts, supplied feedback, and consistency across all supplied files. Do not return while a reported mismatch remains unaddressed.

Messages (JSON):
""",
}


def normalize_model(raw: str) -> str:
    return raw.rsplit("/", 1)[-1]


def profile_for_model(raw: str) -> str | None:
    name = normalize_model(raw)
    if name not in PROFILE_BY_MODEL:
        choices = ", ".join(sorted(PROFILE_BY_MODEL))
        raise ValueError(f"unsupported model {raw!r}; expected one of: {choices}")
    return PROFILE_BY_MODEL[name]


def render_prompt(
    messages: list[dict[str, Any]], adapter_structure: str = "legacy"
) -> str:
    if not isinstance(messages, list) or not messages:
        raise ValueError("messages must be a non-empty array")
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            raise ValueError(f"messages[{index}] must be an object")
        if message.get("role") not in {
            "system",
            "developer",
            "user",
            "assistant",
            "tool",
        }:
            raise ValueError(f"messages[{index}].role is invalid")
        if "content" not in message:
            raise ValueError(f"messages[{index}].content is required")
    try:
        prefix = ADAPTER_PREFIXES[adapter_structure]
    except KeyError as exc:
        raise ValueError(f"unknown adapter structure: {adapter_structure}") from exc
    return prefix + json.dumps(messages, ensure_ascii=False, separators=(",", ":"))


def extract_response(content: str, protocol: str) -> tuple[str, str | None]:
    if protocol == "plain":
        return content, None
    if protocol in {"candidate_set_json_schema", "candidate_set_4_json_schema"}:
        payload = json.loads(content)
        candidates = payload.get("candidates") if isinstance(payload, dict) else None
        expected_count = 4 if protocol == "candidate_set_4_json_schema" else 2
        if (
            not isinstance(candidates, list)
            or len(candidates) != expected_count
            or any(not isinstance(candidate, str) or not candidate.strip() for candidate in candidates)
        ):
            raise ValueError("invalid candidate_set_json_schema response")
        return candidates[0], json.dumps(candidates, ensure_ascii=False)
    if protocol == "reviewed_json_schema":
        payload = json.loads(content)
        if not isinstance(payload, dict) or not isinstance(payload.get("final"), str):
            raise ValueError("invalid reviewed_json_schema response")
        verification = payload.get("verification")
        if not isinstance(verification, list) or not verification:
            raise ValueError("invalid reviewed_json_schema verification")
        final = payload["final"]
        if not final.strip():
            raise ValueError("empty reviewed_json_schema final")
        return final, json.dumps(verification, ensure_ascii=False, sort_keys=True)
    if protocol != "reviewed_xml":
        raise ValueError(f"unknown response protocol: {protocol}")
    match = re.fullmatch(
        r"<review>(.+?)</review>\s*<final>\n?(.*?)\n?</final>\s*",
        content,
        re.DOTALL,
    )
    if not match or not match.group(2).strip():
        raise ValueError("invalid reviewed_xml response envelope")
    final = match.group(2)
    cdata = re.fullmatch(r"<!\[CDATA\[(.*)\]\]>", final, re.DOTALL)
    if cdata:
        final = cdata.group(1)
    return final, match.group(1).strip()


def disabled_skills_override() -> str:
    roots = [Path.home() / ".agents/skills", Path.home() / ".codex/skills/.system"]
    paths = sorted(
        {
            str(path.resolve())
            for root in roots
            if root.is_dir()
            for path in root.glob("*/SKILL.md")
        }
    )
    return (
        "["
        + ",".join("{path=" + json.dumps(path) + ",enabled=false}" for path in paths)
        + "]"
    )


def parse_codex_jsonl(
    stdout: str,
) -> tuple[str, dict[str, int], dict[str, int]]:
    messages: list[str] = []
    usage: dict[str, int] = {}
    diagnostics = {"reasoning_summary_events": 0, "raw_reasoning_events": 0}
    for number, line in enumerate(stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid Codex JSONL at line {number}: {exc}") from exc
        if event.get("type") == "item.completed":
            item = event.get("item") or {}
            if item.get("type") == "agent_message" and isinstance(
                item.get("text"), str
            ):
                messages.append(item["text"])
            elif item.get("type") == "reasoning":
                if isinstance(item.get("text"), str):
                    diagnostics["reasoning_summary_events"] += 1
                if isinstance(item.get("content"), str):
                    diagnostics["raw_reasoning_events"] += 1
        elif event.get("type") == "turn.completed":
            raw_usage = event.get("usage") or {}
            usage = {
                key: int(raw_usage.get(key, 0))
                for key in (
                    "input_tokens",
                    "cached_input_tokens",
                    "output_tokens",
                    "reasoning_output_tokens",
                )
            }
    if not messages:
        raise ValueError("Codex returned no agent_message")
    return messages[-1], usage, diagnostics


def build_codex_command(
    codex: str,
    profile: str | None,
    cwd: Path,
    instructions_file: Path | None,
    omit_permissions: bool = False,
    omit_skills: bool = False,
    reasoning_effort: str | None = None,
    model_verbosity: str | None = None,
    output_schema_path: Path | None = None,
) -> list[str]:
    command = [
        codex,
        "exec",
        "--strict-config",
        "--ephemeral",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--json",
        "-C",
        str(cwd),
    ]
    if profile:
        command.extend(["--profile", profile])
    if omit_permissions:
        command.extend(["-c", "include_permissions_instructions=false"])
    if omit_skills:
        command.extend(["-c", f"skills.config={disabled_skills_override()}"])
    if reasoning_effort:
        command.extend(["-c", f"model_reasoning_effort={reasoning_effort}"])
    if model_verbosity:
        command.extend(["-c", f"model_verbosity={json.dumps(model_verbosity)}"])
    if output_schema_path:
        command.extend(["--output-schema", str(output_schema_path)])
    if instructions_file:
        value = json.dumps(str(instructions_file))
        command.extend(["-c", f"model_instructions_file={value}"])
    command.append("-")
    return command


class Proxy:
    def __init__(
        self,
        codex: str,
        workdir: Path,
        log_path: Path | None,
        concurrency: int,
        instructions_file: Path | None,
        api_key: str,
        allowed_models: set[str],
        adapter_structure: str,
        omit_permissions: bool,
        omit_skills: bool,
        reasoning_effort: str | None,
        model_verbosity: str | None,
        response_protocol: str,
        candidate_sidecar: Path | None,
        instance_id: str,
    ):
        self.codex = codex
        self.workdir = workdir
        self.log_path = log_path
        self.slots = threading.BoundedSemaphore(concurrency)
        self.log_lock = threading.Lock()
        self.instructions_file = instructions_file
        self.api_key = api_key
        self.allowed_models = allowed_models
        self.adapter_structure = adapter_structure
        self.omit_permissions = omit_permissions
        self.omit_skills = omit_skills
        self.reasoning_effort = reasoning_effort
        self.model_verbosity = model_verbosity
        self.response_protocol = response_protocol
        self.output_schema_path = (
            REVIEW_SCHEMA_PATH
            if response_protocol == "reviewed_json_schema"
            else CANDIDATE_SET_SCHEMA_PATH
            if response_protocol == "candidate_set_json_schema"
            else CANDIDATE_SET_4_SCHEMA_PATH
            if response_protocol == "candidate_set_4_json_schema"
            else None
        )
        if self.output_schema_path and not self.output_schema_path.is_file():
            raise ValueError(f"missing output schema: {self.output_schema_path}")
        self.candidate_sidecar = candidate_sidecar
        self.instance_id = instance_id

    def complete(self, payload: dict[str, Any]) -> dict[str, Any]:
        model = str(payload.get("model", ""))
        normalized_model = normalize_model(model)
        request_id = f"chatcmpl-{uuid.uuid4().hex}"
        messages_sha256 = hashlib.sha256(
            json.dumps(
                payload.get("messages"), ensure_ascii=False, sort_keys=True
            ).encode()
        ).hexdigest()
        if normalized_model not in self.allowed_models:
            choices = ", ".join(sorted(self.allowed_models))
            reason = (
                f"model {model!r} is outside this run lane; expected one of: {choices}"
            )
            self.write_log(
                {
                    "timestamp": int(time.time()),
                    "request_id": request_id,
                    "model": normalized_model,
                    "messages_sha256": messages_sha256,
                    "rejected": True,
                    "rejection_reason": reason,
                    "allowed_models": sorted(self.allowed_models),
                }
            )
            raise ValueError(reason)
        profile = profile_for_model(model)
        prompt = render_prompt(payload.get("messages"), self.adapter_structure)
        if self.candidate_sidecar and self.candidate_sidecar.exists():
            self.candidate_sidecar.unlink()
        started = time.monotonic()
        with self.slots:
            result = subprocess.run(
                build_codex_command(
                    self.codex,
                    profile,
                    self.workdir,
                    self.instructions_file,
                    self.omit_permissions,
                    self.omit_skills,
                    self.reasoning_effort,
                    self.model_verbosity,
                    self.output_schema_path,
                ),
                input=prompt,
                text=True,
                capture_output=True,
                check=False,
            )
        elapsed = time.monotonic() - started
        record: dict[str, Any] = {
            "timestamp": int(time.time()),
            "request_id": request_id,
            "model": normalize_model(model),
            "profile": profile or "base",
            "messages_sha256": messages_sha256,
            "elapsed_seconds": round(elapsed, 3),
            "returncode": result.returncode,
            "adapter_structure": self.adapter_structure,
            "omit_permissions": self.omit_permissions,
            "omit_skills": self.omit_skills,
            "workdir": str(self.workdir),
            "model_verbosity": self.model_verbosity,
            "output_schema_sha256": (
                hashlib.sha256(self.output_schema_path.read_bytes()).hexdigest()
                if self.output_schema_path
                else None
            ),
            "instructions_sha256": (
                hashlib.sha256(self.instructions_file.read_bytes()).hexdigest()
                if self.instructions_file
                else None
            ),
        }
        if result.returncode:
            record["stderr_tail"] = result.stderr[-1000:]
            self.write_log(record)
            raise RuntimeError(
                f"Codex exited {result.returncode}: {result.stderr[-500:].strip()}"
            )
        content, usage, diagnostics = parse_codex_jsonl(result.stdout)
        raw_content = content
        record["usage"] = usage
        record["diagnostics"] = diagnostics
        record["response_protocol"] = self.response_protocol
        try:
            content, review = extract_response(content, self.response_protocol)
        except ValueError as exc:
            record["protocol_error"] = str(exc)
            self.write_log(record)
            raise
        if self.response_protocol in {
            "candidate_set_json_schema", "candidate_set_4_json_schema"
        }:
            candidates = json.loads(raw_content)["candidates"]
            if self.candidate_sidecar is None:
                raise ValueError("candidate set protocol requires --candidate-sidecar")
            self.candidate_sidecar.parent.mkdir(parents=True, exist_ok=True)
            candidate_payload = {
                "request_id": request_id,
                "messages_sha256": messages_sha256,
                "candidates": candidates,
            }
            serialized_candidates = (
                json.dumps(candidate_payload, ensure_ascii=False) + "\n"
            )
            self.candidate_sidecar.write_text(serialized_candidates)
            candidate_archive = self.candidate_sidecar.with_suffix(
                self.candidate_sidecar.suffix + ".jsonl"
            )
            with candidate_archive.open("a") as archive:
                archive.write(serialized_candidates)
            record["candidate_archive"] = str(candidate_archive)
            record["candidate_count"] = len(candidates)
        record["review_sha256"] = (
            hashlib.sha256(review.encode()).hexdigest() if review else None
        )
        record["response_sha256"] = hashlib.sha256(content.encode()).hexdigest()
        self.write_log(record)
        prompt_tokens = usage.get("input_tokens", 0)
        completion_tokens = usage.get("output_tokens", 0)
        return {
            "id": request_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": normalize_model(model),
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "prompt_tokens_details": {
                    "cached_tokens": usage.get("cached_input_tokens", 0)
                },
                "completion_tokens_details": {
                    "reasoning_tokens": usage.get("reasoning_output_tokens", 0)
                },
            },
        }

    def write_log(self, record: dict[str, Any]) -> None:
        if self.log_path is None:
            return
        line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        with self.log_lock:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(line)


class Handler(BaseHTTPRequestHandler):
    server_version = "AiderCodexProxy/1"

    @property
    def proxy(self) -> Proxy:
        return self.server.proxy  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:
        sys.stderr.write(f"{self.address_string()} - {fmt % args}\n")

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self.send_json(
                HTTPStatus.OK,
                {
                    "status": "ok",
                    "instance_id": self.proxy.instance_id,
                    "allowed_models": sorted(self.proxy.allowed_models),
                    "adapter_structure": self.proxy.adapter_structure,
                    "omit_permissions": self.proxy.omit_permissions,
                    "omit_skills": self.proxy.omit_skills,
                    "workdir": str(self.proxy.workdir),
                    "model_verbosity": self.proxy.model_verbosity,
                    "response_protocol": self.proxy.response_protocol,
                    "candidate_sidecar": (
                        str(self.proxy.candidate_sidecar)
                        if self.proxy.candidate_sidecar
                        else None
                    ),
                },
            )
            return
        if self.path == "/v1/models":
            data = [
                {"id": name, "object": "model", "owned_by": "local-codex"}
                for name in sorted(self.proxy.allowed_models)
            ]
            self.send_json(HTTPStatus.OK, {"object": "list", "data": data})
            return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": {"message": "not found"}})

    def do_POST(self) -> None:
        if self.path != "/v1/chat/completions":
            self.send_json(HTTPStatus.NOT_FOUND, {"error": {"message": "not found"}})
            return
        if self.headers.get("Authorization") != f"Bearer {self.proxy.api_key}":
            self.send_json(
                HTTPStatus.UNAUTHORIZED, {"error": {"message": "unauthorized"}}
            )
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError(f"Content-Length must be 1..{MAX_BODY_BYTES}")
            payload = json.loads(self.rfile.read(length))
            if payload.get("stream"):
                raise ValueError(
                    "streaming is not supported; configure Aider with streaming: false"
                )
            response = self.proxy.complete(payload)
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": {"message": str(exc)}})
            return
        except Exception as exc:
            self.send_json(
                HTTPStatus.BAD_GATEWAY,
                {"error": {"message": str(exc), "type": type(exc).__name__}},
            )
            return
        self.send_json(HTTPStatus.OK, response)


def self_test() -> None:
    assert normalize_model("openai/codex-speed") == "codex-speed"
    assert profile_for_model("openai/codex-base") is None
    assert profile_for_model("codex-deep") == "deep"
    messages = [{"role": "user", "content": "change x"}]
    prompt = render_prompt(messages)
    assert prompt.startswith(ADAPTER_PREFIXES["legacy"])
    assert render_prompt(messages, "legacy_preflight").startswith(
        ADAPTER_PREFIXES["legacy_preflight"]
    )
    assert render_prompt(messages, "legacy_trace").startswith(
        ADAPTER_PREFIXES["legacy_trace"]
    )
    assert render_prompt(messages, "legacy_literal").startswith(
        ADAPTER_PREFIXES["legacy_literal"]
    )
    assert render_prompt(messages, "legacy_reviewed_xml").startswith(
        ADAPTER_PREFIXES["legacy_reviewed_xml"]
    )
    assert render_prompt(messages, "legacy_reviewed_cdata").startswith(
        ADAPTER_PREFIXES["legacy_reviewed_cdata"]
    )
    extracted, review = extract_response(
        "<review>checked</review><final>PATCH\n</final>", "reviewed_xml"
    )
    assert extracted == "PATCH" and review == "checked"
    extracted, _ = extract_response(
        "<review>checked</review><final><![CDATA[PATCH\n]]></final>",
        "reviewed_xml",
    )
    assert extracted == "PATCH\n"
    extracted, review = extract_response(
        json.dumps(
            {
                "verification": [
                    {"contract": "tests", "status": "satisfied", "evidence": "traced"}
                ],
                "final": "PATCH\n",
            }
        ),
        "reviewed_json_schema",
    )
    assert extracted == "PATCH\n" and review is not None
    extracted, candidates = extract_response(
        json.dumps({"candidates": ["PATCH 1", "PATCH 2"]}),
        "candidate_set_json_schema",
    )
    assert extracted == "PATCH 1" and candidates is not None
    extracted, candidates = extract_response(
        json.dumps({"candidates": ["PATCH 1", "PATCH 2", "PATCH 3", "PATCH 4"]}),
        "candidate_set_4_json_schema",
    )
    assert extracted == "PATCH 1" and candidates is not None
    assert len(json.loads(candidates)) == 4
    verbosity_command = build_codex_command(
        "codex", None, Path("."), None, model_verbosity="high"
    )
    assert "model_verbosity=\"high\"" in verbosity_command
    assert render_prompt(messages, "openai").startswith(ADAPTER_PREFIXES["openai"])
    assert "enabled=false" in disabled_skills_override()
    sample = "\n".join(
        [
            json.dumps({"type": "thread.started", "thread_id": "x"}),
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {"type": "agent_message", "text": "DONE"},
                }
            ),
            json.dumps(
                {
                    "type": "turn.completed",
                    "usage": {
                        "input_tokens": 10,
                        "cached_input_tokens": 3,
                        "output_tokens": 2,
                        "reasoning_output_tokens": 1,
                    },
                }
            ),
        ]
    )
    content, usage, diagnostics = parse_codex_jsonl(sample)
    assert content == "DONE"
    assert usage["reasoning_output_tokens"] == 1
    assert diagnostics == {"reasoning_summary_events": 0, "raw_reasoning_events": 0}
    with tempfile.TemporaryDirectory() as directory:
        instructions = Path(directory) / "prompt.md"
        instructions.write_text("Role: test\n")
        command = build_codex_command(
            "codex", "hermes", Path(directory), instructions, True, True
        )
        assert "--profile" in command
        assert "include_permissions_instructions=false" in command
        assert any(part.startswith("skills.config=") for part in command)
        assert command[-1] == "-"
    print("SELF_TEST_OK")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=18080)
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    parser.add_argument(
        "--workdir", type=Path, default=Path("/private/tmp/aider-codex-proxy")
    )
    parser.add_argument("--log", type=Path)
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--instructions-file", type=Path)
    parser.add_argument(
        "--adapter-structure", choices=sorted(ADAPTER_PREFIXES), default="legacy"
    )
    parser.add_argument("--omit-permissions", action="store_true")
    parser.add_argument("--omit-skills", action="store_true")
    parser.add_argument(
        "--reasoning-effort",
        choices=("none", "low", "medium", "high", "xhigh", "max"),
    )
    parser.add_argument(
        "--model-verbosity", choices=("low", "medium", "high")
    )
    parser.add_argument(
        "--response-protocol",
        choices=(
            "plain",
            "reviewed_xml",
            "reviewed_json_schema",
            "candidate_set_json_schema",
            "candidate_set_4_json_schema",
        ),
        default="plain",
    )
    parser.add_argument("--candidate-sidecar", type=Path)
    parser.add_argument("--allow-model", action="append", dest="allowed_models")
    parser.add_argument("--api-key", default=os.environ.get("AIDER_CODEX_PROXY_KEY"))
    parser.add_argument("--instance-id", default="standalone")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if args.concurrency < 1:
        parser.error("--concurrency must be positive")
    args.workdir.mkdir(parents=True, exist_ok=True)
    if not args.api_key:
        parser.error("--api-key or AIDER_CODEX_PROXY_KEY is required")
    if args.instructions_file and not args.instructions_file.is_file():
        parser.error("--instructions-file must name an existing file")
    allowed_models = {
        normalize_model(model) for model in (args.allowed_models or PROFILE_BY_MODEL)
    }
    unknown_models = allowed_models.difference(PROFILE_BY_MODEL)
    if unknown_models:
        parser.error(
            "unknown --allow-model value: " + ", ".join(sorted(unknown_models))
        )
    proxy = Proxy(
        args.codex,
        args.workdir,
        args.log,
        args.concurrency,
        args.instructions_file,
        args.api_key,
        allowed_models,
        args.adapter_structure,
        args.omit_permissions,
        args.omit_skills,
        args.reasoning_effort,
        args.model_verbosity,
        args.response_protocol,
        args.candidate_sidecar,
        args.instance_id,
    )
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.proxy = proxy  # type: ignore[attr-defined]
    print(f"serving http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
