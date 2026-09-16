# OCCID2 semantic-product demonstrator specification

## 1. Purpose

This demonstrator tests one architectural claim:

> OCCID can retain its existing authored class/model hierarchy and field inheritance while gaining a second way to address information by semantic meaning rather than exact model and field paths.

The semantic layer must not become another ontology tree.

The semantic layer consists of:

- concepts already present in the OCCID model tree;
- typed axes and axis values;
- unordered semantic products;
- directed relations;
- legality rules attached primarily to axes;
- mappings from practical surface vocabulary to deeper semantic products.

The prototype is intentionally bounded. It demonstrates a person, a ground robot, a flying drone, position data, and several Task representations.

---

## 2. One OCCID model tree

There is one normal OCCID inheritance mechanism:

```text
parent:
```

It provides both:

1. ordinary inherited representation fields; and
2. semantic ancestry where the parent is a semantic concept.

There is no separate serialization inheritance mechanism.

The demo therefore has ordinary chains such as:

```text
Root
└── Object
    └── Entity
        ├── Actor
        │   └── Person
        └── Machine
            └── Robot
                ├── GroundRobot
                └── Drone
```

and:

```text
Root
└── Control
    └── Directive
        └── Task
            ├── TaskManeuver
            ├── TaskInformation
            └── TaskEffect
```

A parent may have fields if those fields truthfully apply to all descendants.

For example `Task` owns only fields that make sense for all Task representations in this demo. Spatial-only fields such as `location_uids` and `target_uids` are intentionally absent from `Task`.

---

## 3. Semantic products

A semantic product is an unordered idempotent conjunction of factors.

Conceptually:

```text
A × B × C = C × A × B
A × A = A
```

No universal wrapper fields such as these exist:

```text
subject
property
role
focus
reference
context
```

Factors identify themselves.

Example:

```text
Machine
× MachineKind.ROBOT
× Domain.AIR
× Controller.UNMANNED
× Airframe.MULTIROTOR
```

The generated `Drone._semantics` is such a product.

The Python application API does not need to expose multiplication syntax. The runtime may normalize queries internally to products.

---

## 4. Axes

An axis is a typed semantic dimension whose values answer one coherent semantic question.

Example:

```yaml
Domain:
  semantic_role: axis
  cardinality: one
  values:
    - LAND
    - AIR
    - SEA
```

Axis values are semantic factors:

```python
Domain.AIR
Domain.LAND
```

An axis is not an enum with semantic ambitions. An ordinary enum remains an ordinary bounded representation vocabulary.

The demo contains semantic axes such as:

- `Substrate`
- `Domain`
- `MachineKind`
- `Controller`
- `Locomotion`
- `Airframe`
- `Frame`
- `BloodGroup`
- `Realm`
- `TemporalMode`
- `TruthTarget`

### Cardinality

`cardinality: one` means one value is valid in a complete description.

For partial semantic queries, the demonstrator enforces the maximum side only. Therefore:

```text
Robot
```

can be a valid partial query without a Domain value, while:

```text
Robot × Domain.AIR × Domain.LAND
```

is contradictory.

### Applicability

An axis may be meaningful only inside a semantic region.

Example:

```yaml
BloodGroup:
  applies:
    all:
      - Substrate.BIOLOGICAL
```

Selecting a blood-group coordinate therefore requires the biological substrate region.

Because `Machine` contributes `Substrate.MECHANICAL`, this becomes illegal through the single-valued `Substrate` axis:

```text
Drone × BloodGroup.A_POS
```

No special `Drone cannot have blood group` rule exists.

---

## 5. Concepts, representations, and products

A concept may contribute semantic factors through normal parentage and an optional `product:` declaration.

Example:

```yaml
Machine:
  semantic_role: concept
  parent: Entity
  product:
    - Substrate.MECHANICAL
```

`Robot` adds:

```yaml
product:
  - MachineKind.ROBOT
```

`Drone`, a representation, adds:

```yaml
product:
  - Domain.AIR
  - Controller.UNMANNED
  - Locomotion.SELF_PROPELLED
  - Airframe.MULTIROTOR
```

`product:` is not a record of named semantic fields. It is merely YAML syntax for an unordered product.

The corresponding factors do not need fields named `domain`, `controller`, `locomotion`, or `airframe` unless a concrete wire/representation format independently needs those serialized fields.

---

## 6. Representation-specific versus semantic lookup

`GlobalPosition` is a representation under the `Position` concept:

```yaml
GlobalPosition:
  semantic_role: representation
  parent: Position
  product:
    - Frame.WGS84
```

Therefore its static meaning is available directly:

```python
GlobalPosition._semantics
```

Application code can request the exact representation:

```python
drone.get(GlobalPosition)
```

or request by semantic meaning:

```python
drone.get(Position, Frame.WGS84)
```

Those are deliberately different operations.

The second survives a future representation rename or replacement as long as some representation still satisfies the same semantic product.

Discovery is explicit:

```python
drone.find(Position)
```

and can return multiple stored values if several representations satisfy the query.

Multiple subjects are not flattened into one product:

```python
store.get_many([drone1, drone2, drone3], Position)
```

---

## 7. Products versus relations

Products describe one semantic thing.

Relations connect distinct semantic things and preserve operand order.

The demo defines:

```yaml
Destination:
  semantic_role: relation
  signature:
    - Task
    - Location
```

A move-to-location case is therefore not a `GoHereTask` class.

It is a Task semantic product plus a relation:

```text
Task
× Realm.WORLD
× TemporalMode.ACHIEVE
× Position
```

and:

```text
Destination(task, mark)
```

In Python:

```python
store.relate(Destination, task, mark)
```

`Destination(task, mark)` is not interchangeable with `Destination(mark, task)`.

---

## 8. Task semantics

### 8.1 Task concept

The bounded working definition is:

> A Task is a requirement that some proposition become or remain sufficiently true.

`Task` remains intentionally broad.

The demo does not encode every proposition or quantifier structure. It only proves the factorization of a small surface vocabulary.

### 8.2 Why there is no Action axis

The following words do not answer one coherent semantic question:

```text
MOVE
CREATE
IDENTIFY
CLASSIFY
REMOVE
TRACK
```

Therefore they are not values of one `Action` axis.

They are practical surface codewords that compress different legal products.

### 8.3 General Task axes

The bounded experiment introduces:

```yaml
Realm:
  values:
    - WORLD
    - INFORMATION
```

and:

```yaml
TemporalMode:
  values:
    - ACHIEVE
    - MAINTAIN
```

These are genuine axes because each answers one coherent question.

### 8.4 Surface enums remain enums

The existing practical Task families are kept in reduced form:

```yaml
ManeuverIntent:
  - MOVE = 0
  - HOLD

InformationIntent:
  - LOCATE = 0
  - TRACK
  - IDENTIFY
  - CLASSIFY

EffectIntent:
  - CREATE = 0
  - REMOVE
```

They are ordinary representation enums, not semantic axes.

The compiler associates selected enum members with semantic products.

Examples:

```text
MOVE
= Task
× Realm.WORLD
× TemporalMode.ACHIEVE
× Position
```

```text
HOLD
= Task
× Realm.WORLD
× TemporalMode.MAINTAIN
× Position
```

```text
LOCATE
= Task
× Realm.INFORMATION
× TemporalMode.ACHIEVE
× Position
```

```text
TRACK
= Task
× Realm.INFORMATION
× TemporalMode.MAINTAIN
× Position
```

```text
IDENTIFY
= Task
× Realm.INFORMATION
× TemporalMode.ACHIEVE
× Identity
```

```text
CLASSIFY
= Task
× Realm.INFORMATION
× TemporalMode.ACHIEVE
× Classification
```

`CREATE` and `REMOVE` use a state-specific truth target:

```text
CREATE
= Task
× Realm.WORLD
× TemporalMode.ACHIEVE
× Existence
× TruthTarget.TRUE
```

```text
REMOVE
= Task
× Realm.WORLD
× TemporalMode.ACHIEVE
× Existence
× TruthTarget.FALSE
```

No giant verb list is required.

### 8.5 Instance semantics

`TaskManeuver` itself does not mean MOVE because its `intent` varies.

This instance:

```python
TaskManeuver(
    uid="task-1",
    instruction="move there",
    intent=ManeuverIntent.MOVE,
)
```

has instance semantics equal to its representation semantics plus the semantic product attached to `ManeuverIntent.MOVE`.

This lets the schema retain practical surface vocabulary while the semantic layer reasons about the deeper product.

---

## 9. Legality

The demonstrator implements only the subset required by the examples:

- axis cardinality;
- conjunction-style applicability requirements;
- partial-product legality;
- entailment and equivalence after simple applicability closure.

Examples tested:

```text
Drone × Domain.LAND
-> illegal
```

```text
Drone × BloodGroup.A_POS
-> BloodGroup requires Substrate.BIOLOGICAL
-> Drone entails Substrate.MECHANICAL
-> Substrate is single-valued
-> illegal
```

```text
Person × BloodGroup.A_POS
-> legal
```

The full intended rule language remains larger: alternative requirements, higher-order exclusions, contextual profiles, and more general satisfiability are deliberately outside this small implementation.

---

## 10. Compiler

The authored source is:

```text
occid2.schema.yaml
```

The deterministic compiler produces:

```text
generated/occid2.py
generated/semantic_registry.json
```

The generated Python contains:

- semantic axis classes and values;
- ordinary enums;
- normal inherited dataclass models;
- `_semantics` on generated model classes;
- semantic products attached to selected surface enum values;
- generated relation definitions;
- a generated semantic registry.

The compiler does not generate a second class hierarchy.

---

## 11. Acceptance tests

The demonstrator currently verifies:

1. normal parent field inheritance;
2. absence of spatial-only fields on base `Task`;
3. factored `Drone` semantics without semantic payload fields;
4. Domain cardinality contradiction;
5. derived BloodGroup/Substrate contradiction;
6. exact versus semantic position lookup;
7. multi-subject lookup through `get_many`;
8. MOVE factorization;
9. LOCATE factorization;
10. CREATE factorization;
11. directed relation validation;
12. semantic discovery through enum-provided meaning;
13. `GlobalPosition._semantics` as the static source of representation meaning;
14. deterministic compiler output.

---

## 12. Non-goals

This demonstrator intentionally does not attempt:

- full OCCID migration;
- a complete theorem prover;
- arbitrary graph/path resolution;
- automatic semantic inference from arbitrary legacy fields;
- Task quantification and nested proposition variables;
- generic time semantics;
- representation transforms;
- contextual doctrine profiles;
- state history;
- `EntityState` replacement;
- complete Task/Command/Plan/Objective formalization.

The only question being tested is whether semantic products, axes, relations, and surface-codeword decompositions can coexist cleanly with ordinary OCCID inheritance.
