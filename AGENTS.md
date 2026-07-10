# AGENTS.md

## Overview

This is the global agent map applied across repositories. Treat every repository as independent; keep repository-specific layouts, commands, conventions, and release procedures in that repository's own guidance.

## Read next

- Read the closest project or subtree `AGENTS.md`, `CLAUDE.md`, or `GEMINI.md` before acting, if present.
- Inspect the repository's overview, architecture, contribution, security, and workflow documentation when present. File names vary; discover them from the repository rather than assuming them.
- Use exact source, tests, configuration, and callsites as the authority for behavior and contracts.

## Commands

There are no global build, test, lint, format, or publication commands. Derive them from the active repository's documented tooling and manifests.

## Code style and security

Follow project-local style, API, validation, and security rules. Preserve unrelated user changes, keep secrets out of source and output, and confirm destructive actions, external writes, or material scope expansion.

## Precedence

Direct system, developer, and user instructions override files. Explicit user requests override this map. Among files, the closest project or subtree guidance overrides parent and global guidance.

<!-- codebase-memory-mcp:start -->
## Code discovery

Use codebase-memory-mcp for graph-answerable discovery:

1. `search_graph` for symbols, functions, classes, routes, and variables.
2. `trace_path` for callers and callees.
3. `get_code_snippet` for exact source.
4. `query_graph` for complex patterns.
5. `search_code` for graph-backed text search.
6. `get_architecture` for the high-level map.

Check index state before coverage claims. Index an unindexed repository only when durable graph coverage is required and the call is authorized. For literals, config, generated files, incomplete graph coverage, or a missing index, use exact file or text search.
<!-- codebase-memory-mcp:end -->
