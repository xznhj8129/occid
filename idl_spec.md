**YAML IDL Spec**

**1. Scope**
This is a custom schema IDL written in YAML.
YAML is only the carrier syntax. The schema language is defined here.
Specific example names are not definitive.

**2. YAML Subset**
- YAML version: `1.2`
- Allowed: mappings, sequences, plain scalars, quoted scalars, comments
- Additional 4-space indentation levels are legal for readability even when they do not add structure, as long as the YAML structure is unchanged
- Forbidden: anchors, aliases, tags, flow-style objects/lists, duplicate keys, tabs
- Unknown keys are errors
- string literals must be quoted with `"` in schema examples and authored schema

**3. Top-Level Document**

A schema document is either a **class expansion file** (`type: schema`) or a **module manifest** (`type: module`). They share the same IDL syntax for enums, maps, and models, but differ in header fields and resolution rules.

Common top-level keys (both types):
- `version` required
- `type` required, either `schema` or `module`
- `package` required, the document's package/output module identifier
- `tags` required, list of profile tags for subset selection (see section 17.3)
- `enums`
- `maps`
- `models`

**3.1. Class expansion file** (`type: schema`) additional keys:
- `root` required; the primary model owned by this schema file

**3.2. Module manifest** (`type: module`) additional keys:
- `description` optional, human-readable package purpose
- `requires` optional, list of tags or module packages this module depends on
- `extend_variants` optional, grafts new variants onto existing typed parents (see section 18.4)

Example class expansion file:
```yaml
version: 1
type: schema
package: state
root: State
tags:
  - core

enums:
maps:
models:
  State:
    description: "State data describing current object condition and telemetry."
    parent: Information
```

Minimal schema file:
```yaml
version: 1
type: schema
package: object
root: Object
tags:
  - core

models:
  Object:
    description: "Top-level object branch."
    parent: Root
```

Example module manifest:
```yaml
version: 1
type: module
package: ew
description: "Electronic warfare observations, effects, protection, and spectrum management."
tags:
  - military
requires:
  - core
```

**4. Names**
- Identifier regex: `^[A-Za-z_][A-Za-z0-9_]*$`
- Names must be unique across `enums`, `maps`, and `models`
- Field names use the same identifier regex
- All model and enum names are globally unique and imported flat
- `parent` and `variants` encode the structural inheritance/type graph; they do not by themselves claim that every child is a distinct ontological primitive
- `semantic_role` explicitly records whether a declaration is ontological, a practical schema specialization, or controlled vocabulary where that distinction matters
- For schema files, `package` must match the schema file basename without `.schema.yaml`
- For module files, `package` must be globally unique across loaded packages

**5. Primitive Types**
Built-in primitive types:
- `string`
- `int`
- `int8`
- `int16`
- `int32`
- `int64`
- `uint8`
- `uint16`
- `uint32`
- `uint64`
- `float`
- `bool`
- `bytes`
- `any`

**6. Type Expressions**
Valid type expressions:
- `string`
- `ExampleKind`
- `GlobalPosition`
- `list[string]`
- `list[GlobalPosition]`
- `map[string, string]`
- `map[string, GlobalPosition]`
- `tuple[float, float]`
- `tuple[string, int, bool]`
- `optional string`
- `optional list[string]`
- `const ExampleKind`
- `const map[string, GeometryTypes]`

Rules:
- `optional` means the field may be absent
- `const` means the field value is fixed and not user-supplied
- `optional const ...` is invalid
- `tuple[T1, T2, ...]` is an ordered fixed-length heterogeneous container
- no inline anonymous object types
- write imports, then `\n##Enums\n`, then enums, then `\n##models\n`, then models
- One newline between enums, two newlines between models
- Order by structural/semantic order
- Use IntEnum where only one aspect of the same attribute can be true
- Use List[IntEnum] as a bitflag where many aspects of the same attribute can be true
- Preserve descriptive comments

**7. Enums**
Compact syntax:
```yaml
enums:
  EnumName:
    - VALUE = 0
    - NEXT
    - OTHER = 7
    - FLAG_A = 1 << 1
    - FLAG_B = 1 << 2
```

Expanded syntax for an enum carrying semantic metadata:
```yaml
enums:
  InformationIntent:
    semantic_role: vocabulary
    values:
      - SEARCH = "SEARCH"
      - OBSERVE = "OBSERVE"
```

Rules:
- Each value item is `NAME`, `NAME = INT`, `NAME = "string"`, or `NAME = 1 << INT`
- First unassigned integer item gets `0`
- Later unassigned integer items auto-increment from previous
- Any enum using `1 << INT` values is generated as a bitflag enum
- Enum numeric values must be unique
- Enum names must be unique within the enum
- The compact list form remains valid when no enum metadata is required
- The expanded form accepts only `semantic_role` and `values`
- The only enum semantic role is `vocabulary`

**8. Constant Maps**
Syntax:
```yaml
maps:
  MapName:
    type: map[string, GeometryTypes]
    value:
      "Point": POINT
      "Polygon": POLYGON
```

Rules:
- `maps` defines named constant maps
- `type` must be `map[K, V]`
- `value` must be a YAML mapping
- keys and values must match the declared map type

**9. models**
Syntax:
```yaml
models:
  ModelName:
    description: "Human-readable model purpose."
    semantic_role: specialization
    parent: ParentModel
    fields:
      field_a: string
      field_b: optional string
      field_c: float = 0.0
      field_d: const ExampleKind = PRIMARY
```

Rules:
- `description` is optional on ordinary models and required on a schema file's root model
- `semantic_role` is optional and, when present, must be `ontology` or `specialization`
- `parent` is optional
- `fields` is optional. If absent, the model defines no own fields; inherited fields from a parent still apply
- `parent` must reference another model
- inheritance is single-parent only
- child fields are appended after parent fields
- redefining an inherited field is an error
- a model may define `variants` to create an explicit typed child family (see section 13)
- a child model inherits all fields from its `parent`
- if the parent defines `variants`, the child may be an explicit typed variant of that parent
- a model may be both a child and a parent, allowing nested typed hierarchies
- structural inheritance does not imply an ontology claim; use `semantic_role` when that distinction matters

**9.1. Semantic roles**

OCCID distinguishes three semantic levels where a declaration would otherwise be ambiguous:

1. `ontology` on a model: the model states what semantic kind of thing a record is.
2. `specialization` on a model: the model is a practical typed schema specialization and does not, by its existence alone, claim a new ontological primitive.
3. `vocabulary` on an enum: the values are controlled labels used for classification, routing, filtering, UI grouping, or interoperability rather than model classes.

Task is the canonical example:
```yaml
enums:
  InformationIntent:
    semantic_role: vocabulary
    values:
      - SEARCH = "SEARCH"
      - OBSERVE = "OBSERVE"

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

This represents three different things:

```text
ontology:        Task
schema:          TaskInformation
vocabulary:      SEARCH / OBSERVE / ...
```

Rules:
- `parent` always means structural inheritance. Do not infer ontology merely from inheritance.
- `ontology` and `specialization` are model roles; `vocabulary` is an enum role.
- A model marked `specialization` must have a parent.
- Semantic role metadata is declarative and is emitted into generated Python as `__occid_semantic_role__` on declarations that define it.
- Omission means the declaration has not been classified with this metadata. It must not be interpreted as inherited semantic-role metadata.
- Use specialization when software needs a stable typed shape or restricted field vocabulary without promoting every useful software subtype into the ontology.
- Do not turn individual vocabulary values into child models merely to obtain type safety.
- Do not add a `variants` discriminator merely to restate a set of practical specializations when their model identity already distinguishes them.

**10. Field Shorthand**
Allowed shorthand forms:
- `name: Type`
- `name: optional Type`
- `name: Type = scalar_default`
- `name: Type = null`
- `name: optional Type = scalar_default`
- `name: const Type = scalar_or_enum_value`

Examples:
```yaml
record_id: string
remarks: optional string
speed_ms: float = 0.0
expires_at: int64 = null
kind: const ExampleKind = PRIMARY
path: list[GlobalPosition]
```

Rules:
- shorthand defaults are only for scalar values, enum values, and `null`
- list/map/object defaults must use expanded form
- inline form is preferred for fields that only need a type, optionality, or scalar default
- expanded form is used when a field needs additional metadata

**11. Expanded Field Form**
Syntax:
```yaml
pwm:
  type: int
  min: 900
  max: 2100
  default: 1500

alphabet:
  type: list[string]
  default:
    - a
    - b
    - c
  description: Human text
```

Allowed keys:
- `type` required
- `default` optional
- `value` optional
- `description` optional, comments preferred if inline

Rules:
- `default` is for non-const fields
- `value` is for const fields
- `default` and `value` may not both appear
- `description` is free text
- `required` is not allowed; use `optional` in the type instead

Example const map field:
```yaml
geomap:
  type: const map[string, GeometryTypes]
  value:
    "Point": POINT
    "Polygon": POLYGON
```

**12. Field Presence Semantics**
- Required field: any field not marked `optional`, not `const`, and with no `default`
- Optional field: any field with `optional`
- Nullable field: any field with `default: null` or inline `= null`
- Defaulted field: omission is allowed; default is applied
- Const field: omission is allowed; fixed value is applied

**13. Variants**
A parent/variants relationship is:
- field inheritance
- an explicit typed variant family, equivalent to a tagged union or protobuf `oneof`
- an implicit discriminator enum, derived from the variant model names

It is a structural schema relationship. It is not automatically an ontology relationship, and it is not required merely because child models share a parent.

Syntax:
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

Rules:
- `variants` is a direct key on the model
- `variants` is always a list of declared child model names
- `variants:` with no entries is valid only as an extension point for modules
- each item must reference a declared child model
- each referenced child model must declare `parent: <parent model>`
- not every parent/child relationship needs a `variants` block
- use `variants` only when an explicit discriminator family is part of the schema contract
- enum values auto-increment from 0 in declaration order
- the implicit enum is named `{ModelName}_type` and is a first-class referenceable type
- each implicit enum member is derived from the child model name by dropping the parent model's prefix when present and converting to `SCREAMING_SNAKE_CASE`
- the discriminator is reserved metadata on each child instance and cannot collide with user-defined field names
- the effective shape of a child model includes all inherited parent fields and the child model's own fields
- the parent model itself is a type and may be used in fields like any other model
- a model may define at most one `variants` block
- a child model may also define `variants` of its own, allowing nested typed hierarchies
- source readability takes precedence over normalized expansion

**14. Comments**
- YAML `#` comments are allowed anywhere YAML allows them
- comments have no schema meaning

**15. Errors**
These are always errors:
- unknown top-level section
- unknown model/enum/map reference
- duplicate names
- invalid type expression
- parent is not a model
- redefining inherited fields
- invalid `semantic_role` for the declaration kind
- a `specialization` model without a parent
- an expanded enum without `values`
- unknown keys in an expanded enum
- `optional const ...`
- list/map/object inline defaults in shorthand form
- `required: true/false`
- `variants` contains a value that is not a declared model
- `variants` contains a model whose `parent` is not the declaring model
- `package` does not match the schema file basename without `.schema.yaml`
- missing `version`, `type`, `package`, or `tags`
- missing `root` on a schema file
- `root` on a schema file does not reference a declared model
- schema file root model is missing `description`
- top-level `description` on a schema file
- `root` on a module file
- `type` is not `schema` or `module`
- a module's `extend_variants` references a parent that has no `variants` block
- a module's `extend_variants` introduces a derived variant name that collides with an existing one
- a module's `requires` list is not satisfied at load time
- a module redefines or alters an existing model, enum, or field from core or another module
- a module's model declares a `parent` that does not exist in core schema or required modules

**16. Not Supported**
- anchors / aliases
- multiple inheritance
- anonymous inline models outside terminal variant leaves
- JSON-Schema keys like `$defs`, `oneOf`, `additionalProperties`

**17. File Organization**

Each schema file is a package centered on one primary model, not a subject-domain bucket. If a domain concept touches multiple structural branches, those models belong in their respective class files rather than one subject bucket.

Schema files live under `lib/schema/core/` and may be organized in subdirectories for readability. Directory placement is organizational only and is not part of the schema package. A schema file's `package` is the basename without `.schema.yaml`; `root` is the primary model in that package. The core directory layout should mirror the first-level model branches:

```text
schema/
  core/
    core.schema.yaml
    definition/
    struct/
    objects/
    control/
    communication/
    data/
  modules/
    military/
      military.schema.yaml
```

**17.1. One file, one package**
- Every schema file declares a `root` model: the default entry point for the package, not a hard boundary
- Files are not necessarily hard-bound to a model family; `command.schema.yaml` containing `Command` is a convenience, not a rule
- Split a file only when more compartmentalization is necessary
- A schema package may also contain local enums, maps, variants, and auxiliary models used by that package
- The structural model graph is declared by `parent` and, where explicitly needed, `variants`; semantic role is declared separately by `semantic_role`
- If a model branch has its own schema file, that is an organizational choice
- Enums used exclusively by models in the file are co-located. Enums shared across files belong in the root or a common ancestor file

**17.2. File header**
The header declares the package identity and primary model:

```yaml
version: 1
type: schema
package: information
root: Information
tags:
  - core
```

- `type` always `schema` for class expansion files
- `package` package/output module identifier, matching the schema file basename
- `root` primary model declared in the file
- `tags` profile tags that classify this file for subset selection (see 17.3)

**17.3. Tags and profiles**
Tags classify files by domain applicability. A **profile** is a named set of tag inclusion/exclusion rules that selects a subset of the schema.

Reserved tags:
- `core` foundational, always included in every profile.

Tags are additive: a file tagged `[core, military]` is both foundational and military-relevant. A profile that excludes `military` drops any file whose tags include `military`, unless the file is also tagged `core`, in which case `core` takes precedence as the always-included foundation.

Profile resolution rules:
1. All files tagged `core` are always included
2. A profile declares which non-core tags to include or exclude
3. Include is the default; a profile only needs to declare exclusions
4. If a file carries no matching include tag and no matching exclude tag, it is included by default
5. A file excluded by a profile is entirely absent; its models, enums, and maps do not exist in that profile's schema

Example profiles:
```yaml
profile: civil
exclude:
  - military

profile: military_c2
include_all: true

profile: maritime_isr
include:
  - core
  - maritime
exclude_untagged: true
```

**17.4. Model and ontology resolution**
The structural model tree is resolved from `parent` relationships and explicit `variants` families. `semantic_role` separately identifies declarations that are ontology classes or practical schema specializations. An inheritance edge therefore does not, by itself, make the child an ontological subtype claim.

**18. Modules**

A module is a self-contained extension that adds domain-specific models, enums, and maps without modifying core schema files. Modules are the mechanism for domain-specific, third-party, and classified extensions.

**18.1. What a module is**
- A separate YAML manifest file, not a class expansion file
- It declares new models, enums, and maps that attach to existing parents in the class tree
- It does not modify, override, or redefine anything in core schema files
- It is the extension boundary: adding capability means adding a module rather than forking the core tree

**18.2. Module manifest format**
Module files live under `lib/schema/modules/` as YAML files following the IDL syntax for enums, maps, and models, plus module-specific header fields. A domain module may be organized as a directory containing several `type: module` files. Directory placement is organizational only; each module file still has a globally unique `package`.

```yaml
version: 1
type: module
package: ew
description: "Electronic warfare observations and spectrum planning."
tags:
  - military
requires:
  - core

enums:
  SpectrumObservationKind:
    semantic_role: vocabulary
    values:
      - DETECTION = "DETECTION"
      - IDENTIFICATION = "IDENTIFICATION"
      - DIRECTION_FINDING = "DIRECTION_FINDING"

models:
  SpectrumObservation:
    semantic_role: specialization
    parent: Observation
    fields:
      observation_kind: SpectrumObservationKind
      frequency_hz: optional float
      bearing_deg: optional float

  SpectrumAllocation:
    semantic_role: specialization
    parent: Plan
    fields:
      frequency_range_hz: optional NumericRange
      assigned_to_id: optional StringID
      priority: optional int
```

Header fields, in addition to the common fields in section 3:
- `requires` list of tags or module packages this module depends on. The resolver must include those dependencies before this module can be applied

**18.3. Rules**
- A module's models must declare `parent` referencing a model from the core schema or from a required module
- A module may define models that extend any structural branch of the class tree
- All names, models, enums, and maps must be globally unique across core schema and all loaded modules
- A module may add new variants to an existing parent's explicit `variants` block via `extend_variants` (see 18.4)
- A module cannot redefine, remove, or alter existing models, enums, or fields
- Modules are optional; the core schema is complete and valid without any modules loaded
- A module's `requires` list must be satisfied before the module is loaded; unsatisfied dependencies are an error
- Module models and enums may use `semantic_role` under the same rules as core declarations

**18.4. Extending variants**
When a module adds a new child to an existing parent that explicitly defines a `variants` block, it uses `extend_variants` to graft new members onto that parent's discriminator:

```yaml
extend_variants:
  ExistingTypedParent:
    - NewTypedChild
```

Rules:
- `extend_variants` keys must reference models from core schema or required modules
- The referenced parent must already have a `variants` block
- `extend_variants` values are lists of declared child model names
- New derived variant names must not collide with existing variant names on that parent
- The new variant enum values auto-increment from the last existing value on the parent
- Each model listed must declare `parent` matching the extended parent
- Practical specialization does not require `extend_variants`; use it only when the parent intentionally owns an explicit discriminator family

**18.5. Module resolution**
When building a schema with modules:
1. Resolve the core schema files and model graph
2. For each selected module, verify `requires` are satisfied
3. Apply `extend_variants` only to explicit variant families
4. Merge the module's models, enums, and maps into the global namespace
5. Validate: no name collisions, no orphan parents, no cycles

Module selection is independent of tag filtering but compatible with it:
- A module tagged `military` is excluded when the profile excludes `military`
- A module with no conflicting tags is included by default when explicitly selected
- Modules are never auto-included; they must be explicitly selected by name or by matching tag inclusion rules

**19. Generated schema identity and serialization**

- Every generated model has a numeric ID allocated in `lib/model_ids.yaml` for the current schema.
- The registry contains live models only. Removing a model removes its registry entry; freed numeric IDs may be reused.
- Generation fails when a selected model has no allocated ID or two live names share an ID.
- Declarations with explicit `semantic_role` publish it in generated Python as `__occid_semantic_role__`.
- A declaration without `semantic_role` has generated/runtime semantic role `None`; it does not inherit its parent's semantic role.
- The generated package publishes `OCCID_SCHEMA_VERSION` independently of the YAML IDL document-format version.
- Durable persistence uses ordinary named-field JSON.
- Compact MsgPack uses named fields in an envelope containing `schema_version`, `model_id`, and `fields`.
- Positional field-order encoding is not a stable contract.
- A decoder rejects unsupported schema versions and a top-level model ID that does not identify the requested class.
