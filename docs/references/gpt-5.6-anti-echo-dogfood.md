# GPT-5.6 lexical-echoing promptcraft

Checked 2026-07-12 against Codex CLI `0.144.1`.

## Pattern

The broad failure is **lexical echoing**: user-supplied wording is reproduced despite having no output value. Related mechanisms are:

- **lexical anchoring / nominal fixation:** a supplied name becomes the default subject label;
- **register mirroring:** hype, frustration, branding, marketing language, or jargon leaks into the response;
- **thematic contamination:** a qualifier such as “production-grade” becomes the organizing frame for headings, prose, identifiers, and validation;
- **negation residue:** the response repeats a prohibited term while explaining that it avoided the term;
- **tombstone fixation:** removed terminology or behavior remains present through cleanup narration, compatibility speculation, or backward validation;
- **rationale laundering:** the response discusses its phrasing choice instead of reporting the engineering result; and
- **contract-token collapse:** an overcorrected anti-echo rule generalizes away identifiers, API names, diagnostics, paths, or requested literals that must remain exact.

“Lexical entrainment” and “sycophantic register mirroring” describe parts of the behavior. “Lexical echoing with scope-to-style leakage” is the useful operational label: the model mistakes reference context for a vocabulary and style instruction.

## Frozen suite

`gpt-5.6-anti-echo-cases.json` version 9 is frozen at SHA-256 `6dc90eda68308b45d4b6df07e3cd449d5902920cd8bd51a7722e42c30c254440`.

The 17 natural-prose cases cover quality qualifiers, declared project names, frustrated and marketing register, removed terms and behavior, negated labels, branding near exact identifiers, phrasing rationale, and unseen exact class, diagnostic, path, route, filename, service-name, component-name, and library-name holdouts.

Scoring requires the concrete facts, exact contract tokens, no case-specific forbidden contextual substring, and a concise response. Scorer versions 1, 2, 8, and 9 corrected semantic paraphrase handling; those corrections changed required-fact matching, not forbidden echo families. Excluded artifacts remain under ignored `.tmp/aider-eval/`.

`scripts/run-anti-echo-eval.py` runs isolated read-only calls against rendered wording variants or an exact instruction file.

## Findings

### Neutral and polarity controls

On the initial nine-case calibrated set under Sol medium:

- neutral baseline: 7/9;
- positive reference-only wording: 9/9 twice;
- negative-only prohibition: 8/9;
- balanced wording: 9/9 twice.

Negative-only wording suppressed the required exact identifier `parseAccountId`. The shortest positive wording transferred poorly to Terra, scoring 6/9: it echoed a project label and repository terminology, and generalized away an exact identifier. Balanced wording improved Terra to 8/9 but still generalized the identifier.

### Contract versus context

A rule to preserve contract tokens and suppress contextual framing scored 12/12 on Sol but 10/12 on Terra. Terra both removed `parseAccountId` and echoed `Northstar` beside the required `BillingV2` class. Stronger declarative prohibitions continued to echo declared proper names.

This establishes that keyword lists and abstract prohibitions are insufficient. The behavior occurs during sentence planning, after basic term classification.

### Procedural filter

The successful prompt uses an explicit process:

1. classify input terms as exact contract tokens or contextual tokens;
2. draft only current behavior and evidence in a neutral register;
3. scan the draft against contextual tokens from the input and delete every unrequested match;
4. recheck that deletion did not remove or generalize contract tokens; and
5. describe only the intended current state after removals or renames.

Calling a token a name, official label, theme, or quality target is not an output request.

The filter variant passed:

- Sol medium: 17/17 after semantic scorer normalization;
- Terra medium: 17/17 behaviorally; its only version-8 score miss was the accepted paraphrase “focused `verifyToken` test passes”;
- Luna high: 17/17.

The final live `instructions/default.md` passed all 17 version-9 cases and the existing operational suite at 8/8.

## Adoption

The effective shared instructions now separate contract tokens from contextual language and require a final lexical deletion pass. They also prohibit backward narration of discarded terms or behavior without weakening exact identifiers, diagnostics, paths, or requested literals.

Current `instructions/default.md`:

- 8,375 bytes;
- 1,168 words;
- SHA-256 `411c91cc379efc2fcb8c69d4e221b313c3a0b12507062dae98b4711f5049ded5`.

This is a global communication correction. It applies regardless of whether the contextual token is “enterprise,” “production-grade,” a repository name, an emotional description, or any future label.
