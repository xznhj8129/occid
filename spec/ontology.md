
### Classes

- **Object**: Any distinct part of the overall framework that can be identified, described, or referenced

    - **Entity**: One discrete "atom" capable of actions

        - **Actor**: Entity capable of thought, observation, reflexion, logic, reasoning, introspection, and making judgments and decisions
            - **Person**: Human being
            - **Agent**: Artificial intelligence, distinct from it's substrate 

        - **Machine**: Discrete non-inert man-made object capable of actions
            - **Vehicle**: Machine capable of movement only through onboard human control
            - **Robot**: Machine capable of movement without human presence
            - **Platform**: Reusable, static machine that carries out actions

    - **Organization**: A structured collection of entities and/or subordinate organizations
        - **Group**: An organization that contains subordinate organizations
        - **Unit**: An organization that contains no subordinate organizations and consists only of entities

    - **Collection**: An identifiable collection of objects united by circumstance, relation, or selection criterion, but not constituting an organization or a functional whole

    - **System**: An organized assembly of multiple objects functioning together as a whole, but not by itself a discrete actor, organization, collection, or site

    - **Site**: A clearly delimited location of interest with a specific purpose or clear characteristic

    - **Item**: A discrete bounded non-agent object
        - **Record**: Item whose purpose is holding information
        - **Equipment**: A mission-purpose item physically used, carried, held, or worn by a human being
        - **Component**: An item that is part of a machine and has an internal purpose or effect
        - **Payload**: An item that is part of a machine and has an external effect or mission purpose

- **Reference**: Abstract structure used to define how values, space, geometry, time, or relations are interpreted. 
    - **Frame**: Frames of reference
    - **Coordinate**: Coordinate systems and encodings
    - **Geometry**: Spatial and geometric primitives
    - **Time**: Temporal reference frames
    - **Type**: Categories, classifications, factions, domains
    - **Structs**: Reusable data shapes built on Reference primitives (vectors, positions, quaternions, paths, bounding boxes). Ontologically part of Reference, not a separate root.

- **Control**: Scale-invariant; the binding of agents to objectives through structured decomposition
    - **Directive**: What must be achieved, why, and within what bounds
        - **Intent**: The commitment to act and the reason for acting
        - **Objective**: A desired future condition, effect, or end-state

        - **Task**: A directive binding an action to an objective; "do X to achieve Y"
        - **Instruction**: A directive prescribing specific action and method
        - **Command**: An immediate imperative requiring execution without interpretation

    - **Execution**: How directed activity is structured and carried out
        - **Plan**: The ordered structure of actions toward an objective
        - **Sequence**: The ordered steps within a method or procedure
        - **Action**: A discrete intentional act that changes state

    - **Constraint**: A boundary, limitation, or rule restricting permissible action
        - **Restriction**: "must not do X"
        - **Limitation**: "only within Y"
        - **Condition**: "only when Z is true"

    - **Interface**: The translation of an action into the terms of the executing layer

- **Communication**: Definition, implementation, metadata and formats of information transfer
    - **Node**: Endpoint that transmits or receives messages

    - **Transport**: The form of information flow
        - **Network**: Graph topology of information flow
        - **Carrier**: What are messages transmitted over
        - **Protocol**: Format and standard of messages

    - **Feed**: 
        - **Link**: Discontinuous data flow of discrete packets
        - **Stream**: Continuous flow of data of indeterminate total size, usually Sensory

    - **Message**: Discrete typed envelope for feed data
        - **Command**: Communication whose purpose is to direct or control
        - **Telemetry**: Communication about the sender's own internal state or process
        - **Observation**: Communication about external objects, events, or the environment
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
            - **Location**: Location, address or placement
            - **Navigation**: Status and quality of the navigation solution, mode, source, and validity
            - **Sensor**: Onboard sensor readings, readiness, calibration, and availability
            - **Input**: Current operator / receiver input state and control mapping
            - **Resources**: How much of something something has; power, fuel, food, etc
            - **Condition**: Integrity, damage, faults, readiness
            - **Lifecycle**: Current stage in existence or execution
            - **Mission**: Assignments, tasks, plans, missions, stages

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
