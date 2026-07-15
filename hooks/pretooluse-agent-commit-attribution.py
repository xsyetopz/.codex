#!/usr/bin/env python3
"""Block agent-run git commits that omit the active model attribution trailer."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any

MAX_MESSAGE_BYTES = 1024 * 1024
COMMIT_CREATING_SUBCOMMANDS = {
    "am",
    "cherry-pick",
    "commit",
    "commit-tree",
    "merge",
    "rebase",
    "revert",
}
NON_COMMIT_FLAGS = {"--abort", "--no-commit", "-n", "--quit"}


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )
    raise SystemExit(0)


def model_display_name(slug: str) -> str:
    name = slug.rsplit("/", 1)[-1].lower()
    match = re.fullmatch(r"gpt-(\d+)\.(\d+)(?:-([a-z0-9]+))?", name)
    if match:
        major, minor, variant = match.groups()
        suffix = f" {variant.title()}" if variant else ""
        return f"GPT {major}.{minor}{suffix}"
    return slug


def shell_segments(command: str) -> list[list[str]]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|")
    lexer.whitespace_split = True
    lexer.commenters = ""
    segments: list[list[str]] = []
    current: list[str] = []
    for token in lexer:
        if token and all(character in ";&|" for character in token):
            if current:
                segments.append(current)
                current = []
        else:
            current.append(token)
    if current:
        segments.append(current)
    return segments


def git_subcommand_index(argv: list[str]) -> int | None:
    if not argv or Path(argv[0]).name != "git":
        return None
    index = 1
    value_options = {"-C", "-c", "--git-dir", "--work-tree", "--namespace"}
    while index < len(argv):
        argument = argv[index]
        if argument in value_options:
            index += 2
            continue
        if any(
            argument.startswith(prefix)
            for prefix in ("-C", "-c", "--git-dir=", "--work-tree=", "--namespace=")
        ):
            index += 1
            continue
        if argument.startswith("-"):
            index += 1
            continue
        return index
    return None


def read_message_file(path: str, cwd: Path) -> str:
    if path == "-":
        deny("Agent-authored commits must use a visible message, not `git commit -F -`.")
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    try:
        if candidate.stat().st_size > MAX_MESSAGE_BYTES:
            deny("Commit message file exceeds 1 MiB.")
        return candidate.read_text()
    except OSError as error:
        deny(f"Cannot inspect commit message file: {error}")
    raise AssertionError("unreachable")


def visible_message(argv: list[str], subcommand_index: int, cwd: Path) -> str | None:
    messages: list[str] = []
    index = subcommand_index + 1
    while index < len(argv):
        argument = argv[index]
        if argument in {"-m", "--message"}:
            if index + 1 >= len(argv):
                deny("`git commit -m` requires a visible message.")
            messages.append(argv[index + 1])
            index += 2
            continue
        if argument.startswith("-m") and len(argument) > 2:
            messages.append(argument[2:])
        elif argument.startswith("--message="):
            messages.append(argument.split("=", 1)[1])
        elif argument in {"-F", "--file"}:
            if index + 1 >= len(argv):
                deny("`git commit -F` requires a message file.")
            messages.append(read_message_file(argv[index + 1], cwd))
            index += 2
            continue
        elif argument.startswith("-F") and len(argument) > 2:
            messages.append(read_message_file(argument[2:], cwd))
        elif argument.startswith("--file="):
            messages.append(read_message_file(argument.split("=", 1)[1], cwd))
        index += 1
    return "\n\n".join(messages) if messages else None


def command_text(tool_input: Any) -> str | None:
    if not isinstance(tool_input, dict):
        return None
    for key in ("cmd", "command"):
        value = tool_input.get(key)
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return shlex.join(str(part) for part in value)
    return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as error:
        print(f"invalid hook input: {error}", file=sys.stderr)
        raise SystemExit(2) from error
    if not isinstance(payload, dict):
        print("hook input must be an object", file=sys.stderr)
        raise SystemExit(2)

    command = command_text(payload.get("tool_input"))
    if not command:
        return

    model = payload.get("model")
    if not isinstance(model, str) or not model.strip():
        deny("Cannot attribute an agent-authored commit because the active model is unknown.")
    expected = f"Co-authored-by: {model_display_name(model)} <noreply@openai.com>"
    cwd = Path(payload.get("cwd") or os.getcwd())

    for argv in shell_segments(command):
        subcommand_index = git_subcommand_index(argv)
        if subcommand_index is None:
            continue
        subcommand = argv[subcommand_index]
        if subcommand not in COMMIT_CREATING_SUBCOMMANDS:
            continue
        if subcommand != "commit":
            if any(flag in argv[subcommand_index + 1 :] for flag in NON_COMMIT_FLAGS):
                continue
            deny(
                f"Agent-run `git {subcommand}` can create unattributed commits. "
                f"Use a no-commit form, then `git commit` with trailer: {expected}"
            )
        message = visible_message(argv, subcommand_index, cwd)
        if message is None:
            deny(
                "Agent-authored commit message is not visible to the hook. "
                f"Use `-m` or `-F` and include: {expected}"
            )
        if expected not in message.splitlines():
            deny(f"Agent-authored commits must include: {expected}")


if __name__ == "__main__":
    main()
