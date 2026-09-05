# Development log

## 2026-09-04 - Restore one semantic hierarchy and flat runtime

- Removed the authored and derived `Type` semantic level. Authored models are now only `Concept` or `Representation`; Vocabulary remains the enum declaration kind.
- Made `parent` the sole semantic membership edge: `parent` always means is-a and field inheritance. Authored `variants` and `children` are not part of the language.
- Changed the compiler to emit every Concept and Representation nominally, preserve `parent`, derive direct `children`, flatten inherited fields, and keep named references exact instead of lowering Concepts into descendant unions.
- Removed compiled `family` metadata. The complete parent graph now carries semantic ancestry without a lossy nearest-family projection.
- Kept generated Python classes flat. Runtime `is_a()` follows the compiled parent registry rather than Python inheritance, and `Semantic[T]` permits semantically compatible flat descendants in model fields.
- Preserved compact heterogeneous decoding through concrete model IDs and added semantic compatibility checks for nested values.
- Structural consumer hashes ignore taxonomy-only `parent`/`children` metadata and contract-local model IDs; effective field changes still alter the relevant structural hashes.
- Regenerated `occid.yaml`, Python projections, and contract markers and added regression coverage for direct children, flat runtime ancestry, nominal broad references, and descendant wire round-trips.

## 2026-08-17 - Protocol-neutral observation-state correction

- Traced flat telemetry and endpoint-native state fields back to the pre-ontological HiveLink protocol, where MAVLink-derived flight mode, speed, heading, altitude, RSSI/SNR, network quality, and endpoint-shaped commands were carried directly in transport payloads.
- Established the durable semantic-normalization invariant: no protocol-native scalar enters OCCID merely because the source protocol exposes it. Adapter-local parser/snapshot structures may remain protocol-shaped; the adapter -> OCCID boundary must normalize to protocol-independent semantics.
- Removed `TelemetryState` rather than retaining a generic bag for protocol telemetry.
- Removed `native_mode_name`, `native_mode_code`, active native mode lists, native navigation-state code, and native system-state code from `FlightControlState`. Endpoint mode values may be used to derive `StandardFlightMode` and other semantic state, then stop at the adapter boundary.
- Removed raw `fix_code`, generic source age/error/timeout fields, and duplicate EPH/EPV aliases from `GnssSolution`.
- Removed protocol battery IDs and stray RSSI from `ElectricalResourceState`; distinct electrical resources use semantic source identity.
- Separated static communication definition from mutable observation: `Link` no longer owns connection condition/status; new `LinkState` contains changing condition plus `SignalQuality`, `DeliveryQuality`, and `LinkCounters`.
- Defined signal quality only for measurements whose physical or normalized meaning is actually known. Device-dependent values such as generic MAVLink `RADIO_STATUS.rssi/remrssi` must not be relabeled as dBm or another semantic unit.
- Added typed `Airspeed : Measurement` with an explicit reference vocabulary instead of carrying airspeed in a generic telemetry structure.
- Updated mesh link/node state to reuse the same generic `LinkState` semantics instead of maintaining a parallel flat RSSI/SNR/loss/status mini-model.
- Changed `EntityState` into the semantic observation aggregate and made `UAVTelemetryMessage` carry `EntityState` rather than the removed `TelemetryState`.
- Added regression coverage specifically asserting that protocol-native escape hatches do not return.
- Documented the historical lesson explicitly: an existing protocol-shaped OCCID field is not precedent for another field; it may be legacy residue that should be removed.

## 2026-08-15 - APEX payload mapping primitives

- Mapped the APEX Payload specification against OCCID and used the fit as an external stress test of the core ontology rather than adding APEX-shaped classes.
- Added `Capability` as an Object-carried `Property`, keeping generic `Payload` intentionally open while allowing any Object to declare what it can do.
- Reclaimed `Condition` for reusable predicate logic, renamed the former health/readiness `Condition` state root to `Health`, removed `ConstraintCondition`, added Task preconditions, and made plan contingencies use typed Conditions.
- Simplified Condition composition to one `BooleanLogic` structure driven by the closed `BooleanOperator` enum instead of separate Conjunction/Disjunction/Negation model classes.
- Renamed the GNC state branch from `Guidance` to `GNC`, then added distinct `Cue`, `Activation`, and `Validation` state primitives needed by APEX wayfinding and activation semantics. Cue bearing, elevation, and distance are independently optional because APEX or other sources may only know part of the spatial relation.
- Kept APEX session addressing, device classes, and protocol-specific fields out of the ontology; the changes are protocol-neutral primitives exposed by the APEX mapping.
- Removed historical model-ID reservations: `lib/model_ids.yaml` now contains live models only and freed numeric slots may be reused. Bumped the generated schema version to 5.2.0 and updated generated models and focused tests.

## 2026-08-14 - Task semantic levels correction

- Corrected the reviewed Task design before MPFC/Sigma integration.
- Kept `Task` as the level-1 ontological class and introduced four level-2 practical schema specializations: `TaskManeuver`, `TaskEffect`, `TaskInformation`, and `TaskTransport`.
- Split the former monolithic `TaskIntent` vocabulary into `ManeuverIntent`, `EffectIntent`, `InformationIntent`, and `TransportIntent`.
- Added first-class IDL `semantic_role` metadata so models can distinguish `ontology` from `specialization` and enums can declare `vocabulary`; the generator validates and emits the declared role.
- Removed `TaskType`, `TaskIntent`, `VALID_TASK_INTENT_TYPES`, and the generic runtime convention that scanned `VALID_*` maps to infer cross-field validation.
- Kept individual verbs as level-3 controlled vocabulary rather than rebuilding verb-per-class ontology leaves.
- Allocated model IDs 310-313 to the four practical Task schemas and updated generated Python, examples, the OCCID-only demonstration, IDL documentation, and focused tests.

## 2026-08-14 - Control ontology refactor

- Implemented the Control ontology refactor, subject to repository review before downstream integration.
- Added `Directive` and `Authority`; established Task as instruction-bearing directed work.
- Replaced endpoint-shaped core command classes with semantic StateChange, ProcessControl, Configuration, Motion, Resource, and Execution command families.
- Moved Assignment into Control while retaining Execution, ExecutionAcceptance, ExecutionStatusReport, and TaskDelta as runtime State records.
- Moved Interface under Communication and ControlLease under Authority; removed the Control/Reference branch and rehomed useful location and plan values.
- Removed the military `CombatTask : Task` extension while preserving military tasking data as `CombatTaskProfile` and `MunitionAllocation`.
- Removed obsolete model identities and bumped the schema version to 5.0.0.
- Updated generated Python, OCCID examples, the closed-loop demonstration, MAVSDK mapping, and focused contract/serialization tests.

## 2026-08-03 16:24 EDT - Contract cleanup and freeze boundary

- Renamed `RecordMeta.uid` to `record_id` and documented its distinction from stable model-specific operational IDs.
- Removed mutable satisfaction and execution status from `SuccessCriterion` and `PlanStep` definitions.
- Made `TaskDelta` an independent `State` record with typed task and owner references instead of inheriting assignment semantics.
- Updated generated models and the example, and added contract, source/generated consistency, model-ID, and MsgPack round-trip tests.

## 2026-08-03 15:44 EDT - Sigma contract stabilization

- Separated `Plan` from `Task`; implemented `Objective`, `EntityState`, `Assignment`, `Execution`, and `RecordMeta` contracts.
- Added model-ID allocation and schema-versioned named-field MsgPack; documented named-field JSON persistence.
- Regenerated all core and military Pydantic modules and updated the example.
- Verified full generation, Python compilation, focused contract/serialization checks, example execution, and `git diff --check`.
