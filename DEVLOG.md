# Development log

## 2026-08-14 - Task semantic levels correction

- Corrected the reviewed Task design before MPFC/Sigma integration.
- Kept `Task` as the level-1 ontological class and introduced four level-2 practical schema specializations: `TaskManeuver`, `TaskEffect`, `TaskInformation`, and `TaskTransport`.
- Split the former monolithic `TaskIntent` vocabulary into `ManeuverIntent`, `EffectIntent`, `InformationIntent`, and `TransportIntent`.
- Added first-class IDL `semantic_role` metadata so models can distinguish `ontology` from `specialization` and enums can declare `vocabulary`; the generator validates and emits the declared role.
- Removed `TaskType`, `TaskIntent`, `VALID_TASK_INTENT_TYPES`, and the generic runtime convention that scanned `VALID_*` maps to infer cross-field validation.
- Kept individual verbs as level-3 controlled vocabulary rather than rebuilding verb-per-class ontology leaves.
- Allocated permanent model IDs 310-313 to the four practical Task schemas and updated generated Python, examples, the OCCID-only demonstration, IDL documentation, and focused tests.

## 2026-08-14 - Control ontology refactor

- Implemented the Control refactor from `AI_SHARED/projects/software/skynet/occid/ControlRefactor.md`, subject to repository review before downstream integration.
- Added `Directive` and `Authority`; established Task as instruction-bearing directed work.
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
