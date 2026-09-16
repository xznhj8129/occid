# OCCID2 semantic algebra prototype

Executable prototype for addressing information by semantic meaning instead of
exact model and field paths. The authored schema (`occid2.schema.yaml`) is
canonical; the compiler and runtime derive from it.

## Findings

The full algebraic record is in `SPEC.md`. Summary:

- **Two judgments.** `x ⊨ P` (a thing satisfies an unordered, idempotent factor
  product) and `R(a₁, …, aₙ)` (a directed relation with ordered operands).
  Meaning is the entailment closure `M(x) = closure{f | x ⊨ f}`.
- **Factors identify their own dimensions.** `Domain.AIR`, `BloodGroup.A_POS`;
  no `subject/property/role/focus` wrappers.
- **Constraints are implied by declarations.** Axis cardinality,
  `applies`/`requires` on axes and values, `disjoint`/`excludes` on concepts.
  There is no rules block and no per-value enumeration.
- **Partial products are legal.** A question is illegal only when no completion
  exists: `Mission × Altitude` is unknown, `Mission × Domain.SEA × Altitude` is
  illegal. Contradictions are derived (`Drone × BloodGroup.A_POS` via
  `requires` + substrate cardinality), never listed.
- **Aliases and codewords are the same primitive** (a name denotes a product);
  aliases are registry-scoped, codewords are enum-member-scoped and may open a
  relation (`LOCATE` opens `Target`) without flattening its subject.
- **Every model is a named product.** Parentage entails the parent's full
  semantics, `product:` expands model references, and every model is storable.
  There is no concept/representation split.
- **Values versus referents.** A `Position` is a datum; a `Locality` or
  `Entity` is a referent. A locality has a position, it is not a position.
- **Relations are not factors.** `Destination ≠ Target × factors`. Unify
  "target of something" with a directed base and specialization:

  ```yaml
  Directed:   operands: {source: Root,   target: Root}
  Target:     specializes: Directed, operands: {source: Task, target: Root}
  Destination: specializes: Target,  operands: {target: Position}
  Affects:    specializes: Directed, operands: {source: Object, target: Root}
  ```

  Direction is inherited; queries at `Directed` see every target, at
  `Destination` only position-valued goals. Intent (`Target`, source `Task`) and
  causation (`Affects`, source `Object`) are separate specializations.

## Run

```bash
python compiler.py
python tests.py
python demo.py
```

The compiler regenerates `generated/occid2.py` and
`generated/semantic_registry.json` deterministically. Expected test result:

```text
13 tests passed
```

## Files

- `occid2.schema.yaml` - canonical authored schema
- `compiler.py` - deterministic ahead-of-time compiler
- `runtime.py` - product/relation algebra, solver, and store
- `generated/occid2.py` - generated Python API
- `generated/semantic_registry.json` - inspectable generated registry
- `demo.py` - worked examples
- `tests.py` - focused acceptance tests
- `SPEC.md` - algebraic and semantic findings
