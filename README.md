# OCCID2 semantic algebra prototype

Executable prototype for addressing information by semantic meaning instead of
exact model and field paths. The semantic registry is the live authority for
semantic definitions and relationships. Definitions are data interpreted by the
algebra at runtime.

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
- **Aggregates are not declared.** Entity state packets, telemetry snapshots,
  task views, map markers, and protocol payloads are materialized at the edge
  from semantic queries. `uav * Position * Geodetic` and `uav * Velocity *
  LocalCartesian` are questions about independent facts; nothing that exists
  only to be a packet becomes ontology.
- **Aliases are products, not classes.** `Drone := UAV × Airframe.MULTIROTOR`.
  A named and an unnamed equivalent product have the same normal form.
- **Unknown vs illegal.** No datum is unknown, not illegal
  (`empty.find(Position) == []`); `Mission × SEA × Altitude` is illegal.
- **Control is expressed.** Open expressions have fixed semantic factors, typed
  free variables, and equations. A word names an expression.

## Run

```bash
python -m pip install -e .
python tests.py
python -m unittest tests_runtime
python demo.py
```

Expected algebra test result:

```text
17 semantic invariant groups passed
```

## Files

- `occid2/definitions.yaml` - initial semantic definitions
- `occid2/definitions.py` - runtime definition loading and validation
- `occid2/runtime.py` - product/relation algebra, solver, charts, expressions, store
- `occid2/wire.py` - self-describing MsgPack facts
- `demo.py` - worked examples
- `tests.py` - focused acceptance tests
- `tests_runtime.py` - identity, validation, serialization, revisions
- `SPEC.md` - algebraic and semantic findings

## Runtime

- `new_store()` creates an in-memory semantic runtime. Applications own storage, data sources, and lifecycle.
- `store.ref("uav-1", "UAV")` creates a subject with semantic assertions.
- `subject.set(sem("Position", "Representation.Geodetic"), {"lat": 36.530440, "lon": -83.216383, "h": 125.0}, source="sensor", observed_at=123, validity={"from": 123, "to": 124})` appends an observation.
- `subject.find("Position")` returns matching facts; `subject.get(...)` requires one match.
- `subject.get(Query("Position", source="sensor", observed_before=123, valid_at=123, latest=True))` explicitly constrains the answer. Ties and unknown observation times remain ambiguous.
- `locate.solve(position=Query(source="sensor", latest=True))` applies the same constraints to a sought variable.
- `Position × Representation.Geodetic × AltitudeReference.WGS84Ellipsoid` and `AltitudeReference.MeanSeaLevel` distinguish height references. An omitted reference remains unknown.
- `datum.value` contains the original value; chart coordinates retain their units in `store.registry.at(datum.definition_id)`.
- `registry.update({...})` validates before activation. Updates replace named entries within their sections.
- `store.task("task-1", "TaskIntent.MOVE")` creates an open expression.
- `store.relate("AssignedWork", assignee=uav, work=task.ref)` validates named, directed roles.
- `encode(datum)` and `decode(payload)` preserve named fields, original values, and definition snapshots. Wire values must be MsgPack-serializable; local insertion requires no serialization.
- `encode(datum, include_definitions=False)` uses a definition identity; `decode(payload, registry=registry)` resolves the retained revision.
- `store.add(decode(payload))` retains the sender's fact identity and definition revision.
- `store.interpret(source_datum, mapping_name)` appends a mapped fact linked to the original source datum.
- Queries use current entailment; `Query("Position", interpretation="recorded")` matches original meaning. `datum.meaning` stays recorded; `store.meaning_of(datum)` evaluates current meaning without creating a fact or converting values.
- Mapping revisions retain source values and prior interpretations. Applying a revised field mapping remains explicit.
- `UID.new()` mints a UUIDv4 as exactly 16 bytes; nonempty strings also identify subjects.

`demo.py` exercises the algebra, runtime extension, semantic addressing, and self-describing serialization.
