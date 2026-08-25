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

The repository `VERSION` identifies a release. It is provenance, not a consumer compatibility test.

Structural compatibility is determined by the consumer contract described below.

## Semantic normalization

A protocol-native scalar should not enter the OCCID semantic model only because an external protocol exposes it.

At the current semantic boundary:

1. If OCCID already expresses the protocol-independent meaning, map into that model, enum, measurement, identity, relationship, or state.
2. If OCCID lacks the meaning but the concept is protocol-independent and operationally useful, treat the mismatch as evidence that the model may need refinement.
3. If a value is only useful for decoding, interoperability bookkeeping, diagnostics, or source-specific debugging, it can remain at the adapter boundary.
4. If meaning, units, reference, scale, identity scope, or clock basis are not known strongly enough, do not publish a false semantic claim.

Do not use `native_*` fields, arbitrary metadata, generic telemetry bags, or raw protocol codes as escape hatches from semantic modeling.

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

## Consumer semantic authority

Consumers should not maintain independent copies of OCCID semantic vocabularies when the information can come from the installed OCCID model.

Do not duplicate OCCID enum members, infer semantic names from enum ordinal positions, or maintain local copies of supported OCCID model lists as a second semantic authority.

Presentation-local constants remain application concerns.

A useful review rule is:

> If changing one OCCID semantic fact requires manually changing the same semantic fact in a consumer, check whether the authority boundary is wrong.

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

The transient envelope does not carry one global schema version on every message.

Schema compatibility is a consumer/build concern, not a per-message field. Schema-change detection is handled separately by the structural consumer contract.

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

`OCCID_CONTRACT` is generated output. Do not hand-edit or manually calculate its hashes.

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

CI is a verifier, not an updater. It regenerates `OCCID_CONTRACT` and verifies that the checked-in receipt does not change. A changed generated receipt is expected repository content and must be committed with the consumer change.

The receipt contains:

- one global structural hash for the current OCCID schema;
- recursive structural hashes for OCCID symbols used by the consumer.

Compatibility is structural and consumer-specific.

The global schema hash can change while the OCCID symbols used by one consumer remain structurally unchanged.

`check` reports changes to symbols used by that consumer.

Git remains the history of schema revisions. The installed OCCID module is the contract source being checked.

There is no separate compatibility archive, lock directory, caller-supplied OCCID root, or schema-version ladder required by this mechanism.

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
