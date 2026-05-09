# Data

## Information

### Properties

#### Identity

Identity [facets]:
- name, model
- unique identifier (uuid4)

[facets] extended:
- callsign
- description (human-readable)
- alternate IDs (list of typed ID pairs)
- aliases
- provenance (source attribution)
- visual markings (hull/tail number, tactical markings, color scheme)
- electronic signature
- IFF / transponder codes

#### Attributes
Fundamental characteristics, type, form.
Speciates by what Object is being described.

[facets] all Attributes:
- faction (Faction)

MachineAttributes [facets]:
- faction (Faction)
- propulsion
- max range, max speed, cruise speed, max altitude, max flight time
- weather limits
- roles (list)
- sensors, links, weapons
- dimensions (length)
- indicators (simulated, exercise, emergency, c2, egressable, starred)

OrganizationAttributes [facets]:
- faction (Faction)
- organizational class (OrgClass)
- echelon (ArmyEchelon)
- unit category (UnitCategory)
- composition (personnel, equipment counts)

PersonAttributes [facets]:
- faction (Faction)
- nationality
- role, specialty

Capability [facets]:
- capability type (CapabilityType)
- description
- max range
- min range
- rate
- supported ammunition or effects

WeaponMount [facets]:
- weapon reference
- mount type (WeaponMountType)
- traverse limits
- elevation limits

ArmorProtection [facets]:
- armor type (ArmorType)
- armor level (ArmorLevel)
- coverage

MobilityProfile [facets]:
- max speed
- cruise speed
- max gradient
- max side slope
- max fording depth
- turning radius
- ground pressure

VisualDetails [facets]:
- color scheme
- markings
- tail number
- camouflage pattern
- special identifiers

RangeRings [facets]:
- center position
- ring radii (ordered list)
- ring labels

Dimensions [facets]:
- length
- width
- height
- wingspan (optional)

#### Parameters
Current operating configuration or control regime.

Robot Parameters [facets]:
- current autonomy mode (vs ceiling on Robot itself)
- control authority holder (Entity reference)
- flight mode
- armed state
- in-air state
- active modes
- override active
- failsafe state

Task Parameters [facets]:
- lifecycle phase (LifecyclePhase)

#### Relationship

[variants] by nature:
- CONTROL: ControlAuthority
- ASSIGNMENT: TaskAssignment
- OWNERSHIP: Ownership
- COMPOSITION: Composition
- TRACKING: TrackingRelationship
- GROUP: GroupRelationship
- CORRELATION: CorrelationRelationship
- ACTIVE_TARGET: ActiveTargetRelationship
- COMMAND: CommandRelationshipEntry

ControlAuthority [facets]:
- controller (Entity reference)
- authority level (AuthorityLevel)

TaskAssignment [facets]:
- task reference

Ownership [facets]:
- owner (Organization reference)

Composition [facets]:
- part (Item reference — Component or Payload)

CorrelationRelationship [facets]:
- primary entity, secondary entities
- type (Manual, Automated)
- replication mode (Local, Global)

Handoff [facets]:
- handoff type (HandoffType)
- from entity
- to entity
- subject reference
- initiated time
- completed time
- status
- authorization token

### State
Telemetric, changing data about the condition of an object at a given time.

#### Kinematic

Kinematic [facets]:
- attitude (rotation, eg Quaternion or EulerAngles)
- ground speed
- airspeed (optional)
- velocity vector (optional, ENU)
- acceleration vector (optional, ENU)
- angular rate vector (optional)
- heading
- course
- climb rate
- throttle

#### Location

Location [facets]:
- position (geographic, eg LLA)
- altitude (meters, with reference datum)
- satellite count (optional, GPS quality indicator)
- velocity ENU (optional)
- speed (scalar, optional)
- acceleration ENU (optional)
- attitude (Quaternion, body→ENU, optional)

IndoorPosition [facets]:
- building reference
- floor number
- room identifier
- x offset
- y offset
- location method (IndoorPosMethod)

DeadReckoningState [facets]:
- last fix position
- last fix time
- estimated position
- drift estimate
- method

RelativePosition [facets]:
- reference entity
- offset
- frame

LocationUncertainty [facets]:
- position covariance (CovarianceMatrix3x3, ENU)
- velocity covariance (CovarianceMatrix3x3, ENU)
- error ellipse (ErrorEllipse)
- circular error (CE)
- linear error (LE)

#### Navigation

Navigation [facets]:
- navigation mode
- fix type
- global position valid
- home position valid
- position source
- heading source
- altitude source
- GNSS diagnostic statistics

NavigationState [facets]:
- navigation mode
- fix type
- position source
- heading source
- altitude source
- raw GNSS sample
- GNSS diagnostics

RawGNSSSample [facets]:
- latitude
- longitude
- absolute altitude
- ground speed
- ground course
- HDOP
- VDOP
- yaw

GNSSDiagnostics [facets]:
- last message age
- error count
- timeout count
- HDOP
- EPH
- EPV

#### Sensor

[variants] by kind:
- IMU: IMUState
- READINESS: SensorReadiness

IMUState [facets]:
- acceleration vector
- angular rate vector
- magnetic field vector
- temperature (optional)
- timestamp (optional)
- frame (optional)

SensorReadiness [facets]:
- gyro ready
- accel ready
- mag ready
- local position ready
- global position ready
- home position ready
- armable

FieldOfView [facets]:
- horizontal field of view
- vertical field of view
- minimum range
- maximum range

ProjectedFrustum [facets]:
- apex position
- direction (AzimuthElevation)
- horizontal field of view
- vertical field of view
- near range
- far range

RFConfiguration [facets]:
- center frequency
- bandwidth range
- operational modes

Bandwidth [facets]:
- center frequency
- bandwidth

BandwidthRange [facets]:
- min frequency
- max frequency

#### Input

Input [facets]:
- RC channel values
- receiver calibration / min / max / center
- channel mapping
- mode ranges

RCInputState [facets]:
- RC channel values

ReceiverConfig [facets]:
- min pulse
- max pulse
- center pulse

ChannelMap [facets]:
- channel mapping entries

ModeRangeSet [facets]:
- mode ranges

#### Resources

[variants] by resource type:
- BATTERY: Battery
- FUEL: Fuel
- CONSUMABLE: Consumable

Battery [facets]:
- voltage
- current draw (optional)
- remaining percentage
- remaining capacity
- temperature (optional)
- cell voltages (optional list)
- cell count (optional)
- power watts
- consumed charge / energy
- source identifier (optional)
- link quality proxy / RSSI (optional)

Fuel [facets]:
- volume (or gallons)
- remaining percentage
- max capacity
- operational requirement
- consumption rate

Consumable [facets]:
- total count
- remaining count

PowerSource [facets]:
- status (PowerStatus)
- type (PowerType)
- level (PowerLevel: capacity, remaining, percent, voltage, current, run time, consumption rate)
- offloadable (bool)

#### Condition

Condition [facets]:
- readiness level
- fault list
- damage assessment

Health [facets]:
- overall health status (HealthStatus)
- connection status (ConnectionStatus)
- component health map (ComponentHealth by ID)
- alerts (list of Alert)

ComponentHealth [facets]:
- component identifier
- health status (HealthStatus)
- last update time
- error codes (optional list)

ComponentMessage [facets]:
- component identifier
- message text
- severity (AlertLevel)
- timestamp

Alert [facets]:
- alert level (AlertLevel)
- condition (AlertCondition)
- message
- timestamp

AlertCondition [facets]:
- condition identifier
- description
- severity (AlertLevel)
- acknowledged flag
- timestamp

#### Lifecycle

#### Internal

Internal [facets]:
- operational mode
- error codes
- cpu load, memory used, disk used
- uptime
- temperature
- software version, build hash
- FC connectivity
- cycle time
- flight controller identity

SoftwareState [facets]:
- version
- build hash
- last updated
- config hash

AutopilotState [facets]:
- mode
- armed state
- in-air state
- throttle percentage
- navigation mode
- geofence active
- failsafe active

FlightControllerIdentity [facets]:
- API version
- FC variant
- board info
- hardware UID
- legacy UID
- vendor ID
- vendor name
- product ID
- product name
- flight software version
- flight software git hash
- OS software version
- OS software git hash

#### Mission

MissionProgress [facets]:
- current waypoint index
- total waypoints
- mission valid

WaypointStatus [facets]:
- total waypoint count
- current waypoint index
- mission valid

### Event
A discrete occurrence — something that happened at a point in time, whether planned or not.
Peer of State and Intel under Information. Not a sub-class of State.

[variants] by subject:
- FLIGHT: FlightEvent
- MISSION: MissionEvent

FlightEvent [variants] by transition:
- ARMED: ArmedEvent
- DISARMED: DisarmedEvent
- TAKEOFF_DETECTED: TakeoffDetectedEvent
- LANDED: LandedEvent
- FAILSAFE_CHANGED: FailsafeChangedEvent

TakeoffDetectedEvent [facets]:
- altitude

FailsafeChangedEvent [facets]:
- failsafe state

MissionEvent [variants] by outcome:
- ABORTED: MissionAbortedEvent
- COMPLETED: MissionCompletedEvent

MissionAbortedEvent [facets]:
- reason

GeofenceViolation [facets]:
- entity reference
- geofence reference
- violation type (GeofenceViolationType)
- position
- timestamp
- action taken

InterfaceHealth [facets]:
- transport connected
- last error
- received count
- transmitted count
- parse error count
- last received message summary
- last transmission result

### Intel

#### Detection

Detection [facets]:
- position (where)
- timestamp (when)
- confidence (float 0-1)

[variants] by sensor:
- ACOUSTIC: AcousticDetection
- MOTION: MotionDetection
- SEISMIC: SeismicDetection
- CBRNE: CBRNEDetection
- LAUNCH: LaunchDetection
- IMPACT: ImpactDetection
- VIDEO: VideoDetection
- RADAR: RadarDetection
- RF: RFDetection

VideoDetection [facets]:
- bounding box (x, y, w, h)
- class id, class name
- confidence
- track id

#### Classification

Classification [facets]:
- detection reference (what was detected)
- assessed type/category
- confidence
- method

#### Track

Track [facets]:
- detection reference or track ID
- position history or current estimated state
- confidence

[facets] extended:
- track quality score (0-15)
- sensor hits count
- last measurement time
- line of bearing
- radar cross section (dBsm)
- number of objects (range)

#### Assessment

##### BDA (Battle Damage Assessment)

BDAResult [facets]:
- target reference
- assessment time
- assessor
- method (BDAMethod)
- phase (BDAPhase)
- damage level (DamageLevel)
- functional impact (FunctionalImpact)
- confidence
- restrike recommendation
- imagery reference

IntelReport [facets]:
- report identifier
- classification
- intelligence discipline (IntelDiscipline)
- DTG
- content summary
- reliability rating
- credibility rating

HUMINTReport [facets]:
- source reliability
- information credibility
- source identifier
- handler reference

SIGINTReport [facets]:
- SIGINT type (SIGINTType)
- intercept time
- emitter reference
- content summary

OSINTReport [facets]:
- source URL
- source type
- access time
- relevance score

GEOINTReport [facets]:
- imagery reference
- coverage area
- resolution
- collection time
- source platform

MASINTReport [facets]:
- measurement type
- sensor type
- data reference
- analysis summary

##### Target Management (Assessment)

HighValueTarget [facets]:
- is high value (bool)
- priority (int, lower = higher)
- is high payoff (bool)
- target matches

HighValueTargetMatch [facets]:
- high value target reference
- match confidence
- match time
- matching criteria

TargetPriority [facets]:
- high value target info
- threat assessment (is_threat bool)

IPBProduct [facets]:
- IPB product type (IPBType)
- area of operations
- prepared date
- prepared by

CommonOperatingPicture [facets]:
- timestamp
- entities
- tracks
- events
- area of operations

RecognizedAirPicture [facets]:
- timestamp
- air tracks
- airspace status

RecognizedMaritimePicture [facets]:
- timestamp
- maritime tracks
- maritime status

HighValueTargetList [facets]:
- ordered targets
- justification

HighPayoffTargetList [facets]:
- ordered targets
- engagement criteria

NoStrikeList [facets]:
- protected entities or sites
- reasons

##### Intelligence Reliability (Assessment)

#### Fusion

## Sensory

### AV

[variants]:
- VIDEO: Video
- IMAGE: Image
- AUDIO: Audio

ThermalImage [facets]:
- temperature range
- palette

SARImage [facets]:
- SAR mode (SARMode)
- resolution
- look direction
- incidence angle
- polarization

### Spatial

[variants]:
- POINTCLOUD: PointCloud
- MESH: Mesh
- SCAN: Scan

### Samples

[variants]:
- IQ: IQSamples — in-phase/quadrature
- ANALOG: AnalogSamples

