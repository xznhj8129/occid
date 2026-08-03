# Development log

## 2026-08-03 16:24 EDT — Contract cleanup and freeze boundary

- Renamed `RecordMeta.uid` to `record_id` and documented its distinction from stable model-specific operational IDs.
- Removed mutable satisfaction and execution status from `SuccessCriterion` and `PlanStep` definitions.
- Made `TaskDelta` an independent `State` record with typed task and owner references instead of inheriting assignment semantics.
- Updated generated models and the example, and added contract, source/generated consistency, model-ID, and MsgPack round-trip tests.

## 2026-08-03 15:44 EDT — Sigma contract stabilization

- Separated `Plan` from `Task`; implemented `Objective`, `EntityState`, `Assignment`, `Execution`, and `RecordMeta` contracts.
- Added permanent model-ID allocation and schema-versioned named-field MsgPack; documented named-field JSON persistence.
- Regenerated all core and military Pydantic modules and updated the example.
- Verified full generation, Python compilation, focused contract/serialization checks, example execution, and `git diff --check`.
