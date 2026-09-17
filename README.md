# OCCID2 semantic algebra prototype

Executable prototype for addressing information by semantic meaning instead of
exact model and field paths. The authored schema (`occid2.schema.yaml`) is a set
of equations; the compiler and runtime derive from it. YAML is only the
transport.

## Findings

The full algebraic record is in `SPEC.md`. Summary:

- **Two judgments.** `x ⊨ P` (a thing satisfies an unordered, idempotent factor
  product) and `R(a₁, …, aₙ)` (a directed relation with ordered, named roles).
  Meaning is the entailment closure `M(x) = closure{f | x ⊨ f}`. The product is
  the semantic address: `uav-1 × Position × Geodetic`.
- **Factors identify their own dimensions.** `PhysicalDomain.AIR`,
  `BloodGroup.A_POS`; no `subject/property/role/focus` wrappers.
- **Constraints are implied by declarations.** Axis cardinality,
  `applies`/`requires` on axes and values, `disjoint`/`excludes` on concepts.
  Contradictions are derived (`Drone × BloodGroup.A_POS`), never listed.
- **Charts reduce quantity × representation to variables.** `chart Position ×
  Representation.Geodetic := lat × lon × h`. Chart produces the primitives;
  units stay metadata; the same quantity may exist in several representations
  and be narrowed by factors.
- **Tasks are open expressions.** Fixed semantic factors + typed free
  variables + equations. An unbound variable is an unknown, not an error:
  `MOVE(actor=uav-1, destination=?)`. Sought variables are solved from the
  store when the fact exists: `LOCATE(target-42) => position`.
- **Relations have named roles.** `AssignedWork(assignee=uav-1,
  work=task-move-1)`; specialization inherits direction positionally. A
  destination is not a relation — it is a variable.
- **Projections are compiled normal forms.** `VehicleState` compiles to
  `uid × lat × lon × h × vx × vy × vz × roll × pitch × yaw` and is
  materialized from whatever facts exist; missing facts leave coordinates
  unset rather than illegal.
- **Aliases are products, not classes.** `Drone := UAV × Airframe.MULTIROTOR`.
  A named and an unnamed equivalent product have the same normal form.
- **Unknown vs illegal.** No datum is unknown, not illegal
  (`empty.find(Position) == []`); `Mission × SEA × Altitude` is illegal.

## Run

```bash
python compiler.py
python tests.py
python demo.py
```

The compiler regenerates `generated/occid2.py` and
`generated/semantic_registry.json` deterministically. Expected test result:

```text
14 tests passed
```

## Files

- `occid2.schema.yaml` - canonical authored algebra
- `compiler.py` - deterministic ahead-of-time compiler
- `runtime.py` - product/relation algebra, solver, charts, expressions, store
- `generated/occid2.py` - generated Python API
- `generated/semantic_registry.json` - inspectable generated registry
- `demo.py` - worked examples
- `tests.py` - focused acceptance tests
- `SPEC.md` - algebraic and semantic findings
