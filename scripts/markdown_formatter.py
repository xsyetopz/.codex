#!/usr/bin/env python3
"""Format instruction-style Markdown for markdownlint-friendly docs.

This helper is intentionally small and opinionated:
- keeps a single top-level title
- demotes later H1 headings to H2
- wraps normal prose to a fixed width
- preserves fenced code blocks and HTML comments verbatim
- lightly wraps one-line bullet and numbered list items

It is designed for the prompt/instructions files in this workspace, not as a
full Markdown formatter.
"""

from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})(\s+)(.*)$")
LIST_RE = re.compile(r"^([ \t]*)([-*+]|\d+[.)])(\s+)(.*)$")
FENCE_RE = re.compile(r"^([ \t]*)(`{3,}|~{3,})(.*)$")
COMMENT_START_RE = re.compile(r"^\s*<!--")
COMMENT_END_RE = re.compile(r"-->\s*$")
INDENTED_CODE_RE = re.compile(r"^(?:\t| {4,})")


def wrap_paragraph(lines: list[str], width: int) -> list[str]:
    if not lines:
        return [""]

    if all(len(line) <= width for line in lines):
        return lines[:]

    text = " ".join(part for part in (line.strip() for line in lines) if part)
    if not text:
        return [""]
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [text]


def format_markdown(text: str, width: int = 80) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    in_fence = False
    fence_token = ""
    in_comment = False
    saw_h1 = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.extend(wrap_paragraph(paragraph, width))
            paragraph = []

    i = 0
    while i < len(lines):
        line = lines[i]

        if in_fence:
            out.append(line)
            if line.lstrip().startswith(fence_token):
                in_fence = False
                fence_token = ""
            i += 1
            continue

        if in_comment:
            out.append(line)
            if COMMENT_END_RE.search(line):
                in_comment = False
            i += 1
            continue

        if not line.strip():
            flush_paragraph()
            if out and out[-1] != "":
                out.append("")
            elif not out:
                out.append("")
            i += 1
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            flush_paragraph()
            out.append(line)
            in_fence = True
            fence_token = fence_match.group(2)
            i += 1
            continue

        if COMMENT_START_RE.match(line):
            flush_paragraph()
            out.append(line)
            if not COMMENT_END_RE.search(line):
                in_comment = True
            i += 1
            continue

        if INDENTED_CODE_RE.match(line):
            flush_paragraph()
            out.append(line)
            i += 1
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            flush_paragraph()
            hashes, spacing, title = heading_match.groups()
            if len(hashes) == 1:
                if saw_h1:
                    hashes = "##"
                else:
                    saw_h1 = True
            out.append(f"{hashes}{spacing}{title}")
            i += 1
            continue

        list_match = LIST_RE.match(line)
        if list_match:
            flush_paragraph()
            indent, marker, spacing, item_text = list_match.groups()
            raw_item = f"{indent}{marker}{spacing}{item_text}"
            if len(raw_item) <= width:
                out.append(raw_item)
                i += 1
                continue
            wrapped = textwrap.wrap(
                item_text.strip(),
                width=width - len(indent) - len(marker) - len(spacing),
                break_long_words=False,
                break_on_hyphens=False,
            ) or [item_text.strip()]
            out.append(f"{indent}{marker}{spacing}{wrapped[0]}")
            continuation_indent = " " * (len(indent) + len(marker) + len(spacing))
            for continuation in wrapped[1:]:
                out.append(f"{continuation_indent}{continuation}")
            i += 1
            continue

        paragraph.append(line)
        i += 1

    flush_paragraph()

    while out and out[-1] == "":
        out.pop()

    return "\n".join(out) + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Normalize instruction-style Markdown files.",
    )
    parser.add_argument("paths", nargs="+", help="Markdown files to format")
    parser.add_argument(
        "--width",
        type=int,
        default=80,
        help="Wrap width for prose paragraphs and list items (default: 80)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if any file would change.",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Rewrite files in place instead of printing formatted text.",
    )
    args = parser.parse_args(argv)

    if args.check and args.in_place:
        parser.error("--check and --in-place are mutually exclusive")

    changed = False
    for raw_path in args.paths:
        path = Path(raw_path)
        original = path.read_text(encoding="utf-8")
        formatted = format_markdown(original, width=args.width)
        if formatted != original:
            changed = True
            if args.in_place:
                path.write_text(formatted, encoding="utf-8")
            elif not args.check:
                sys.stdout.write(formatted)
                if len(args.paths) > 1:
                    sys.stdout.write(f"\n--- {path} ---\n")
        elif not args.in_place and not args.check and len(args.paths) == 1:
            sys.stdout.write(formatted)

    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
