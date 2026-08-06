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
and more

OCCID does not replace these protocols. It provides a common information model that translations between them are written against.

## Operational contract

OCCID separates durable identity and specification from time-indexed operational state:

- `Objective` describes the intended outcome and typed success criteria. Whether a criterion is currently satisfied belongs to assessment or execution state, not the criterion definition.
- `Task` describes work to accomplish; `Mission` is a task that can contain subordinate tasks.
- `Plan` is a separate control record describing how objectives and tasks use actors, resources, steps, routes, constraints, and contingencies. `PlanStep` describes the intended sequence and does not carry runtime status.
- `Assignment` binds one task to an assignee; `Execution` records each attempt by an executor. `TaskDelta` is an independent task-state update, not a subtype of assignment.
- `Entity` holds identity, classification, capabilities, relations, node references, and stable specification. `EntityState` carries reported position, motion, status, health, resources, links, and control state.
- Durable records compose `RecordMeta`; embedded value structs do not acquire persistent identity.

### Record identity

`RecordMeta.record_id` identifies one persisted record instance or revision. Model-specific identifiers such as `task_id`, `plan_id`, `entity_id`, and `assignment_id` identify the stable logical operational object across record revisions. They are intentionally distinct and must not be treated as interchangeable aliases.

## Persistence and serialization

Use named-field JSON (`model_dump(mode="json")` or `model_dump_json()`) for durable Sigma persistence. Generated models expose `OCCID_SCHEMA_VERSION`, currently `(2, 0, 0)`.

`encode()` produces a named-field, versioned MsgPack envelope for compact transient interchange. It is not a wire-protocol compatibility promise. Positional field-order encoding is no longer used. Polymorphic model IDs are allocated permanently in `lib/model_ids.yaml`; existing IDs must not be changed or reused. Schema-version migration or negotiation must be defined before encoded payloads are treated as durable storage.

## Executable closed-loop demonstration

`end_to_end_ooda.py` demonstrates one complete OCCID-only command, control, telemetry, and OODA cycle. A deterministic decision agent consumes entity identity, capability, mutable state, and flight telemetry; creates an `Objective`, `IsrTask`, approved `Plan`, `Assignment`, `Execution`, and command; receives semantic acceptance, progress, telemetry, an ISR observation, and completion evidence; then closes the objective.

Every participant boundary performs a real OCCID encode/decode round trip. Sigma, HiveLink, MPFC, MAVLink, MSP, flight-control simulation, brokers, and network services are not required.

```bash
python end_to_end_ooda.py
python end_to_end_ooda.py --json
python -m unittest discover -s tests -p 'test_end_to_end_ooda.py'
```

See [`docs/end_to_end_ooda.md`](docs/end_to_end_ooda.md) for the scenario, invariants, scope, and machine-readable trace output.