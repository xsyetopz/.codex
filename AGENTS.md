# AGENTS.md

<!-- CodeGraphContext:start -->
## Code discovery

Use CodeGraphContext (CGC) for graph-answerable repository discovery:

1. `list_indexed_repositories` to check index coverage before graph-based claims.
2. `find_code` to locate symbols, functions, classes, variables, and relevant files.
3. `analyze_code_relationships` for callers, callees, dependencies,
inheritance, and change impact.
4. `calculate_cyclomatic_complexity` and `find_most_complex_functions` for
targeted maintainability analysis.
5. `find_dead_code` for cleanup investigations.
6. `execute_cypher_query` for graph questions the standard tools cannot express.
7. `visualize_graph_query` only when a visual graph materially helps explain relationships.

Use `add_code_to_graph` or `add_package_to_graph` only when durable graph
coverage is needed and indexing is authorized. For asynchronous indexing, use
`check_job_status` and `list_jobs` rather than repeatedly starting jobs.

Use `watch_directory`, `list_watched_paths`, and `unwatch_directory` only when
persistent automatic reindexing is explicitly required. Do not use
`delete_repository` without explicit authorization.

For literals, configuration, generated files, incomplete graph coverage, or
exact source verification, use local file reads and text search. Treat CGC
results as navigation aids and verify relevant code in the working tree before editing.
<!-- CodeGraphContext:end -->
