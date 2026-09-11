# OCCID

**Open Command, Control, Intelligence Data**

OCCID is a shared semantic model for operational systems.

It exists so that different software, devices, protocols, organizations, databases, user interfaces, autonomy systems, and transports can describe the **same operational world** without first becoming the same system.

A vehicle may speak MAVLink. A tactical application may exchange Cursor-on-Target. A flight controller may expose MSP. A C2 backend may persist JSONB. A web client may use TypeScript. A radio or mesh system may care mostly about routing and delivery. An autonomy framework may care about tasks, assignments, state, execution, and resources.

Those systems do not naturally share one vocabulary, one object model, one wire protocol, or one application architecture. OCCID provides the semantic layer between them.

```text
                  external systems and representations

        CoT / TAK      MAVLink      MSP      APIs      sensors
            \             |          |        |          /
             \            |          |        |         /
              +-----------+----------+--------+--------+
                                      |
                                      v
                                    OCCID
                                      |
                           shared operational meaning
                                      |
                 +--------------------+--------------------+
                 |                    |                    |
                 v                    v                    v
              humans               software             machines
```

OCCID is **not** a transport, message bus, database, C2 application, autonomy engine, rendering engine, or endpoint API. It is also not a schema copied from MAVLink, CoT, TAK, MSP, NATO documents, one military system, one robotics stack, or any other external vocabulary.

It is the common semantic model those systems can map **into** and **out of**.

The repository contains both that semantic model and the machinery required to compile it into usable runtime bindings, serialize it, test it, compare consumer contracts, and map it to external representations.

The current model is large because operational reality is large: the current compiled contract contains hundreds of models and controlled vocabularies spanning objects, state, communications, work, organizations, resources, media, spatial information, representations, robotics, aviation, ISR, and related domains. The goal is not to keep the vocabulary artificially tiny. The goal is to keep it **semantically coherent, reusable, and deep enough that integrations do not need to smuggle protocol-specific meaning through generic escape hatches**.

---

## The problem OCCID is trying to solve

Interoperability is not merely converting field names.

Two systems may both contain a number called `altitude`, a string called `mode`, an identifier called `uid`, or a value called `rssi`, while meaning completely different things.

A position may describe:

- the current location of a vehicle;
- the estimated location of an observed object;
- a waypoint inside a plan;
- the target of a task;
- an annotation anchor;
- a named physical place;
- a geographic region or boundary;
- the origin of an observation.

A timestamp may mean wall-clock time, boot-relative time, source observation time, receive time, or validity time.

An identifier may mean global object identity, a short class-local operational ID, a protocol address, a MAVLink system/component pair, a CoT UID, a database record key, or a transient correlation token.

A state update may describe the changing condition of a thing, while another record describes the stable identity and definition of that thing. A symbol shown on a map may be a **representation** of an entity rather than part of the entity itself.

OCCID therefore starts with meaning.

```text
external representation
        |
        v
semantic interpretation
        |
        v
      OCCID
        |
        v
semantic interpretation
        |
        v
external representation
```

The core objective is:

> **Different systems should be able to talk about the same operational reality without first becoming the same system.**

---

## What OCCID is, structurally

The authored model has three semantic building blocks:

```text
Concept          a semantic category in the ontology
Representation   an explicit data-bearing shape
Vocabulary       a closed set of controlled values
```

A **Concept** says what kind of thing something is in the semantic model.

A **Representation** gives concrete structure to information: records, values, measurements, messages, states, graphics, media, locations, identifiers, and other data-bearing forms.

A **Vocabulary** is a controlled enum or flag set used where a bounded set of meanings is appropriate.

There is no separate authored `Type` level. There is no second ontology file that can drift away from the schemas. The single `parent` relation is the semantic **is-a** relation and field-inheritance relation. The compiler derives child relationships from it.

For example, the current high-level semantic tree begins approximately like this:

```text
Root
├── Communication
│   ├── Link
│   ├── Message
│   ├── Network
│   ├── Node
│   ├── Protocol
│   └── Interface
│
├── Definition
│   ├── Frame
│   ├── SemanticType
│   ├── ResourceTemplate
│   └── OrgTemplate
│
├── Struct
│   ├── ID
│   ├── Text
│   ├── Vector
│   ├── Measurement
│   └── Uncertainty
│
├── Control
│   ├── Objective
│   ├── Directive
│   │   ├── Task
│   │   └── Command
│   ├── Plan
│   ├── Constraint
│   ├── Authority
│   └── Assignment
│
├── Data
│   ├── Condition
│   ├── Event
│   ├── Execution
│   ├── Observation
│   ├── Representation
│   ├── State
│   ├── Context
│   └── Property
│
└── Object
    ├── Entity
    ├── Set
    ├── Item
    └── Location
```

That tree is semantic. The generated Python runtime deliberately does **not** require a corresponding Python inheritance tree. Generated classes are flat runtime records and semantic ancestry is carried by OCCID metadata. This avoids using Python inheritance as the ontology itself.

---

## The major semantic areas

### Objects

`Object` is the broad branch for things that exist as operational subjects.

Current major forms include:

- `Entity` — a discrete actor or machine capable of action;
- `Actor`, `Agent`, and `Person`;
- `Machine`, `Vehicle`, `Platform`, ground and air machine specializations;
- `Set` — collections of objects;
- `Organization`, `Group`, `Unit`, `Side`, `Coalition`, and informal collections;
- `Item` — bounded non-agent objects such as equipment, components, and payloads;
- `Location` — identified physical-world places, marks, paths, regions, and boundaries.

The purpose of the object tree is not to classify every noun in existence. It provides stable semantic anchors for objects that operational software needs to identify, reference, relate, assign, observe, display, or update.

### Identity

OCCID distinguishes several kinds of identity instead of pretending every `id` is interchangeable.

A `UID` is a globally self-contained OCCID identity value. Current UID representation is fixed binary data.

`IntID(Namespace)` represents a compact integer identity explicitly scoped to a semantic namespace. The namespace is part of the **schema**, not guessed from the field name or containing class. Therefore:

```text
Entity 38
Track 38
Task 38
```

are three unrelated class-local integer IDs even though the integer happens to be the same.

Durable cross-object references generally use UIDs. Short integer IDs exist where systems need compact, stable human/operational handles.

Protocol identity is not automatically OCCID identity. MAVLink sysid/compid, CoT UIDs, packet IDs, transport addresses, database keys, callsigns, names, and correlation tokens are not silently promoted into OCCID identity merely because some external system uses them as identifiers.

`Record` metadata is also separate from logical-object identity. A persisted record has its own record UID, record-local integer ID, revision, creation/update timestamps, origin, and provenance. That record metadata describes the stored record; it is not a replacement for the UID of the Entity, Task, Track, Plan, Organization, or other logical object represented by the record.

### Definition versus state

A recurring OCCID rule is:

> **Stable definition and changing condition are not the same thing.**

An Entity is not rewritten every time its location changes. Its changing condition belongs in state such as `EntityState`.

An Organization has durable identity and definition; its changing membership, roster, readiness, and operational condition belong in organization state.

A communication `Link` describes communication capability or connection kind. Mutable condition, signal quality, counters, and delivery condition belong in `LinkState`.

A `Condition` describes predicate logic. Whether that condition currently evaluates true or false is mutable validation state.

The same pattern occurs throughout the ontology because mixing definition and state makes history, synchronization, reasoning, persistence, and interoperability much harder.

### State

`State` is the branch for changing operational condition.

It currently includes forms for:

- subject and entity state;
- position and kinematics;
- guidance, navigation, and control state;
- health, damage, faults, readiness, and activation;
- sensor state;
- operator/receiver input state;
- internal machine diagnostics;
- resources such as fuel, power, inventory, supplies, and electrical condition;
- communication link state;
- condition-validation state;
- spatial cueing.

State records can be time-indexed observations of a subject. They are not generic revision snapshots of every field on the subject.

### Spatial information

OCCID contains reusable spatial structures and persistent spatial objects.

Current structures cover:

- global positions;
- local vectors and directions;
- Euler angles and angular velocity;
- velocity vectors;
- altitude datums and altitude state;
- paths, areas, circles, multi-geometries, bounding boxes, and uncertainty;
- position state and location state;
- named/persisted `Mark`, `Path`, `Region`, and `Boundary` objects.

A route point embedded in a plan is not automatically a persistent named Location. Conversely, a named operational place that must be independently referenced can be a Location with its own identity.

OCCID distinguishes semantic geometry from graphics used to draw that geometry.

### Representation and graphics

A Representation is an authored or shared depiction, view, presentation, or organization of operational information.

This branch exists specifically so that presentation does not contaminate the represented subject.

Examples include:

- `Graphic` and `GeometryGraphic`;
- `SymbolGraphic` and `MilitarySymbolGraphic`;
- annotation, label, note, callout, and media graphics;
- georeferenced media graphics;
- measurement graphics;
- layers and layer views;
- saved map views;
- map-grid representations such as UTM, MGRS, latitude/longitude, and local grids;
- style values for stroke, fill, text, color, and opacity;
- tactical graphics.

An Entity does not become a military symbol because it is drawn as one. The symbol is a separate Representation referring to the Entity.

A Mark does not own renderer symbology. A Graphic can depict that Mark.

This separation allows different users, systems, or views to represent the same semantic subject differently without mutating the subject itself.

### Observation, ISR, tracks, and assessment

`Observation` represents information about the external world rather than the observer's own state.

Current structures include:

- detections;
- classifications;
- assessments;
- persistent tracks;
- vision boxes and vision detections;
- ISR observations and ISR parameters;
- track updates and ISR results;
- evidence and confidence-related vocabulary.

A `Track` is a maintained correlated identity for an observed object or phenomenon. It is not automatically identical to the real-world Entity it may eventually be associated with.

Observation semantics keep source, evidence, uncertainty, and time basis explicit instead of flattening everything into generic telemetry.

### Media

Media is modeled semantically rather than with one generic `media_type` switch.

The current hierarchy includes:

```text
Media
└── MediaItem
    ├── ImageMedia
    │   └── StillImage
    │       ├── Photograph
    │       └── VideoFrame
    ├── VideoMedia
    │   ├── VideoRecording
    │   └── LiveVideoStream
    ├── AudioMedia
    │   ├── AudioRecording
    │   └── LiveAudioStream
    ├── SpectrumMedia
    │   └── SpectrumRecording
    ├── PointCloudMedia
    ├── DocumentMedia
    └── BinaryMedia
```

Concrete media forms can carry the fields appropriate to that kind of media while remaining members of the broader semantic family.
Media resources carry a controlled `MediaModality`, use typed network addresses,
identify their producing Entity and acquisition sensor when known, and put pixel
dimensions directly on image and video media.

Media itself is also separate from how that media is displayed. A photograph can exist as media, while a `MediaGraphic` or `GeoreferencedMediaGraphic` represents how it is placed in a visual product or map.

### Communication

OCCID models communication as semantic information about endpoints, networks, links, protocols, messages, and interfaces rather than as one assumed transport stack.

The current Communication branch includes:

- `Node` — a deployed compute/communications endpoint participating on behalf of an Entity;
- `Network` and network addresses;
- `Link`, link capacity, data rates, quality, counters, and link state;
- `Protocol` plus protocol/crypto/radio-related profiles;
- `Interface` and concrete interface specializations;
- `Message` plus response, command, observation, telemetry, human-text, delivery, delta, and receipt structures;
- radio and mesh semantics where those are protocol-independent enough to belong in the shared model.

Transport delivery is not execution success. A message being delivered only means the transport accomplished delivery.

```text
transport delivery
    != semantic executor acceptance
    != execution progress
    != execution completion
```

OCCID has separate structures for those facts.

### Control, intent, tasking, and execution

The Control branch separates **desired outcomes**, **directed work**, **authority**, **assignment**, **planning**, and **runtime execution**.

The core shape is approximately:

```text
Control
├── Objective
├── Directive
│   ├── Task
│   │   ├── TaskManeuver
│   │   ├── TaskEffect
│   │   ├── TaskInformation
│   │   └── TaskTransport
│   └── Command
│       ├── StateChangeCommand
│       ├── ProcessControlCommand
│       ├── ConfigurationCommand
│       ├── MotionCommand
│       ├── ResourceCommand
│       └── ExecutionCommand
├── Plan
│   ├── OperationalPlan
│   ├── RoutePlan
│   └── AirPlan / flight-plan representations
├── Constraint
├── Authority
└── Assignment
```

The central distinction is:

> **Task preserves intent. Command prescribes an immediate bounded operation.**

A Task describes work that must be accomplished. A Command describes an immediate operation to perform on a concrete target.

Individual verbs such as movement, observation, protection, transport, or effect are generally controlled vocabulary rather than a new ontology class for every verb.

Task does not contain its assignee as an intrinsic property. `Assignment` binds directed work or another subject to an assignee under the relevant authority and constraints. Reassignment therefore does not mutate the Task itself.

`Execution` describes one runtime execution attempt. One assignment may produce multiple attempts. Acceptance, progress, status, delivery, and final outcome remain distinguishable evidence.

### Plans and aviation

Plans describe proposed or approved methods for accomplishing work rather than becoming giant application-specific mission documents.

Current planning structures include operational plans, routed plans, autopilot missions, air plans, group and unit flight plans, mission route geometry, flight mission points, loiter/orbit data, flight-level bands, and related planning representations.

Aerial semantics include useful flight-plan phases, roles, formations, route categories, and other representations while avoiding the assumption that one flight-control API defines the ontology.

### Organizations, ORBAT, and sides

OCCID distinguishes:

- a reusable organization **template**;
- a concrete `Organization` with its own identity;
- mutable `OrganizationState`;
- doctrinal/compositional structures;
- operational side or coalition membership;
- military organization and order-of-battle specializations where the semantics genuinely require them.

This prevents one static organization record from becoming a dumping ground for doctrine, current membership, readiness, display affiliation, resources, and runtime state.

Organization size/echelon, category, strength, readiness, reinforcement condition, role, and similar concerns are represented at the appropriate semantic level rather than being inferred from a display symbol.

### Resources, supplies, power, and payloads

Resources are things that can be held, required, allocated, consumed, authorized, assigned, or reported.

OCCID separates reusable resource definitions/templates from actual runtime holdings and state.

Current structures include:

- resource templates and requirements;
- personnel, equipment, supply, and military supply templates;
- resource holdings and inventory state;
- supplies and fuel;
- power sources and power state;
- electrical state with typed electrical quantities;
- payloads, payload allocation/planning/mounts;
- sensor payloads, image/RF sensors, fields of view, measurement quality, data formats, and capability vocabularies.

The APEX Payload work was used as an interoperability stress test for this part of OCCID. APEX protocol/session structure does not become OCCID merely because OCCID can map to it; useful protocol-independent distinctions discovered through that work can become shared semantic primitives.

### Robotics, UAVs, and interfaces

OCCID contains robotics and UAV-oriented representations because those systems are major real consumers, not because OCCID is a drone-specific ontology.

Current structures include robot/controller configuration, receiver and channel mapping, remote-control interfaces, media-production capabilities, identified image sensors, imaging-sensor state, flight-control state, video configuration, autopilot and RC vocabularies, and UAV-related telemetry/message forms.

Endpoint-specific calls such as `arm()`, `goto_location()`, or `start_offboard()` do not automatically become ontology classes. They are adapter/runtime operations that may map to more general OCCID intent or command semantics.

### Context

OCCID includes semantic operational context without forcing every object participating in an operation or scenario into one monolithic aggregate document.

`OperationalContext`, `Operation`, and `Scenario` can identify a bounded context, reality, temporal extent, and membership while referenced objects retain their own identities and records.

### Military semantics

OCCID is not defined as a military-only model, but military C2, ISR, symbology, organization, supply, aviation, effects, and tasking provide demanding interoperability requirements.

Generic operational semantics are kept in core even when a common standard originated in military practice. The current source layout intentionally moved broadly useful organization/OOB, SIDC/symbology, standard identity/affiliation, tactical graphics, NATO supply classification, radio conventions, and non-combat aviation semantics into their appropriate core packages.

The remaining `modules/military/` area is for genuinely effects/combat-specific semantics such as weapons, munitions, fires, targeting/attack, and directly effects-bearing specializations.

Standard-specific vocabularies remain named honestly when the meaning really is standard-specific. Moving them into core does not pretend that NATO terminology is universal; it means the underlying concept is broadly part of the shared operational model and can explicitly carry the standard vocabulary that defines it.

---

## Semantic normalization: the most important development rule

> **No protocol-native scalar enters OCCID merely because a protocol exposes it.**

OCCID represents facts and concepts about the operational world. It does not preserve packet layouts, message fields, numeric status codes, masks, endpoint names, convenience aggregates, or transport-local IDs unless those values carry a protocol-independent semantic meaning that belongs in the shared model.

A protocol adapter should therefore have an asymmetric boundary:

```text
external protocol
    |
    v
protocol-shaped parser / snapshot
    |
    v
semantic interpretation
    |
    v
OCCID
```

The parser or adapter-local snapshot **may and often should remain protocol-shaped**. MAVLink `custom_mode`, CoT attributes, MSP message fields, ROS structures, proprietary status masks, packet IDs, protocol component addresses, and similar information can remain there when needed to decode the source.

The normalization boundary is where protocol vocabulary stops and shared semantics begin.

For each source datum:

1. **If OCCID already expresses the meaning**, map it into the existing semantic model, vocabulary, measurement, state, identity, relationship, or representation.
2. **If OCCID does not express it, but the concept is protocol-independent and operationally useful**, investigate whether OCCID is too shallow and should be refined.
3. **If the value exists only for decoding, routing, interoperability bookkeeping, diagnostics, or source-specific debugging**, keep it at the boundary.
4. **If the meaning is not known strongly enough**, do not publish a false semantic claim merely to avoid losing the field.

This applies especially to measurements and state.

A field called `rssi` is not automatically dBm. A speed is not automatically airspeed. Heading is not automatically course over ground. A source timestamp is not automatically wall-clock time. A numeric mode code is not automatically a universal flight mode.

The adapter must understand units, reference frame, scale, time basis, optional/sentinel meaning, identity scope, and source semantics before making an OCCID claim.

### Do not create escape hatches

Two shortcuts repeatedly produce bad ontology:

- copying unknown information into `native_*`, arbitrary metadata, generic telemetry bags, or generic protocol fields because modeling it is inconvenient;
- discarding meaningful protocol-independent information because OCCID does not yet have a clean place for it.

The first pollutes the shared model with source vocabulary. The second hides missing semantic depth.

The correct question is:

> **What does this datum actually mean, independent of the source encoding?**

Then ask whether that meaning is already expressible, can be composed from existing primitives, requires a new controlled vocabulary, or exposes a genuinely missing semantic concept.

### Historical warning: the HiveLink lineage

This rule comes from actual project history rather than abstract ontology preference.

Early HiveLink, before OCCID matured, combined transport with an informal data protocol. Payloads carried flat fields such as flight-mode strings, airspeed, groundspeed, heading, altitude, RSSI, SNR, latency, and endpoint-shaped commands. Early MAVLink integrations naturally copied MAVLink-derived values directly into those transport structures.

Some of that lineage survived into later OCCID work as generic telemetry bags and `native_*` state fields. Once real adapters expanded, those escape hatches encouraged more source-shaped data to enter the ontology.

The resulting correction removed generic `TelemetryState`, removed native flight-mode/system-state fields, separated static `Link` definition from mutable `LinkState`, removed protocol battery IDs and ambiguous RSSI fields, and added real semantic primitives such as typed airspeed and protocol-neutral communication quality/counter models.

The durable lesson is:

> **An existing protocol-shaped OCCID field is not precedent for adding another one. It may be historical residue that should be corrected.**

---

## Interoperability is also ontology discovery

OCCID is intended to be minimal in duplication, not shallow in meaning.

External protocols, APIs, standards, databases, sensors, and operating systems are useful stress tests. When a real integration does not fit cleanly, that can reveal a missing semantic distinction.

A useful investigation order is:

1. determine what the source datum actually means;
2. state that meaning without relying on the source field name or numeric encoding;
3. identify its units, reference frame, clock, identity scope, uncertainty, validity, and lifecycle;
4. try to represent it using existing OCCID concepts, representations, state, relations, measurements, definitions, and vocabulary;
5. if the meaning is protocol-independent and still cannot be expressed cleanly, investigate a missing primitive or decomposition;
6. only then decide that the value is truly protocol-local bookkeeping and should remain outside OCCID.

A mapping failure is evidence. It is neither automatic proof that the foreign datum belongs in core nor automatic proof that OCCID should ignore it.

---

## Interoperability helpers

The [`interop/`](interop/) package contains deterministic mappings between external representations and OCCID semantics.

Current helpers include CoT, MAVSDK/MAVLink-related, and MSP-oriented mappings.

The interop layer may perform deterministic conversion of:

- fields;
- units and scaling;
- enums;
- coordinate/reference frames;
- altitude references;
- sentinel values;
- protocol representations.

The same semantic input should produce the same representation output without hidden network state or application policy.

Interop does **not** own:

- endpoint connections;
- retries;
- transport routing;
- session lifecycle;
- autonomy;
- planning policy;
- operation selection;
- recovery behavior;
- C2 workflow.

Those are responsibilities of runtimes and applications around OCCID.

---

## Schema authority and source of truth

The authoritative authored schema lives under:

```text
lib/schema/
```

Those YAML schema files are the semantic source of truth.

The rest of the runtime artifacts are generated:

```text
lib/schema/**/*.schema.yaml
        |
        v
compile_occid.py
        |
        v
occid.yaml
        |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
generate_pydantic.py   generate_typescript.py   contract metadata
        |                      |                      |
        v                      v                      v
schema/*.py          typescript/occid.ts       OCCID contract data
```

Normal regeneration uses the single entry point:

```bash
python generate.py
```

Do not hand-maintain generated Python or generated TypeScript as a second semantic authority.

[`idl_spec.md`](idl_spec.md) is the normative schema-language reference. [`docs/development.md`](docs/development.md) describes the current compiler/runtime mechanics and development invariants in more detail.

### Parent graph and runtime generation

`parent` is the sole authored semantic ancestry edge.

If a model says:

```yaml
parent: Entity
```

it means the model **is a kind of Entity** and inherits Entity fields at the schema level.

The compiler resolves effective fields into the compiled contract, preserves semantic ancestry metadata, and derives direct child lists.

Generated Python record classes remain flat rather than using Python class inheritance as ontology. Semantic compatibility is resolved from OCCID's parent registry. A field typed as a semantic parent can therefore accept a compatible concrete child because OCCID knows the child is-a parent, not because Python happened to inherit one generated class from another.

This distinction matters for generated runtimes, structural hashes, and future language bindings.

---

## Python runtime

Install the repository in editable mode with:

```bash
python -m pip install -e .
```

Consumers import models from the canonical `occid` namespace:

```python
from occid import Entity, EntityState, Photograph, Task, UID
```

Generated Python modules physically live under `schema/`, but consumers should not treat that directory as a separate model authority.

The Python runtime currently uses generated Pydantic-based models for strongly typed object creation and validation, plus OCCID runtime metadata for semantic ancestry.

---

## TypeScript runtime

TypeScript is a sibling binding of the same compiled OCCID contract.

It is **not** a separate frontend schema and it is not the purpose of this repository.

`generate_typescript.py` reads the same compiled `occid.yaml` and emits:

```text
typescript/occid.ts
```

The generated TypeScript runtime includes model creation, named-data conversion, runtime semantic ancestry checks, enum/vocabulary definitions, and compact-wire structure helpers.

Example:

```ts
const point = createModel("GlobalPosition", {
  lat: 45.0,
  lon: -73.0,
  alt: 100,
  alt_frame: AltitudeDatum.SEA_LEVEL,
});

point.lat;
point.$model; // "GlobalPosition"
```

Semantic relationships come from OCCID's generated parent graph rather than handwritten frontend unions:

```ts
isA(point, "GeoPos");
childrenOf("Task");
```

The TypeScript binding exists so a browser or TypeScript service can consume the same model rather than inventing a parallel one.

---

## Named data: explicit self-describing interchange

`occid.named` provides the human/API/persistence-oriented named codec.

It preserves concrete model names and symbolic enum names rather than replacing everything with compact numeric wire IDs.

Use:

```python
from occid.named import to_data, from_data, dumps, loads
```

for JSON-compatible Python data or JSON text.

The named representation preserves important distinctions such as:

- concrete nested model names;
- symbolic enum names;
- binary UID values in a stable textual form;
- omitted fields versus explicit null where the runtime supports that distinction;
- unusual bytes, integers, tuples, and map-key forms through tagged representations when plain JSON would lose information.

Named data is appropriate where self-description and inspectability matter: APIs, diagnostics, application boundaries, persistent documents, test fixtures, and similar uses.

Application persistence policy remains the application's responsibility. OCCID supplies a lossless named semantic representation; it does not dictate a database engine or collection layout.

---

## Compact transient wire

OCCID also has a compact structural encoding for transports where names are unnecessary overhead because both peers already share the same structural contract.

The current record-shaped envelope is conceptually:

```text
[
  model_id,
  {
    field_ordinal: value,
    ...
  }
]
```

Nested records use the same model-ID/field-map structure. Enums and flags use numeric values. Exact atomic representations can use their underlying compact values directly. UID values, for example, can be encoded as raw fixed-size binary where the schema says the field is a UID.

This encoding is intentionally **contract-local**.

Model IDs are generated from the current compiled contract. They are implementation discriminators for peers sharing that contract, not permanent semantic identities for the represented things and not an ontology-discovery mechanism.

The transient envelope does not carry a giant schema declaration or global version on every message. Contract compatibility is handled separately.

Compact transient encoding is also not a promise that arbitrary old wire payloads should be used as durable storage forever. Durable persistence and migration policies belong at explicit application boundaries.

---

## Structural consumer contracts

OCCID changes frequently during active development. A consumer should not need a full rewrite simply because **some unrelated part of OCCID expanded**.

Direct consumers can maintain a generated:

```text
OCCID_CONTRACT
```

using:

```bash
python -m occid.contract generate .
python -m occid.contract check .
```

The generated receipt contains:

- a global structural fingerprint for the complete compiled OCCID contract;
- recursive structural fingerprints for the OCCID symbols that consumer actually uses.

The global hash answers:

> Did anything in OCCID change?

It does **not** answer:

> Is this consumer incompatible?

If an unrelated model changes while every model a consumer actually uses remains structurally unchanged, that consumer can remain compatible.

If a consumed model changes or disappears, the contract checker identifies the affected symbol.

This makes compatibility consumer-specific rather than treating OCCID as one monolithic version bomb.

Release `VERSION` is provenance. It is not a substitute for consumer-specific structural compatibility checking.

---

## Executable field manual

[`example_usage.py`](example_usage.py) is intentionally more than a tiny syntax example.

It is the executable answer to:

> **How is OCCID supposed to work end to end?**

The current walkthrough covers a small but coherent operational scenario involving:

- identity provisioning;
- organizations and organization state;
- relationships;
- nodes and communications;
- external protocol identity versus OCCID identity;
- authority and control leases;
- objectives, tasks, assignments, plans, and execution;
- MAVLink-derived vehicle telemetry mapped into OCCID state;
- CoT-derived observations;
- tracking;
- messages and delivery evidence;
- compact OCCID wire representation.

Run it with:

```bash
python example_usage.py
```

The protocol parsers in the field manual are deliberately small teaching boundaries, not full protocol implementations.

---

## Deep Ontology

OCCID grew out of a larger interoperability problem.

Trying to merge large operational vocabularies directly tends to produce duplicated concepts, mixed abstraction levels, giant enumerations, protocol-shaped object trees, and taxonomies that grow faster than their semantic clarity.

The **Deep Ontology** research direction asks how much of those vocabularies can instead be explained by smaller reusable semantic structures, composition, relationships, controlled vocabularies, and legality constraints.

OCCID is the practical engineering side of that work.

The research does not need to be "finished" before OCCID is useful. In fact, concrete integrations are one of the main ways the model is tested. A real mapping that fails cleanly can expose a missing semantic distinction. A representation that collapses too many meanings can expose a bad abstraction. A consumer that must duplicate large pieces of OCCID can expose a bad authority boundary.

The objective is not a frozen universal ontology declared correct in advance. It is a model that becomes more coherent through contact with real systems while avoiding needless protocol contamination.

---

## Development principles

The project history has repeatedly converged on a few rules that should survive individual refactors.

### 1. One semantic authority

`lib/schema/` is authoritative.

Generated Python, generated TypeScript, compiled YAML, contract markers, OpenAPI projections, consumer caches, and application-specific schemas must not become competing writable definitions of OCCID semantics.

### 2. Translate meaning, not source field names

A convenient endpoint field or API method name does not automatically deserve an OCCID model.

### 3. Keep definition, state, representation, and protocol encoding separate

These are related concerns, not interchangeable data shapes.

### 4. Identity must say what kind of identity it is

UIDs, namespaced integer IDs, record IDs, protocol addresses, source IDs, correlation tokens, and human names are not aliases.

### 5. Task is intent; Command is immediate operation

Do not rebuild endpoint APIs as ontology classes.

### 6. Delivery is not execution

Transport delivery, semantic acceptance, progress, and completion remain distinct evidence.

### 7. Avoid generic semantic escape hatches

`native_*`, arbitrary telemetry bags, untyped metadata, or catch-all status dictionaries usually hide missing modeling work.

### 8. Minimal does not mean shallow

Do not add a concept merely because a protocol has a field. But do not discard a real protocol-independent distinction merely to keep the model numerically small.

### 9. Consumers do not become second semantic authorities

If a consumer must manually duplicate OCCID vocabularies, descendant lists, or semantic facts, first ask whether that information should be generated from OCCID instead.

### 10. Compatibility should follow actual dependencies

An unrelated OCCID expansion should not force every consumer to rewrite itself. Structural consumer contracts exist to identify the real blast radius.

---

## Repository layout

```text
lib/schema/                 authoritative authored OCCID schemas
  core/                     general semantic model
  modules/military/         genuinely combat/effects-specific extensions

compile_occid.py            compile authored schemas into occid.yaml
generate.py                 regenerate compiled contract and bindings
generate_pydantic.py        generate Python runtime models
generate_typescript.py      generate TypeScript runtime binding

occid.yaml                  compiled OCCID contract
ontology.yaml               generated readable semantic hierarchy
occid-contract.json         generated structural contract metadata

occid/                      canonical Python package/runtime tooling
schema/                     generated Python models
typescript/                 generated TypeScript binding and parity fixtures
interop/                    deterministic external representation mappings

tests/                      compiler, runtime, identity, contract, codec,
                            interoperability, and semantic regression tests

example_usage.py            executable end-to-end OCCID field manual
idl_spec.md                 normative IDL/schema-language specification
docs/development.md         current development mechanics and invariants
DEVLOG.md                   historical development decisions
notes/                      source/reference material and older baselines
```

---

## Typical development workflow

Install editable:

```bash
python -m pip install -e .
```

Edit authoritative schemas under `lib/schema/`.

Regenerate everything:

```bash
python generate.py
```

Run tests:

```bash
python -m pytest
```

Run the executable field manual:

```bash
python example_usage.py
```

A direct consumer that tracks an OCCID contract can regenerate its receipt with:

```bash
python -m occid.contract generate .
```

and verify it with:

```bash
python -m occid.contract check .
```

Generated output should be deterministic. If generated files change, the source schema or generator should explain why.

---

## Current scale and status

OCCID is experimental and under active development.

At the current repository state, the compiled contract contains roughly:

- **419 models**;
- **170 controlled vocabularies**;
- approximately **65 generated semantic packages** across the runtime.

Those numbers are descriptive, not design goals. A model should exist because it represents a real useful semantic distinction, not to make the ontology look comprehensive. Conversely, a real distinction should not be suppressed merely to keep the count small.

The exact class tree, vocabularies, and representation choices will continue to evolve as integrations expose better decompositions.

The stable purpose is:

> **Provide a shared semantic foundation for heterogeneous operational systems.**

The current release identifier is stored in [`VERSION`](VERSION). During active development, compatibility should be assessed from the actual structural contract a consumer depends on, not inferred from the release string alone.

---

## License

OCCID is licensed under the GNU General Public License version 3 only.

See [`LICENSE`](LICENSE).
