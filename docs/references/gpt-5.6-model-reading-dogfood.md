# GPT-5.6 model-reading promptcraft

Checked 2026-07-12 against Codex CLI `0.144.1`, the live model catalog, and the official Codex configuration reference.

## Question

Determine which instruction forms Sol, Terra, and Luna follow most reliably, and whether reasoning summaries or raw reasoning events explain observable differences.

“How a model reads” is shorthand for repeatable input/output behavior. It is not a claim about private internal cognition.

## Diagnostic controls

The official schema exposes:

- `model_reasoning_summary = "auto" | "concise" | "detailed" | "none"`;
- `model_verbosity = "low" | "medium" | "high"`;
- `hide_agent_reasoning = false` to retain reasoning events; and
- `show_raw_agent_reasoning = true` to display raw reasoning only when the active model/provider emits it.

The live catalog reports reasoning-summary and verbosity support for Sol, Terra, and Luna. `model_verbosity` controls response detail; it does not expose thinking. A detailed reasoning summary is generated diagnostic output, not complete or authoritative chain-of-thought.

A direct Terra probe requested detailed summaries, high verbosity, and raw reasoning. It returned one short reasoning summary and no raw reasoning. Across the controlled matrix, raw reasoning events were zero in every run.

`promptlab.config.toml` is an isolated diagnostic profile with detailed summaries, high verbosity, visible reasoning events, and raw-event display enabled. Normal profiles remain unchanged.

## Matrix

Five discriminating anti-echo cases were held fixed:

- declared project-name suppression;
- exact identifier preservation;
- exact class preservation beside branding;
- declared service-name suppression; and
- current-state reporting after removed terminology.

All runs used the same cases, no tools, read-only execution, high output verbosity, detailed reasoning summaries, and the intended model effort: Sol/medium, Terra/medium, Luna/high.

Three instruction forms were compared:

1. **Positive principle:** state the desired neutral behavior.
2. **Balanced rules:** state desired behavior plus explicit prohibitions.
3. **Procedure/filter:** classify contract versus contextual tokens, draft, delete contextual matches, and recheck contract tokens.

### Results

| Model | Positive | Balanced | Procedure/filter |
|---|---:|---:|---:|
| Sol / medium | 4/5 | not rerun in this focused matrix | 5/5 |
| Terra / medium | 1/5 | 1/5 | 5/5 |
| Luna / high | 2/5 | not rerun in this focused matrix | 5/5 |

The broader frozen anti-echo program supplies the missing controls: Sol positive and balanced each repeated 9/9 on the original calibrated slice; Terra positive previously scored 6/9 and balanced 8/9; the full procedural filter reached 17/17 behaviorally across all three models.

## Observable reading styles

### Sol

Sol often generalizes an abstract positive principle correctly. In the focused high-verbosity matrix it missed one declared service name, then passed all cases when given the procedure. The procedure did not require visible reasoning summaries in that run.

Working guidance: concise principles are usually adequate for ordinary Sol work; use a short procedure or final audit for exact separation, multi-constraint transformations, or known edge patterns.

### Terra

Terra treated positive and balanced instructions as descriptive preferences rather than an operation. It echoed declared names, inserted repository terminology, or generalized exact identifiers. The same model passed all focused cases when told to classify, draft, filter, and recheck.

The successful Terra run emitted reasoning summaries on only two of five cases. Summary presence therefore does not explain correctness; the executable instruction structure does.

Working guidance: give Terra an ordered transformation with explicit intermediate categories, a mechanical decision boundary, and a final invariant check. Do not rely on abstract values, adjectives, or a longer prohibition list.

### Luna

Luna/high followed the positive principle on only two of five focused cases, but passed all five under the procedure. Every successful procedural case emitted a reasoning summary and the run used 315 reasoning tokens, whereas the positive run emitted none.

Working guidance: give Luna a crisp algorithm, exact inputs, and a binary done check. Avoid asking it to infer a policy from broad prose. Higher effort provides room to execute a procedure; it does not supply the missing procedure.

## Reasoning visibility findings

Detailed summaries are useful for confirming that a model sometimes recognized an operation, but they are sparse and inconsistent:

- Sol procedural run: 0 summaries, 5/5;
- Terra procedural run: 2 summaries, 5/5;
- Luna procedural run: 5 summaries, 5/5;
- raw reasoning content: 0 for every model and variant.

Correct output without a summary and incorrect output without a summary are both common. Behavioral scoring remains authoritative. Summaries are supporting diagnostics only.

## Promptcraft rule

Choose instruction form by task shape:

- **Principle:** one familiar judgment with low ambiguity.
- **Rules/decision table:** stable categorical boundaries.
- **Procedure:** transformations, competing constraints, exact preservation plus suppression, or multi-stage verification.
- **Final invariant check:** any task where a locally plausible answer can violate an adjacent contract.

For shared prompts across Sol, Terra, and Luna, use the shortest explicit procedure that preserves the invariant. This is more portable than abstract principles and more reliable than adding prohibitions.
