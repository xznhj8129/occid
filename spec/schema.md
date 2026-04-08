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

Schema is created in three stages. No stage may be skipped.

1. **Ontology** — define what fundamentally exists as a position in the class tree. Vague clades. Expressed as the parent/child hierarchy in ontology.md.
2. **Typology** — specialize. Define how classes differentiate: what enums form the vocabulary, what variants speciate the tree, what facets each struct conceptually needs. Typology never defines typed fields. See typology.md.
3. **Schema** — define. Write the actual IDL: typed fields on structs, enums with values, variants blocks. A struct's facets graduate to typed fields here. See idl_spec.md for the IDL format.

A struct may not have typed fields (stage 3) until it has a typology entry (stage 2) whose specializations and required facets are stable.


## Schema Rules

* Each struct defines the shape of a value or state slice, not a fully materialized whole object
* Structs define the smallest necessary attributes and push specifics down to children
* Everything must be representable as JSON
* Every struct that speciates uses a `variants` block; the discriminator enum is implied by the hierarchy
* Structs speciate by domain, in ascending order of specificity, using parent/variants inheritance
* Split schema files by general ontological subject
* The source of truth is the Ontology, then the Typology, them the actual defined structs. Changes only flow down.

## Composition Rules

These rules exist to prevent flattening, reinvention, and anonymous garbage.

* **Ontological classes are families.** Every class in the ontology tree maps to a struct via the IDL parent/variants mechanism. A class with children is a parent struct; each child class is a child struct. The tree expresses what exists and how it speciates — the IDL hierarchy IS the ontology.
* **The `variants` block implies its discriminator enum.** The enum is a product of the parent/variants relationship, not a standalone declaration. Adding a child to a parent adds a member to that parent's discriminator. Do not maintain the enum separately from the hierarchy it describes.
* **The ontology tree stops where enumeration becomes impractical.** The class tree is intentionally finite. It terminates at the depth where further specialization is domain-specific and open-ended. Below that boundary, typology defines the variants and their required facets before typed fields are authored.
* **Separate the object from its data.** An entity struct defines identity and classification. Its state, properties, and events are separate structs composed by reference, not flattened into the entity.
* **Separate message and medium and messenger.** What is sent, how it travels, and who sends it are different structs.
* **Separate cause and effect.** A directive is not an action. An action is not a result.
* **Separate will and action.** Intent, instruction, objective, and task are distinct concepts.
* **No anonymous tuples.** A position is not `list[int]`. It is a typed struct, variant of a parent, with named fields.
* **No local helper shapes.** Do not invent local structs to hold a few fields. If the concept exists, it has a name in the ontology and a reusable struct. If it doesn't exist, define it properly or don't define it.
* **Reference existing types by name.** If `GlobalPosition` exists, use `GlobalPosition`. Do not write `lat: float, lon: float` inline. Do not create a new struct that duplicates an existing one.
* **Consume reusable typed values.** Facets like position, attitude, power, identity are shared composites. Compose them by reference. Never flatten their fields into a parent struct.

Objects use Transport to send Message that contain Data 