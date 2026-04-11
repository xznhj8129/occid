# Schema Definition
This document is canonical.

Format: as defined in idl_spec.md

## What this is

This schema is a domain-agnostic ontology of directed activity. It describes the fundamental structure of things existing, things being directed, things communicating, and things being known.

It is not a drone protocol, a military C2 format, or an application schema. It is the grammar that any of those would use. A UAV patrol mission and a McDonalds drive-through order use the same structural bones: entities with identities, directives with intent, messages with envelopes and content, state separate from identity. The domain-specific part is only which variants exist at the leaves and what fields they carry.

The roots reflect irreducible concerns:

- **Definition** — how to interpret values: frames, geometry, time, types
- **Struct** — Low level definitions
- **Object** — what exists: entities, organizations, items, sites, systems
- **Control** — what should happen and how it gets done: directives and processes
- **Communication** — how information moves: nodes, transports, messages
- **Data** — High level definitions, what is known: properties, state, events, assessments, sensory signals

Specificity increases downward. The roots and their immediate children are stable and universal. The leaves are where domain-specific vocabulary appears — MAVLink is a Protocol, a patrol route is Data, a camera gimbal is a Payload. Nothing above the leaf layer needs to know or care which domain it serves.

attempts 1: ontology, expand into typology, cram 10000000 things into typology, fail
attempt 2: split typology into class files
attempt 3: all enums moved to lexicon
attempt 4: axis

ontology -> typology * axis -> specialized unique types -> schema primitives -> fielded schema

attempt 5: classes + axis into typology, expand
- not every class needs an axis


## Pipeline

Schema is created in four stages. Stages 1–3 are sequential and gated. The lexicon is a parallel resource, not a gate.

1. **Ontology** — define what fundamentally exists as a position in the class tree. Vague clades. Expressed as the parent/child hierarchy in ontology.yaml. This stage answers: *what is it?* Axis defines, if necessary, their expansion in the next stage.

2. **Typology** — define how ontological classes differentiate. What variants speciate the tree, ~~what facets each class conceptually needs.~~ Typology is strictly structural: it names the branching decisions and the concepts each class carries, nothing more. It does not define enum members, typed fields, or compositional helper shapes. This stage answers: *how does it speciate, and what does it need?*

3. **Lexicon** — collect domain vocabulary and compositional shapes. Enum member lists, value sets, classification systems, and reusable building-block shapes (things like `LocationUncertainty`, `GNSSStatistics`, `SpotCorrection`) that are not themselves ontological classes. The lexicon is a reference library — it captures domain research and external standards without committing to placement in the tree. A concept in the lexicon has no `parent`, no position in the hierarchy. It exists as raw material the schema draws from. This stage answers: *what are the valid values, and what do compositional shapes look like?*

4. **Schema** — commit. Write the actual IDL: typed fields on structs, enums with committed values, variants blocks, and placement of compositional shapes. Facets graduate to typed fields. Lexicon entries graduate to committed enums and helper structs with parents and positions. See idl_spec.md for the IDL format. This stage answers: *what exactly does the struct contain, and where does everything attach?*

A struct may not have typed fields (stage 4) until it has a typology entry (stage 2) whose specializations and required facets are stable.

### Stage boundaries


## Schema Rules

* Each struct defines the shape of a value or state slice, not a fully materialized whole object
* Structs define the smallest necessary attributes and push specifics down to children
* Everything must be representable as JSON
* Every struct that speciates uses a `variants` block; the discriminator enum is implied by the hierarchy
* Structs speciate by domain, in ascending order of specificity, using parent/variants inheritance
* Split schema files by ontological class branch, not by subject domain (see idl_spec.md section 17)
* The source of truth flows down: Ontology → Typology → Schema. The lexicon is a lateral reference, not a link in the chain. Structural changes (new classes, new branches) must originate in the ontology and flow through typology before reaching schema.

## Composition Rules

These rules exist to prevent flattening, reinvention, and anonymous garbage.

* **Ontological classes are families.** Every class in the ontology tree maps to a struct via the IDL parent/variants mechanism. A class with children is a parent struct; each child class is a child struct. The tree expresses what exists and how it speciates — the IDL hierarchy IS the ontology.
* **The `variants` block implies its discriminator enum.** The enum is a product of the parent/variants relationship, not a standalone declaration. Adding a child to a parent adds a member to that parent's discriminator. Do not maintain the enum separately from the hierarchy it describes.
* **The ontology tree stops where enumeration becomes impractical.** The class tree is intentionally finite. It terminates at the depth where further specialization is domain-specific and open-ended. Below that boundary, typology defines the variants and required facets, the lexicon collects the domain vocabulary, and the schema commits the typed fields.
* **Separate the object from its data.** An entity struct defines identity and classification. Its state, properties, and events are separate structs composed by reference, not flattened into the entity.
* **Separate message and medium and messenger.** What is sent, how it travels, and who sends it are different structs.
* **Separate cause and effect.** A directive is not an action. An action is not a result.
* **Separate will and action.** Intent, instruction, objective, and task are distinct concepts.
* **No anonymous tuples.** A position is not `list[int]`. It is a typed struct, variant of a parent, with named fields.
* **No local helper shapes.** Do not invent local structs to hold a few fields. If the concept exists, it has a name in the ontology and a reusable struct. If it doesn't exist, define it properly or don't define it.
* **Reference existing types by name.** If `GlobalPosition` exists, use `GlobalPosition`. Do not write `lat: float, lon: float` inline. Do not create a new struct that duplicates an existing one.
* **Consume reusable typed values.** Facets like position, attitude, power, identity are shared composites. Compose them by reference. Never flatten their fields into a parent struct.

Objects use Transport to send Message that contain Data 