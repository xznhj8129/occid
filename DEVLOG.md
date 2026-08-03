# Development log

## 2026-08-03 15:44 EDT — Sigma contract stabilization

- Separated `Plan` from `Task`; implemented `Objective`, `EntityState`, `Assignment`, `Execution`, and `RecordMeta` contracts.
- Added permanent model-ID allocation and schema-versioned named-field MsgPack; documented named-field JSON persistence.
- Regenerated all core and military Pydantic modules and updated the example.
- Verified full generation, Python compilation, focused contract/serialization checks, example execution, and `git diff --check`.
