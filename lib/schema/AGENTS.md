# OCCID schema agent rules

These rules apply specifically to authored ontology/schema work under `lib/schema/`.

The root [`AGENTS.md`](../../AGENTS.md) remains authoritative. This file exists because schema work is where semantic mistakes become expensive, and agents editing this tree must see the ontology rules at the point of use.

Before editing any schema here, read:

1. `../../AGENTS.md`
2. `../../README.md`
3. `../../docs/development.md`
4. the relevant parent, sibling, and child schemas
5. `../../example_usage.py`
6. `../../idl_spec.md` if touching the IDL/compiler/generator contract

Do not treat this directory as a collection of DTO definitions. It is the authored semantic source of truth for OCCID.

---

## 1. Semantic depth is not taxonomy inflation

A semantic level should exist because the ontology needs it, not because it can be imagined.

Do **not** prebuild abstraction layers merely because a concept could theoretically have children someday.

A parent or intermediate semantic level is justified when at least one of these is true:

- multiple concrete children/representations already exist;
- multiple concrete children/representations are credibly expected from the domain being modeled;
- several children need shared fields or constraints at that level;
- other schemas need to refer to the parent meaning independently of any one child;
- code or interop needs polymorphism over that semantic family;
- the parent captures a durable reusable distinction that would otherwise be duplicated across children.

A parent is questionable when:

- it has one child and no independent semantic use;
- its only purpose is to make the tree look more elegant;
- it merely restates the child's meaning more abstractly;
- no credible sibling is expected;
- the supposed distinction can be handled more truthfully by a Vocabulary, Definition, Property, Capability, Representation, or ordinary conversion code.

One-child parents are not forbidden. They are a **review smell**. Explain why the parent is expected to become a real semantic family or why it is independently useful.

---

## 2. Expected polymorphism is the main test

Before adding an intermediate parent, ask:

> **Do we genuinely expect more than one semantic child or representation to appear here?**

If the answer is no, do not create hierarchy merely for theoretical purity.

### Example: measurement/unit representations

Suppose a field represents distance.

Ask whether OCCID genuinely needs several first-class distance representations with materially different semantics, or whether OCCID should use one canonical semantic representation and convert external units at the boundary.

If the operational model is perfectly served by canonical meters:

```text
external feet / yards / nautical miles
        -> adapter conversion
        -> canonical OCCID distance in meters
```

then creating a hierarchy such as:

```text
Quantity
└── Distance
    └── Meters
```

may be unnecessary abstraction if `Distance` has no sibling representations and no independent use.

The same question applies to electrical quantities such as amperes, volts, watts, and similar typed scalar representations. A typed representation can be useful and defensible, but do not assume that every physical unit needs an abstract parent hierarchy merely because dimensional analysis permits one.

Ask:

- Will there actually be multiple OCCID representations under this parent?
- Do consumers need to accept the parent polymorphically?
- Does the parent carry shared fields or semantics?
- Is the distinction semantic, or only a unit-conversion problem?
- Can adapters normalize to one canonical representation instead?

Canonicalization in code is often preferable to speculative ontology.

---

## 3. Conversely, preemptive parents are justified when the family is obvious

Do not wait for the second child when the domain already makes the semantic family obvious and reusable.

For example, if adding:

```text
MainBattleTank
```

placing it directly under an overly broad parent such as `GroundVehicle` may be too shallow.

A level such as:

```text
GroundVehicle
└── ArmoredVehicle
    ├── MainBattleTank
    ├── InfantryFightingVehicle
    ├── ArmoredPersonnelCarrier
    ├── ArmoredReconnaissanceVehicle
    └── SelfPropelledArtillery
```

can be justified **before every sibling is implemented**, because multiple real members of the semantic family are already obvious and likely, and shared armored-vehicle semantics may reasonably emerge.

This is not speculative taxonomy for its own sake. It is preserving an obvious reusable level in a family that is known to be plural.

The test is not "does the parent have two children in the repository today?"

The test is:

> **Is this a real semantic family with credible polymorphism, or am I inventing an abstraction because abstractions feel clean?**

---

## 4. Do not skip meaningful levels either

The opposite failure remains equally important:

> **If the ontological tree goes directly from `Car` to `1973 Chevy Impala`, you are probably missing one or more semantic levels.**

The word **directly** matters.

A specific product/designation may be legitimate somewhere in the model, but jumping straight from a broad category to a highly specific implementation usually collapses reusable semantic structure.

You may need levels such as:

```text
Vehicle
└── GroundVehicle
    └── Automobile
```

while manufacturer, model family, model designation, year, trim, capability package, serial number, and the particular physical object may belong in Definitions, Properties, Vocabularies, templates, or instance data rather than ontology subclasses.

Do not blindly create all imaginable intermediate levels. Create the levels the domain actually needs.

---

## 5. Parent-field test

Before adding a field to a parent model `X`, ask:

> **Do all semantic descendants of `X` truthfully possess this field?**

If no, stop.

Possible explanations include:

- the field belongs on a narrower existing child;
- a missing intermediate semantic family is now justified;
- the field belongs in State;
- the field belongs in a Representation;
- the field belongs in a Definition/template;
- the field belongs in a Property or Capability;
- the distinction belongs in Vocabulary;
- the datum is protocol-local and should remain in the adapter.

Do not poison a broad parent because the current consumer mostly uses one child family.

---

## 6. New parent checklist

Before creating an intermediate parent, answer:

1. What semantic statement does this parent make?
2. What concrete children exist or are credibly expected?
3. Why are those children meaningfully a family?
4. What fields/constraints/behavior, if any, are genuinely shared?
5. Does another model need to refer to this parent polymorphically?
6. Would a Vocabulary express the distinction more simply?
7. Would a Definition/template/property express the distinction more truthfully?
8. Is this merely a unit conversion or formatting concern?
9. If only one child exists, why is the parent independently useful or why are additional children expected?
10. Would removing the parent lose meaning, or merely make the tree visually flatter?

If the last answer is "it would only look less elegant," do not add it.

---

## 7. New child checklist

Before adding a specialized child, answer:

1. Does it have materially different structure or semantics?
2. Is it merely a vocabulary value with no structural difference?
3. Is its proposed parent too broad?
4. Are one or more missing semantic levels now evident?
5. If an intermediate parent is introduced, is there credible future polymorphism at that level?
6. Are product/designation facts being confused with ontology categories?
7. Could Definition/template/Property/Capability hold the specialization instead?

---

## 8. Typed primitives and representations: useful, but not automatically hierarchical

OCCID uses typed IDs, timestamps, spatial values, measurements, text forms, ranges, vectors, quantities, and other representations because semantic typing matters.

That does **not** imply every typed scalar must sit inside a deep class tree.

A named atomic Representation is justified when the name itself carries useful semantic meaning and prevents ambiguity.

A parent hierarchy above it requires a separate justification.

For example:

- `Amperes` may be useful because a bare float is ambiguous.
- A generic parent above `Amperes` is justified only if that parent is itself useful or is expected to support a real family of sibling representations.
- `Distance` may be useful as a semantic quantity, but if every OCCID distance is canonical meters and external units are converted at the boundary, a separate `Meters` child may add little value.

Do not confuse **typed value** with **need for hierarchy**.

---

## 9. Canonical units versus multiple representations

Prefer canonical semantic units when multiple external units are merely alternate encodings of the same fact.

Example:

```text
feet        \
yards        +--> conversion --> OCCID canonical distance
meters      /
nautical mi/
```

Different units deserve separate first-class OCCID representations only when preserving the distinction is operationally meaningful, required for round-trip fidelity, required by a standard OCCID intentionally represents, or otherwise semantically significant.

Do not make the ontology carry unit diversity that adapters can losslessly normalize.

Conversely, do not throw away distinctions that are **not** lossless conversion problems. Datum, reference frame, clock basis, identity scope, uncertainty model, coordinate frame, and similar semantics may require explicit representation even if the underlying primitive is numerically convertible.

---

## 10. Concrete heuristic

Use this rough decision rule:

```text
Need one concrete typed thing only?
    -> define the simplest truthful Representation / field.

Need alternate external units only?
    -> prefer canonical OCCID representation + adapter conversion.

Need a bounded categorical distinction only?
    -> Vocabulary.

Need reusable configuration/type metadata?
    -> Definition/template/Property/Capability as appropriate.

Need several concrete shapes that are genuinely kinds of one thing?
    -> semantic parent + children.

Only one child exists, but several real siblings are clearly expected?
    -> preemptive parent can be justified.

Only one child exists and future siblings are hypothetical?
    -> usually do not create the parent yet.
```

---

## 11. `example_usage.py` remains canonical usage

Schema design and runtime usage are connected.

If a new semantic family changes how consumers are expected to construct, refer to, serialize, or compose common OCCID objects, update `../../example_usage.py` in the same change.

Do not invent a new pattern in a subsystem and leave the canonical field manual behind.

When in doubt about how existing OCCID structures are supposed to be used, copy from `example_usage.py` first.

---

## 12. Final test

Before adding a semantic level, ask both questions:

> **Am I missing a reusable semantic level that the domain genuinely needs?**

and

> **Am I inventing a semantic level that the domain does not need yet?**

Both errors are real.

OCCID should be deep where reality is deep and flat where extra hierarchy would only be decoration.