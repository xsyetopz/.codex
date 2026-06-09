# .codex

## Purpose

This file documents common failure modes, explains how Codex works, and shows how to configure it.

## Common Failure Modes

GPT models commonly exhibit one or more of the following issues:

- Prioritizes inferred assumptions over the literal text of the user's prompt.
- Reframes complaints as advice requests, corrections as new creation tasks, and errors as prompt-engineering issues.
- Appends unwanted summaries, next steps, frameworks, or cautionary notes after delivering the core answer.
- Inserts unrequested filler text, transitions, rationales, and prompt rewrites to avoid silence.
- Skews outputs toward appearing complete or generic rather than honoring user-defined boundaries.
- Interprets user frustration as an instruction to redesign processes or resolve ambiguity.
- Responds to negative feedback or rejected outputs by generating more text.
- Acknowledges boundaries or errors but immediately repeats the mistake.
- Uses polished, abstract phrasing to obscure boundary violations or deflect from mistakes.
- Forces users to repeatedly police constraints, correct the same assumptions, and undo hallucinated limitations.
- Adopts a coach, teacher, or manager persona instead of acting as a precise, compliant tool.
- Claims an issue is fixed or verified without objective proof.
- Fails to state when something is unknown or unverified, masking lack of evidence.
- Uses overly confident language for speculative leaps instead of separating facts from guesses.
- Equates successful compilation or passing tests with user acceptance, ignoring visual flaws or runtime bugs.
- Hides uncertainty with smooth prose and treats plausible explanations as facts.
- Ignores broader programming context and treats debugging like generic documentation.
- Treats legacy behavior or feature parity as optional rather than required.
- Restricts analysis to the target file, ignoring essential context in related files.
- Truncates necessary research and dogmatically defends initial code changes.
- Acts like a superficial code cleaner rather than an investigative engineer, preserving broken premises.
- Reduces complex requirements to standard, model-friendly tasks, favoring generic "helpfulness" over strict accuracy.
- Misquotes the user or falsely claims authorization for specific premises or actions.
- Gives rule explanations instead of diagnosing root causes or identifying source requests.
- Burdens the user with extra review work, messy git diffs, and repeated correction cycles.
- Produces outputs that require manual pruning and invents unauthorized constraints that stall investigation.
- Inserts unrequested markdown formatting, headers, or structures contrary to instructions.
- Uses incidental words from a correction to lecture on unrelated topics.
- Injects unrelated tools, commands, or configurations after identifying a specific defect.
- Treats a boundary instruction as an invitation to debate or reframe it.
- Answers its own generated question rather than the user's actual command.
- Leans on non-committal words like "minimal," "likely," or "good enough" where exact parity is required.
- Uses testing-budget limits as an excuse for incomplete implementations.
- Relies on "uncertainty" disclaimers to bypass hard blockers when parity is unknown.
- Keeps prompt wording that triggers bad behavior, then blames model architecture for failures.
- Dilutes accountability by burying errors in process explanations and tool commentary.
- Discusses rejected topics simply because the user mentioned them.

## How Codex Works

Codex runs an autonomous loop that executes coding intentions, maintains state, and reduces the LLM errors listed above.

- **Execution Loop:** Plan -> Edit Code -> Run Tools/Sandbox -> Observe Results -> Repair Failures -> Compact History -> Repeat.
- **Context Assembly Stack:** Each iteration builds a fresh, layered payload including the System Base, Developer Guardrails, Active Agents, Local Environment Metadata, and Compressed History.
- **Evaluation Cycle:** Instead of a single inference pass, Codex uses tool feedback, sandboxed execution, and structural rule checks to validate code before concluding a step.

## Configuration Layers

To avoid model drift into common GPT bad habits, split configuration across separate operational layers:

- **`config.toml` (Global, Project, Per-Directory):**
  - *When:* When setting up base configuration or overriding environment parameters for a repository or subdirectory.
  - *What:* Key-value parameters like active models, context limits, paths to instruction files, and local tool permissions.
  - *Why:* Enables a cascading hierarchy: directory overrides project, which overrides global defaults.
- **`model_instructions_file`:**
  - *When:* When you need to replace Codex's default system personality.
  - *What:* A text or Markdown file containing a comprehensive structural system prompt.
  - *Why:* Enforces a clean baseline by replacing generic agent prompts with explicit structural rules.
- **`developer_instructions`:**
  - *When:* Enforcing immutable project constraints, runtime guardrails, or strict coding parameters.
  - *What:* String directives in `config.toml` that act as an unyielding developer-role block.
  - *Why:* Reinforces base layers per profile, enforcing tech stacks, sandboxing rules, or API usage limits.
- **`AGENTS.md` (Global, Project, Per-Directory):**
  - *When:* Defining developer workflows, team roles, review rules, and directory conventions.
  - *What:* Cascading Markdown files injected as user/contextual instructions.
  - *Why:* Keeps the workspace structured by mapping automated workflows across global, project, and local folders.
- **`compact_prompt` / `experimental_compact_prompt_file`:**
  - *When:* Triggered when loop history token usage crosses set thresholds.
  - *What:* Inline strings or template files that define how conversational history is condensed.
  - *Why:* Prevents context loss during long tasks by removing filler while preserving key code decisions.

## Recommended Limits

- **Inline `developer_instructions`:** Keep under 1,500 characters. Short, precise directives receive higher prompt-weight density.
- **Target `AGENTS.md` Context Windows:** Keep combined global, project, and directory agent files under 6,000 to 8,000 characters.
- **History Compaction Threshold:** Trigger at 50-60% of model context to preserve critical system rules and avoid truncation.

# Related

[openai/codex -- Add `developer_instructions_file` for stronger local guidance #12926](https://github.com/openai/codex/issues/12926)
