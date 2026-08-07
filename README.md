# OCCID

**Open Command, Control and Information Data model**

OCCID is a domain-agnostic data model for C5ISR systems. It defines what can be known, said, commanded, and reported across entities, organizations, platforms, and networks.

It is not a wire protocol. It is not an application schema. It is the semantic layer that protocols and applications build on. A UAV patrol mission and a search-and-rescue coordination use the same structural bones: entities with identities, directives with intent, messages with envelopes, state separate from identity. The domain-specific part is only which variants exist at the leaves.

## Interoperability Targets

OCCID is designed to map cleanly to:

- MAVLink (drone control)
- Cursor on Target / CoT / ATAK
- Anduril Lattice (entity management)
- Constellation Overwatch (ISR)
- STANAG 4586 (unmanned systems interop)
- Meshtastic (mesh transport)
- DDS (pub/sub middleware)
- ROS2 (robotics framework)
- and more

OCCID does not replace these protocols. It provides a common information model that translations between them are written against.

## Specification and SDK layers

The repository currently contains both the protocol-neutral OCCID specification and its reference Python SDK/runtime. They are separate architectural layers even though they live in one repository.

```text
OCCID specification and schema sources
        -> generated runtime models
        -> serialization and validation
        -> deterministic interoperability mappings
```

The specification layer must remain independent of applications and endpoint libraries.

`interop/` is the reference interoperability layer. It converts **types and structures**, not operational intent. Appropriate responsibilities include field mappings, enums, units, scaling, sentinel values, radians/degrees, reference frames, and validation required to translate between an external representation and OCCID.

Interop functions should normally be deterministic transformations: the same input structure produces the same output structure without network access, endpoint state, or hidden runtime policy.

The SDK does **not** choose which endpoint operation should satisfy an OCCID command. It does not generate or upload missions, arm vehicles, sequence takeoff/landing, choose modes, start offboard control, retry commands, manage sockets or serial links, or implement autonomy/recovery. Those are responsibilities of consuming runtimes such as MPFC or Sigma.

Current reference modules include CoT spatial mappings, MAVSDK representation mappings, and MSP/INAV normalization. Raw MAVLink message mappings can coexist with MAVSDK mappings without conflating the two representations.

## Operational contract

OCCID separates durable identity and specification from time-indexed operational state:

- `Objective` describes the intended outcome and typed success criteria. Whether a criterion is currently satisfied belongs to assessment or execution state, not the criterion definition.
- `Task` describes work to accomplish; `Mission` is a task that can contain subordinate tasks.
- `Plan` is a separate control record describing how objectives and tasks use actors, resources, steps, routes, constraints, and contingencies. `PlanStep` describes the intended sequence and does not carry runtime status.
- `Assignment` binds one task to an assignee; `Execution` records each attempt by an executor. `TaskDelta` is an independent task-state update, not a subtype of assignment.
- `Entity` holds identity, classification, capabilities, relations, node references, and stable specification. `EntityState` carries reported position, motion, status, health, resources, links, and control state.
- Durable records compose `RecordMeta`; embedded value structs do not acquire persistent identity.

### Immediate flight control

Low-level flight control is represented as a distinct immediate command family under `LowLevelFlightCommand`. These commands do not acquire Task, Assignment, or Execution lifecycle semantics merely because they use OCCID. Endpoint runtimes choose the native operation; the OCCID SDK may convert the selected operation's structures.

Portable flight-mode meaning is represented by `StandardFlightMode`. Endpoint-native mode names and numeric codes may accompany the standard mode when required, but remain opaque adapter-facing metadata rather than becoming OCCID enum constants.

Attitude and attitude-control values use radians. Body and inertial reference frames may be omitted when context is genuinely sufficient, but control and transform code that depends on frame semantics must explicitly require and validate the relevant frame metadata.

### Record identity

`RecordMeta.record_id` identifies one persisted record instance or revision. Model-specific identifiers such as `task_id`, `plan_id`, `entity_id`, and `assignment_id` identify the stable logical operational object across record revisions. They are intentionally distinct and must not be treated as interchangeable aliases.

## Persistence and serialization

Use named-field JSON (`model_dump(mode="json")` or `model_dump_json()`) for durable Sigma persistence. Generated models expose `OCCID_SCHEMA_VERSION`, currently `(3, 0, 0)`.

`encode()` produces a named-field, versioned MsgPack envelope for compact transient interchange. It is not a wire-protocol compatibility promise. Positional field-order encoding is no longer used. Polymorphic model IDs are allocated permanently in `lib/model_ids.yaml`; existing IDs must not be changed or reused. Schema-version migration or negotiation must be defined before encoded payloads are treated as durable storage.

## Executable closed-loop demonstration

`end_to_end_ooda.py` demonstrates one complete OCCID-only command, control, telemetry, and OODA cycle. A deterministic decision agent consumes entity identity, capability, mutable state, and flight telemetry; creates an `Objective`, `IsrTask`, approved `Plan`, `Assignment`, `Execution`, and command; receives semantic acceptance, progress, telemetry, an ISR observation, and completion evidence; then closes the objective.

Every participant boundary performs a real OCCID encode/decode round trip. Sigma, HiveLink, MPFC, MAVLink, MSP, flight-control simulation, brokers, and network services are not required.

```bash
python end_to_end_ooda.py
python end_to_end_ooda.py --json
python -m unittest discover -s tests -p 'test_end_to_end_ooda.py'
python -m unittest tests.test_interop_sdk
```

See [`docs/end_to_end_ooda.md`](docs/end_to_end_ooda.md) for the scenario, invariants, scope, and machine-readable trace output.
