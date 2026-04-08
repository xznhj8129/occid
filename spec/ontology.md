
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

- **Control**:
    - **Directive**: Intentions, directives, desired objective, requested outcome, or prescribed behavior
        - **Intent**: A self-held commitment or plan to act, "X must be done"
        - **Instruction**: A directive instructing specific action
        - **Objective**: A desired future condition, effect, or end-state
        - **Task**: An intent-based instruction with intent through actions to an objective
        - **Constraint**: A boundary, limitation, or rule that restricts permissible action

    - **Process**: Cause-side, intentional or directed activity over time
        - **Plan**: What actions a task requires to accomplish an objective
        - **Method**: How an action is decomposed into steps
        - **Action**: An intentional act, "the act of doing X"
        - **Interface**: How an action is translated at lowest layer (ie: )

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
            - **Resources**: How much of something something has; power, fuel, food, etc
            - **Condition**: Integrity, damage, faults, readiness
            - **Lifecycle**: Current stage in existence or execution
            - **Mission**: Assignments, tasks, plans, missions, stages

        - **Event**: A discrete occurrence — something that happened at a point in time, whether planned or not

        - **Intel**: Effect-side data that something happened or changed external to the sender object
            - **Detection**: Assessment that something exists or occurred
            - **Classification**: Assessment assigning type or identity to an object
            - **Track**: Assessment of the state of an external object over time
            - **Assessment**: Evaluation of effect, damage, outcome, or threat

    - **Sensory**: Unstructured, non-symbolic sensory signal data that has to be interpreted
        - **AV**: Seen or heard; video, images, audio recordings
        - **Spatial**: point clouds, 3D models, scans, etc
        - **Samples**: IQ samples or other analog data


