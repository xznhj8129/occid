# OCCID

**Open Command, Control and Information Data model**

OCCID is a domain-agnostic semantic model for command, control, information, state, observations, entities, organizations, platforms, and networks. It is not a wire protocol and it is not an application database schema. Protocol and application adapters map to OCCID rather than defining OCCID around one endpoint API.

The canonical Python namespace is:

```python
from occid import Task, Assignment, MotionCommand
```

Generated runtime models live physically in `schema/`, but consumers should import through `occid`.

## Control contract

The Control ontology is deliberately small:

```text
Control
├── Objective
├── Directive
│   ├── Task
│   └── Command
│       ├── StateChangeCommand
│       ├── ProcessControlCommand
│       ├── ConfigurationCommand
│       ├── MotionCommand
│       ├── ResourceCommand
│       └── ExecutionCommand
├── Plan
├── Constraint
├── Authority
└── Assignment
```

The central distinction is:

> **Task preserves intent. Command prescribes operation.**

`Task` is one generic instruction-bearing record. Its machine-readable classification is deliberately coarse: `TaskType` selects `MANEUVER`, `EFFECT`, `INFORMATION`, or `TRANSPORT`, and optional `TaskIntent` adds a controlled second-level vocabulary. Invalid type/intent combinations are declared by the typed `VALID_TASK_INTENT_TYPES` map and rejected by the generated runtime. The free-text `instruction` remains the authoritative human meaning.

Task does not contain an assignee. `Assignment` binds a Task to an assignee under an optional first-class `Authority` reference. Reassignment therefore does not mutate the Task itself.

`Execution` remains runtime `State`. One Assignment may have multiple Execution attempts, while `TaskDelta`, `ExecutionAcceptance`, and `ExecutionStatusReport` report changing runtime condition and executor evidence.

`Mission` is not a Task subtype. The old Task subclass tree and endpoint-shaped command classes are retired rather than preserved as compatibility aliases.

## Command families

Core Commands describe semantic operation families, not UAV or API method names:

- `StateChangeCommand`: set, enable, or disable state.
- `ProcessControlCommand`: start, stop, pause, resume, or cancel a process.
- `ConfigurationCommand`: set a parameter or load configuration.
- `MotionCommand`: move to, follow a path, maintain, or stop motion.
- `ResourceCommand`: acquire, release, allocate, or transfer resources.
- `ExecutionCommand`: execute, abort, or reset an executable target.

Endpoint adapters may still expose convenient functions such as `arm()`, `goto_location()`, or `start_offboard()`. Those function names do not become OCCID ontology classes.

High-rate setpoints and control samples remain `Input` models rather than Commands.

## Other structural boundaries

- `Interface` is under `Communication` and represents a real system/protocol interface.
- `ControlLease` is under `Authority` because it represents delegated control rights.
- named operational places are `Object/Location` records.
- embedded waypoints, route points, flight-level bands, and similar planning values are `Struct` values inside Plan-related schemas.
- the military module may attach doctrine/profile data to a generic Task but does not create `CombatTask : Task`.

## Specification, generation, and serialization

Authoritative schema sources live under `lib/schema/`. `generate_pydantic.py` generates the reference Python runtime into `schema/`. Generated files must not be hand-maintained as an independent schema.

Permanent polymorphic model IDs live in `lib/model_ids.yaml`. Retired IDs remain reserved and are never reused. The Control refactor is schema version `5.0.0`.

Use named-field JSON (`model_dump(mode="json")` or `model_dump_json()`) for durable application persistence. `encode()` uses a versioned named-field MsgPack envelope for compact interchange. A schema-version migration boundary is required before old durable payloads are interpreted as a newer schema.

## Interoperability layer

`interop/` contains deterministic representation conversions. It may convert fields, units, enums, reference frames, and endpoint-native representations, but it does not choose operational intent or own endpoint sessions.

For example, the MAVSDK helper accepts `MotionCommand(MOVE_TO)` and converts its destination into MAVSDK `goto_location` fields. It does not restore the removed `GoToCommand` ontology class.

## Demonstration and tests

`end_to_end_ooda.py` demonstrates a complete OCCID-only Task -> Authority -> Assignment -> Plan -> Execution -> Command -> acceptance/progress/completion loop with real OCCID encode/decode boundaries.

```bash
python end_to_end_ooda.py
python end_to_end_ooda.py --json
python -m unittest discover -s tests
```

See `docs/end_to_end_ooda.md` for the scenario invariants.
