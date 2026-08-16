# OCCID YAML IDL Specification

## 1. Purpose and authority

This document defines the OCCID schema language.

The language is a custom interface-definition language carried in YAML. YAML provides syntax only; YAML itself does not define OCCID schema semantics.

This specification is normative. The parser, validator, generator, generated runtimes, and authored schemas are expected to conform to it. If an implementation accepts invalid syntax, silently ignores a declared constraint, or generates behavior inconsistent with this document, that is an implementation bug rather than an extension of the language.

The language deliberately separates three concerns:

```text
semantic meaning        schema structure        runtime identity
----------------        ----------------        ----------------
ontology                models / fields         model_id
specialization          parent / variants       serialization
vocabulary              enums                    wire values
```

These concerns may interact, but they are not interchangeable.

---

## 2. Mental model

An OCCID schema is built from three declaration kinds:

```text
MODEL
    A named structured record.
    Models may represent ontology classes or practical schema specializations.

ENUM
    A closed controlled vocabulary.
    Enums are the vocabulary level by construction.

MAP
    A named typed constant mapping.
```

Two model relationships are distinct:

```text
parent
    Structural inheritance: the child inherits the parent's fields.

variants
    Explicit typed-family membership: the parent declares which structural
    children belong to its polymorphic variant family.
```

Runtime `model_id` values are separate again: they identify concrete generated models on the wire. A model ID does not establish inheritance, ontology, or variant-family membership.

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
    semantic_role: ontology
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
string
ExampleKind
GlobalPosition
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

A useful grammar sketch is:

```text
TypeExpr    := [Qualifier] UnionExpr
Qualifier   := "optional" | "const"
UnionExpr   := Atom ("|" Atom)*
Atom        := Identifier
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
  ModelName:
    description: "Human-readable purpose."
    semantic_role: specialization
    parent: ParentModel
    fields:
      field_a: string
      field_b: optional string
```

Allowed model keys:

- `description`
- `semantic_role`
- `parent`
- `fields`
- `variants`

Unknown model keys are errors.

### 9.1 Semantic roles

Every model must declare exactly one of:

```text
semantic_role: ontology
semantic_role: specialization
```

The roles correspond to two model levels:

```text
Level 1 — ontology
    The model represents a semantic node present in ontology.yaml. Schema naming
    may differ where the global model namespace requires a distinct spelling,
    but the model must correspond to that ontology node rather than merely being
    a useful software subtype.

Level 2 — specialization
    The model is a practical typed shape required by software, without claiming
    that the specialization is a new ontological primitive.

Level 3 — vocabulary
    Represented by enums, not by semantic_role metadata.
```

`semantic_role` applies only to models. Omission is invalid. Semantic roles never inherit through `parent`.

A `specialization` model must declare a `parent`.

The engineering criterion for introducing a specialization is structural divergence: members of the same ontological kind require materially different fields, constraints, or restricted vocabularies to be represented safely and usefully.

Canonical example:

```yaml
enums:
  InformationIntent:
    - SEARCH
    - OBSERVE

models:
  Task:
    semantic_role: ontology
    parent: Directive

  TaskInformation:
    semantic_role: specialization
    parent: Task
    fields:
      intent: InformationIntent
```

This means:

```text
Task                    ontology
TaskInformation         practical typed specialization
SEARCH / OBSERVE        vocabulary
```

`TaskInformation` is not promoted to a new ontological primitive merely because it needs a distinct struct.

---

## 10. Fields

A model's `fields` mapping declares fields owned by that model. Inherited fields come from `parent`.

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

## 11. Structural inheritance: `parent`

`parent` defines single structural inheritance between models.

Example:

```yaml
models:
  Data:
    fields:
      timestamp: float

  Observation:
    parent: Data
    fields:
      source_ref: StringID
```

`Observation` contains both `timestamp` and `source_ref`.

Rules:

- A model has at most one parent.
- The parent must resolve to a model.
- Inheritance cycles are errors.
- A child inherits all parent fields.
- A child may not redefine an inherited field.
- `parent` does not by itself make an ontological claim.
- `parent` does not by itself add the child to an explicit variant family.

A model may structurally inherit from another model without being listed in that parent's `variants`.

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
- schema root model missing `description`;
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
- `specialization` without a parent;
- redefining an inherited field;
- invalid or cyclic variant-family declarations;
- variant whose structural parent does not match the declaring family.

### Field errors

- unknown expanded-field keys;
- invalid type expression;
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

Every generated model has a numeric OCCID model ID allocated by the schema's model-ID registry.

Model IDs exist for runtime identity and compact heterogeneous serialization.

They do **not** encode:

- ontology level;
- semantic role;
- structural parentage;
- variant-family membership;
- enum/vocabulary identity.

Those relationships come from the schema itself.

Removing a model removes its live registry entry. Numeric IDs not assigned to a live model are free according to the current OCCID version policy.

Generation must fail if:

- a generated model has no allocated ID; or
- two live models share an ID.

### 16.2 Semantic-role metadata

Every generated model exposes its explicitly declared `semantic_role` to schema reflection/runtime tooling.

Semantic role never propagates from a parent. Enums need no semantic-role metadata because their declaration kind already identifies them as vocabulary.

### 16.3 Enum representation

Enums are encoded by their numeric values on compact machine interfaces.

The member identifier remains the human-readable symbolic label and may be recovered by the generated runtime from the enum type and numeric value.

The IDL does not require redundant string-backed values such as:

```text
CARGO = "CARGO"
```

### 16.4 Named-field serialization

OCCID durable and compact serializations use named fields. Field declaration order is not a stable wire contract.

The reference compact MsgPack envelope is:

```text
schema_version
model_id
fields
```

Nested heterogeneous OCCID models may likewise carry their concrete model ID alongside their named fields.

A decoder must reject:

- an unsupported schema version;
- an unknown model ID;
- a top-level model ID inconsistent with a specifically requested concrete class;
- malformed field payloads.

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
- implicit ontology derived from inheritance;
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

Core documents may be grouped into subdirectories for readability. Directory placement does not define inheritance, ontology, package identity, or variant families.

The model graph is defined by `parent`. Explicit typed families are defined by `variants` and `extend_variants`. Semantic model level is defined by `semantic_role`. Vocabulary is defined by enums.

Generated language bindings are build artifacts derived from these authoritative schema sources and must not become an independent source of schema truth.
