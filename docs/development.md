# OCCID development notes

This document describes the current repository mechanics.

These rules are implementation guidance for the present OCCID codebase. They are not a claim that every surrounding system boundary is permanent.

## Install and import

Install the repository in editable mode:

```bash
python -m pip install -e .
```

Consumers use the canonical namespace:

```python
from occid import Entity, EntityState, TaskInformation, Assignment, Execution
```

Generated runtime models live under `schema/` internally and are re-exported through `occid`.

## Semantic normalization

A protocol-native scalar should not enter the OCCID semantic model only because an external protocol exposes it.

At the current semantic boundary:

1. If OCCID already expresses the protocol-independent meaning, map into that model, enum, measurement, identity, relationship, or state.
2. If OCCID lacks the meaning but the concept is protocol-independent and operationally useful, treat the mismatch as evidence that the model may need refinement.
3. If a value is only useful for decoding, interoperability bookkeeping, diagnostics, or source-specific debugging, it can remain at the adapter boundary.
4. If meaning, units, reference, scale, identity scope, or clock basis are not known strongly enough, do not publish a false semantic claim.

Interop work should preserve the distinctions that matter to meaning. Examples include:

- identity;
- units;
- ranges and sign conventions;
- coordinate and body frames;
- altitude datums;
- time bases;
- sentinel values;
- optionality;
- stable definition versus changing state.

Protocol identity is not automatically operational identity.

MAVLink system/component IDs, CoT UIDs, endpoint-native IDs, and packet IDs can be useful for routing or provenance without automatically becoming the OCCID identity of the represented object.

## Interoperability helpers

The current `interop/` package contains deterministic representation helpers for MAVSDK, MSP, and CoT data.

For example:

```python
from interop.mavsdk import goto_command_to_fields
```

The helpers currently focus on deterministic conversion such as:

- fields;
- enums;
- units;
- scaling;
- coordinate frames;
- altitude references;
- sentinel values.

Runtime systems can build broader endpoint behavior around those mappings.

See [`../example_usage.py`](../example_usage.py) for a complete small example that begins with raw CoT and MAVLink data.

## Permanent model IDs

Generated OCCID models currently have permanent numeric model IDs.

They provide durable registry identity for transient encoding and persisted model identity.

The IDs are implementation registry identity. They are not a semantic discovery mechanism or a claim that the current model taxonomy is final.

A numeric slot assigned to a model must not later be reused for an unrelated model only because the previous class was removed.

## Transient encoding

`OCCIDModel.encode()` currently emits a compact MsgPack envelope:

```text
{
  model_id,
  fields
}
```

Nested models use the same model-ID-plus-fields representation.

`decode_model()` resolves the concrete model from its model ID.

Schema-change detection is handled separately by the structural consumer contract.

## Structural consumer contract

A direct OCCID consumer can keep one generated root file:

```text
OCCID_CONTRACT
```

Generate or check it with the OCCID module installed in that Python environment:

```bash
python -m occid.contract generate .
python -m occid.contract check .
```

`OCCID_CONTRACT` is generated output. Do not hand-edit its hashes.

The current workflow is:

```text
install or select the intended OCCID revision
    |
    v
python -m occid.contract generate .
    |
    v
commit OCCID_CONTRACT with the consumer change
    |
    v
CI regenerates it independently
    |
    v
the committed receipt must match
```

The receipt contains:

- one global structural hash for the current OCCID schema;
- recursive structural hashes for OCCID symbols used by the consumer.

A global schema change does not automatically mean every consumer changed structurally.

`check` reports changes to symbols used by that consumer.

Git remains the history of schema revisions. The installed OCCID module is the contract source being checked.

## Generation

Canonical schema sources and the model-ID registry generate the runtime Python models:

```bash
python generate.py
```

Generated output and structural integrity markers must remain deterministic.

The schema language is documented in [`../idl_spec.md`](../idl_spec.md).

## Development rule

OCCID should grow from demonstrated semantic requirements.

Do not add foreign protocol structure to the shared model only to make an adapter easier.

Also do not discard a useful protocol-independent distinction only to keep the model small.

When a real integration cannot be represented truthfully, investigate whether the semantic model is missing something.
