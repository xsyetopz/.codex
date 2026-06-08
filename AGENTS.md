Role: Repository-local rules for Codex agents in this worktree. These rules add local scope, parity, staging, asset/resource, and reuse expectations; they do NOT authorize work outside the user's current request.

# Personality
Terse engineering communication. No filler.

# Goal
Keep repository changes literal, narrow, reusable, and verifiable.

# Success criteria
- Parity work is treated as strict behavior/runtime/UI parity with the existing or legacy implementation, NOT redesign.
- Related source, tests, build files, resources, and assets are inspected when needed to understand ownership or parity.
- Mutated paths are only the requested slice or directly required dependencies.
- Test helpers and compatibility shims have one shared owner when project structure supports it.
- Staged paths match the requested commit slice.
- Validation gaps are reported as uncertainty.

# Constraints
- Prefer `rg` and `rg --files` for discovery.
- Read broadly enough to understand behavior and ownership; mutate narrowly.
- Do NOT edit README or docs unless the current user request explicitly asks for README/docs edits.
- Do NOT include tools, scripts, plans, formatting churn, unrelated config, or generated files unless explicitly requested or directly required by the requested code change.
- Do NOT delete or move assets, resources, databases, icons, or packaging files merely because they are located under a legacy directory. Inspect references and ownership first; delete or move them only when explicitly requested or directly required by the requested change.
- For parity commits, stage only requested parity source, parity tests, directly required project/build references, and matched source deletions.
- Before creating a duplicate helper, shim, fixture, utility, project, abstraction, generated file, or support file, search for an existing owner. Reuse, link, move, or extend that owner when repository structure supports it.
- Prefer linked/shared compile items for cross-project test compatibility helpers when available.
- Treat untracked files, unrelated modifications, and pre-existing staged files as user-owned.
- Before committing, verify `git diff --cached --name-only` contains only the intended slice.
- Passing builds/tests are evidence, NOT proof of parity, visual correctness, runtime correctness, or user acceptance.

# Output
For mutation tasks, final reports end exactly with:

```text
changed: <files modified, created, OR deleted>
checked: <commands, files, systems, OR tests evaluated>
uncertain: <unverified behavior, missing evidence, OR assumptions>
```

# Stop rules
- IF a repo-local rule conflicts with the user's current explicit request, follow the user request unless it would damage unrelated/user-owned work.
- IF a requested mutation would require README/docs/tools/scripts/config/assets outside the explicit scope, stop and report exact paths before editing them.
- IF asset/resource ownership is unclear, stop before delete or move.
- IF staged paths differ from the requested slice, stop before commit.

@/Users/krystian/.codex/RTK.md
