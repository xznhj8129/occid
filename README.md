# OCCID

**Open Command, Control and Information Data model**

OCCID is a domain-agnostic data model for C3ISR systems. It defines what can be known, said, commanded, and reported across entities, organizations, platforms, and networks.

It is not a wire protocol. It is not an application schema. It is the semantic layer that protocols and applications build on. A UAV patrol mission and a search-and-rescue coordination use the same structural bones: entities with identities, directives with intent, messages with envelopes, state separate from identity. The domain-specific part is only which variants exist at the leaves.

## Five Roots

| Root | What it covers |
|------|---------------|
| **Object** | What exists: entities, organizations, collections, systems, sites, items |
| **Reference** | How to interpret values: frames, coordinates, geometry, time, types, units |
| **Control** | What should happen and how: directives, constraints, tasks, plans, methods |
| **Communication** | How information moves: nodes, transports, feeds, messages |
| **Data** | What is known: properties, state, events, intelligence, sensory |

## Pipeline

The model is built in three stages. No stage is skipped.

1. **Ontology** (`ontology.md`) — the class tree. What fundamentally exists and how it relates.
2. **Typology** (`typology.md`) — how classes speciate. Enums, variants, facets. No typed fields.
3. **Schema** (`idl_spec.md` for format) — the actual IDL. Typed fields, concrete structs, wire-ready definitions.

Each stage consumes the one above. Changes only flow down.

## Interoperability Targets

OCCID is designed to map cleanly to:

- MAVLink (drone control)
- Cursor on Target / CoT (tactical SA)
- Anduril Lattice (entity management)
- Constellation Overwatch (ISR)
- STANAG 4586 (unmanned systems interop)
- Link 16 / VMF (tactical data links)
- Meshtastic (mesh transport)
- DDS (pub/sub middleware)
- ROS2 (robotics framework)

OCCID does not replace these protocols. It provides a common information model that translations between them are written against.

## Consumers

- **Sigma** — C2 planning and decision engine
- **HiveOS** — autonomous vehicle runtime
- **HiveLink** — mesh transport layer

These systems implement OCCID. They do not own it.
