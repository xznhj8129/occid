# OCCID

> **VERSION INVARIANT: 0.0.1.** OCCID is version **0.0.1** and remains **0.0.1** until the Conqueror Frog project owner explicitly authorizes a version change. Schema breaks, refactors, regeneration, milestones, and internal compatibility changes do **not** increment it.

**Open Command, Control and Information Data model**

OCCID is a domain-agnostic semantic model for command, control, information, state, observations, entities, organizations, platforms, and networks. It is not a wire protocol and it is not an application database schema. Protocol and application adapters map to OCCID rather than defining OCCID around one endpoint API.

The canonical Python namespace is:

```python
from occid import TaskInformation, Assignment, MotionCommand
```

Generated runtime models live physically in `schema/`, but consumers should import through `occid`.

APEX Payload is an interoperability target and an explicit external stress test of OCCID's payload, capability, condition, and state model. APEX wire/session concepts remain adapter concerns; only protocol-neutral semantic primitives exposed by the mapping belong in OCCID core.

## Semantic normalization invariant

> **No protocol-native scalar enters OCCID merely because a protocol exposes it.**

OCCID represents facts and concepts about the world, systems, work, and operational condition. It does not preserve endpoint packet layouts, message fields, numeric codes, names, masks, IDs, or convenience aggregates unless those values have a protocol-independent semantic meaning in the OCCID model.

Protocol adapters are expected to have a deliberately asymmetric boundary:

```text
external protocol
    -> protocol-shaped parser/snapshot
    -> semantic interpretation
    -> OCCID
```

The parser or adapter-local snapshot **may and usually should remain protocol-shaped**. MAVLink `custom_mode`, CoT attributes, ROS message fields, proprietary status masks, protocol component IDs, and similar values belong there when needed to decode the source. The normalization boundary is the point where protocol vocabulary stops and OCCID semantics begin.

For every external value, apply this rule:

1. **OCCID already expresses the meaning:** map into that semantic model, enum, measurement, identity, relationship, or State.
2. **OCCID lacks the meaning, but the concept is protocol-independent and operationally useful:** treat the mismatch as a possible semantic-depth defect and refine OCCID before reaching for an escape hatch.
3. **The value is useful only for decoding, interoperability bookkeeping, diagnostics, or source-specific debugging:** keep it in the adapter/interop layer or explicit provenance/mapping data.
4. **The meaning or units are not known strongly enough:** do not publish it as semantic data yet; investigate the source semantics before deciding that OCCID does not need the concept.

### Semantic-depth refinement principle

> **When external data cannot be cleanly represented by OCCID's existing semantic primitives, compositions, or controlled vocabularies, first treat that as evidence that OCCID may be too shallow in that area, not as evidence that the data is irrelevant.**

Interoperability work is therefore an ontology-discovery mechanism. A foreign protocol, API, sensor, database, or operational system can expose a distinction that OCCID has not yet modeled. The correct response is to determine what fact about reality the datum carries and whether that fact can be reduced to existing semantic primitives, composed from them, or represented by controlled vocabulary.

Use this investigation order:

1. Determine what the source datum actually means, including units, reference frame, scale, time basis, identity scope, and any source-specific interpretation rules.
2. Restate it without relying on the source protocol's field name or encoding.
3. Try to render that meaning using existing OCCID primitives, relationships, measurements, State, composition, and controlled vocabulary.
4. If the meaning is protocol-independent but OCCID still cannot represent it cleanly, treat the mismatch as evidence for a missing primitive, relation, structure, or vocabulary and refine the model at the appropriate semantic level.
5. Only after the meaning is understood should a value be classified as genuinely protocol-local bookkeeping, provenance, decoding state, or diagnostic data that belongs outside OCCID core.

Two easy ways out are specifically wrong:

- copying an unmodeled datum into `native_*`, arbitrary metadata, or a generic telemetry bag because modeling it properly is inconvenient;
- discarding a useful datum merely because the current ontology has nowhere clean to put it.

The first avoids semantic normalization. The second hides a possible hole in the ontology. Both prevent OCCID from becoming deeper through contact with real systems.

A useful design smell test is:

> **If a proposed field cannot be rendered as a semantic primitive, a lawful composition of primitives, or controlled vocabulary, investigate whether the surrounding part of OCCID is shallow before adding the field or throwing the datum away.**

This does not imply that every source field belongs in OCCID. It means that exclusion is a conclusion reached after semantic investigation, not the default response to a modeling mismatch.

There is intentionally no escape hatch of the form:

```text
native_mode_code: int
native_mode_name: string
native_status: int
protocol_whatever: float
```

A `native_*` field is especially suspect because it makes the common model depend on the foreign protocol it is supposed to normalize. If a protocol has a useful state distinction that OCCID cannot express, model the distinction itself rather than carrying the source code beside the ontology.

The same rule applies to physical measurements. A source field called `rssi` is not automatically dBm; a speed is not automatically airspeed; heading is not ground course; a protocol timestamp is not automatically wall-clock time. Values may enter `Measurement`, `State`, or other semantic structures only with the units, reference, direction, clock basis, or interpretation required to make the claim true.

Likewise, stable description and mutable observation must not be conflated merely because a source packet contains both. For example, `Link` describes communication capability/configuration, while changing connection condition and quality belong in `LinkState`.

Protocol identity is not automatically domain identity. Source addresses, MAVLink sysid/compid, protocol message IDs, endpoint-native object IDs, and similar values may be required for routing or provenance without becoming the OCCID identity of the represented Entity or Object.

### Historical warning: the HiveLink lineage

This rule is not theoretical. Early HiveLink, before OCCID matured into the semantic model, combined transport with an informal data protocol. Its payloads carried flat fields such as flight mode strings, airspeed, groundspeed, heading, altitude, RSSI, SNR, latency, and endpoint-shaped commands. Early MAVLink examples copied MAVLink-derived values directly into those HiveLink payload structures.

Some of that design lineage survived later migrations as generic telemetry bags and `native_*` fields. The 2026 field-observation correction exposed the problem when a MAVLink adapter naturally began extending those fields with still more protocol-shaped values. OCCID then removed `TelemetryState`, removed native flight-mode/system-state escape hatches, separated `Link` from `LinkState`, removed protocol battery IDs and stray RSSI fields, and added real semantic primitives such as typed `Airspeed` and protocol-neutral link quality/counter models.

That history is a design warning: **an existing protocol-shaped OCCID field is not precedent for adding another one. It may be residue that should be removed.**

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

Task semantics are represented at three deliberately separate levels:

```text
Level 1: ontology
Task

Level 2: practical schemas
Task
├── TaskManeuver
├── TaskEffect
├── TaskInformation
└── TaskTransport

Level 3: controlled vocabulary
TaskManeuver    -> ManeuverIntent
TaskEffect      -> EffectIntent
TaskInformation -> InformationIntent
TaskTransport   -> TransportIntent
```

The distinction between ontology models and practical schema specializations is first-class IDL metadata, not documentation convention. Models may declare `semantic_role: ontology` or `semantic_role: specialization`; enums are inherently controlled vocabularies and do not carry a redundant semantic role. The generator validates model roles and emits `__occid_semantic_role__` on generated models that define one.

`Task` is the ontological class and owns the fields common to directed work: identity, instruction, references, objective, constraints, optional preconditions, timing, priority, and status. The four child records are practical schema specializations, not claims that four new ontological primitives have been discovered. They inherit the complete Task record and add only a family-specific `intent` vocabulary.

Individual verbs such as `MOVE`, `HOLD`, `SEARCH`, `OBSERVE`, `PROTECT`, or `EVACUATE` remain enum values. There is no `MoveTask`, `SearchTask`, or similar ontology tree. There is also no monolithic `TaskIntent`, `TaskType`, or cross-field validity map: an information intent cannot be supplied to a maneuver task because the schema types are different.

Task does not contain an assignee. `Assignment` binds a Task to an assignee under an optional first-class `Authority` reference. Reassignment therefore does not mutate the Task itself.

`Execution` remains runtime `State`. One Assignment may have multiple Execution attempts, while `TaskDelta`, `ExecutionAcceptance`, and `ExecutionStatusReport` report changing runtime condition and executor evidence.

`Mission` is not a Task subtype. The old verb-per-class Task tree and endpoint-shaped command classes are removed rather than preserved as compatibility aliases.

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
- `Object` may carry `Capability` properties describing what the object can do without turning each capability into an Object subtype.
- `Condition` is reusable predicate logic, not mutable state. Atomic `Predicate` values compose through one `BooleanLogic` structure with a closed `BooleanOperator` enum; `Validation` records the changing state of evaluating a Condition.
- `GNC` is vehicle guidance, navigation, and control state. `Cue` is separate spatial cueing state; bearing, elevation, and distance are independent optional measurements rather than assuming a bearing is always known.
- named operational places are `Object/Location` records.
- embedded waypoints, route points, flight-level bands, and similar planning values are `Struct` values inside Plan-related schemas.
- the military module may attach doctrine/profile data to a Task but does not create `CombatTask : Task`.

## Specification, generation, and serialization

Authoritative schema sources live under `lib/schema/`. `generate_pydantic.py` generates the reference Python runtime into `schema/`. Generated files must not be hand-maintained as an independent schema. `idl_spec.md` defines the schema language, including the explicit semantic-role distinction between ontology models and practical specializations.

Polymorphic model IDs live in `lib/model_ids.yaml` and identify the live models in the current schema. Removed models are removed from the registry; their numeric slots are ordinary free space and may be reused. `OCCID_SCHEMA_VERSION` is **0.0.1** and stays **0.0.1** until the project owner explicitly says otherwise; pre-release schema churn is not represented by pretending the project has advanced through release versions.

Use named-field JSON (`model_dump(mode="json")` or `model_dump_json()`) for durable application persistence. `encode()` uses a named-field MsgPack envelope for compact interchange. The schema-version field currently carries `0.0.1`; incompatible pre-release development payloads are migrated explicitly or discarded/reset rather than manufacturing release-number progression.

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
