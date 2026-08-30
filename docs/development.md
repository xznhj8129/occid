# OCCID development notes

This document describes the current repository mechanics and development rules.

These rules apply to the present OCCID codebase. They do not claim that every surrounding system boundary or current model decomposition is permanent.

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

## Schema authority and semantic levels

[`../idl_spec.md`](../idl_spec.md) is the normative schema-language specification.

Authoritative schema sources live under `lib/schema/`. Generated Python under `schema/` is derived runtime output. Do not maintain generated files as a second independent schema.

The current IDL separates semantic meaning, schema structure, and runtime identity:

```text
semantic meaning        schema structure        runtime identity
----------------        ----------------        ----------------
ontology                models / fields         model_id
specialization          parent / variants       serialization
vocabulary              enums                    wire values
```

These are different concerns.

Every model is currently classified as either:

- `ontology` - a semantic kind represented by the ontology;
- `specialization` - a practical typed shape needed by software without claiming a new ontological primitive.

Enums are the controlled-vocabulary level.

Structural inheritance does not by itself make an ontological claim. `parent` means field inheritance. `variants` means explicit typed-family membership. `model_id` identifies a concrete runtime model. None of those mechanisms should be treated as a substitute for semantic classification.

A practical specialization is justified when members of one semantic kind need materially different fields, constraints, or restricted vocabularies to be represented safely and usefully.

Do not create a new ontology class only because software needs a convenient struct. Do not create a new model for every vocabulary word only to obtain type safety.

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

A source field name does not establish its semantic meaning. For example, a value called `rssi` is not automatically dBm, a speed is not automatically airspeed, and a protocol timestamp is not automatically wall-clock time.

Protocol identity is not automatically operational identity.

MAVLink system/component IDs, CoT UIDs, endpoint-native IDs, and packet IDs can be useful for routing or provenance without automatically becoming the OCCID identity of the represented object.

An existing protocol-shaped OCCID field is not precedent for adding another one. It can be historical residue that should be corrected.

### Semantic-depth refinement

OCCID is intended to remain minimal but semantically deep.

A concept should enter the shared model because real semantic requirements need it, not because one source protocol happens to expose a field. But keeping the model small is not a reason to discard a useful protocol-independent distinction.

External protocols, APIs, sensors, databases, and standards are therefore also stress tests of the model.

When a real integration does not fit cleanly:

1. determine what the source datum actually means;
2. restate that meaning without relying on the source field name or encoding;
3. try to express it using existing OCCID primitives, relations, measurements, state, composition, or vocabulary;
4. if the meaning is protocol-independent and still does not fit, investigate a missing primitive, relation, structure, or vocabulary;
5. only then classify the datum as protocol-local bookkeeping, provenance, decoding state, or diagnostics if that is what it really is.

A mapping failure can expose a shallow part of OCCID. It is evidence to investigate, not automatic proof that the datum belongs in the core model and not automatic proof that it should be discarded.

## Identity, definition, and state

Persistent record identity and operational identity are different.

`RecordMeta.uid` is the global UID of one persisted record instance or revision, and `RecordMeta.id` is its class-local Record ID. The logical object described by that record has its own `uid` and class-local `id`. Entity 38, Track 38, and Task 38 may all exist simultaneously: their integer IDs are scoped to their semantic classes, while their UIDs are globally unique.

Durable cross-object references use UIDs. Class-local IDs are for class-scoped lookup and human/operator use; they must not be mixed with UIDs or treated as globally unique.

Do not treat record identity, logical-object identity, class-local ID, external or protocol identifiers, or transport addresses as interchangeable aliases.

Stable definition and changing observation or assessment are also different concerns.

A definition should not acquire mutable runtime state only because an application wants to display progress beside it. Current contract tests enforce this distinction in places such as success criteria and plan-step definitions. Runtime progress and assessment use state records instead.

Likewise, an embedded value does not automatically need persistent operational identity. Give a value independent identity when the operational system needs to name, reference, revise, relate, or persist it as a thing in its own right.

## Execution evidence

Transport delivery, semantic executor acceptance, execution progress, and terminal completion are distinct facts.

```text
transport delivery
    != semantic acceptance
    != execution progress
    != execution completion
```

A delivered message does not prove that an executor accepted the work. Acceptance does not prove that the work started or succeeded.

Current `ExecutionAcceptance` and `ExecutionStatusReport` models preserve those distinctions explicitly.

## Consumer semantic authority

Consumers use OCCID semantics. They do not become a second authority for those semantics.

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

Within these helpers, the same semantic input should produce the same representation output without network access, endpoint state, or hidden runtime policy.

The current interop package performs type and structure conversion. Endpoint I/O, operation selection, sequencing, retries, session lifecycle, recovery, and autonomy can be built by runtimes around those mappings rather than hidden inside the conversion functions.

External protocol or API method names do not automatically become OCCID model classes. Translate the operational meaning, not the convenience name of one endpoint call.

See [`../example_usage.py`](../example_usage.py) for a complete small example that begins with raw CoT and MAVLink data.

## Model IDs

Generated OCCID models currently have numeric model IDs.

They provide registry identity for transient encoding and persisted model identity.

The IDs are implementation registry identity. They are not a semantic discovery mechanism, an ontology catalog, inheritance, or variant-family membership.

During Year Zero, model IDs are part of the current generated contract, not compatibility promises. If a model is removed, its numeric slot may be reused immediately as part of the same schema change. Regenerate affected outputs and consumers together; do not preserve tombstones or compatibility reservations for removed internal models.

## Transient encoding

`OCCIDModel.encode()` currently emits a compact MsgPack envelope:

```text
[
  model_id,
  {
    field_ordinal: value,
    ...
  }
]
```

Nested OCCID models use the same shape. UIDs are encoded as 16 raw bytes, enums and flags use numeric wire values, and unset fields are omitted. Field ordinals are the zero-based effective generated field order, including inherited fields; the compact wire carries no model names, field names, or UUID text.

`decode_model()` resolves the concrete model from its model ID. Peers using this encoding are expected to share the same structural contract.

The transient envelope does not carry one global schema version on every message.

Schema compatibility is a consumer/build concern, not a per-message field. Schema-change detection is handled separately by the structural consumer contract.

Transient encoding is not a promise that old payloads can be treated as durable storage forever. Durable persistence and migration policy must be explicit where an application needs them.

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

Do not keep parallel writable semantic representations only to postpone updating consumers. If a compatibility or migration boundary is needed, make it explicit instead of allowing two competing meanings to become authoritative.

When a real integration cannot be represented truthfully, investigate whether the semantic model is missing something.
