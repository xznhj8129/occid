# OCCID2 semantic algebra notes

## 1. Schema is canonical

The authored schema (`occid2.schema.yaml`) is the source of truth. The compiler
and runtime derive everything from it: there is no rules block, no
`semantic_role`, no hard-coded inheritance logic, and no second hierarchy. When
this document and the schema disagree, the schema wins and the derivation must
be fixed.

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
factor identifies its own dimension (`Domain.AIR`, `BloodGroup.A_POS`).

A **relation** is not a factor. It is directed and its operands are ordered, so
`Wags(dog, tail) ≠ Wags(tail, dog)`. Products describe things; relations connect
things.

---

## 3. Factors and axes

An axis is one typed semantic dimension; its values are factors:

```yaml
Domain:
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
  applies: [Domain.AIR]                       # emerging: no assertion

Machine:
  disjoint: [Biological]
  excludes: [[Locomotion.SELF_PROPELLED, Domain.CYBER]]
```

Constraints compose `ALL`, `ANY`, and `NOT`. There is one generic rule per axis
declaration, never one rule per value.

### Emergent dimensions

Adding a factor can make a dimension meaningful without creating a class:

```text
Mission × Domain.AIR      gains Altitude applicability
AirTask = Task × Domain.AIR
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
Mission × Domain.SEA × Altitude   illegal (Altitude is air-only)
Drone                             legal partial product
Drone × Domain.SEA                illegal (Domain is single-valued)
```

This keeps "unknown answer" and "semantically illegal question" distinct.

### Derived contradictions

Consequences are derived, not enumerated:

```text
Drone entails Machine and Substrate.MECHANICAL
BloodGroup requires Biological
Biological entails Substrate.BIOLOGICAL
Substrate is single-valued
=> Drone × BloodGroup.A_POS is illegal
```

No `Drone cannot have a blood group` rule exists.

---

## 5. Names: aliases and codewords

Both are the same primitive: **a name denotes a product**.

- An **alias** is a registry-scoped name for a product:

```yaml
aliases:
  UGV: [UnmannedVehicle, Domain.LAND]
  UAV: [UnmannedVehicle, Domain.AIR]
  Drone: [UAV, Airframe.MULTIROTOR]
```

- A **codeword** is an enum-member-scoped name. Enum members are representation
  vocabulary; they are never semantic factors, they bind to products:

```yaml
InformationIntent.LOCATE:
  product: [Task, Realm.INFORMATION, TemporalMode.ACHIEVE, Position]
  relation: Target
```

Alias resolution is recursive and canonical: `Drone` expands through `UAV` to
`UnmannedVehicle × Domain.AIR × Airframe.MULTIROTOR`. Unknown terms stay exactly
as authored; nothing is invented or dropped.

A codeword may also declare the relation it opens. `LOCATE` asks "locate what?";
the subject is not flattened into the product, it lives in the relation.

---

## 6. Models are named products

Every model is a named region of semantic space:

```text
semantics(model) = parent's full semantics + model name + product factors
```

- parentage **entails** (including the parent's `product:` factors);
- a `product:` entry naming another model expands to that model's full
  semantics;
- every model is storable; there is no concept/representation split;
- exact class lookup remains available, with semantic lookup as the fallback.

Example (`Mark` under `Data`, representing a point):

```text
Mark = Root × Data × Mark × State × Position × GlobalPosition × Frame.WGS84
```

Renaming or restructuring a model does not change the meaning of stored data as
long as the semantic region it denotes is preserved. Fields are representation
and can reach other things; they are not factors:

```text
Drone.mission: Mission     is a relation, not Drone × Mission
```

---

## 7. Values versus referents

A `Position` is a state datum (a value). A `Locality` (village, bridge,
mountain) and an `Entity` are referents in the world. This distinction is
semantic, not cosmetic:

- a locality **has** a position: `LocatedAt(locality, position)`; it is not a
  position;
- a relation to a value and a relation to a referent are different operand
  sorts;
- the two live in different branches (`Data` vs `Object`), so neither can be
  narrowed into the other.

---

## 8. Relations

A relation declares its own operands: named, ordered, and directed. Operand
names belong to the relation, not to a global schema.

A relation cannot be derived by multiplying a relation with a factor:

```text
Destination ≠ Target × factors
```

`×` conjoins factors of one thing; a relation is a directed link. Reifying a
relation instance allows qualifier products (`r ⊨ Existence × TruthTarget.TRUE`),
but that qualifies the link, not the operands.

The only legal relation derivations are:

```text
R|ᵢ : Pᵢ'    where Pᵢ' ⊆ Pᵢ      operand narrowing
R ∘ S                              composition
```

---

## 9. Directed base and specialization

The concept "target of something" is unified at the directed-pair level, not by
widening one relation's operands:

```yaml
relations:
  Directed:                      # arity and direction declared once
    operands:
      source: Root
      target: Root

  Target:                        # intentional: a directive is about something
    specializes: Directed
    operands:
      source: Task
      target: Root               # anything may be targeted

  Destination:
    specializes: Target
    operands:
      target: Position           # narrower: the goal is a position value

  Affects:                       # causal: actor/cause -> effect receiver
    specializes: Directed
    operands:
      source: Object             # any object may be a cause, not only an Entity
      target: Root
```

Consequences:

- direction and operand order are inherited; they are never re-declared;
- a query at `Directed` returns every target of a task; at `Target` it filters
  by source; at `Destination` it filters by target region — one concept, graded
  constraints;
- intent (`Target`, source = `Task`) and causation (`Affects`, source =
  `Object`) stay separate specializations of `Directed`; a task is not a cause,
  its execution is;
- why not one flat `Root/Root` relation with distinctions as factors: a
  `Position` target is a value, a `Locality`/`Entity` target is a referent.
  Same shape, different operand sort; flattening erases exactly that.

The engine supports `operands:` and `specializes:` with topological relation
order, inherited direction, and base-level queries.

---

## 10. Queries

A query is a partial semantic product, optionally involving relations:

```text
frog-1 × Position
frog-1 × Position × Frame:World × Time:T
```

More factors narrow the region; an underspecified query may legitimately return
multiple matches. Ambiguity is resolved by adding factors, not by inventing
compound constants (`DRONE_CONTROL_RADIO_MODEL`) or requiring exact model paths.

---

## 11. Schema mapping

| Schema | Derivation |
| --- | --- |
| `axes` | typed dimensions; cardinality; `applies`/`requires`/value declarations become solver rules |
| `enums` + `codewords` | ordinary representation vocabulary; each member binds to a product, optionally opens a relation |
| `models` | named products: name factor, parent entailment, `product:` expansion |
| `aliases` | class-free named products, resolved recursively |
| `relations` | named ordered operands; `specializes` inherits direction |

`generated/occid2.py` and `generated/semantic_registry.json` are deterministic
outputs. The compiler produces no rules block, no role flags, and no second
class hierarchy.
