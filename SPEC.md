# OCCID2 semantic algebra notes

## 1. Runtime-defined semantics

The semantic registry is the live authority for semantic definitions and
relationships. Definitions are data interpreted by the algebra at runtime.
`occid2/definitions.yaml` supplies the initial definitions. Runtime updates are
validated before becoming active.

---

## 2. Two judgments

The algebra has exactly two judgments:

```text
x ⊨ P            satisfaction: the thing x satisfies the product P
R(a₁, …, aₙ)     relation: a directed link between things
```

A **product** `P = f₁ × f₂ × …` is an unordered, idempotent conjunction of
factors that describes **one** thing:

```text
A × B = B × A
A × A = A
```

Meaning is the entailment closure:

```text
M(x) = closure{ f | x ⊨ f }
```

`M(x)` is a product, not a sentence. It is the strongest product x satisfies.
There is no global wrapper (`subject`, `property`, `role`, `focus`, …); a
factor identifies its own dimension (`PhysicalDomain.AIR`, `BloodGroup.A_POS`).
The product itself is the semantic address: `uav-1 × Position × Geodetic`.

A **relation** is not a factor. It is directed and its operands are ordered, so
`Wags(dog, tail) ≠ Wags(tail, dog)`. Products describe things; relations connect
things.

---

## 3. Factors and axes

An axis is one typed semantic dimension; its values are factors:

```yaml
PhysicalDomain:
  cardinality: one
  values: [LAND, AIR, SEA, UNDERSEA, SPACE]
```

- **Cardinality** bounds a dimension in a complete description. `cardinality:
  one` means at most one value; two values contradict automatically. No pairwise
  disjointness declarations are needed for values of the same axis.
- **Applicability** says a dimension is meaningful only where a region can
  hold. It is a satisfiability check and **does not assert** the region.
- **Requirement** asserts the region into the closure.

Both are declared where they belong — on the axis, an axis value, or a concept:

```yaml
BloodGroup:
  applies: { all: [Substrate.BIOLOGICAL] }   # meaningful only for biological
  requires: [Biological]                      # asserting: closure adds it

Altitude:
  applies: [PhysicalDomain.AIR]               # emergent: no assertion
```

Emergent dimensions need no classes:

```text
Mission × PhysicalDomain.AIR   gains Altitude applicability
AirTask = Task × PhysicalDomain.AIR
```

---

## 4. Legality, partial products, unknown vs illegal

The solver has two layers:

1. `closure(product)` applies requirements and implications whose `when` holds,
   adding each forced region's semantic ancestry.
2. `consistent(closed)` rejects axis-cardinality violations, disjointness,
   exclusions, and unsatisfiable requirements.

A partial product is legal without pretending to be complete. A question is
illegal only when **no completion exists**:

```text
Mission × Altitude                legal, but unknown
Mission × SEA × Altitude          illegal (Altitude is air-only)
Drone                             legal partial product
Drone × PhysicalDomain.SEA        illegal (PhysicalDomain is single-valued)
```

Consequences are derived, never enumerated:

```text
Drone entails Machine and Substrate.MECHANICAL
BloodGroup requires Biological
Biological entails Substrate.BIOLOGICAL
Substrate is single-valued
=> Drone × BloodGroup.A_POS is illegal
```

---

## 5. Aliases

An alias is a registry-scoped name for a product. Naming creates no ontology:

```yaml
aliases:
  UAV: [UnmannedVehicle, PhysicalDomain.AIR]
  Drone: [UAV, Airframe.MULTIROTOR]
  Geodetic: [Representation.Geodetic]
```

Alias resolution is recursive and canonical: `Drone` expands through `UAV` to
`UnmannedVehicle × PhysicalDomain.AIR × Airframe.MULTIROTOR`. A named
combination and an unnamed equivalent combination have the same normal form.

---

## 6. Semantic descriptions and data

The store operates on semantic descriptions and data. A datum consists of its
subject, semantic product, value, source, provenance, time or validity, identity,
and definition revision. The semantic product is its address.

Unresolved and irreducible concepts remain representable. Representation names
such as `GlobalPosition` are product aliases, not required Python classes.

---

## 7. Charts: a quantity in a representation reduces to variables

A chart is the reduction rule that connects meaning to data:

```text
chart Q × C  ≅  v₁ × v₂ × … × vₙ
```

```yaml
charts:
  Position * Representation.Geodetic:
    lat: float[deg]
    lon: float[deg]
    h: float[m]

  Position * Representation.LocalCartesian:
    x: float[m]
    y: float[m]
    z: float[m]
```

**Chart produces the primitives.** `Position` stays semantic; the
representation selects how it becomes data; the coordinates emerge only after
that selection. A coordinate's unit is algebraic metadata, not its Python type.

The same quantity may be stored in several representations. Each is a separate
datum; each answers `entity × Position`, and a representation factor narrows to
one:

```text
uav-1 × Position            -> [geodetic fact, Cartesian fact]
uav-1 × Position × Geodetic -> {lat, lon, h}
```

This is the operational answer to "how does a semantic quantity become actual
data?" It also means a different struct can represent the same product without
changing the product.

---

## 8. Relations

A relation connects independently existing things. Only links that are neither
factors of one thing nor variables of an expression are relations:

```yaml
relations:
  AssignedWork:                   # intentional: entity -> task
    operands: {assignee: Entity, work: Task}

  ConstrainedBy:                  # a bound on directed work
    operands: {subject: Control, constraint: Constraint}
```

Consequences:

- roles and operand order belong to the relation; specialization preserves
  operand order;
- participant roles of work are **not** relations; they are the typed free
  variables of the work's expression (section 9), and binding a reference to a
  variable is the link;
- aggregates such as plans are queries over facts, not pointer columns;
- roles are part of the fact's spelling: `AssignedWork(assignee=uav-1,
  work=task-move-1)`.

A relation cannot be derived by multiplying a relation with a factor:
`Destination ≠ Target × factors`. `×` conjoins factors of one thing; a relation
is a directed link, and a destination is not a relation at all.

---

## 9. Open expressions

A task, intent, or operational verb is often an **open expression**:

```text
E := fixed semantic factors + typed free variables + equations
```

```yaml
expressions:
  POSITION_GOAL:
    factors: [Task, Realm.WORLD]
    given: {actor: Entity, destination: Position}
    equations: ["Position(actor) = destination"]
    words:
      TaskIntent.MOVE: [TemporalMode.ACHIEVE]
      TaskIntent.HOLD: [TemporalMode.MAINTAIN]
```

- a **form** declares the invariant structure of an expression; a `words:`
  mapping binds the remaining dimensions per vocabulary member and the
  runtime resolves each word to its expression (`MOVE` is the
  position form at `ACHIEVE`, `HOLD` at `MAINTAIN`);
- members that differ only in one axis value are one form at different
  coordinates; a **synonym or antonym** in a vocabulary is a red flag for a
  form that has not been factored;
- a word vocabulary (`TaskIntent`, `CommandOperation`) is defined by the
  words the expressions declare;
- `given` variables are inputs; `sought` variables are answers;
- an **unbound variable is an unknown, not an error**:

```text
MOVE(actor=?, destination=?)
MOVE(actor=uav-1, destination=?)
MOVE(actor=uav-1, destination=mark-alpha)
```

- a **binding** is a reference or a value assigned to a variable; binding a
  reference is how a UID-like pointer answers "who do you mean" without
  answering any other semantic question;
- a sought variable is solved from the store through the equation when the
  corresponding fact exists:

```text
LOCATE(target=target-42) => position=?    # unknown
LOCATE(target=target-42) => position={lat, lon, h}       # after the fact exists
```

A UID does not answer a semantic question; it binds an expression variable to a
particular semantic object. Unknownness is the normal semantic state of
distributed information, and it is distinct from illegality.

Surface vocabulary (`ManeuverIntent.MOVE`) is representation, never a factor:
each word **names** an expression. A codeword is therefore not a primitive; it
is a word, and the expression carries the meaning.

---

## 10. Aggregates are not declared

Entity state packets, telemetry snapshots, task views, map markers, and
protocol payloads are not ontology and are not schema declarations. A position, a velocity, an attitude, an assignment, a fuel level, and a classification are independent facts with independent lifetimes and provenance, and they do not become one object merely because some consumer wants them in one packet.

Such aggregates are materialized at the edge — by the caller or the protocol
adapter — from semantic queries (section 11). What the algebra owes a consumer
is the ability to ask `uav × Position × Geodetic` or `uav × Velocity ×
LocalCartesian` without knowing the representation topology; assembling the
answers into a struct is compilation, not meaning, and is nobody's declaration
but the consumer's.

---

## 11. Queries

A query is a partial semantic product, optionally involving relations:

```text
frog-1 × Position
frog-1 × Position × PhysicalDomain.AIR
frame-991 × Gimbal × Attitude × Time:Capture(frame-991)
```

More factors narrow the region; an underspecified query may legitimately return
multiple matches. Ambiguity is resolved by adding factors, not by inventing
compound constants (`DRONE_CONTROL_RADIO_MODEL`) or requiring exact model paths.

---

## 12. Runtime definitions and persistence

| Definition | Derivation |
| --- | --- |
| `axes` | typed dimensions; cardinality; `applies`/`requires`/value declarations become solver rules |
| `factors` | implications, applicability, requirements, disjointness, exclusions |
| `vocabularies` + expression `words` | surface values and words naming expressions |
| `charts` | `Q * C` reduces to typed primitive variables with unit metadata; optional `coords`/`context` declares reference information |
| `relations` | named ordered operands; specialization preserves operand order |
| `expressions` | fixed factors + typed free variables + equations; `of:` selects a form; `binds:` fixes factors; `words:` names the expression |
| `aliases` | named products, resolved recursively |
| `mappings` | associations between external representations and semantic products |

Updates replace named entries within their sections and validate the complete
candidate before activation. SQLite persists definition revisions, append-only
facts, subject assertions, expression bindings, and directed relations.

Each fact retains its original values and definition revision. A mapping revision
creates a new interpretation linked to the source fact; the original source data
and previous interpretations remain available. Queries do not rewrite historical
fact meaning. Several matching facts are ambiguous, including equal values from
separate observations.

MsgPack exchange uses named fields and includes the original definition snapshot.
Unknown value and envelope fields are preserved. No generated model IDs or field
ordinals are required. Units, frames, altitude references, uncertainty, and source
times are retained without numerical conversion or fusion.
