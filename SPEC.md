# OCCID2 semantic algebra notes

## 1. Schema is canonical

The authored schema (`occid2.schema.yaml`) is a set of equations, not a class
hierarchy. The compiler and runtime derive everything from it: there is no
rules block, no second hierarchy, and no hard-coded inheritance logic. When
this document and the schema disagree, the schema wins and the derivation must
be fixed. YAML is only the transport.

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

## 6. Models are named products

Every model is a named region of semantic space:

```text
semantics(model) = inherited factors + model name + product factors
```

- parentage **entails**: an ancestor's name is a label, not a factor, so
  inheritance carries the ancestor's `product:` factors and drops its labels;
  the closure re-derives the labels from parentage;
- a `product:` entry naming another model expands to that model's semantics,
  keeping its label, because that name is part of this model's own meaning;
- a `chart:` entry contributes the chart's factors and compiles its variables
  into the model's fields;
- every model is storable; there is no concept/representation split.

Example:

```yaml
GlobalPosition:
  chart: Position * Representation.Geodetic
```

```text
GlobalPosition = GlobalPosition × Position × Representation.Geodetic
               ≅ lat:float[deg] × lon:float[deg] × h:float[m]
```

A product surfaces at its first level: the most specific model name plus all
factors, never the whole chain. `Drone` surfaces as

```text
Drone = UnmannedVehicle × Controller.UNMANNED × Locomotion.SELF_PROPELLED
      × Substrate.MECHANICAL × PhysicalDomain.AIR × Airframe.MULTIROTOR
```

`Machine`, `Vehicle`, `Entity`, `Object`, and `Root` are entailed labels; they
are not repeated as factors.

Renaming or restructuring a model does not change the meaning of stored data as
long as the semantic region it denotes is preserved. Fields are representation
and can reach other things; they are not factors:

```text
Drone.mission: Mission     is a relation, not Drone × Mission
```

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
that selection. A coordinate's unit is algebraic metadata (`_units`), not its
Python type.

The same quantity may be stored in several representations. Each is a separate
datum; each answers `entity × Position`, and a representation factor narrows to
one:

```text
uav-1 × Position            -> [GlobalPosition, LocalPosition]
uav-1 × Position × Geodetic -> GlobalPosition(lat, lon, h)
```

This is the operational answer to "how does a semantic quantity become actual
data?" It also means a different struct can represent the same product without
changing the product.

---

## 8. Relations

A relation declares its own operands: named, ordered, and directed. Operand
roles belong to the relation, not to a global schema:

```yaml
relations:
  Directed:                       # arity and direction declared once
    operands: {source: Root, target: Root}

  Affects:                        # causal: object -> receiver
    specializes: Directed
    operands: {source: Object, target: Root}

  AssignedWork:                   # intentional: entity -> task
    specializes: Directed
    operands: {assignee: Entity, work: Task}
```

Consequences:

- direction and operand order are inherited positionally; a specialization may
  narrow operand regions and rename roles;
- a query at `Directed` returns every fact whose relation specializes it;
- roles are part of the fact's spelling: `AssignedWork(assignee=uav-1,
  work=task-move-1)`.

A relation cannot be derived by multiplying a relation with a factor:
`Destination ≠ Target × factors`. `×` conjoins factors of one thing; a relation
is a directed link. Destination-like holes in tasks are not relations at all;
they are free variables of an open expression (section 9).

---

## 9. Open expressions

A task, intent, or operational verb is often an **open expression**:

```text
E := fixed semantic factors + typed free variables + equations
```

```yaml
expressions:
  MOVE:
    factors: [Task, Realm.WORLD, TemporalMode.ACHIEVE]
    given: {actor: Entity, destination: Position}
    equations: ["Position(actor) = destination"]

  LOCATE:
    factors: [Task, Realm.INFORMATION, TemporalMode.ACHIEVE]
    given: {target: Entity}
    sought: {position: Position}
    equations: ["Position(target) = position"]
```

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
LOCATE(target=target-42) => position=GlobalPosition(…)   # after the fact exists
```

A UID does not answer a semantic question; it binds an expression variable to a
particular semantic object. Unknownness is the normal semantic state of
distributed information, and it is distinct from illegality.

Surface vocabulary (`ManeuverIntent.MOVE`) is representation, never a factor:
each word **names** an expression. A codeword is therefore not a primitive; it
is a word, and the expression carries the meaning.

---

## 10. Projections

A projection is a compiled aggregate over independent facts, not an
ontological object:

```yaml
projections:
  VehicleState:
    product:
      - Position * Representation.Geodetic
      - Velocity * Representation.LocalCartesian
      - Attitude * Representation.LocalEuler
    fields: {uid: UID}
```

The compiler reduces each listed product through its chart and emits the
concrete typed coordinates; the runtime materializes them from whatever facts
exist:

```text
VehicleState ≅ uid × lat × lon × h × vx × vy × vz × roll × pitch × yaw
```

A projection may be partial: a fact that does not exist leaves its coordinates
unset rather than illegal. `EntityState`, `TelemetrySnapshot`, `TaskView`, map
markers, and protocol payloads are all projections in this sense — useful
aggregations that do not become ontology.

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

## 12. Schema mapping

| Schema | Derivation |
| --- | --- |
| `axes` | typed dimensions; cardinality; `applies`/`requires`/value declarations become solver rules |
| `enums` + expression `words` | surface vocabulary; each member names an expression and entails its factors |
| `charts` | `Q * C` reduces to typed variables; a quantity's data normal form |
| `relations` | named ordered operands; `specializes` inherits direction positionally |
| `expressions` | fixed factors + typed free variables + equations |
| `models` | named products; parent entailment; `product:`/`chart:` expansion |
| `projections` | compiled aggregates over chart-selected facts |
| `aliases` | class-free named products, resolved recursively |

`generated/occid2.py` and `generated/semantic_registry.json` are deterministic
outputs. The compiler produces no rules block, no role flags, and no second
class hierarchy.
