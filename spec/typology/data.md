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

[enum] AltIdType:
- TrackId
- SPI_Id
- AssetId
- Link16TrackNumber
- Link16_JU
- Callsign
- MMSI
- VMF_URN
- IMO
- SerialNumber
- RegistrationId
- DODAAC
- UIC
- NORAD_CAT_ID
- UNOOSA_Name
- UNOOSA_Id

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

[enum] CapabilityType:
- Maneuver
- FireSupport
- ISR
- Strike
- Relay
- Logistics
- Medical
- AirDefense
- EW
- Cyber

Capability [facets]:
- capability type (CapabilityType)
- description
- max range
- min range
- rate
- supported ammunition or effects

[enum] WeaponMountType:
- Fixed
- Turret
- Pintle
- Coaxial
- Wing
- Pylon
- Internal

WeaponMount [facets]:
- weapon reference
- mount type (WeaponMountType)
- traverse limits
- elevation limits

[enum] ArmorType:
- None
- Ballistic
- Composite
- Reactive
- Slat
- Active
- Cage

[enum] ArmorLevel:
- None
- SmallArms
- HeavyMachineGun
- Autocannon
- ShapedCharge
- KineticEnergy

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

[enum] AirRole:
- GroundAttack
- AntiAir
- Fighter
- Reconnaissance
- IMINT
- SIGINT
- Minelaying
- Cargo

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

[enum] Template:
- Track
- SensorPointOfInterest
- Asset
- Geo
- SignalOfInterest

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

[enum] AuthorityLevel:
- Full
- Shared
- Delegated
- Monitor

[enum] CorrelationType:
- Manual
- Automated

[enum] CorrelationReplicationMode:
- Local
- Global

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

[enum] HandoffType:
- ControlAuthority
- TrackCustody
- TaskAssignment
- SensorCue
- CommunicationRelay
- LogisticResponsibility

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

[enum] IndoorPosMethod:
- WiFi
- BLE_Beacon
- UWB
- RFID
- Optical
- DeadReckoning
- Manual

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

[enum] GPSFixType:
- NoFix
- Fix2D
- Fix3D
- DGPS
- RTK_Float
- RTK_Fixed
- Static
- PPS

[enum] NavSource:
- GPS
- GLONASS
- Galileo
- BeiDou
- INS
- VIO
- OpticalFlow
- SLAM
- Barometer
- Radar
- Altimeter
- Fused

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

[enum] NavMode:
- Manual
- Waypoint
- RTL
- Loiter
- Guided
- Land
- Takeoff
- Circle
- Drift
- PositionHold
- Brake
- Throw
- ADSB
- SmartRTL
- FlowHold
- Follow
- Zigzag
- SystemID
- AutoRotate

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

[enum] SensorMode:
- Search
- Track
- WeaponSupport
- Auto
- Mute

[enum] SensorType:
- Radar
- Camera
- Transponder
- RF
- GPS
- PTU_Pos
- Perimeter
- Sonar

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

[enum] PowerStatus:
- Unknown
- NotPresent
- Operating
- Disabled
- Error

[enum] PowerType:
- Unknown
- Gas
- Battery

#### Condition

Condition [facets]:
- readiness level
- fault list
- damage assessment

[enum] HealthStatus:
- Healthy
- Warn
- Fail
- Offline
- NotReady

[enum] ConnectionStatus:
- Online
- Offline

[enum] OperationalState:
- Off
- NonOperational
- Degraded
- Operational
- Denied

[enum] AlertLevel:
- Advisory
- Caution
- Warning

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

[enum] LifecyclePhase:
- Planned
- Active
- Paused
- Complete
- Aborted
- Failed

[enum] RequestStatus:
- Submitted
- Acknowledged
- Approved
- Denied
- InTransit
- Delivered
- Cancelled

[enum] OverrideStatus:
- Applied
- Pending
- Timeout
- Rejected
- DeletionPending

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

[enum] OperationalMode:
- Off
- Startup
- Nominal
- Degraded
- Emergency
- Maintenance
- Calibrating
- Standby
- Sleep

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

[enum] EntityLifecycleEvent:
- FirstSeen
- Updated
- LocationChanged
- StatusChanged
- HealthChanged
- Correlated
- Decorrelated
- Overridden
- OverrideRemoved
- Expired
- PostExpiryOverride
- Deleted
- Lost
- Recovered
- HandedOff
- TaskAssigned
- TaskCompleted

[enum] GeofenceViolationType:
- Entered
- Exited
- AltitudeExceeded

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

[enum] PIDMethod:
- Visual
- Electronic
- Behavioral
- Intelligence

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

[enum] TrackState:
- Tentative
- Confirmed
- Coasting
- Dropped

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

[enum] BDAMethod:
- Visual
- ElectroOptical
- Infrared
- Radar
- SignalIntel
- HumanIntel

[enum] BDAPhase:
- Phase1_Initial
- Phase2_Supplemental
- Phase3_Restrike

[enum] DamageLevel:
- Undamaged
- Light
- Moderate
- Heavy
- Destroyed

[enum] FunctionalImpact:
- FullyOperational
- Degraded
- SignificantlyDegraded
- NonOperational
- Destroyed

[enum] BDAStatusColor:
- Grey
- Yellow
- Green
- Red

[enum] IntelDiscipline:
- HUMINT
- SIGINT
- OSINT
- GEOINT
- MASINT

[enum] SIGINTType:
- COMINT
- ELINT
- FISINT

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

[enum] IPBType:
- TerrainAnalysis
- WeatherAnalysis
- ThreatEvaluation
- ThreatIntegration
- CourseOfActionDevelopment

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

[enum] SourceReliability:
- A_CompletelyReliable
- B_UsuallyReliable
- C_FairlyReliable
- D_NotUsuallyReliable
- E_Unreliable
- F_CannotBeJudged

[enum] InfoCredibility:
- 1_Confirmed
- 2_ProbablyTrue
- 3_PossiblyTrue
- 4_Doubtful
- 5_Improbable
- 6_CannotBeJudged

#### Fusion

[enum] FusionMethod:
- NearestNeighbor
- Bayesian
- DempsterShafer
- KalmanFilter
- CovarianceIntersection
- Voting
- WeightedAverage

[enum] FusionLevel:
- L0_SourcePreprocessing
- L1_ObjectAssessment
- L2_SituationAssessment
- L3_ImpactAssessment
- L4_ProcessRefinement

[enum] GateType:
- Rectangular
- Ellipsoidal
- Mahalanobis

## Sensory

### AV

[variants]:
- VIDEO: Video
- IMAGE: Image
- AUDIO: Audio

ThermalImage [facets]:
- temperature range
- palette

[enum] SARMode:
- Spotlight
- Stripmap
- ScanSAR
- ISAR
- GMTI

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

