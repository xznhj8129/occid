# OCCID YAML IDL Specification

## 1. Purpose and authority

This document defines the OCCID schema language.

The language is a custom interface-definition language carried in YAML. YAML provides syntax only; YAML itself does not define OCCID schema semantics.

This specification is normative. The parser, validator, generator, generated runtimes, and authored schemas are expected to conform to it. If an implementation accepts invalid syntax, silently ignores a declared constraint, or generates behavior inconsistent with this document, that is an implementation bug rather than an extension of the language.

The language separates authored semantic meaning from compiled runtime representation.

OCCID uses four semantic levels:

```text
Concept          authored semantic category
Type             derived childless Concept; concrete at the current semantic frontier
Representation   authored explicit data-bearing shape
Vocabulary       authored closed controlled values (enums)
```

`Type` is never authored as a `semantic_role`. It is derived by the compiler. A Concept is a Type when it has no Concept children; Representation children do not make a Concept non-leaf.

The authored hierarchy is compiler input. Runtime model identity and serialization apply only to compiled Types and Representations.

---

## 2. Mental model

An authored OCCID schema is built from three declaration kinds:

```text
MODEL
    A named Concept or Representation.

ENUM
    A closed controlled Vocabulary.

MAP
    A named typed constant mapping.
```

Compilation derives Types from childless Concepts, resolves inherited fields and Concept references, and emits the flat runtime schema `occid.yaml`.

Two model relationships are distinct:

```text
parent
    Structural inheritance: the child inherits the parent's fields.

variants
    Explicit typed-family membership: the parent declares which structural
    children belong to its polymorphic variant family.
```

Runtime `model_id` values identify compiled Types and Representations on the wire. A model ID does not establish Concept ancestry or variant-family membership.

Schema documents are either:

```text
schema
    Part of the core OCCID schema.

module
    An optional extension package that adds declarations to the core schema.
```

There is no profile language.

---

## 3. YAML carrier subset

IDL documents use YAML 1.2.

Allowed YAML constructs:

- mappings
- sequences
- plain scalars
- quoted scalars
- comments

Forbidden YAML constructs:

- anchors
- aliases
- YAML tags
- flow-style mappings or lists
- duplicate keys
- tabs

Unknown IDL keys are errors at every level where an allowed-key set is defined. An implementation must not silently discard an unknown key.

Comments have no schema meaning and need not survive generation.

---

## 4. Identifiers and namespace

Identifiers use:

```text
^[A-Za-z_][A-Za-z0-9_]*$
```

This rule applies to:

- package names
- model names
- enum names
- map names
- field names
- enum member names

All loaded model, enum, and map names share one global schema namespace and must be unique.

Field names must be unique within the effective model shape, including inherited fields.

References to models, enums, or maps must resolve in the loaded schema.

---

## 5. Documents

### 5.1 Core schema document

A core schema document has `type: schema`.

Allowed top-level keys:

- `version` — required
- `type` — required, must be `schema`
- `package` — required
- `root` — required
- `tags` — required
- `enums` — optional
- `maps` — optional
- `models` — optional

Example:

```yaml
version: 1
type: schema
package: state
root: State
tags:
  - core

models:
  State:
    description: "Current condition of an object or process."
    semantic_role: concept
    parent: Data
```

Rules:

- `root` must name a model declared in the same document.
- The root model must have a `description`.
- `package` identifies the generated package/module for the document.
- In the OCCID repository, a schema document's `package` must match its filename without `.schema.yaml`.
- `requires` and `extend_variants` are not valid on core schema documents.
- Core schema documents are always part of the core schema; tags do not make core documents optional.

### 5.2 Module document

A module document has `type: module`.

Allowed top-level keys:

- `version` — required
- `type` — required, must be `module`
- `package` — required
- `description` — optional
- `tags` — required
- `requires` — optional
- `extend_variants` — optional
- `enums` — optional
- `maps` — optional
- `models` — optional

Example:

```yaml
version: 1
type: module
package: ew
description: "Electronic-warfare schema extensions."
tags:
  - military
requires:
  - core
```

A module extends a loaded schema. It does not override or redefine existing declarations.

---

## 6. Primitive types

Built-in primitive types are:

```text
string
bool
bytes
float
int
int8
int16
int32
int64
uint8
uint16
uint32
uint64
any
```

Named values such as `UID` are not primitives. They are ordinary authored Representations and must be declared in the schema. For example, the core schema declares `UID` as an atomic Representation with `type: bytes[16]`.

Integer-width types are semantic ranges, not aliases for an unrestricted integer:

| Type | Range |
| --- | --- |
| `int8` | -128 .. 127 |
| `int16` | -32768 .. 32767 |
| `int32` | -2147483648 .. 2147483647 |
| `int64` | -9223372036854775808 .. 9223372036854775807 |
| `uint8` | 0 .. 255 |
| `uint16` | 0 .. 65535 |
| `uint32` | 0 .. 4294967295 |
| `uint64` | 0 .. 18446744073709551615 |

Generated runtimes must enforce those ranges.

`int` is an implementation-sized/general integer with no narrower OCCID range claim.

`any` is an escape hatch for genuinely unconstrained data. It should not be used where a concrete OCCID type exists.

---

## 7. Type expressions

Supported type expressions include:

```text
UID
IntID(Entity)
string
bytes[16]
ExampleKind
GlobalPosition
list[UID]
list[string]
list[GlobalPosition]
map[string, string]
map[string, GlobalPosition]
tuple[float, float]
tuple[string, int, bool]
A | B
A | B | C
optional string
optional (A | B)
const ExampleKind
const map[string, GeometryTypes]
```

Semantics:

- `IntID(Namespace)` — an `IntID` interpreted in the explicitly named OCCID namespace. The runtime value is only the integer; the namespace is part of the schema type expression and is not repeated in each value. The namespace is independent of the containing model and does not imply that the identifier refers to the containing instance.
- `bytes[N]` — exactly `N` binary bytes; `N` must be a positive integer. Text is not a valid `bytes[N]` value and runtimes must not silently coerce text into it.
- `list[T]` — variable-length ordered homogeneous collection.
- `map[K, V]` — mapping from `K` to `V`.
- `tuple[T1, T2, ...]` — fixed-length ordered heterogeneous collection.
- `A | B` — union of the listed types.
- `optional T` — field may be omitted or explicitly null; when non-null it must satisfy `T`.
- `const T` — field has one schema-defined value and callers cannot supply a different value.

Rules:

- `optional const T` is invalid.
- Repeating `optional` or `const` is invalid.
- Anonymous inline object/model declarations are not supported.
- Referenced named types must resolve.
- `IntID(Namespace)` is the form for an integer identity whose OCCID namespace is part of the contract. Bare `IntID` carries no namespace semantics and must not be interpreted as `Namespace.id` by convention.
- The `Namespace` in authored `IntID(Namespace)` must name an authored OCCID model. The compiler validates it and preserves the name exactly in `occid.yaml`, even when that Concept is not itself emitted as a runtime model.
- Parentheses on a named type are semantic arguments and are currently valid only for `IntID(Namespace)`. Square brackets remain structural type syntax.
- Bracketed arguments are valid only for `bytes[N]`, `list[T]`, `map[K, V]`, and `tuple[T1, T2, ...]`; malformed arity is rejected by the IDL parser.

A useful grammar sketch is:

```text
TypeExpr    := [Qualifier] UnionExpr
Qualifier   := "optional" | "const"
UnionExpr   := Atom ("|" Atom)*
Atom        := Identifier
             | "IntID(" Identifier ")"
             | "bytes[" PositiveInteger "]"
             | "list[" TypeExpr "]"
             | "map[" TypeExpr "," TypeExpr "]"
             | "tuple[" TypeExpr ("," TypeExpr)+ "]"
             | "(" UnionExpr ")"
```

---

## 8. Enums: vocabulary level

Every enum is a controlled vocabulary by definition. Enums do not carry `semantic_role`.

Syntax:

```yaml
enums:
  InformationIntent:
    - SEARCH = 0
    - OBSERVE
    - IDENTIFY
    - CLASSIFY

  PermissionFlags:
    - READ = 1 << 0
    - WRITE = 1 << 1
    - EXECUTE = 1 << 2
```

Allowed member forms:

```text
NAME
NAME = INTEGER
NAME = 1 << INTEGER
```

String-backed enum values are not part of the OCCID IDL. The enum member name already provides the stable symbolic label; external textual spellings belong in adapters or explicit mappings.

### 8.1 Ordinary enums

For an ordinary enum:

- If the first member has no explicit value, it receives `0`.
- A later member without an explicit value receives the previous numeric value plus one.
- Explicit integer assignments may create gaps.
- Member names must be unique.
- Numeric values must be unique.

Example:

```yaml
TaskPhase:
  - CREATED
  - DISPATCHED
  - RUNNING = 10
  - DONE_OK
```

has values `0`, `1`, `10`, `11`.

### 8.2 Bitflag enums

An enum using `1 << N` is a bitflag vocabulary.

For a bitflag enum:

- every member must have an explicit bit value;
- each value must contain exactly one set bit;
- bit positions must be unique.

A generated runtime should expose a flag type appropriate to the target language.

---

## 9. Models and semantic levels

Model syntax:

```yaml
models:
  RecordRepresentation:
    description: "Human-readable purpose."
    semantic_role: representation
    parent: ParentModel
    fields:
      field_a: string
      field_b: optional string

  AtomicRepresentation:
    description: "One directly typed value."
    semantic_role: representation
    parent: ParentModel
    type: bytes[16]
```

Allowed model keys:

- `description`
- `semantic_role`
- `parent`
- `type`
- `fields`
- `variants`

Unknown model keys are errors.

### 9.1 Authored semantic roles

Every authored model must declare exactly one of:

```text
semantic_role: concept
semantic_role: representation
```

The four levels are:

```text
Level 1 — Concept
    An authored semantic category. Concept ancestry states what a thing is and
    provides fields inherited by more specific Concepts and Representations.

Level 2 — Type
    A derived Concept with no Concept children in the loaded schema. A Type is
    the most specific semantic classification currently available at that branch
    and is emitted as a flat runtime model. Type is not an authored semantic_role.

Level 3 — Representation
    An authored explicit data-bearing shape required by software. A Representation
    may be record-shaped (`fields`) or atomic (`type`). It may attach anywhere in
    the model graph without claiming a new Concept. It is always emitted as a flat
    runtime model.

Level 4 — Vocabulary
    A closed controlled value set represented by an enum. Vocabulary is identified
    by declaration kind and has no semantic_role.
```

A Concept remains a Type even if it has Representation children. Only a Concept child makes its parent a non-leaf Concept. This lets a semantic branch be usable before it is subdivided further without inventing a meaningless wrapper Representation.

`semantic_role` applies only to authored models. Omission is invalid. A `representation` must declare a `parent`.

The engineering criterion for introducing a Representation is that software needs an explicit data-bearing shape distinct from the Concept itself: materially different fields, one named atomic value, constraints, restricted vocabulary, or another concrete layout requirement.

An atomic Representation declares `type` instead of `fields`. It says that the named Representation **is exactly one value of that type**, rather than a record containing a one-field wrapper. `type` and `fields` are mutually exclusive, and model-level `type` is valid only on `semantic_role: representation`.

Canonical atomic example:

```yaml
models:
  ID:
    semantic_role: concept
    parent: Struct
    variants:
      - IntID
      - UID

  IntID:
    semantic_role: representation
    parent: ID
    type: int

  UID:
    semantic_role: representation
    parent: ID
    type: bytes[16]
```

`IntID` is an atomic integer Representation. A use of it supplies the namespace in the field type, for example `id: IntID(Entity)` or `task_id: IntID(Task)`. The namespace belongs to the schema declaration, not to each runtime `IntID` value.

`UID` therefore has an exact 16-byte value shape. UUIDv4, UUIDv7, random allocation, deterministic allocation, or any other producer policy is outside the Representation definition unless explicitly modeled elsewhere.

Canonical example:

```yaml
enums:
  InformationIntent:
    - SEARCH
    - OBSERVE

models:
  Task:
    semantic_role: concept
    parent: Directive

  TaskInformation:
    semantic_role: representation
    parent: Task
    fields:
      intent: InformationIntent
```

If `Task` has no Concept children, compilation emits both:

```text
Task                    Type (derived from childless Concept)
TaskInformation         Representation
SEARCH / OBSERVE        Vocabulary
```

If a Concept child is later added beneath `Task`, `Task` stops being a Type automatically while `TaskInformation` remains an emitted Representation.

### 9.2 Compilation semantics

The authoritative authored schemas live under `lib/schema/`. They compile to one flat generated runtime schema:

```text
lib/schema/**/*.schema.yaml
        |
        v
compile_occid.py
        |
        v
occid.yaml
        |
        v
generate_pydantic.py
        |
        v
schema/*.py
```

`occid.yaml` contains only:

- `types` — derived childless Concepts;
- `representations` — authored Representations;
- `vocabulary` — enums;
- `maps` — named constant maps.

For record-shaped models, the compiler resolves inherited effective fields before emission. For atomic Representations, the compiler lowers the model-level `type` expression directly. `parent`, `variants`, and authored `semantic_role` do not survive into `occid.yaml`. Generated target-language classes are flat projections of the compiled models, not an executable copy of the Concept hierarchy.

Each compiled Representation contains either `fields` or `type`, never both. A compiled atomic Representation therefore remains visibly atomic in `occid.yaml`:

```yaml
representations:
  UID:
    package: struct
    type: bytes[16]
```

Field references compile according to the referenced level:

```text
non-leaf Concept reference   -> union of emitted descendants
Type reference               -> exact Type
Representation reference     -> exact Representation
Vocabulary / primitive       -> exact
```

A Representation reference is never widened merely because another Representation descends from it.

---

## 10. Fields

A record-shaped model's `fields` mapping declares fields owned by that model. Inherited fields come from `parent`.

An atomic Representation uses model-level `type` instead and has no fields. Do not encode a single atomic value as a synthetic field such as `value: T`; declare `type: T` on the Representation itself.

### 10.1 Shorthand form

Supported shorthand forms:

```yaml
name: string
remarks: optional string
speed_ms: float = 0.0
kind: const ExampleKind = PRIMARY
path: list[GlobalPosition]
```

Rules:

- Scalar and enum defaults may use shorthand.
- Structured list/map/object defaults must use expanded form.
- A const field must declare its fixed value.

### 10.2 Expanded form

Expanded field syntax:

```yaml
pwm:
  type: int
  min: 900
  max: 2100
  default: 1500
  description: "PWM pulse width in microseconds."

alphabet:
  type: list[string]
  default:
    - a
    - b
    - c
```

Allowed expanded-field keys:

- `type` — required
- `default` — optional
- `value` — optional; used only for `const` fields
- `description` — optional
- `min` — optional numeric inclusive minimum
- `max` — optional numeric inclusive maximum

Unknown expanded-field keys are errors.

Rules:

- `default` and `value` are mutually exclusive.
- `value` requires a `const` type.
- A `const` type requires `value` in expanded form or `= VALUE` in shorthand.
- `min` and `max` are valid only for numeric scalar fields.
- `min <= max` is required when both are present.
- A default or const value must satisfy the field's type and constraints.
- Generated runtimes must enforce `min` and `max`; accepting them and then discarding them is non-conforming.
- `required: true/false` is not supported. Presence is expressed by the type/default semantics below.

### 10.3 Presence semantics

A field is **required** when it is not `optional`, not `const`, and has no default.

An `optional T` field:

- may be omitted;
- defaults to null when omitted unless another default is explicitly provided;
- may be explicitly null;
- otherwise must contain `T`.

A defaulted non-optional field may be omitted, in which case its default is applied.

A const field may be omitted, in which case its fixed value is supplied. Supplying any other value is a validation error.

---

## 11. Authored inheritance: `parent`

`parent` defines the single authored ancestry used to inherit fields before compilation.

For a Concept child, `parent` is semantic `is-a` ancestry as well as field inheritance. For a record-shaped Representation, `parent` identifies the Concept or Representation whose effective fields form the base of that data shape. For an atomic Representation, `parent` attaches the value shape to its semantic ancestry, but that ancestry must contribute no fields. Representation parentage does not create a new Concept.

Example:

```yaml
models:
  Data:
    semantic_role: concept
    fields:
      timestamp: float

  Observation:
    semantic_role: concept
    parent: Data
    fields:
      source_ref: UID
```

Every emitted descendant of `Observation` receives both `timestamp` and `source_ref` after flattening. No generated runtime class needs to inherit from `Data` or `Observation`.

Rules:

- A model has at most one parent.
- The parent must resolve to a model.
- Ancestry cycles are errors.
- A child inherits all parent fields into its effective compiled shape.
- An atomic Representation may not declare or inherit fields.
- An atomic Representation may not be used as a parent; its value shape is complete.
- Concept parentage expresses semantic ancestry.
- Representation parentage is representational attachment and does not by itself create a Concept.
- `parent` does not by itself add the child to an explicit `variants` family.

---

## 12. Explicit typed families: `variants`

`variants` explicitly declares which structural children belong to a model's typed polymorphic family.

Example:

```yaml
models:
  Result:
    variants:
      - SuccessResult
      - FailureResult

  SuccessResult:
    parent: Result
    fields:
      value: string

  FailureResult:
    parent: Result
    fields:
      reason: string
```

This states two independent facts:

```text
SuccessResult parent Result
    -> SuccessResult inherits Result structure.

Result variants SuccessResult
    -> SuccessResult is an explicit member of Result's typed family.
```

Both declarations are intentional. The duplication makes the family explicit and validates both ends of the relationship.

Rules:

- `variants` is a list of model names.
- `variants: []` is valid and declares an empty family/extension point.
- Every listed variant must exist.
- Every listed variant must declare `parent` equal to the declaring parent.
- A structural child not listed in `variants` is not implicitly a member of the variant family.
- A model may itself be a variant and also declare its own variants.
- Derived family cycles are errors.
- Duplicate variant membership is an error.

For a field typed as a model with an explicit variant family, polymorphic schema handling may admit the parent model and models reachable through that explicit variant relation. Structural descendants that are not members of the explicit family are not implicitly admitted by the IDL contract.

### 12.1 No implicit discriminator enum

`variants` does not create a second semantic vocabulary and does not require a generated `{Model}_type` enum.

A target runtime may use its ordinary concrete-model mechanism, including OCCID `model_id`, to encode which concrete variant instance is present. That runtime mechanism does not replace or define the schema-level `variants` relationship.

In short:

```text
parent      = field inheritance
variants    = explicit family membership
model_id    = concrete runtime/wire identity
```

---

## 13. Constant maps

A named constant map is declared under `maps`:

```yaml
maps:
  GeometryByName:
    type: map[string, GeometryTypes]
    value:
      Point: POINT
      Polygon: POLYGON
```

Allowed map keys:

- `type`
- `value`

Rules:

- `type` is required and must be `map[K, V]`.
- `value` is required and must be a YAML mapping.
- Every key must satisfy `K`.
- Every value must satisfy `V`.
- Enum names in map values resolve to enum members, not arbitrary strings.
- Unknown map declaration keys are errors.

Constant maps are schema constants. They are not models and have no runtime model ID.

---

## 14. Modules

Modules are optional schema extensions.

A module may add:

- models
- enums
- maps
- variant-family members through `extend_variants`

A module may not:

- redefine an existing declaration;
- alter an existing field;
- remove a core declaration;
- override an enum member;
- change the parent of an existing model.

### 14.1 Module model attachment

Every model declared by a module must attach to the loaded structural model graph through `parent`.

The parent may be:

- a core model; or
- a model provided by a required module.

A module must not introduce floating parentless models.

A module may introduce a new local branch by attaching its first model to an existing loaded parent and then deriving additional module-local models beneath it.

### 14.2 Tags

`tags` are labels used to classify and select modules and to satisfy tag-based dependencies.

There is no `profile`, `include`, `exclude`, `include_all`, or `exclude_untagged` IDL construct.

Core schema documents may carry tags for classification, but core schema loading is not controlled by tags.

A reference implementation may select optional modules by package name, tag, or an "all modules" mode.

### 14.3 Dependencies: `requires`

A module's `requires` list contains package names or tags.

Resolution rules:

1. `core` is always satisfied by the core schema.
2. If a requirement matches an available module package name, that module is required.
3. Otherwise the requirement is treated as a tag, and available modules carrying that tag are selected to satisfy the dependency.
4. Dependencies are resolved transitively before schema validation.
5. An unsatisfied requirement is an error.

A module may reference declarations only from core, itself, or dependencies that are resolved before it.

### 14.4 Extending explicit variant families

A module may add children to an existing model's variant family:

```yaml
extend_variants:
  ExistingParent:
    - NewChild
```

Rules:

- The parent must resolve to a loaded model.
- The child must be declared by the module or one of its resolved dependencies.
- The child must declare `parent: ExistingParent`.
- `extend_variants` may create the parent's explicit variant family if the parent did not previously declare one.
- If the parent already has a family, the new members are appended to it.
- Adding an already-present member is an error.
- A variant extension must not alter the parent's structural fields or semantic role.

`extend_variants` therefore extends explicit family membership; it does not modify inheritance.

---

## 15. Validation requirements

A conforming implementation must reject at least the following:

### Document and YAML errors

- forbidden YAML constructs;
- duplicate YAML keys;
- unknown top-level IDL keys;
- missing required document keys;
- invalid `type`;
- `root` on a module document;
- missing `root` on a schema document;
- schema `root` not declared in that document;
- schema root model missing a `description`;
- `requires` or `extend_variants` on a core schema document.

### Naming and reference errors

- invalid identifier syntax;
- duplicate declaration names in the loaded global namespace;
- unknown model/enum/map/type references;
- unknown parent;
- inheritance cycles.

### Enum errors

- enum declaration not expressed as a list;
- duplicate member names;
- duplicate values;
- invalid enum member syntax;
- mixed/invalid bitflag values;
- string-backed enum values.

### Model errors

- unknown model keys;
- missing `semantic_role`;
- invalid `semantic_role`;
- `representation` without a parent;
- model-level `type` on anything other than a Representation;
- model declaring both `type` and `fields`;
- atomic Representation with inherited fields;
- atomic Representation used as a parent;
- atomic Representation declaring variants;
- redefining an inherited field;
- invalid or cyclic variant-family declarations;
- variant whose structural parent does not match the declaring family.

### Field errors

- unknown expanded-field keys;
- invalid type expression;
- non-positive `bytes[N]` length;
- `optional const`;
- const field without a fixed value;
- `value` on a non-const field;
- `default` and `value` together;
- `min`/`max` on nonnumeric fields;
- `min > max`;
- default or const value outside declared type/range constraints;
- structured shorthand defaults where expanded form is required;
- unsupported `required:` metadata.

### Module errors

- unsatisfied dependency;
- parentless module model;
- module redefinition/override of an existing declaration;
- module model parent not available through core or resolved dependencies;
- invalid `extend_variants` parent or child;
- duplicate variant-family extension.

Silently accepting any of these and dropping the invalid information is non-conforming behavior.

---

## 16. Generated model identity and serialization

### 16.1 Model IDs

Every compiled Type and Representation has a numeric OCCID model ID generated as part of the compiled contract.

The compiler assigns model IDs deterministically by sorting the complete emitted runtime model names and numbering them from 1. `occid.yaml` contains the resulting IDs and is their sole source of truth; there is no separately maintained model-ID registry.

Model IDs exist for runtime discrimination and compact heterogeneous serialization.

They do **not** encode:

- authored Concept ancestry;
- compiled Type/Representation level;
- authored parentage;
- variant-family membership;
- enum/vocabulary identity.

Those relationships come from the schema itself.

Model IDs are local to one compiled structural contract. Adding, removing, or renaming an emitted model may renumber other models. Compact peers therefore must use the same OCCID contract; no compatibility reservation or tombstone is implied by a numeric value.

Generation must fail if a compiled runtime model lacks a positive model ID or two live models share an ID.

### 16.2 Compiled-level metadata

Every generated runtime model exposes `__occid_semantic_role__` as either `type` or `representation`.

For a Type this value is compiler-derived from a childless authored Concept. For a Representation it reflects the authored Representation role. Concepts that are not Types do not exist as runtime models. Enums need no model-level metadata because their declaration kind already identifies them as Vocabulary.

### 16.3 Enum representation

Enums are encoded by their numeric values on compact machine interfaces.

The member identifier remains the human-readable symbolic label and may be recovered by the generated runtime from the enum type and numeric value.

The IDL does not require redundant string-backed values such as:

```text
CARGO = "CARGO"
```

### 16.4 Compact binary serialization

The OCCID IDL is descriptive and human-readable. The compact OCCID wire representation is not.

The reference compact MessagePack representation of a record-shaped model is:

```text
[
    model_id,
    {
        field_ordinal: value,
        ...
    }
]
```

The representation of an atomic model encoded as a top-level or otherwise heterogeneous OCCID value is:

```text
[
    model_id,
    value
]
```

Rules:

- `model_id` is the contract-local numeric model discriminator emitted in `occid.yaml`.
- `field_ordinal` is the zero-based position of the field in the effective generated model field order for the active OCCID contract, including inherited fields.
- Field names and model names are never serialized on the compact wire.
- A nested OCCID model uses the same `[model_id, {field_ordinal: value}]` representation.
- An atomic Representation used through an exact field type is serialized as its underlying value directly; the field's schema already identifies the atomic type.
- An atomic Representation used where its concrete type is heterogeneous or ambiguous carries `[model_id, value]` so the concrete Representation can be recovered.
- `UID` is therefore 16 binary bytes when used through an exact `UID` field type because its declared representation is `bytes[16]`; this is not a serializer special case.
- Enums and flags are serialized by numeric value.
- Optional or defaulted fields that are not explicitly present are omitted from the numeric field map.
- Actual semantic strings remain strings: names, callsigns, free text, protocol-native textual identifiers, URIs, and other fields whose declared type is `string`.
- Compact serialization does not transmit literal schema keys such as `"model_id"`, `"fields"`, `"subject_id"`, or `"target_ref"`.

Field ordinals are contract-local rather than a second permanent registry. Compact peers therefore must use the same OCCID structural contract. Schema/contract negotiation belongs outside individual model payloads; the payload does not repeat schema names or versions.

Human/API representations are separate. JSON/YAML may use model and field names and may choose a human-friendly rendering for atomic values. Such rendering is target/runtime policy and does not redefine the underlying OCCID Representation or compact wire ABI.

A compact decoder must reject:

- an unknown model ID;
- a malformed model envelope;
- a nonnumeric or out-of-range field ordinal;
- an atomic value that violates its declared type or size constraint, including a `bytes[16]` value of any other length;
- a nested model inconsistent with the field's declared model family;
- a top-level model ID inconsistent with a specifically requested concrete class.

`model_id` may be used to dispatch a concrete instance of an explicit variant family, but the presence of a model ID does not itself declare that family.

---

## 17. Unsupported constructs

The OCCID IDL does not support:

- YAML anchors or aliases;
- YAML tags;
- flow-style YAML objects/lists;
- multiple model inheritance;
- anonymous inline models;
- string-backed enums;
- implicit Concept role inferred from `parent` when `semantic_role` is absent;
- implicit variant-family membership derived only from `parent`;
- implicit variant discriminator enums;
- profile/include/exclude language;
- JSON-Schema constructs such as `$defs`, `oneOf`, or `additionalProperties`.

A needed feature should be added deliberately to the language and this specification rather than accepted accidentally by a permissive parser.

---

## 18. OCCID repository organization

This section describes the reference repository layout; it does not add semantic meaning to directory names.

```text
lib/schema/
  core/
    ... *.schema.yaml
  modules/
    ... *.schema.yaml
```

Core documents may be grouped into subdirectories for readability. Directory placement does not define parentage, Concept ancestry, package identity, or variant families.

The authored model graph is defined by `parent`. Explicit typed families are defined by `variants` and `extend_variants`. Authored model role is defined by `semantic_role`. Vocabulary is defined by enums. There is no separate authoritative ontology file; a complete Concept tree can be derived from the authored schemas.

The reference generation path is:

```text
lib/schema/              authoritative authored semantics
compile_occid.py         semantic compiler
occid.yaml               generated flat runtime schema
generate_pydantic.py     Python projection generator
schema/                  generated Python runtime
```

`occid.yaml` and generated language bindings are build artifacts derived from the authoritative authored schemas. They are checked in for deterministic inspection and consumer tooling, but must not become independent authored sources of semantic truth.
