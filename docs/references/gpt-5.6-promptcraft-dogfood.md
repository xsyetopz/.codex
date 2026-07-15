# GPT-5.6 promptcraft dogfood

Checked 2026-07-12.

## Question

Measure which semantically equivalent instruction wording and body structure most reliably produces precise behavior, then determine the cheapest sufficient reasoning effort. This is not a search for benchmark hints or decorative XML.

## Frozen suite

`gpt-5.6-promptcraft-cases.json` freezes six operational cases and an exact structured result contract before any variant exposure. Cases cover analysis-only scope, destructive confirmation, unverified handoff, missing environment context, exact API/diagnostic preservation, and evidence-supported stopping.

Scoring requires the exact decision, action and completion booleans, exact literal copy, valid schema output, and no tool use. Token and latency metrics are secondary to behavioral correctness.

## Staged experiment

1. **Wording polarity:** positive-only, negative-only, and balanced wording under Markdown, Sol medium, isolated calls.
2. **Body structure:** render the winning semantic clauses as Markdown, XML, and a restrained Markdown-plus-XML hybrid. Tags may delimit role, constraints, scenario, and output contract; they may not add semantics.
3. **Effort:** with wording and structure frozen, compare Sol low, medium, high, and xhigh. Test max only if failures are plausibly reasoning-limited. Treat ultra separately because the installed catalog says it can automatically delegate, changing behavior rather than only reasoning depth.
4. **Model/profile:** only after the Sol effort curve is known, compare the intended Luna and Terra lanes at the cheapest adequate supported efforts.
5. Repeat prospective winners before changing live prompt or profile files.

## Controls

- Same cases, schema, order, model, effort, service tier, and no-tool execution within each A/B stage.
- No wording may mention repository benchmark instances or expected code answers.
- Do not interpret lower token use as improvement when exact behavior regresses.
- XML wins only if repeated behavior or cost improves; familiarity or visual neatness is not evidence.
- Positive and negative variants must remain semantically aligned. If a polarity changes authorization or completion meaning, revise controls before candidate exposure.

## Community evidence

The curated `docs/reddit/codex/` corpus is real-world behavioral evidence at user scale: Sol medium repeatedly works as a practical default, higher efforts materially consume allowance, and long-context or compaction behavior varies across actual workloads. Local controlled runs serve a different purpose: they isolate likely causes and check whether a configuration reproduces those field outcomes. A narrow frozen eval does not overrule repeated user experience; disagreement is a signal to broaden the workload and investigate the boundary.

## Current catalog evidence

The installed Codex `0.144.1` catalog exposes Sol and Terra at low, medium, high, xhigh, max, and ultra; Luna exposes low through max. Medium is the catalog default for all three. Ultra is not a pure effort comparison because its description includes automatic delegation.


## Executed results

### Harness preflight

The first positive/Markdown/Sol-medium preflight is excluded. Suite v1 said to copy a required literal but did not label which substring was required, and it used `act` both for prohibited tool execution and for the output authorization field. The resulting 0/6 exposed contract ambiguity rather than model behavior. Before comparing candidates, suite v2 labeled the required literal, defined `act` as immediate implementation authorization, aligned all polarity variants, and froze hash `6887bb32446f3466fed3e8db30a954b9190373d4a686e918e94a135274c0817e`. The excluded artifact remains at `.tmp/aider-eval/promptcraft-wording-positive-markdown-medium-r1.json` for auditability.

`scripts/run-promptcraft-eval.py` is the dedicated runner. It locks the frozen cases, strict JSON schema, no-action/read-only execution, model, effort, and isolated calls; it varies only the requested wording or structure dimension and records exact results, tokens, and elapsed time. Python compilation and Ruff validation pass.

### Wording polarity

With Markdown and Sol medium fixed:

- positive: 6/6 in both repetitions; rendered instructions 784 bytes / 105 words;
- negative: 4/6; it incorrectly marked the analysis-only case complete and withheld authorization for the exact-contract implementation;
- balanced: 6/6 in both repetitions; rendered instructions 969 bytes / 135 words.

Positive wording wins the Sol-only golf because it repeats the same exact behavior with 185 fewer bytes than balanced. Negative-only wording is rejected: prohibitions described boundaries less reliably than direct authorization and completion criteria.

### Body structure

With positive wording and Sol medium fixed, Markdown, XML, and Markdown-plus-XML each scored 6/6. Rendered instruction sizes were 784, 1,030, and 1,092 bytes respectively. Output was identical at 224 total tokens per six-case run, and none used reasoning tokens. XML therefore adds 246 bytes and the hybrid adds 308 bytes without behavioral benefit. Markdown remains the supported structure for this workload.

### Sol effort curve

Positive Markdown scored 6/6 at low, medium, high, and xhigh. Low and medium each repeated 6/6. Every run emitted 224 output tokens and zero reasoning tokens, so this suite is not reasoning-limited. Aggregate elapsed times were noisy and cache-dependent: low 36.462 and 33.602 seconds; medium 33.271 and 33.387; high 55.518; xhigh 31.512.

Conclusion: Sol low is sufficient for narrow, schema-bound operational classification. This does **not** justify replacing Sol medium as the general default: repository implementation dogfood exercised materially different reasoning and all three cases remained unresolved.

### Cross-model boundary

The shortest positive wording did not transfer perfectly:

- Luna low and medium scored 5/6; both withheld `act` for the authorized exact-contract implementation.
- Terra low and medium scored 5/6; both treated SDK/context repair as immediate implementation action.
- Balanced Markdown fixed Terra medium and repeated 6/6 twice.
- Balanced Luna medium and high remained 5/6 on the exact-contract authorization case; increasing effort added reasoning tokens without changing the decision.

This is evidence for profile-specific wording only at a narrow boundary, not enough to fork live instruction files. Terra benefits from an explicit positive-plus-negative action boundary. Luna’s miss persisted across wording and effort, so duplicating more prose into its profile would be speculative. Keep the existing profile defaults until a broader task suite repeats the behavior.

## Adoption decision

Adopt no live prompt change from this stage. The evidence supports three durable rules already reflected in `instructions/default.md`: use explicit authorization/completion boundaries, prefer concise Markdown over decorative XML, and do not substitute higher effort for missing context or model-specific behavior. The shorter positive form is the Sol-local winner; balanced wording is the cross-model Terra winner; neither is universally dominant. Preserve the then-current 6,205-byte live prompt and proceed to a requirement-level configuration audit rather than golf it from a six-case classifier.

## Enterprise peer-programming follow-up

A later user-directed pass broadened the target from minimal operational classification to corporate and enterprise peer programming. The isolated lifecycle rewrite preserved the operational suite at 8/8 twice, tied the controlled six-language coding baseline at 4/6, and improved the new frozen enterprise suite from the prior prompt’s repeated 7/8 to 8/8 twice. It was adopted at 7,623 bytes and SHA-256 `9398b1ff7253f1f15b2433eaffec90405137a00e5d10487e4ba88451c6cc94db`. See `gpt-5.6-enterprise-peer-dogfood.md`; the earlier no-adoption decision remains the correct conclusion for the narrower wording/structure experiment at that time.
