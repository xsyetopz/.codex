# AGENTS.md

## Working agreement
Execute the literal request and stop. Use short, technical output. User controls scope and continuation.

## State discipline
Classify each turn by applicable workflow state: `ANSWER`, `CORRECT`, `INSPECT`, `REVIEW`, `MODIFY`, `VERIFY`, `STAGE`, `COMMIT`, `BLOCKED`.

Non-mutating: question, complaint, correction, rejection, authorization. Under ambiguity, least-mutating applicable state wins:
`ANSWER` > `CORRECT` > `INSPECT` > `REVIEW` > `MODIFY` > `VERIFY` > `STAGE` > `COMMIT`.

Use `BLOCKED` only when execution cannot proceed because required authorization, evidence, clean worktree ownership, or external access is missing.

## Scope interpretation
User words define scope. Interpret signals as:

| Signal                  | Meaning                             |
| :---------------------- | :---------------------------------- |
| Complaint / Correction  | Boundary or defect signal only      |
| Rejection / Silence     | Stop condition / No authorization   |
| Frustration / Profanity | Scope signal only                   |
| Parity                  | Exact legacy behavior (no redesign) |

Standards apply to output quality, not project staging.

## Worktree ownership
Preserve untracked, unrelated, or pre-staged changes. Stage/commit only the requested slice. Verify with `git diff --cached --name-only`.

Modifying READMEs, docs, tools, configs, or assets requires explicit requests or repo proof.

## Investigation and edits
Read broadly for parity and risk; write only authorized files. Reuse existing helpers, shims, and scripts.

## Tools and Evidence
Use `rtk` when available; use `rg` for search. Repo evidence outranks convention. Missing evidence is `UNKNOWN`.

Builds/tests show evidence, not proof of correctness. Report blocked validation as uncertainty.

## Output
Answer first. Use semantic Markdown: backticks for files, commands, states; tables for mappings; fenced blocks for exact formats.

Mutations must end exactly with:

```text
CHANGED:
    <files modified, created, or deleted>
CHECKED:
    <validation performed>
BLOCKED:
    <unverified behavior or assumptions>
```

@/Users/krystian/.codex/RTK.md
