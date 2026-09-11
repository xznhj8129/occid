# OCCID agent rules

This file is the operating contract for coding agents and automated contributors working in this repository.

OCCID is not a pile of convenient DTOs. It is a shared semantic model for heterogeneous operational systems. A locally convenient schema change can create expensive downstream churn across Sigma, HiveLink, MPFC, web clients, adapters, databases, and future consumers.

Treat ontology work as model design, not ordinary feature coding.

The central rule is:

> **Model the meaning, not the source system, current application, current UI, current protocol, or current task.**

If a change makes one adapter easier by making the shared model less truthful, the change is wrong.

If a change adds a concept that should have been composed from existing semantic pieces, the change is wrong.

If an unrelated OCCID expansion forces unrelated consumers to rewrite their models, the surrounding architecture should be examined before widening the blast radius.

---

## 1. Mandatory reading before editing OCCID

Do not begin by opening the first schema file whose name looks relevant and adding fields.

Before changing the ontology, read in this order:

1. **`AGENTS.md`** — these rules.
2. **`README.md`** — what OCCID is, what it models, and the major semantic boundaries.
3. **`docs/development.md`** — current mechanics, schema authority, identity rules, serialization, contracts, and development invariants.
4. **The relevant authored schemas under `lib/schema/`** — not generated Python.
5. **Parent, sibling, and child schemas around the concept being changed.** Never inspect only the target model.
6. **`example_usage.py`** — the canonical executable field manual showing how real OCCID is expected to be used.
7. **`idl_spec.md`** whenever changing schema syntax, compiler behavior, generation rules, atomic representations, inheritance semantics, or anything about the IDL itself.
8. **`DEVLOG.md` and Git history** when a model looks strange, duplicated, recently moved, or apparently missing. It may be the result of a deliberate semantic correction rather than an omission.

When project-specific design notes in AI_SHARED are available, they are additional design authority and must be read before re-solving a problem already documented there. Do not silently substitute a new local design because repository code is easier to inspect than the project notes.

### Documentation roles

Use the root documents for their intended purposes:

- `README.md`: durable introduction to OCCID as a whole.
- `AGENTS.md`: durable rules for agents and contributors.
- `docs/development.md`: repository mechanics and detailed development invariants.
- `idl_spec.md`: normative schema-language specification.
- `example_usage.py`: executable usage manual and canonical copy-paste examples.
- `DEVLOG.md`: history of important changes and their rationale.
- feature-specific notes: feature-specific files under `docs/`, `notes/`, or the relevant subsystem.

**Never clobber a durable root document with documentation for the current feature.** A TypeScript generator, adapter, compiler experiment, media subsystem, or other current task does not get to become the new meaning of `README.md`, `AGENTS.md`, or `example_usage.py`.

---

## 2. First question: does OCCID need to change at all?

A foreign system containing a field is not evidence that OCCID needs a field.

A UI wanting a column is not evidence that OCCID needs a field.

A consumer having inconvenient code is not evidence that OCCID needs a field.

Before adding anything, write down the semantic statement you are trying to represent **without using the source field name, protocol message name, UI label, endpoint method name, or database column name**.

Bad reasoning:

```text
MAVLink has custom_mode, therefore EntityState needs custom_mode.
TAK has type, therefore Entity needs cot_type.
The UI needs icon, therefore Entity needs icon.
This radio API returns rssi, therefore LinkState needs rssi: float.
```

Better reasoning:

```text
The source reports a vehicle operating mode. What protocol-independent state does that actually mean?
The source carries a classification/symbol code. Is that subject semantics, identity, or a representation?
The UI needs to depict an entity. Does the depiction belong in Representation rather than Entity?
The source reports signal strength. What physical quantity is it, in what unit/reference, and is that distinction already modeled?
```

Use this decision sequence:

1. Determine what the source datum or requested concept actually means.
2. Search OCCID for an existing semantic primitive, model, representation, state, relationship, measurement, vocabulary, or composition that already expresses it.
3. If OCCID can express it compositionally, use the existing model.
4. If the meaning is protocol-independent and cannot be expressed truthfully, investigate whether OCCID is missing semantic depth.
5. If the value is only useful for parsing, routing, provenance, debugging, endpoint bookkeeping, or protocol-specific state, keep it outside OCCID core.
6. If the meaning is not understood strongly enough, do not model it yet.

**Do not add a field merely to stop an adapter from complaining.**

---

## 3. Semantic-depth rule: if one concept needs more fields, inspect its descendants

This is a primary ontology design test.

Suppose you are about to add fields to a parent model `X`.

Ask:

> **Do all semantic descendants of `X` truthfully have these fields?**

If yes, the parent may be the correct level.

If no, **stop**. You are probably missing a semantic level or putting a specialized concern too high in the tree.

Example:

```text
Vehicle
├── GroundVehicle
├── Aircraft
└── Watercraft
```

If a proposed field only makes sense for aircraft, it does not belong on `Vehicle` merely because the current application happens to work mostly with aircraft.

The correct answer may be an intermediate semantic level:

```text
Vehicle
├── GroundVehicle
├── AirVehicle
│   ├── FixedWing
│   └── Rotorcraft
└── Watercraft
```

or it may be a separate Representation, Property, Capability, State, Definition, Struct, or Vocabulary rather than another object level at all.

### Parent-field checklist

Before adding a field to a parent:

- enumerate the parent's direct children;
- inspect representative descendants;
- ask whether the field is universally meaningful at that level;
- ask whether it describes stable identity/definition, mutable state, a representation, a capability, a relationship, or a protocol artifact instead;
- ask whether a missing intermediate semantic concept would make the tree more truthful;
- ask whether the requested field is actually a reusable Struct or Representation that should be referenced rather than copied.

If you cannot explain why the field belongs to the descendants that inherit it, do not put it on the parent.

---

## 4. Semantic-level rule: do not skip directly from broad kind to specific designation

A useful smell test is:

> **If the ontological tree goes directly from `Car` to `1973 Chevy Impala`, you are probably missing one or more semantic levels.**

The problem is the **direct jump**. A specific product or designation may be meaningful somewhere in the system, but the ontology should not leap from a broad category straight to a very specific implementation while skipping reusable distinctions in between.

A semantic tree may need levels such as:

```text
Vehicle
└── GroundVehicle
    └── Automobile
```

while manufacturer, model family, model designation, production year, configuration, capability package, serial number, and the particular physical vehicle may belong in Definitions, templates, Properties, Vocabularies, or instance data depending on their meaning.

Do not encode every named product, platform variant, national designation, weapon designation, API operation, mission verb, or equipment catalog item as a new ontology class.

A new semantic node is justified when the distinction changes **meaning or structure**, not merely because the thing has a different name.

### Do not overcorrect into taxonomy inflation

The opposite mistake is also wrong.

Do not invent intermediate classes merely to make the tree look detailed. Every semantic level must represent a real, reusable distinction in meaning or structure.

If the distinction has no different fields, no different semantic behavior, and no independent meaning beyond a bounded category value, it probably belongs in a Vocabulary or Definition rather than another Concept.

### Warning signs that you are too specific

Stop and reconsider if a proposed model name looks like:

- a manufacturer + product;
- a year + product;
- a particular military designation that differs only by equipment package;
- a UI feature;
- an endpoint method;
- a protocol message name;
- a mission verb with no unique structure;
- a database table name;
- one consumer's internal class name.

Some named standards and standard-specific vocabularies are legitimate because the standard itself defines meaning. The existence of a standard-specific term does not automatically make it a new ontology class.

---

## 5. Choose the right semantic mechanism: Concept, Representation, or Vocabulary

OCCID currently has three authored semantic building blocks:

```text
Concept          semantic category in the ontology
Representation   explicit data-bearing shape
Vocabulary       closed controlled values
```

Use them deliberately.

### Use a Concept when

- the distinction is a real semantic category;
- other things can truthfully be said to be a kind of it;
- the concept is useful independently of one encoding or presentation;
- the distinction belongs in the ontology rather than only in a data shape.

### Use a Representation when

- the thing is an explicit data-bearing shape;
- it represents, measures, depicts, records, structures, or carries semantic information;
- it is a practical typed form without claiming a new fundamental category of reality;
- it is a reusable value or record needed by multiple concepts.

### Use a Vocabulary when

- the difference is a bounded controlled word/category/operation;
- the alternatives do not need materially different fields;
- the alternatives do not deserve independent identity;
- the distinction is better represented as one typed choice than as a class explosion.

Example:

```text
Task
  TaskManeuver(intent: ManeuverIntent)
```

with movement/hold/search-style distinctions in vocabulary is generally better than:

```text
MoveTask
HoldTask
SearchTask
...hundreds more verb classes...
```

Do not create a model merely to make an enum value feel more object-oriented.

---

## 6. Field-type rule: plain strings and plain numbers are suspicious

OCCID already contains typed IDs, measurements, text forms, spatial structures, timestamps, ranges, vectors, units, resource structures, representations, and controlled vocabularies **for a reason**.

Before adding a field typed as plain `string`, `int`, or `float`, stop and search the schema.

### String smell test

A plain string may be correct for an irreducible human-readable name, label, free text, opaque external token, or code that is semantically a string.

It is probably wrong when the value is actually:

- an OCCID identity;
- an external/protocol identity that deserves an explicit `*_ref`, `*_code`, or `*_address` meaning;
- a bounded category that should be a Vocabulary;
- a measurement encoded as text;
- a timestamp;
- a URI;
- a callsign or standardized code for which a typed representation already exists;
- structured content being flattened because defining the structure is inconvenient.

Do not use strings as universal semantic solvent.

### Integer smell test

A plain integer may be correct for a genuine count, ordinal, bounded scalar, or local index.

It is probably wrong when the value is actually:

- an OCCID ID — use `IntID(Namespace)`;
- a bitmask — use flags/vocabulary or a typed representation;
- a timestamp — use the appropriate time representation;
- an enum encoded numerically — use a Vocabulary;
- a measurement — use an existing measurement/quantity representation;
- a foreign protocol numeric code being copied directly into OCCID.

### Float smell test

A plain float is especially suspicious when the value has units, datum, frame, direction, uncertainty, scale, or reference semantics.

A source field named `speed`, `altitude`, `rssi`, `heading`, `range`, `power`, `voltage`, `temperature`, or `frequency` is not semantically complete merely because it is numeric.

Search for an existing typed representation first.

### Collection smell test

Avoid generic maps, arbitrary metadata bags, `dict[str, Any]`, or string-keyed property dumps as an escape hatch from semantic modeling.

If the fields are operationally meaningful enough for consumers to rely on them, they deserve explicit semantics.

---

## 7. Reuse existing Structs, primitives, and vocabulary

> **We have predefined Structs, primitives, Representations, and Vocabularies for a reason.**

Before inventing a new field shape:

1. search the compiled and authored schemas for the concept;
2. search for synonyms, not only the exact requested term;
3. inspect sibling packages;
4. inspect existing measurements, ranges, vectors, geometry, timestamps, identities, resource types, and state structures;
5. inspect `example_usage.py` for the canonical way existing primitives are composed.

Do not duplicate an existing semantic structure under a new name simply because the current feature uses different terminology.

Bad:

```text
DronePosition
VehiclePosition
TargetPosition
MapPoint
ObservationPosition
```

when the difference is already expressible through shared spatial structures plus context.

Better:

```text
GlobalPosition
PositionState
Location
Observation
```

composed according to the meaning of each record.

Duplication creates fake distinctions, translation code, and downstream churn.

---

## 8. Definition, state, observation, context, and representation are different jobs

Many ontology errors come from putting a valid field on the wrong semantic kind.

Before adding a field, ask what kind of fact it is.

### Definition

Stable description, template, type information, reusable profile, doctrinal structure, or configuration that is not a current observation.

### State

Changing operational condition of a subject at a time.

### Observation

Information observed or assessed about the external world, with source/time/evidence semantics.

### Context

The operational or scenario context that bounds interpretation or membership without forcing all members into one giant aggregate record.

### Representation

How information is depicted, encoded, organized, viewed, measured, or presented.

A military symbol shown on a map is not an intrinsic field of the Entity merely because the UI displays it there. The Entity is the subject; the symbol is a Representation.

A Mark does not become its line style, color, label, or tactical graphic.

An Organization does not become its momentary member roster.

A vehicle definition does not become its current fuel level or position.

A Task definition does not become the mutable progress of an execution attempt.

When a field seems awkward, first ask whether it belongs to another semantic job rather than adding another field to the current model.

---

## 9. Identity rules are strict

Do not invent identity semantics locally.

- `UID` is OCCID global identity.
- `IntID(Namespace)` is a compact integer identity explicitly scoped by schema namespace.
- `Entity.38`, `Track.38`, and `Task.38` are distinct identities even though their integer values match.
- Durable cross-object references generally use UIDs.
- A string is not an OCCID ID.
- Protocol IDs, addresses, packet IDs, database keys, CoT UIDs, MAVLink sysid/compid, callsigns, names, and correlation tokens are not automatically OCCID identity.
- `Record.uid` is record identity; it is not a substitute for the logical subject UID.

If an external identifier must be preserved, name it for what it is: `*_ref`, `*_code`, `*_address`, or another truthful explicit representation.

Never collapse protocol identity, record identity, semantic object identity, and transport addressing into one field because they all look like IDs.

---

## 10. Protocols and APIs are stress tests, not schema authorities

MAVLink, CoT/TAK, MSP, ROS, MAVSDK, external databases, standards, sensors, and proprietary APIs are useful because they expose semantic requirements OCCID may have missed.

They do **not** own OCCID's vocabulary.

At an external boundary:

```text
foreign protocol
    -> protocol-shaped parse/snapshot
    -> semantic interpretation
    -> OCCID
```

The parser may remain protocol-shaped. That is not a failure.

Do not drag protocol-native structure through the semantic boundary merely to avoid translation.

The same is true outbound:

```text
OCCID
    -> semantic mapping
    -> protocol-specific representation
```

Endpoint methods such as `arm()`, `goto_location()`, `start_offboard()`, or message names do not automatically become ontology classes.

### Historical warning: the HiveLink lineage

Early HiveLink combined transport with an informal data protocol. Flat payloads carried flight-mode strings, airspeed, groundspeed, heading, altitude, RSSI, SNR, latency, endpoint-shaped commands, and similar convenient fields.

Some of that lineage later leaked into OCCID as generic telemetry bags and `native_*` fields. That made adapters easy to extend but made the semantic model shallow and protocol-shaped.

The eventual cleanup removed those escape hatches and replaced them with semantic primitives, typed state, and protocol-neutral structures.

Remember the lesson:

> **An existing protocol-shaped OCCID field is not precedent for adding another one. It may be historical residue that should be corrected.**

---

## 11. No `native_*`, `misc`, `extra`, or generic telemetry escape hatches

Do not solve modeling uncertainty with fields such as:

```text
native_mode
native_status
protocol_code
misc
extra
metadata
telemetry: map[string, any]
properties: map[string, string]
```

unless the field is genuinely and explicitly modeling provenance/opaque external data at a boundary whose semantics require it.

If consumers are expected to understand the contents semantically, the contents belong in the ontology as explicit typed meaning.

If the meaning is not understood, investigate it.

If it is protocol-local bookkeeping, leave it in the adapter.

Do not create a universal bag because semantic modeling is inconvenient.

---

## 12. Do not make one consumer a second semantic authority

Consumers use OCCID semantics. They do not redefine them.

Do not make consumers maintain parallel copies of:

- OCCID enum values;
- model descendant lists;
- semantic names;
- identity rules;
- unit meaning;
- the ontology tree;
- model fields;
- structural contracts.

If changing one OCCID semantic fact requires manually changing the same semantic fact in many consumers, check whether the authority boundary is wrong.

Generated bindings, contract metadata, runtime semantic registries, and the OCCID schema should provide the shared information where possible.

Presentation-local constants remain application concerns; semantic constants belong to OCCID.

---

## 13. Consumer resilience is part of ontology design

OCCID is expected to expand.

Adding an unrelated model, optional field, child specialization, representation, or vocabulary member should not require every consumer to rewrite itself.

Consumers should depend on the semantic symbols and fields they actually use.

Therefore, while changing OCCID:

- do not treat the global schema hash as proof that every consumer is incompatible;
- use per-symbol structural contract information where appropriate;
- do not introduce broad compatibility gates when a narrow dependency is sufficient;
- do not encourage consumers to reconstruct or validate entire durable documents merely to read one known field;
- do not preserve old bad semantics as parallel writable models merely to avoid updating a real consumer.

A real semantic breaking change should break the consumers that actually depend on that semantic contract. It should not detonate unrelated subsystems by accident.

---

## 14. `example_usage.py` is canonical and must be maintained

`example_usage.py` is not disposable sample code.

It is the **canonical executable OCCID field manual** and the preferred copy-paste source for how the model is supposed to be used.

Its opening statement is authoritative:

> It is the readable, executable answer to “how is OCCID supposed to work?”

Treat it as architecture expressed in code.

### Requirements

When a schema change affects a major usage pattern, update `example_usage.py` in the **same change**.

Examples include changes to:

- identity creation and references;
- Record construction;
- organizations and organization state;
- Nodes and communication;
- tasks, assignments, plans, authority, and execution;
- commands and vehicle-facing operations;
- EntityState and telemetry;
- observations and tracks;
- named/compact serialization;
- interop boundaries;
- representations used in common workflows.

Do not leave the field manual showing obsolete patterns while new code demonstrates a different architecture elsewhere.

### Canonical copy-paste rule

If an agent needs to know how to:

- create a UID;
- create a Record;
- create a Task;
- create an Assignment;
- represent state;
- link identities;
- send an OCCID message;
- map CoT/MAVLink data;
- serialize a model;
- express a complete small workflow;

**look in `example_usage.py` first.**

If the canonical example does not show a basic pattern that every consumer needs, consider adding a concise example there rather than inventing a new competing HOWTO.

### Keep it executable

After ontology changes, `example_usage.py` must still execute successfully.

It must use the current canonical namespace and current semantic patterns.

Do not turn it into a giant test fixture full of mocks. It must remain readable enough that a human or coding agent can follow the operational story linearly.

Do not replace it with language-binding examples. Python and TypeScript generator examples supplement the field manual; they do not supersede it.

---

## 15. Generated code is not the schema

The authored source of truth lives under:

```text
lib/schema/
```

The normal generation path is:

```text
lib/schema/**/*.schema.yaml
        -> compile_occid.py
        -> occid.yaml
        -> runtime generators
        -> generated Python / TypeScript bindings
```

Do not hand-maintain generated Python or TypeScript as an independent ontology.

If generated output is wrong, fix the authored schema, compiler, or generator as appropriate and regenerate.

Do not infer ontology semantics from Python inheritance. The generated runtime is intentionally flat; semantic ancestry comes from OCCID metadata and the authored `parent` graph.

---

## 16. Schema-language changes are different from ontology changes

Do not modify the compiler or IDL to solve one awkward model unless the language itself is genuinely missing a reusable capability.

If you think the IDL needs a new feature:

1. read `idl_spec.md` completely around the relevant mechanism;
2. inspect existing syntax and compiler behavior;
3. prove that the requirement cannot be represented correctly with the current language;
4. define the semantics of the new syntax, not only how to parse it;
5. update the specification;
6. update compiler validation;
7. update generators;
8. add focused tests;
9. regenerate outputs;
10. update `example_usage.py` if the usage model changes.

A one-off schema inconvenience is not enough reason to make the language more complicated.

---

## 17. Creation of new models: required questions

Before adding a new model, answer all of these:

1. What real semantic distinction does this model represent?
2. Why can existing OCCID concepts not represent it by composition?
3. Is it a Concept, Representation, or Vocabulary concern?
4. What is its correct semantic parent?
5. Are you skipping one or more meaningful semantic levels between the parent and this model?
6. Does the model actually need unique fields, or is it only a vocabulary value/definition?
7. Are any proposed fields duplicated from an existing Struct/Representation?
8. Are any proposed strings actually IDs, codes, addresses, names, URIs, or vocabulary?
9. Are any proposed integers actually IDs, enums, flags, timestamps, or measurements?
10. Are any proposed floats missing units/reference/frame semantics?
11. Does any field belong in State, Observation, Representation, Definition, Property, Capability, or Context instead?
12. Is the model named after a protocol/API/UI/product instead of the underlying meaning?
13. Which existing consumers truly need to know about this new model?
14. Does `example_usage.py` need to demonstrate the new pattern?

If several answers are unclear, do not start coding yet.

---

## 18. Adding fields: required questions

Before adding a field to an existing model, answer:

1. What exact semantic fact does the field represent?
2. Does every descendant that inherits it truthfully possess that fact?
3. If not, is there a missing semantic level?
4. Is the field stable definition or changing state?
5. Is it subject semantics or representation/display semantics?
6. Is it an intrinsic property or a relationship to another object?
7. Is there already a typed OCCID primitive/Struct/Representation for it?
8. Is the type truthful about units, reference, datum, time basis, identity scope, and optionality?
9. Is it protocol-independent?
10. Could a vocabulary express the distinction instead of another field/model?
11. What existing consumers actually read this field?
12. What regression tests prove unrelated schema changes remain unrelated?

---

## 19. Moving or removing semantics

During active development, correcting the semantic model is allowed and expected.

Do not preserve a bad field forever merely because some current consumer uses it.

When moving/removing semantics:

1. identify why the old location is semantically wrong;
2. establish the correct semantic home;
3. update the authored schema;
4. update canonical usage in `example_usage.py` where applicable;
5. update directly affected interop helpers and tests;
6. regenerate outputs;
7. inspect structural contract changes;
8. update affected consumers deliberately.

Do not maintain two writable authoritative forms indefinitely as a compatibility shortcut.

Compatibility or migration boundaries, when genuinely required, must be explicit and temporary.

---

## 20. Representations must remain separate from subjects

Do not put map/UI/rendering concerns on semantic subjects simply because the current application needs them together.

Examples:

- symbology belongs to symbol/graphic Representation, not Entity;
- line style/color/fill belongs to graphic style, not spatial subject;
- a media overlay is not the media object itself;
- a range ring is a derived graphic/measurement representation, not a property of the tracked object;
- a saved map view is not an operational Entity.

A subject can exist without one particular representation, and several different representations may depict the same subject.

This separation is intentional and must be preserved.

---

## 21. Organizations: definition, instance, and state are distinct

Do not collapse:

```text
organization template
organization instance
organization state
```

into one structure.

A template describes reusable organization structure or requirements.

An Organization is a concrete identified organization.

OrganizationState describes mutable membership, roster, readiness, or similar changing condition.

Likewise, Side/Coalition/grouping semantics are not automatically equivalent to rendering affiliation or symbology standard identity.

---

## 22. Media: semantic specialization instead of type switches

Do not regress media back into one generic record with a string/enum type switch when concrete media forms have real semantic structure.

The current direction is semantic specialization such as:

```text
MediaItem
├── ImageMedia
│   └── StillImage
│       ├── Photograph
│       └── VideoFrame
├── VideoMedia
│   ├── VideoRecording
│   └── LiveVideoStream
├── AudioMedia
├── SpectrumMedia
├── PointCloudMedia
├── DocumentMedia
└── BinaryMedia
```

If a new media kind has materially different structure, model the semantic specialization. If it differs only by a bounded format/code with the same semantics, use an appropriate field/vocabulary instead.

---

## 23. Control and tasking: preserve the semantic layers

Do not collapse intent, assignment, authority, execution, and command into one convenience object.

The durable distinction is:

```text
Objective        desired outcome
Task             directed work / intent
Authority        permission/right to direct work
Assignment       binding of work to an assignee
Plan             organized intended course of action
Execution        runtime attempt/progress
Command          immediate bounded operation
```

> **Task preserves intent. Command prescribes operation.**

Transport delivery is not executor acceptance. Acceptance is not execution progress. Progress is not completion.

Do not encode endpoint methods as ontology classes merely because a flight controller or SDK exposes them.

---

## 24. Tests must protect semantic rules, not only generated syntax

A generator compiling successfully does not prove the ontology is correct.

Tests should protect important invariants such as:

- parent/child semantic relationships;
- required type/field semantics;
- identity namespaces;
- vocabulary values where interoperability depends on them;
- separation of definition/state/representation;
- named JSON round trips;
- compact-wire behavior;
- contract generation;
- canonical usage in `example_usage.py`;
- historical regressions that previously caused semantic collapse.

When fixing a semantic regression, add a test that makes the same regression difficult to reintroduce.

---

## 25. Required workflow for ontology changes

For a normal schema expansion or correction:

```text
1. Read AGENTS.md, README.md, development docs, relevant schemas,
   parents/siblings/children, and example_usage.py.

2. State the semantic requirement in protocol-independent language.

3. Search existing OCCID semantics before adding anything.

4. Decide Concept vs Representation vs Vocabulary.

5. Check semantic depth:
      - does the parent fit all descendants?
      - are semantic levels being skipped?
      - are unnecessary levels being invented?

6. Design fields using existing typed primitives/Structs where possible.

7. Edit authored schema under lib/schema/.

8. Update example_usage.py if the canonical usage pattern changed.

9. Add/update focused semantic tests.

10. Run generation.

11. Run tests and example_usage.py.

12. Inspect generated diff and structural contract changes.

13. Update only consumers whose used semantics actually changed.

14. Record important semantic rationale in DEVLOG.md when the change is
    non-obvious, corrective, or likely to be questioned later.
```

Do not skip directly from step 1 to editing generated Python.

---

## 26. Review smell tests

Before declaring an ontology change complete, scan it for these smells.

### Smell: broad parent got a specialized field

Ask whether every descendant needs it. If not, find the missing level or move the concern.

### Smell: lots of new strings

Search for typed primitives, vocabularies, IDs, URIs, names, codes, addresses, or structs.

### Smell: lots of new plain ints/floats

Check IDs, enums, flags, measurements, units, time, reference frames, ranges, and counters.

### Smell: class per verb/product/model

Check whether vocabulary, Definition, template, property, or a missing intermediate semantic level is more truthful.

### Smell: UI/rendering field on Entity/Location/etc.

Move it to Representation/Graphic/style semantics.

### Smell: current value on stable definition

Consider State or Observation.

### Smell: protocol name in core semantic field/model

Restate the meaning without the protocol name and reconsider the boundary.

### Smell: generic metadata bag

Ask whether the data is important enough to model or protocol-local enough to leave outside OCCID.

### Smell: consumer duplicates OCCID semantic tables

Generate/derive them from OCCID instead.

### Smell: README/example replaced by current feature docs

Restore durable project documentation and put feature docs in their own file.

### Smell: every consumer breaks after unrelated ontology expansion

Do not normalize that as expected. Investigate the consumer boundary and contract design.

---

## 27. What “minimal but semantically deep” means

OCCID should not grow by speculative taxonomy.

It also must not stay artificially small by flattening real distinctions.

Minimal means:

- avoid duplicate concepts;
- avoid source-protocol vocabulary in core;
- avoid one class per product/verb/category;
- reuse common semantic primitives;
- compose existing structures where truthful;
- add semantic levels only when they carry reusable meaning.

Semantically deep means:

- preserve distinctions that materially affect meaning;
- model units, references, identity scopes, states, relationships, and representations explicitly;
- treat real integration failures as evidence that the model may be shallow;
- refine the model when a protocol-independent fact cannot otherwise be represented truthfully.

The target is not the smallest possible YAML file.

The target is the smallest coherent semantic system that can truthfully express the operational distinctions real consumers need.

---

## 28. Final rule

When uncertain, do not ask:

> “What field/class would make this code easiest to write?”

Ask:

> **“What is this fact actually saying about the operational world, and where does that meaning belong?”**

Then check the existing ontology, its semantic levels, its typed primitives, its vocabulary, its state/definition/representation boundaries, and the canonical field manual before adding anything.
