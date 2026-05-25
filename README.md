# OCCID

**Open Command, Control and Information Data model**

OCCID is a domain-agnostic data model for C5ISR systems. It defines what can be known, said, commanded, and reported across entities, organizations, platforms, and networks.

It is not a wire protocol. It is not an application schema. It is the semantic layer that protocols and applications build on. A UAV patrol mission and a search-and-rescue coordination use the same structural bones: entities with identities, directives with intent, messages with envelopes, state separate from identity. The domain-specific part is only which variants exist at the leaves.

## Interoperability Targets

OCCID is designed to map cleanly to:

- MAVLink (drone control)
- Cursor on Target / CoT / ATAK
- Anduril Lattice (entity management)
- Constellation Overwatch (ISR)
- STANAG 4586 (unmanned systems interop)
- Meshtastic (mesh transport)
- DDS (pub/sub middleware)
- ROS2 (robotics framework)
and more

OCCID does not replace these protocols. It provides a common information model that translations between them are written against.
