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

## Schema authority and semantic roles

[`../idl_spec.md`](../idl_spec.md) is the normative schema-language specification.

Authoritative authored schemas live under `lib/schema/`. Models have exactly two authored roles:

```text
Concept          semantic category in the ontology
Representation   explicit data-bearing shape
Vocabulary       enum / closed controlled values
```

```yaml
semantic_role: concept
semantic_role: representation
```

There is no authored or compiler-derived `Type` semantic level. Whether a name may appear in a runtime field is not an ontological category. Concepts and Representations are both nominal semantic nodes and may be referenced by fields.

`parent` is the single source of truth for the model tree. If a model declares `parent: X`, it means that model **is a kind of X** and inherits `X` fields where applicable. There is no authored reverse child list and no `variants` membership graph. The compiler derives direct `children` from `parent`.

Atomic Representations are the direct form for named single values:

```yaml
IntID:
  semantic_role: representation
  parent: ID
  type: int

UID:
  semantic_role: representation
  parent: ID
  type: bytes[16]
```

Do not create a one-field wrapper merely to give a value semantic identity. `type:` and `fields:` are mutually exclusive. An atomic Representation cannot inherit fields and cannot be a parent because its value shape is complete. Fixed binary forms such as `bytes[16]` are exact binary values; text coercion is not part of the representation.

The runtime generation path is deliberately one-way:

```text
lib/schema/**/*.schema.yaml
        -> compile_occid.py
        -> occid.yaml
        -> generate_pydantic.py
        -> schema/*.py
```

`compile_occid.py` resolves effective inherited fields for record models and emits one flat `occid.yaml`. All Concepts and Representations live together under one compiled `models` mapping; each model preserves its `semantic_role` and authored `parent`, and direct `children` are derived from that parent graph. Named field references remain exactly as authored; the compiler never expands a semantic parent into a descendant union.

`generate_pydantic.py` reads only `occid.yaml`. Record-shaped runtime models derive directly from `OCCIDModel`; atomic Representations derive from `OCCIDValue[T]`. No generated Python class inherits another OCCID model class. Generated models expose `__occid_parent__` and `__occid_children__`, while `is_a()` follows that semantic registry independently of Python inheritance.

A model-valued field is generated as a nominal semantic reference. For example, authored `condition: Condition` remains semantically `Condition`; a concrete `Predicate` value is accepted because `Predicate is_a Condition`, not because the generator rewrote the field into a union of current descendants.

Consumer structural hashes describe data shape rather than taxonomy metadata. Reparenting or adding a child does not change an existing symbol hash unless its effective fields or another real data dependency change. The complete `occid.yaml` fingerprint still changes, so compact-wire peers can detect a different compiled contract.

There is no separate authoritative `ontology.yaml`. The Concept tree is derived from the authored schemas so there is only one semantic source of truth.

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

`Record.uid` is the global UID of one persisted record instance or revision, while the logical object described by that record has its own identity. A UID is globally self-contained. An integer ID is not: `IntID(Namespace)` makes its namespace explicit in the schema. `Entity.38`, `Track.38`, and `Task.38` are therefore distinct even though their integer values match.

The namespace is authored at each use, for example `id: IntID(Entity)`, `task_id: IntID(Task)`, or `assignee_id: IntID(Entity)`. It is not inferred from field names, the containing model, ancestry, or the Concept that first declares a field. An ID field does not necessarily identify the object containing it; it may reference an object in another namespace. The runtime `IntID` value remains only an integer, while generated type metadata preserves the schema-defined namespace.

Durable cross-object references generally use UIDs. Namespaced IntIDs are compact operational references for namespaces that need short stable handles; not every UID-bearing model requires an IntID. Plain integers may still be local ordinals or keys when they are not OCCID identities.

Identity field names are type claims: `uid` and `*_uid` are OCCID `UID` values; OCCID namespaced integer identities use `IntID(Namespace)`. A string is never an OCCID ID. Protocol tokens, external identifiers, correlation values, addresses, names, codes, labels, and similar strings must be named for what they actually are, such as `*_ref`, `*_address`, `*_code`, or `*_name`.

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

Every compiled Concept and Representation has a numeric model ID used as a compact runtime/wire discriminator.

The compiler derives these IDs deterministically from the complete emitted model set: emitted model names are sorted canonically and numbered from 1. The generated `occid.yaml` is the sole source of truth for those IDs. There is no hand-maintained model-ID registry.

Model IDs are contract-local implementation identity. They are not semantic discovery, Concept ancestry, semantic ancestry, or durable identity for the thing represented by a model. Adding, removing, or renaming an emitted model may renumber other models. That is acceptable because compact peers are already required to share the same OCCID structural contract.

During Year Zero, model IDs are not compatibility promises and no tombstones or numeric reservations are preserved. Regenerate affected outputs and consumers together.

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

Nested record-shaped OCCID models use the same model-ID-plus-field-map shape. Atomic Representations use their underlying value directly when the containing field has an exact atomic type; heterogeneous atomic values carry their model ID with the value. `UID` is consequently encoded as 16 raw bytes in an exact `UID` field because the schema declares `UID` as `bytes[16]`, not because the serializer knows anything special about UUIDs. Enums and flags use numeric wire values, and unset fields are omitted. Field ordinals are the zero-based effective generated field order, including inherited fields; the compact wire carries no model names or field names.

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

Canonical schema sources generate the compiled contract and runtime Python models:

```bash
python generate.py
```

Generated output and structural integrity markers must remain deterministic.

The schema language is documented in [`../idl_spec.md`](../idl_spec.md).

## Development rule

### Lossless named boundary codec

`occid.named` supplies the shared human/API/persistence boundary codec. Use
`to_data` / `from_data` for JSON-compatible Python values and `dumps` / `loads`
for JSON text. `Named[T]` integrates the same validation with Pydantic request
models. It is separate from the compact-wire codec.

```python
from occid import UID
from occid.named import dumps, loads

value = UID(bytes.fromhex("0180ff102030405060708090a0b0c0d0"))
assert loads(dumps(value)) == value
```

Models carry concrete names, and enums carry symbolic names. Nested semantic
references retain their concrete model. Atomic UID values use 32 lowercase hex
digits. Tagged forms preserve large integers, arbitrary bytes, tuples, unusual
map keys, and otherwise JSONB-incompatible text. Only explicitly set model
fields are serialized, preserving omitted versus explicitly null fields.
Malformed values, unknown symbols, and non-finite numbers raise `CodecError`.

Durable callers must not replace these names with compact-wire numeric model
IDs. The codec does not select database collections or application operations.

OCCID should grow from demonstrated semantic requirements.

Do not add foreign protocol structure to the shared model only to make an adapter easier.

Also do not discard a useful protocol-independent distinction only to keep the model small.

Do not keep parallel writable semantic representations only to postpone updating consumers. If a compatibility or migration boundary is needed, make it explicit instead of allowing two competing meanings to become authoritative.

When a real integration cannot be represented truthfully, investigate whether the semantic model is missing something.
