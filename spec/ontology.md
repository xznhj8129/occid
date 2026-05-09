
# Classes

**Definition**: Abstract structure used to define how values, space, geometry, time, or relations are interpreted; semantic descriptors.
    - **Frame**: Frames of reference
    - **Coordinate**: Coordinate systems and encodings
    - **Geometry**: Spatial and geometric types
    - **Time**: Temporal reference frames
    - **Type**: Orthogonal typology axes used to speciate objects, control wrappers, and data without changing their structural class
        - **Category**: What kind of thing something is within its structural class (ie, waypoint, route, zone)
        - **Purpose**: Why something exists, is designated, or is intended to be used
        - **Function**: What something does, how it behaves, or what rule semantics it carries (ie, include, exclude, trigger, hold)
        - **Factions**: Appartnance buckets
        - **Domains**: Domains of existence, movement, operations and effects
    - **Relationship**: Nature of relations, ownership, provenance, link

**Struct**: Primitive reusable low-level struct families.
    - **Vector**: Basic numeric vector structs
    - **Measurement**: Scalar value structs with optional uncertainty or metadata
    - **Bearing**: Angular value structs with reference semantics
    - **GeoPos**: Geographic position structs
    - **LocalPos**: Local coordinate position structs
    - **Line**: Two-point linear structs
    - **Path**: Ordered multi-point path structs
    - **Shape**: Area and volume geometry-carrier structs
    - **Bounding**: Bounding region structs
    - **Uncertainty**: Error and covariance structs
    - **Pose**: Position and attitude combination structs
    - **Range**: Interval and bound structs
    - **Transform**: Spatial transform structs
    - **Orbital**: Orbital state or element structs

- **Object**: Atoms
    - **Entity**: One discrete "atom" capable of actions
        - **Actor**: Entity capable of thought, observation, reflexion, logic, reasoning, introspection, and making judgments and decisions
            - **Person**: Human being
            - **Agent**: Artificial intelligence, distinct from it's substrate

        - **Machine**: Discrete non-inert man-made object capable of actions

    - **Set**: An object that represents many objects
        - **Organization**: A structured collection of organized entities and/or subordinate organizations with common command and control

        - **Collection**: Informal, adhoc grouping of objects with common purpose, appartnance, affinity or goal

        - **Cluster**: A set of objects united only by criterion

        - **System**: An organized assembly of multiple objects bound together as a functional whole, but not by itself a discrete actor, organization, collection, or site

    - **Item**: A discrete bounded non-agent object
        - **Record**: Item whose purpose is holding information
        - **Equipment**: A mission-purpose item physically used, carried, held, or worn by a human being
        - **Component**: An item that is part of a machine and has an internal purpose or effect
        - **Payload**: An item that is part of a machine and has an external effect or mission purpose

    - **World**: 
        - **Feature**: Immovable, immutable, clearly recognizable and distinct real-world feature (ie, river, town, hill)
        - **Location**: Spatially bounded physical location (ie, building, town, bridge; not conceptual, ie, waypoint) of interest
        - **Site**: Spatially bounded area or building designated, recognized or assigned a specific function

- **Control**: Scale-invariant; the binding of agents to objectives through structured decomposition
    - **Reasoning**: 
        - **Purpose**: Reason, justification, imperative for action
        - **Intent**: Desired effect and operational meaning that guides execution
        - **Objective**: Specific desired future condition, effect, or end-state

    - **Directive**: What must be achieved, why, and within what bounds

    - **Execution**: How directed activity is structured and carried out

    - **Reference**: Control-side structural wrapper binding spatial definitions and structs into control-usable referents
        - **Mark**: A discrete spatial reference wrapper used by control logic or execution
        - **Path**: An ordered composition wrapper over spatial references
        - **Region**: A bounded spatial reference wrapper over an area or volume
        - **Boundary**: A delimiting spatial reference wrapper over an edge, line, or bound

    - **Constraint**: A boundary, limitation, or rule restricting permissible action
        - **Restriction**: must not do X
        - **Limitation**: only within Y
        - **Condition**: only when Z is true

    - **Interface**: The translation of an action into the terms of the executing layer

- **Communication**: Definition, implementation, metadata and formats of information transfer
    - **Node**: Endpoint that transmits or receives messages

    - **Transport**: The form of information flow
        - **Network**: Graph topology of information flow
        - **Carrier**: What are messages transmitted over
        - **Protocol**: Format and standard of messages

    - **Feed**: Information pipe
        - **Link**: Discontinuous data flow of discrete packets
        - **Stream**: Continuous data flow at a constant rate, usually Sensory

    - **Message**: Discrete typed envelope for feed data
        - **C3**: Communication whose purpose is to direct, command or control
        - **ISR**: Communication about external objects, events, or the environment
        - **Telemetry**: Communication about the sender's own internal state or process
        - **Response**: Communication whose purpose is acknowledgment, acceptance, rejection, result, or completion notice

- **Data**: Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects
    - **Information**: Symbolic, usually structured data that can be directly read
        - **Properties**: A generally fixed characteristic, classification, disposition, or capability that defines an object, but is not merely its momentary condition
            - **Identity**: Fundamental identity, name, ID
            - **Attributes**: Fundamental characteristics, type, form
            - **Parameters**: Current operating configuration or control regime
            - **Relationship**: Nature of relations, ownership, provenance, link

        - **State**: Telemetric, changing data describing the own state or condition of an object at a given time
            - **Kinematic**: Physical orientation, velocity, acceleration, angular rates
            - **Internal**: Diagnostic internals of a machine or system (CPU, memory, cycles, firmware, connectivity)
            - **Position**: Position in space, address or placement
            - **Guidance**: Status and quality of the navigation solution, mode, source, and validity
            - **Sensor**: Onboard sensor readings, readiness, calibration, and availability
            - **Input**: Current operator / receiver input state and control mapping
            - **Resources**: How much of something something has; power, fuel, food, etc
            - **Condition**: Integrity, damage, faults, readiness
            - **Lifecycle**: Current stage in existence or execution
            - **Assignment**: Assignments, tasks, plans, missions, stages

        - **Event**: A discrete occurrence — something that happened at a point in time, whether planned or not
            - **FlightEvent**: Discrete transition in flight state or safety state
            - **MissionEvent**: Discrete transition in mission execution state

        - **Intel**: Effect-side data that something happened or changed external to the sender object
            - **Detection**: Assessment that something exists or occurred
            - **Classification**: Assessment assigning type or identity to an object
            - **Track**: Assessment of the state of an external object over time
            - **Assessment**: Evaluation of effect, damage, outcome, or threat

    - **Sensory**: Unstructured, non-symbolic sensory signal data that has to be interpreted
        - **AV**: Seen or heard; video, images, audio recordings
        - **Spatial**: point clouds, 3D models, scans, etc
        - **Samples**: IQ samples or other analog data
