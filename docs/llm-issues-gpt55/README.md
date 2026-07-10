# Compressed LLM Issue Corpus

The issue corpus is compressed into data files instead of one markdown file per issue.

| File | Role |
| --- | --- |
| `issues.jsonl` | One behavior issue per JSON line. |
| `issue-index.tsv` | ID/title/use_when table for fast lookup. |
| `issue-template.md` | Template for adding a new compressed issue. |
