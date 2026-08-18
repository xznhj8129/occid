# OCCID

**Open Command, Control, Intelligence Data**

OCCID is a domain-agnostic semantic model for command, control, state, observations, entities, organizations, platforms, networks, and directed work. It is not a wire protocol, transport, application database schema, or service API. Protocol and application adapters map into OCCID rather than defining OCCID around one endpoint.

The current release version is read from [`VERSION`](VERSION). Release version is provenance; structural consumer compatibility is handled by the OCCID contract mechanism described below.

## Install and import

OCCID is a normal Python package:

```bash
python -m pip install -e .
```

Consumers use the canonical namespace:

```python
from occid import Entity, EntityState, TaskManeuver, Assignment, Execution
```

Generated runtime models remain under `schema/` internally and are re-exported through `occid`.

## Semantic normalization invariant

> **No protocol-native scalar enters OCCID merely because a protocol exposes it.**

An adapter-local parser or snapshot may remain protocol-shaped. At the semantic boundary:

1. If OCCID already expresses the protocol-independent meaning, map into that model, enum, measurement, identity, relationship, or State.
2. If OCCID lacks the meaning but the concept is protocol-independent and operationally useful, treat the mismatch as evidence that OCCID may need refinement.
3. If a value is useful only for decoding, interoperability bookkeeping, diagnostics, or source-specific debugging, keep it outside OCCID core.
4. If meaning, units, reference, scale, identity scope, or clock basis are not known strongly enough, do not publish a false semantic claim.

Do not use `native_*` fields, arbitrary metadata, generic telemetry bags, or protocol codes as escape hatches from modeling.

Interoperability work should explicitly preserve identity, units, ranges, sign conventions, coordinate/reference frames, altitude datums, time bases, sentinels, optionality, and the distinction between stable definition and changing observed state.

Protocol identity is not automatically domain identity. MAVLink sysid/compid, CoT UID, endpoint-native IDs, packet IDs, and similar values may be needed for routing/provenance without becoming the OCCID identity of the represented object.

## Control

The Control model separates desired work from immediate operation:

```text
Objective
Directive
  Task
    TaskManeuver
    TaskEffect
    TaskInformation
    TaskTransport
  Command
    StateChangeCommand
    ProcessControlCommand
    ConfigurationCommand
    MotionCommand
    ResourceCommand
    ExecutionCommand
Plan
Constraint
Authority
Assignment
Execution
```

The central distinction is:

> **Task preserves intent. Command prescribes operation.**

Task specializations describe what should be achieved. Endpoint/runtime code decides how to realize supported work. Command families express precise immediate operations without importing one protocol's vocabulary into the shared model.

## Interoperability package

The distribution includes the existing `interop` package for deterministic representation conversion such as MAVSDK, MSP, and CoT mappings.

```python
from interop.mavsdk import goto_command_to_fields
```

Interop owns deterministic type/field/unit/frame conversion only. It does **not** own endpoint connections, operation selection, sequencing, retries, session lifecycle, recovery, or autonomy. Those remain consumer/runtime responsibilities.

## Permanent model IDs

Generated OCCID models have permanent numeric model IDs. They are durable registry identity for transient encoding and persisted model identity.

Model IDs are **not** semantic discovery and are not an ontology catalog. A numeric slot assigned to a model must not later be repurposed for an unrelated model merely because a class was removed.

## Transient encoding

`OCCIDModel.encode()` emits a compact MsgPack envelope:

```text
{
  model_id,
  fields
}
```

Nested models use the same model-ID-plus-fields form. `decode_model()` resolves the concrete model from its permanent model ID.

No global schema version is carried on every transient message. Schema-change detection belongs to the structural consumer contract.

## Structural consumer contract

A direct OCCID consumer keeps one generated root file:

```text
OCCID_CONTRACT
```

Generate or check it with the OCCID module actually installed in that Python environment:

```bash
python -m occid.contract generate .
python -m occid.contract check .
```

The receipt contains:

- one global structural hash for the current OCCID schema;
- recursive structural hashes for the OCCID symbols that consumer actually uses.

If the global hash changes but the consumer's used symbols do not, the consumer can still be structurally compatible. If a used symbol changed or disappeared, `check` reports the specific model names.

There is no compatibility-history database, schema archive, caller-supplied OCCID root, or version tag on every message. Git is history; the installed OCCID module is the contract source being checked.

## Generation

Canonical schema sources and the permanent model-ID registry generate the runtime Python models:

```bash
python generate.py
```

Generated output and the checked-in structural integrity marker must remain deterministic. Direct consumers should regenerate their own `OCCID_CONTRACT` whenever their OCCID usage changes.

## Design rule

OCCID should grow from demonstrated semantic requirements, not speculative taxonomy expansion. But "minimal" must not mean shallow: if a real consumer exposes a protocol-independent distinction that OCCID cannot truthfully represent, investigate the missing semantic depth instead of discarding the fact or copying the foreign protocol into the model.
