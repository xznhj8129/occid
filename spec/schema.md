# Schema Definition
This document is canonical.

Format: as defined in idl_spec.md

## What this is

This schema is a domain-agnostic ontology of directed activity. It describes the fundamental structure of things existing, things being directed, things communicating, and things being known.

It is not a drone protocol, a military C2 format, or an application schema. It is the grammar that any of those would use. A UAV patrol mission and a McDonalds drive-through order use the same structural bones: entities with identities, directives with intent, messages with envelopes and content, state separate from identity. The domain-specific part is only which variants exist at the leaves and what fields they carry.

The five roots reflect five irreducible concerns:

- **Object** — what exists: entities, organizations, items, sites, systems
- **Reference** — how to interpret values: frames, geometry, time, types
- **Control** — what should happen and how it gets done: directives and processes
- **Communication** — how information moves: nodes, transports, messages
- **Data** — what is known: properties, state, events, assessments, sensory signals

Specificity increases downward. The roots and their immediate children are stable and universal. The leaves are where domain-specific vocabulary appears — MAVLink is a Protocol, a patrol route is a Task, a camera gimbal is a Payload. Nothing above the leaf layer needs to know or care which domain it serves.


## Pipeline

Schema is created in four stages. Stages 1–3 are sequential and gated. The lexicon is a parallel resource, not a gate.

1. **Ontology** — define what fundamentally exists as a position in the class tree. Vague clades. Expressed as the parent/child hierarchy in ontology.md. This stage answers: *what is it?*
2. **Typology** — define how ontological classes differentiate. What variants speciate the tree, what facets each class conceptually needs. Typology is strictly structural: it names the branching decisions and the concepts each class carries, nothing more. It does not define enum members, typed fields, or compositional helper shapes. This stage answers: *how does it speciate, and what does it need?*
3. **Lexicon** — collect domain vocabulary and compositional shapes. Enum member lists, value sets, classification systems, and reusable building-block shapes (things like `LocationUncertainty`, `GNSSStatistics`, `SpotCorrection`) that are not themselves ontological classes. The lexicon is a reference library — it captures domain research and external standards without committing to placement in the tree. A concept in the lexicon has no `parent`, no position in the hierarchy. It exists as raw material the schema draws from. This stage answers: *what are the valid values, and what do compositional shapes look like?*
4. **Schema** — commit. Write the actual IDL: typed fields on structs, enums with committed values, variants blocks, and placement of compositional shapes. Facets graduate to typed fields. Lexicon entries graduate to committed enums and helper structs with parents and positions. See idl_spec.md for the IDL format. This stage answers: *what exactly does the struct contain, and where does everything attach?*

A struct may not have typed fields (stage 4) until it has a typology entry (stage 2) whose specializations and required facets are stable.

### Stage boundaries

These boundaries prevent the pipeline stages from collapsing into each other:

* **Ontology → Typology**: the ontology defines classes; the typology defines how they branch and what they conceptually need. The typology may not introduce new classes that aren't in the ontology. If a new branch is needed, add it to the ontology first.
* **Typology → Lexicon**: the typology names concepts (`fix quality`, `position source`); the lexicon enumerates their possible values (`NoFix, Fix2D, Fix3D, ...`). The typology must not list enum members or define helper struct shapes. If a facet references an enum, the typology says the facet exists — the lexicon says what the enum contains.
* **Lexicon → Schema**: the lexicon collects vocabulary and shapes without placement; the schema commits them. A lexicon enum is a candidate — the schema decides which members to include, what integer values to assign, and which struct the enum is used by. A lexicon shape is a sketch — the schema decides whether it's a standalone struct, a child of a parent, or folded into another struct's fields. Not everything in the lexicon graduates to schema.
* **The lexicon does not gate the schema.** Simple enums and helper structs can go straight from typology facet to schema field without a lexicon entry. The lexicon exists for domain research that needs a staging area — large enums transcribed from standards, value sets collected from multiple sources, compositional shapes whose placement isn't yet decided.


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