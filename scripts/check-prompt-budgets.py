#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
import re
import sys
import tomllib
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
ROLE_CONTRACT = {
    "explorer": {
        "model": "gpt-5.6-luna",
        "effort": "low",
        "permissions": ":read-only",
        "spawnable": True,
    },
    "worker": {
        "model": "gpt-5.6-luna",
        "effort": "low",
        "permissions": None,
        "spawnable": True,
    },
    "reviewer": {
        "model": "gpt-5.6-sol",
        "effort": "low",
        "permissions": ":read-only",
        "spawnable": True,
    },
    "responder": {
        "model": "gpt-5.6-sol",
        "effort": "medium",
        "permissions": None,
        "spawnable": True,
    },
    "architect": {
        "model": "gpt-5.6-sol",
        "effort": "high",
        "permissions": ":read-only",
        "spawnable": False,
    },
    "orchestrator": {
        "model": "gpt-5.6-luna",
        "effort": "medium",
        "permissions": None,
        "spawnable": False,
    },
}
LEGACY_PATHS = (
    "quick-fix.config.toml",
    "build.config.toml",
    "debug.config.toml",
    "think-hard.config.toml",
    "profiles/quick-fix.instructions.md",
    "profiles/build.instructions.md",
    "profiles/debug.instructions.md",
    "profiles/think-hard.instructions.md",
)
DISALLOWED_GENERIC_PHRASES = (
    "think step by step",
    "be concise",
    "be thorough",
    "best effort",
    "if possible",
    "try to",
)
UNSTABLE_FEATURES = (
    "apply_patch_streaming_events",
    "artifact",
    "chronicle",
    "code_mode",
    "concurrent_reasoning_summaries",
    "current_time_reminder",
    "default_mode_request_user_input",
    "deferred_executor",
    "enable_fanout",
    "enable_mcp_apps",
    "exec_permission_approvals",
    "item_ids",
    "local_thread_store_compression",
    "network_proxy",
    "non_prefixed_mcp_tool_names",
    "realtime_conversation",
    "request_permissions_tool",
    "respect_system_proxy",
    "rollout_budget",
    "runtime_metrics",
    "shell_zsh_fork",
    "terminal_visualization_instructions",
    "token_budget",
    "unified_exec_zsh_fork",
    "use_agent_identity",
)

failed = False
checks = 0


def report(ok: bool, label: str, detail: str) -> None:
    global checks, failed
    checks += 1
    print(f"{'ok' if ok else 'FAIL'} {label}: {detail}")
    failed |= not ok


def check_size(label: str, text: str, low: int, high: int) -> None:
    report(low <= len(text) <= high, label, f"{len(text)} chars [{low}, {high}]")


def load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def normalized_paragraphs(text: str) -> list[str]:
    paragraphs = []
    for block in re.split(r"\n\s*\n", text):
        normalized = " ".join(line.strip() for line in block.splitlines()).strip()
        if len(normalized) >= 100:
            paragraphs.append(normalized)
    return paragraphs


base_path = ROOT / "config.toml"
base = load_toml(base_path)
model_path = ROOT / "model-instructions.md"
agents_path = ROOT / "AGENTS.md"
harness_path = ROOT / "docs/references/gpt-5.6-harness.md"
model_text = model_path.read_text(encoding="utf-8")
agents_text = agents_path.read_text(encoding="utf-8")
harness_text = harness_path.read_text(encoding="utf-8")

report(base.get("model") == "gpt-5.6-luna", "base model", str(base.get("model")))
report(base.get("review_model") == "gpt-5.6-sol", "review model", str(base.get("review_model")))
report(base.get("model_reasoning_effort") == "low", "base effort", str(base.get("model_reasoning_effort")))
report(base.get("plan_mode_reasoning_effort") == "low", "base plan effort", str(base.get("plan_mode_reasoning_effort")))
report(base.get("model_instructions_file") == str(model_path), "shared model instructions", str(base.get("model_instructions_file")))
report(base.get("model_reasoning_summary") == "concise", "reasoning summary", str(base.get("model_reasoning_summary")))
report(base.get("features", {}).get("fast_mode") is False, "fast mode", "disabled")
status_line = base.get("tui", {}).get("status_line", [])
report("five-hour-limit" in status_line, "five-hour usage indicator", "present")
report("weekly-limit" in status_line, "weekly usage indicator", "present")
report(base.get("notice", {}).get("hide_rate_limit_model_nudge") is False, "rate-limit model nudge", "visible")

prompt_surfaces = {
    "model-instructions.md": model_text,
    "AGENTS.md": agents_text,
    "base developer_instructions": base.get("developer_instructions", ""),
    "base compact_prompt": base.get("compact_prompt", ""),
}
check_size("model-instructions.md", model_text, 3500, 6500)
check_size("AGENTS.md", agents_text, 900, 2200)
check_size("base developer_instructions", prompt_surfaces["base developer_instructions"], 160, 650)
check_size("base compact_prompt", prompt_surfaces["base compact_prompt"], 350, 950)

PROMPT_SECTIONS = (
    "Role:",
    "Personality:",
    "Goal:",
    "Success criteria:",
    "Constraints:",
    "Tools:",
    "Output:",
    "Stop rules:",
)
for structure_label, prompt in (
    ("shared prompt", model_text),
    ("compact prompt", prompt_surfaces["base compact_prompt"]),
):
    section_positions = [prompt.find(section) for section in PROMPT_SECTIONS]
    report(all(position >= 0 for position in section_positions), f"{structure_label} GPT-5.6 sections", ", ".join(PROMPT_SECTIONS))
    report(section_positions == sorted(section_positions), f"{structure_label} GPT-5.6 section order", "published order")
    report(all(prompt.count(section) == 1 for section in PROMPT_SECTIONS), f"{structure_label} GPT-5.6 section uniqueness", "one each")
    for legacy_heading in (
        "# Outcome",
        "# Authority",
        "# Execution",
        "# Goal",
        "# Communication",
        "# Stop",
        "# Objective",
        "# Work state",
        "# Exclude",
    ):
        report(legacy_heading not in prompt, f"{structure_label} custom heading removed", legacy_heading)

required_shared_fragments = (
    "Standing Goal permission: the root may call `create_goal`",
    "Slash commands are client input, not model actions",
    "Plan mode is host-selected",
    "`update_goal` with `blocked`",
    "model-tool pause surrogate",
    "bypasses the normal repeated-blocker threshold",
    "five-hour and weekly allowance",
    "Goal spanning hours or days",
    "run a Brief",
    "Close delegation loops",
    "spawned agents never delegate",
    "Use SBAR",
    "scan STEP",
    "Hold a Huddle only when",
    "with an IPASS handoff",
    "apply STAR",
    "Debrief",
    "Creating or changing text is a textual edit: use Python 3",
)
for fragment in required_shared_fragments:
    report(fragment in model_text, "shared protocol fragment", fragment)

agents_cfg = base.get("agents", {})
report(agents_cfg.get("max_threads") == 3, "V1 thread limit", str(agents_cfg.get("max_threads")))
report(agents_cfg.get("job_max_runtime_seconds") == 900, "agent runtime cap", str(agents_cfg.get("job_max_runtime_seconds")))
report(agents_cfg.get("max_depth") == 1, "V1 depth limit", str(agents_cfg.get("max_depth")))
spawnable_names = {name for name, contract in ROLE_CONTRACT.items() if contract["spawnable"]}
registered_names = {name for name, value in agents_cfg.items() if isinstance(value, dict)}
report(registered_names == spawnable_names, "spawnable role set", ", ".join(sorted(registered_names)))

role_paths = []
for role, contract in ROLE_CONTRACT.items():
    role_path = ROOT / f"{role}.config.toml"
    role_paths.append(role_path)
    report(role_path.exists(), f"{role} profile exists", str(role_path))
    if not role_path.exists():
        continue
    cfg = load_toml(role_path)
    report(cfg.get("model") == contract["model"], f"{role} model", str(cfg.get("model")))
    report(cfg.get("model_reasoning_effort") == contract["effort"], f"{role} effort", str(cfg.get("model_reasoning_effort")))
    report(cfg.get("plan_mode_reasoning_effort") == contract["effort"], f"{role} plan effort", str(cfg.get("plan_mode_reasoning_effort")))
    report(cfg.get("default_permissions") == contract["permissions"], f"{role} permissions", str(cfg.get("default_permissions")))
    report("model_instructions_file" not in cfg, f"{role} shared prompt inheritance", "no override")
    report("compact_prompt" not in cfg, f"{role} compact inheritance", "no duplicate")
    allowed_keys = {
        "model",
        "model_reasoning_effort",
        "plan_mode_reasoning_effort",
        "developer_instructions",
    }
    if contract["permissions"] is not None:
        allowed_keys.add("default_permissions")
    report(set(cfg) == allowed_keys, f"{role} config scope", ", ".join(sorted(cfg)))
    developer = cfg.get("developer_instructions", "")
    prompt_surfaces[f"{role} developer_instructions"] = developer
    check_size(f"{role} developer_instructions", developer, 180, 520)
    if contract["spawnable"]:
        registration = agents_cfg.get(role, {})
        report(registration.get("config_file") == f"./{role}.config.toml", f"{role} shared config_file", str(registration.get("config_file")))
        check_size(f"{role} dispatch description", registration.get("description", ""), 50, 180)
        prompt_surfaces[f"{role} dispatch description"] = registration.get("description", "")
    else:
        report(role not in registered_names, f"{role} root-only", "not spawnable")

for legacy in LEGACY_PATHS:
    report(not (ROOT / legacy).exists(), "legacy profile removed", legacy)
report(not (ROOT / "profiles").exists(), "legacy prompt directory removed", "profiles/")
configured_efforts = {
    load_toml(path).get("model_reasoning_effort")
    for path in role_paths
}
report(configured_efforts.isdisjoint({"xhigh", "max", "ultra"}), "standing high-cost efforts", ", ".join(sorted(configured_efforts)))
report("Use `/goal`" not in model_text, "model slash-command invocation", "absent")

features = base.get("features", {})
report(features.get("goals") is True, "stable goals feature", "enabled")
report(features.get("multi_agent") is True, "stable multi_agent feature", "enabled")
v2 = features.get("multi_agent_v2", {})
report(isinstance(v2, dict), "V2 metadata table", type(v2).__name__)
report("enabled" not in v2, "V2 catalog selection", "not forced")
report(v2.get("max_concurrent_threads_per_session") == 3, "V2 slot count", str(v2.get("max_concurrent_threads_per_session")))
report(v2.get("tool_namespace") == "team", "V2 role-aware namespace", str(v2.get("tool_namespace")))
report(v2.get("hide_spawn_agent_metadata") is False, "named role metadata", "visible")
for feature in ("apps", "computer_use", "personality", "secret_auth_storage"):
    report(features.get(feature) is False, f"feature {feature}", "disabled globally")
report(features.get("workspace_dependencies") is True, "feature workspace_dependencies", "enabled")
for feature in UNSTABLE_FEATURES:
    value = features.get(feature)
    enabled = value is True or isinstance(value, dict) and value.get("enabled") is True
    report(not enabled, f"unstable feature {feature}", "not forced")

AGENTS_SECTIONS = (
    "# AGENTS.md",
    "## Overview",
    "## Read next",
    "## Commands",
    "## Code style and security",
    "## Precedence",
    "## Code discovery",
)
agents_section_positions = [agents_text.find(section) for section in AGENTS_SECTIONS]
report(all(position >= 0 for position in agents_section_positions), "AGENTS map sections", ", ".join(AGENTS_SECTIONS))
report(agents_section_positions == sorted(agents_section_positions), "AGENTS map section order", "skill order")
report(all(agents_text.count(section) == 1 for section in AGENTS_SECTIONS), "AGENTS map section uniqueness", "one each")
for old_heading in ("## Repository scope", "## Repository evidence", "## Validation", "## Local boundaries", "## Workspace map"):
    report(old_heading not in agents_text, "old AGENTS structure removed", old_heading)
report(agents_text.count("<!-- codebase-memory-mcp:start -->") == 1, "AGENTS start sentinel", "one")
report(agents_text.count("<!-- codebase-memory-mcp:end -->") == 1, "AGENTS end sentinel", "one")
report("Treat every repository as independent" in agents_text, "global AGENTS scope", "cross-repository")
report("keep repository-specific layouts" in agents_text, "global AGENTS local-boundary rule", "present")
for local_fragment in (
    "scripts/check-prompt-budgets.py",
    "ARCHITECTURE.md",
    "config.toml",
    "explorer.config.toml",
    "docs/references",
    "This directory is a live Codex home",
    "Workspace map",
):
    report(local_fragment not in agents_text, "global AGENTS avoids local detail", local_fragment)
for definition in ("Use SBAR", "scan STEP", "IPASS handoff", "apply STAR", "Standing Goal permission"):
    report(definition not in agents_text, "AGENTS avoids shared protocol", definition)

all_prompt_paths = [model_path, agents_path, base_path, *role_paths]
for path in all_prompt_paths:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    invalid = sorted({ord(char) for char in text if char not in "\t\n" and not 0x20 <= ord(char) <= 0x7E})
    report(b"\r" not in raw, f"{path.name} line endings", "LF only")
    report(text == unicodedata.normalize("NFC", text), f"{path.name} normalization", "NFC")
    report(not invalid, f"{path.name} prompt codepoints", "printable ASCII plus tab/LF" if not invalid else ", ".join(f"U+{value:04X}" for value in invalid))

for label, text in prompt_surfaces.items():
    lowered = text.lower()
    found = [phrase for phrase in DISALLOWED_GENERIC_PHRASES if phrase in lowered]
    report(not found, f"{label} generic scaffolding", ", ".join(found) if found else "none")

paragraph_owners = defaultdict(set)
for label, text in prompt_surfaces.items():
    for paragraph in normalized_paragraphs(text):
        paragraph_owners[paragraph].add(label)
duplicates = {paragraph: owners for paragraph, owners in paragraph_owners.items() if len(owners) > 1}
report(not duplicates, "cross-file prompt duplication", "; ".join(f"{sorted(owners)}: {paragraph[:80]}" for paragraph, owners in duplicates.items()) if duplicates else "none >=100 chars")

required_harness_fragments = (
    "dc5ae378967cff0de2cfb30b98c52047ab978e3d",
    "656a2d0905c9e0b9bdade1badab07ef6d42ca17c",
    "additional weekly limits may apply",
    "pause surrogate",
    "Long duration is not evidence that Sol, Max, or Ultra is needed",
    "275-line generic contract checklist",
    "Role, Personality, Goal, Success criteria, Constraints, Tools, Output, and Stop rules",
    "AGENTS.md` is a short global map",
    "`explorer`",
    "`worker`",
    "`reviewer`",
    "`responder`",
    "`architect`",
    "`orchestrator`",
    "one-hop delegation",
    "hide_spawn_agent_metadata = false",
    '`tool_namespace = "team"`',
    "Budget exhaustion is not completion",
    "update_plan is a TODO/checklist tool and is not allowed in Plan mode",
)
for fragment in required_harness_fragments:
    report(fragment in harness_text, "harness evidence coverage", fragment)

ignore_text = (ROOT / ".gitignore").read_text(encoding="utf-8")
for role in ROLE_CONTRACT:
    report(f"!/{role}.config.toml" in ignore_text, f"{role} public source", "allowlisted")
for private in ("/config.toml", "/history.jsonl", "/goals_*.sqlite*", "/sessions/"):
    report(private in ignore_text, "private boundary", private)

print(f"{checks} checks")
sys.exit(1 if failed else 0)
