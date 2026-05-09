# Provenance [cross-cutting]

Provenance [facets]:
- integration name (source system)
- data type
- source ID
- source update time
- source description

AuditEntry [facets]:
- timestamp
- actor
- action
- resource
- old value
- new value
- reason

AccessControlEntry [facets]:
- subject reference
- resource reference
- permission level

Role [facets]:
- role name
- permissions
- inherited roles

DataPolicy [facets]:
- data reference
- classification
- handling instructions
- releasability
- retention period

Notification [facets]:
- notification type
- severity
- subject reference
- message
- timestamp
- acknowledged

DataQuality [facets]:
- freshness in seconds
- accuracy estimate
- source reliability
- completeness percentage
- consistency check passed

VersionStamp [facets]:
- major
- minor
- patch
- build hash

TimeSync [facets]:
- sync source
- UTC offset
- sync accuracy
- last sync time

ClockDrift [facets]:
- estimated drift
- last calibration time

CoordinateTransform [facets]:
- from frame
- to frame
- transform method
- transform accuracy

ProtocolBridge [facets]:
- source protocol
- target protocol
- translation rules
- unmappable fields

SimulationConfig [facets]:
- simulated flag
- time acceleration factor
- injected entities
- scenario name

EOBEntry [facets]:
- emitter reference
- location
- signal characteristics
- associated platform type
- threat level
- first detected
- last detected
- active

OperationalPhase [facets]:
- phase name
- phase number
- H-hour offset
- description
- trigger conditions
- end conditions

ISRRequest [facets]:
- requester
- collection type
- priority
- area
- time window
- sensor requirements
- latest time info is of value

SALUTEReport [facets]:
- size
- activity
- location
- uniform
- time
- equipment

HeartbeatConfig [facets]:
- interval
- timeout
- jitter

MapLayer [facets]:
- layer name
- layer type
- visible
- opacity
- z-order
- source

Reachability [facets]:
- from node
- to node
- reachable
- path
- latency
- bandwidth
- reliability

FrequencyAllocation [facets]:
- band
- min frequency
- max frequency
- purpose
- assigned to
- priority
- exclusive

DecisionPoint [facets]:
- decision name
- trigger conditions
- options
- deadline
- authority

PowerBudget [facets]:
- entity reference
- total available power
- allocated power map
- reserve percentage

