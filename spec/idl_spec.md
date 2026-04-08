**YAML IDL Spec**

**1. Scope**
This is a custom schema IDL written in YAML.
YAML is only the carrier syntax. The schema language is defined here.

**2. YAML Subset**
- YAML version: `1.2`
- Allowed: mappings, sequences, plain scalars, quoted scalars, comments
- Forbidden: anchors, aliases, tags, flow-style objects/lists, duplicate keys, tabs
- Unknown keys are errors
- string literals must be quoted with `"` in schema examples and authored schema

**3. Top-Level Document**
Allowed top-level keys:
- `version`
- `enums`
- `maps`
- `structs`

Example:
```yaml
version: 1
enums: 
maps: 
structs: 
```

**4. Names**
- Identifier regex: `^[A-Za-z_][A-Za-z0-9_]*$`
- Names must be unique across `enums`, `maps`, and `structs`
- Field names use the same identifier regex
- All struct and enum names are globally unique and imported flat — the ontological hierarchy is encoded in parent/variants relationships, not in qualified import paths

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
- `TaskType`
- `GlobalPosition`
- `list[string]`
- `list[GlobalPosition]`
- `map[string, string]`
- `map[string, GlobalPosition]`
- `tuple[float, float]`
- `tuple[string, int, bool]`
- `optional string`
- `optional list[string]`
- `const TaskType`
- `const map[string, GeometryTypes]`

Rules:
- `optional` means the field may be absent
- `const` means the field value is fixed and not user-supplied
- `optional const ...` is invalid
- `tuple[T1, T2, ...]` is an ordered fixed-length heterogeneous container
- no inline anonymous object types
- write imports, then `\n##Enums\n`, then enums, then `\n##structs\n`, then structs
- One newline between enums, two newlines between structs 
- Order by ontological order
- Use IntEnum for where only one aspect of the same attritube can be true
- Use List[IntEnum] as a bitflag for where many aspects of the same attritube can be true
- Preserve descriptive comments

**7. Enums**
Syntax:
```yaml
enums:
  EnumName:
    - VALUE = 0
    - NEXT
    - OTHER = 7
```

Rules:
- Each item is `NAME` or `NAME = INT`
- First unassigned item gets `0`
- Later unassigned items auto-increment from previous
- Enum numeric values must be unique
- Enum names must be unique within the enum

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

**9. structs**
Syntax:
```yaml
structs:
  structName:
    fields:
      field_a: string
      field_b: optional string
      field_c: float = 0.0
      field_d: const TaskType = MOVE
```

Rules:
- `parent` is optional
- `fields` is optional. If absent, the struct defines no own fields (inherited fields from a parent still apply)
- `parent` must reference another struct
- inheritance is single-parent only
- child fields are appended after parent fields
- redefining an inherited field is an error
- a struct may define `variants` to create a typed child family (see section 13)
- a child struct inherits all fields from its `parent`
- if the parent defines `variants`, the child is a typed variant of that parent
- a struct may be both a child and a parent, allowing nested typed hierarchies

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
task_id: string
remarks: optional string
speed_ms: float = 0.0
expires_at: int64 = null
task_type: const TaskType = MOVE
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
- additional fields are allowed as the schema language evolves, currently used includes `min`, `max`, `min_length`, and `max_length`

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
- a typed variant family, equivalent to a tagged union or protobuf `oneof`
- an implicit discriminator enum, derived from the variant keys

There is no separate union mechanism or standalone enum declaration needed. `variants` on a struct defines the family: the keys are the enum members, and each value maps to a child struct.

Syntax:
```yaml
structs:
  Task:
    fields:
      task_id: string
      unit_id: string
      priority: int
    variants:
      MOVE: MoveTask
      PATROL: PatrolTask

  MoveTask:
    parent: Task
    fields:
      destination: GlobalPosition
      speed_ms: optional float

  PatrolTask:
    parent: Task
    fields:
      path: list[GlobalPosition]
      loiter_s: optional int

```

Rules:
- `variants` is a direct key on the struct
  - each key becomes a member of the implicit discriminator enum
  - each value must reference a struct
  - enum values auto-increment from 0 in declaration order
- the implicit enum is named `{StructName}Type` (e.g., `Task` → `TaskType`) and is a first-class referenceable type
- the discriminator is reserved metadata on each child instance (accessible as `_type`). It cannot collide with user-defined field names
- each referenced child struct must declare `parent: <parent struct>`
- the effective shape of a child struct includes:
  - all inherited parent fields
  - the child struct's own fields
- the parent struct itself is a type and may be used in fields like any other struct
- a struct may define at most one `variants` block
- a child struct may also define `variants` of its own, allowing nested typed hierarchies
- when naming a child, if necessary, prefix only the parent's name

**14. Comments**
- YAML `#` comments are allowed anywhere YAML allows them
- comments have no schema meaning

**15. Errors**
These are always errors:
- unknown top-level section
- unknown struct/enum/map reference
- duplicate names
- invalid type expression
- parent is not a struct
- redefining inherited fields
- `optional const ...`
- list/map/object inline defaults in shorthand form
- `required: true/false`
- `variants` contains a value that is not a declared struct
- `variants` contains a struct whose `parent` is not the declaring struct

**16. Not Supported**
- anchors / aliases
- multiple inheritance
- anonymous inline structs
- JSON-Schema keys like `$defs`, `oneOf`, `additionalProperties`

**17. Canonical Examples**
```yaml
version: 1

maps:
  JsonGeometryTypes:
    type: map[string, GeometryTypes]
    value:
      "Point": POINT
      "Polygon": POLYGON

structs:
  Task:
    fields:
      task_id: string
      unit_id: string
      priority: int
    variants:
      MOVE: MoveTask
      PATROL: PatrolTask

  MoveTask:
    parent: Task
    fields:
      speed_ms: float = 0.0
      destination: GlobalPosition
      path: list[GlobalPosition]

      geomap:
        type: const map[string, GeometryTypes]
        value:
          "Point": POINT
          "Polygon": POLYGON

  PatrolTask:
    parent: Task
    fields:
      path: list[GlobalPosition]
      loiter_s: optional int
```
