# AGENTS.md

Prioritize modern implementations and current best practices. Default to
disregarding legacy code, outdated libraries, deprecated features, and obsolete
patterns—unless the user explicitly requires backward compatibility, public API
stability, or existing functionality retention.

<!-- CodeGraphContext:start -->
## Code discovery

Use CodeGraphContext (CGC) for graph-answerable repository discovery:

- `list_indexed_repositories`, `find_code`, `analyze_code_relationships` for navigation
- `calculate_cyclomatic_complexity`, `find_most_complex_functions`,
`find_dead_code` for analysis
- `execute_cypher_query` for complex graph questions
- `visualize_graph_query` only when visual output materially clarifies relationships

Index with `add_code_to_graph`/`add_package_to_graph` only when authorized
Track async jobs with `check_job_status`/`list_jobs`. Use `watch_directory`
`unwatch_directory` only when persistent reindexing is required.

For exact verification, use local file reads and text search. Verify all CGC
results in the working tree before editing. Never use `delete_repository`
without explicit authorization.
<!-- CodeGraphContext:end -->
