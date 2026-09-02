# OCCID

**Open Command, Control, Intelligence Data**

OCCID is a shared semantic model for operational systems.

It gives different software, devices, protocols, and organizations a common way to describe the same operational world.

It provides shared meaning for what operational systems can know, observe, communicate, request, command, and report.

A vehicle can use MAVLink. A tactical application can use Cursor-on-Target. Another system can use MSP, a database schema, or its own API.

OCCID lets those systems exchange meaning without making one external vocabulary the center of the whole system.

```text
     external systems and protocols

  CoT / TAK   MAVLink   MSP   APIs   sensors   other data
      \          |       |      |       |          /
       \         |       |      |       |         /
        +--------+-------+------+-------+--------+
                         |
                         v
                       OCCID
                         |
             shared operational meaning
                         |
            +------------+------------+
            |            |            |
            v            v            v
          humans       software      machines
```

## Why

Different operational domains often share the same structural bones.

Things have identity. Their state changes. Intent can be expressed. Information can be observed and exchanged. Relationships connect these facts into an operational picture.

The domain vocabulary can differ while the underlying meaning overlaps.

Interoperability is therefore not only a field-conversion problem.

The same numbers can have different meaning.

A position can describe:

- where a vehicle is;
- where an observation occurred;
- where something should move;
- a route point;
- an area reference.

Different systems can also use very different structures for the same underlying idea.

OCCID therefore treats interoperability as a semantic problem first.

```text
external representation
        |
        v
operational meaning
        |
        v
external representation
```

The goal is simple:

> Different systems should be able to talk about the same operational reality without first becoming the same system.

## How it works

At a system boundary, protocol data is parsed in its native form.

Useful protocol-independent meaning is then mapped into OCCID.

Application logic can work with that semantic model.

When data must leave through another boundary, the relevant OCCID meaning can be mapped into the destination representation.

```text
foreign data
    |
    v
parser / adapter
    |
    v
semantic mapping
    |
    v
  OCCID
    |
    +-----------> application logic
    |
    v
semantic mapping
    |
    v
another external representation
```

OCCID is under active development. The exact model will continue to change as real integrations expose better abstractions.

## Example

[`example_usage.py`](example_usage.py) shows the basic idea with actual protocol-shaped input.

It starts with:

- a hardcoded Cursor-on-Target XML event;
- a hardcoded MAVLink v2 `GLOBAL_POSITION_INT` frame.

The example parsers decode both inputs.

The CoT contact becomes an OCCID observation.

The MAVLink telemetry becomes OCCID state for a vehicle.

The example then uses those records in a small control flow and maps an OCCID movement operation toward a MAVSDK `goto_location` call.

```text
CoT XML
   |
   v
contact observation ----+
                        |
                        +----> OCCID operational model
                        |
MAVLink telemetry ------+
   |
   v
vehicle state

        |
        v

intent / work / responsibility / execution

        |
        v

vehicle operation
```

Run it with:

```bash
python example_usage.py
```

The parsers in the example are intentionally small. They demonstrate the boundary. They are not complete CoT or MAVLink implementations.

## What OCCID models

OCCID currently contains structures for operational concepts such as:

- identity and objects;
- changing state;
- position and motion;
- observations and information;
- intent and directed work;
- authority and responsibility;
- execution and status;
- relationships between operational records.

These structures are not assumed to be the final decomposition.

They are the current engineering model.

The stable goal is the shared semantic layer.

## Deep Ontology

OCCID grew from a larger interoperability problem.

Attempts to merge operational vocabularies directly produced duplicated concepts, mixed abstraction levels, and expanding taxonomies.

That led to the **Deep Ontology** research direction: investigate how much of those vocabularies can be explained by smaller reusable semantic structures and legality rules.

OCCID is the practical engineering side of that work.

The deeper research does not need to be complete before OCCID can be useful. Real OCCID integrations also provide evidence about which abstractions work and which do not.

## Current implementation

This repository currently includes:

- authored Concept / Representation schemas and Vocabulary;
- record-shaped and atomic Representations (`fields:` or model-level `type:`);
- a compiler that resolves them into flat `occid.yaml`;
- generated Python models produced only from `occid.yaml`;
- compact serialization and validation;
- interoperability helpers;
- structural consumer-contract tooling;
- examples and tests.

The current package version is stored in [`VERSION`](VERSION).

Install the package locally with:

```bash
python -m pip install -e .
```

Import models from the canonical package namespace:

```python
from occid import EntityState, IsrObservation, TaskInformation
```

## Repository structure

```text
lib/schema/             authoritative authored semantic schemas
compile_occid.py         compile Concept/Representation/Vocabulary to flat runtime schema
occid.yaml               generated flat runtime schema
generate_pydantic.py     generate record and atomic Python projections from occid.yaml
schema/                  generated Python runtime models
occid/                  canonical Python package namespace and tooling
interop/                interoperability mappings
tests/                  tests and regression coverage
example_usage.py        end-to-end interoperability example
idl_spec.md             schema language reference
docs/                   developer and implementation documentation
```

For schema generation, serialization, model IDs, consumer contracts, and current adapter rules, see [`docs/development.md`](docs/development.md).

## Status

OCCID is experimental and under active development.

Its purpose is stable:

> provide a shared semantic foundation for heterogeneous operational systems.

The exact structures used to achieve that purpose can evolve as the project is tested against more systems.

## License

OCCID is licensed under the GNU General Public License version 3 only.

See [`LICENSE`](LICENSE).
