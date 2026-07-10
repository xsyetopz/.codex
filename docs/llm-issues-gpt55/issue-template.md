# LLM Issue JSONL Template

Add one line to `issues.jsonl` with this shape:

```json
{"id":"short-kebab-id","title":"Plain title","use_when":"Trigger condition","failure":"Observed failure pattern","required_behavior":"Required behavior","bad_forms":["bad response shape"],"acceptance_check":"Evidence that proves the behavior was avoided","examples":"Short evidence note","source_status":"local_behavior_policy"}
```

Keep examples local and falsifiable. Do not use this corpus as evidence for Codex product capability.
