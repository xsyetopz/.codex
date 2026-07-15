# Agent commit attribution

Checked 2026-07-12 against Codex CLI `0.144.1` and the official [Codex hooks reference](https://learn.chatgpt.com/docs/hooks#pretooluse).

## Contract

When Codex invokes a Git command that creates or amends a commit, the resulting message must contain an exact model-derived trailer:

```text
Co-authored-by: GPT 5.6 Sol <noreply@openai.com>
```

The display name is derived from the hook input's active model slug, so the standing lanes produce `GPT 5.6 Sol`, `GPT 5.6 Terra`, or `GPT 5.6 Luna`. The normal Git author remains unchanged.

The policy does not apply when the user runs Git directly. `hooks.json` is a Codex lifecycle hook, not a repository `.git/hooks` installation, so human terminal and editor commits are untouched.

## Enforcement

`hooks.json` registers `hooks/pretooluse-agent-commit-attribution.py` for `PreToolUse` Bash calls. The hook:

- allows non-commit Git commands;
- accepts visible `-m`, `--message`, `-F`, or `--file` messages only when they contain the exact active-model trailer;
- blocks editor-only messages, stdin message files, and missing trailers;
- blocks commit-producing `merge`, `cherry-pick`, `revert`, `rebase`, `am`, and `commit-tree` commands unless a safe no-commit/abort form is used;
- tells Codex the exact trailer required so it can retry correctly.

Codex requires review of new or changed non-managed hooks. Use `/hooks` in a fresh client session to review and trust this definition. The hook was runtime-tested with `--dangerously-bypass-hook-trust` only for validation; that flag is not a standing configuration. `hooks.json` is the sole hook-definition source. Codex may persist a generated `[hooks.state]` trust hash in `config.toml`; that table records review state and does not define a hook. No hook command or event definition is duplicated in TOML, so the mixed-definition warning does not apply.

## Validation

Direct fixtures covered non-Git commands, missing and correct Sol trailers, Terra mismatch, Luna `-F` messages, no-commit cherry-picks, commit-producing cherry-picks, and rebase continuation. JSON parsing, Python compilation, and Ruff passed.

A fresh Codex session then attempted exactly:

```text
git commit -m 'test: hook'
```

with no staged files. `PreToolUse` denied it before execution and reported:

```text
Agent-authored commits must include: Co-authored-by: GPT 5.6 Sol <noreply@openai.com>
```

Official documentation states that PreToolUse interception is not a complete security boundary and does not yet cover every equivalent shell path. The hook is deterministic default enforcement for supported Codex Bash calls, not proof that arbitrary external Git plumbing cannot bypass it. A concise model instruction should be added only after the current unchanged profile baseline matrix finishes, so that benchmark comparisons retain one prompt hash.
