# Development log

## 2026-08-14 - Control ontology refactor

- Implemented the locked Control refactor from `AI_SHARED/projects/software/skynet/occid/ControlRefactor.md`.
- Added `Directive` and `Authority`; made `Task` one generic instruction-bearing model with controlled `TaskType` and `TaskIntent` vocabularies and generated cross-field validation.
- Replaced endpoint-shaped core command classes with semantic StateChange, ProcessControl, Configuration, Motion, Resource, and Execution command families.
- Moved Assignment into Control while retaining Execution, ExecutionAcceptance, ExecutionStatusReport, and TaskDelta as runtime State records.
- Moved Interface under Communication and ControlLease under Authority; removed the Control/Reference branch and rehomed useful location and plan values.
- Removed the military `CombatTask : Task` extension while preserving military tasking data as `CombatTaskProfile` and `MunitionAllocation`.
- Retired removed model identities without reusing permanent IDs and bumped the schema version to 5.0.0.
- Updated generated Python, OCCID examples, the closed-loop demonstration, MAVSDK mapping, and focused contract/serialization tests.

## 2026-08-03 16:24 EDT - Contract cleanup and freeze boundary

- Renamed `RecordMeta.uid` to `record_id` and documented its distinction from stable model-specific operational IDs.
- Removed mutable satisfaction and execution status from `SuccessCriterion` and `PlanStep` definitions.
- Made `TaskDelta` an independent `State` record with typed task and owner references instead of inheriting assignment semantics.
- Updated generated models and the example, and added contract, source/generated consistency, model-ID, and MsgPack round-trip tests.

## 2026-08-03 15:44 EDT - Sigma contract stabilization

- Separated `Plan` from `Task`; implemented `Objective`, `EntityState`, `Assignment`, `Execution`, and `RecordMeta` contracts.
- Added permanent model-ID allocation and schema-versioned named-field MsgPack; documented named-field JSON persistence.
- Regenerated all core and military Pydantic modules and updated the example.
- Verified full generation, Python compilation, focused contract/serialization checks, example execution, and `git diff --check`.
