# GPT-5.6 prompt representation experiment

Date: 2026-07-12

## Decision

Keep the current Markdown procedure. Do not globally convert the anti-echo policy to uppercase pseudocode, JSON, or the compact DSP syntax.

Code-shaped prompting is feasible as a controlled, task-specific experiment. It is not a general advantage for GPT-5.6, and uppercase control-flow keywords did not make the policy more reliable in this suite.

## GPT-5.6-specific basis

The experiment follows the GPT-5.6 guidance to start from outcomes and constraints, keep prompts lean, reserve ALWAYS/NEVER for true invariants, add procedural scaffolding only for measured gaps, and rerun representative evaluations after surgical prompt changes:

- https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6

## Frozen design

- Source cases: `gpt-5.6-anti-echo-cases.json`, SHA-256 `6dc90eda68308b45d4b6df07e3cd449d5902920cd8bd51a7722e42c30c254440`
- Primary cases: 9
- Prospective holdouts: 8
- Representations: Markdown procedure, uppercase pseudocode, JSON policy, compact DSP syntax
- Intended efforts: Sol/medium, Terra/medium, Luna/high
- Calls used no tools, low output verbosity, detailed supported reasoning summaries, and a raw-reasoning probe.
- Private chain-of-thought was neither requested nor available; raw-reasoning events were zero.
- Exact lexical scorer checked required contract terms, forbidden context echoes, and word limits.

## Results

### First primary pass (9 cases per cell)

| Model | Markdown | Pseudocode | JSON | DSP |
|---|---:|---:|---:|---:|
| Sol | 9/9 | 9/9 | 9/9 | 8/9 |
| Terra | 8/9 | 8/9 | 8/9 | 8/9 |
| Luna | 9/9 | 6/9 | 9/9 | 8/9 |

The uppercase pseudocode copied forbidden names or qualifiers in three Luna cases. The compact DSP form was shortest at 42 words but regressed on at least one model.

### Prospective Markdown/JSON repeat and holdout

Across the first and repeated primary passes, Markdown and JSON tied at 52/54. On the frozen holdouts, isolated JSON scored 19/24 and Markdown 13/24. JSON added 38 measured input tokens per call, about 0.3 percent in this harness.

That isolated result justified an integration check, not adoption.

### Full-prompt integration check

The exact pre-change global prompt (SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`) and the JSON candidate were each run on all 17 cases:

| Full prompt | Sol | Terra | Luna | Total |
|---|---:|---:|---:|---:|
| Existing Markdown | 17/17 | 16/17 | 15/17 | 48/51 |
| JSON candidate | 16/17 | 15/17 | 14/17 | 45/51 |

The representation benefit did not transfer into the surrounding global prompt. JSON was reverted.

## Interpretation

- Models can follow prompt-as-code, so JSON or a DSL is a valid experimental representation.
- Syntax does not substitute for semantics. Uppercase IF/THEN/ELSE is not a privileged reasoning channel.
- Compactness alone is insufficient: DSP saved prompt words but lost correctness.
- Structured JSON may help some isolated classification tasks, but surrounding instructions materially affect the result.
- Use code-shaped policies only after task-specific evaluation and an integrated regression check.
- Detailed reasoning summaries can help diagnose behavior, but they are supporting observations rather than authoritative explanations.

## Caveat

The scorer is deliberately strict and lexical. Some failures are semantically acceptable phrases that miss a frozen alternative, such as no change to the benchmark versus no benchmark changes. Comparisons remain useful because cases and scoring were unchanged across candidates; absolute pass rates should not be treated as semantic quality estimates.
