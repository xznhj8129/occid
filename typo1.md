# Typology

## Notation

Each entry is marked with what it produces at the Schema stage:

| Marker | What it does here | What Schema produces from it |
|--------|------------------|------------------------------|
| `[enum]` | Defines the vocabulary of differentiation | `enums:` block |
| `[variants]` | Declares how a class speciates into children | `variants:` block on parent struct |
| `[facets]` | Describes what a struct must capture (conceptual) | `fields:` on a struct (typed, named) |

Typology never defines typed fields. That is Schema's job.
Facets describe *what* must be captured; Schema decides *how* (names, types, optionality).

---

# Object

[variants] by class:
- ENTITY: Entity
- ORGANIZATION: Organization
- COLLECTION: Collection
- SYSTEM: System
- SITE: Site
- ITEM: Item

## Entity

[variants] by class:
- ACTOR: Actor
- MACHINE: Machine

### Actor

[variants] by nature:
- PERSON: Person
- AGENT: Agent

#### Person

[facets]:
- role (string)
- specialty / MOS (string)
- rank (string)

#### Agent

[variants] by type:
- LLM: LLMAgent
- VISION: VisionAgent
- PLANNING: PlanningAgent
- CONTROL: ControlAgent
- FUSION: FusionAgent
- CLASSIFICATION: ClassificationAgent

[facets]:
- model identifier
- capability set (inference types)
- context capacity
- tool manifest (available actions)

### Machine

[variants] by class:
- VEHICLE: Vehicle
- ROBOT: Robot
- PLATFORM: Platform

[enum] PropulsionType:
- Electric
- Gasoline
- Diesel
- Turbine
- Hybrid
- Hydrogen
- Solar

[enum] LandPropulsion:
- Wheeled
- Tracked
- Bipedal
- Legged

#### Vehicle

[variants] by domain:
- LAND: LandVehicle
- AIR: AirVehicle
- SEA: SeaVehicle
- SUBSEA: SubseaVehicle
- SPACE: SpaceVehicle

[enum] LandVehicleClass:
- Light
- Armored

LandVehicle [facets]:
- class (LandVehicleClass)
- propulsion (LandPropulsion)

[enum] AirVehicleClass:
- Fighter
- Bomber
- Transport
- Tanker
- Trainer
- Reconnaissance
- Helicopter
- Tiltrotor
- LighterThanAir

AirVehicle [facets]:
- class (AirVehicleClass)
- propulsion (PropulsionType)

[enum] SeaVehicleClass:
- Frigate
- Destroyer
- Carrier
- Submarine
- Patrol
- Amphibious
- Auxiliary
- Merchant

SeaVehicle [facets]:
- class (SeaVehicleClass)

#### Robot

[variants] by PhysicalDomain:
- AIR: AirRobot (UAV/UAS)
- LAND: LandRobot (UGV)
- SEA: SeaRobot (USV)
- SUBSEA: SubseaRobot (UUV)
- SPACE: SpaceRobot

[facets]:
- domain (PhysicalDomain)
- autonomy ceiling (AutonomyClass) — ceiling capability, not current mode

[enum] AutonomyClass:
- Remote — directly piloted, no onboard autonomy
- Assisted — human controls, machine assists (stabilization, failsafes)
- SemiAutonomous — machine executes discrete tasks, human approves each
- Supervised — machine acts continuously, human monitors and can intervene
- Autonomous — machine acts independently within parameters

[enum] MultirotorConfig:
- Quad
- Hex
- Octo
- Coaxial
- Y6
- X8

[enum] FixedWingConfig:
- Conventional
- FlyingWing
- Canard
- TandemWing
- BlendedWingBody
- Delta

[enum] VTOLConfig:
- Tiltrotor
- Tailsitter
- LiftAndCruise
- QuadPlane
- CopterPlane

[enum] LaunchMethod:
- HTOL
- VTOL
- Catapult
- HandLaunch
- RailLaunch
- TubeLaunch
- DropLaunch
- BalloonLaunch

[enum] RecoveryMethod:
- HTOL
- VTOL
- Parachute
- DeepStall
- NetRecovery
- SkyHook
- BellyLand
- Ditching

AirRobot [facets]:
- airframe config (MultirotorConfig, FixedWingConfig, VTOLConfig as applicable)
- launch method
- recovery method
- propulsion (PropulsionType)
- max range, max flight time, max speed, cruise speed, max altitude
- weather limits

LandRobot [facets]:
- propulsion (LandPropulsion)
- max range, max speed

#### Platform

[variants] by function:
- LAUNCHER: Launcher
- CHARGER: Charger
- RELAY: Relay
- GCS: GroundControlStation
- COMMAND_POST: MobileCommandPost
- SENSOR_PLATFORM: SensorPlatform
- OPERATOR_STATION: OperatorStation

GroundControlStation [facets]:
- operator station count
- supported protocols
- mobile (bool)

## Organization

[variants] by structure:
- GROUP: Group — contains subordinate organizations
- UNIT: Unit — contains only entities

[enum] OrgClass:
- Civilian
- Military
- Commercial
- NGO
- Unknown

[enum] CommandRelationship:
- OPCON — operational control
- TACON — tactical control
- ADCON — administrative control
- SUPCON — support
- DIRLAUTH — direct liaison authority

[enum] SupportRelationship:
- DirectSupport
- GeneralSupport
- Reinforcing
- GeneralSupportReinforcing

[enum] ArmyEchelon:
- FireTeam
- Squad
- Section
- Platoon
- Company
- Battery
- Troop
- Battalion
- Squadron
- Regiment
- Brigade
- Division
- Corps
- Army
- ArmyGroup
- Theater

[enum] UnitSize:
- IND
- TEM
- SQD
- SEC
- PLT
- COY
- BTN
- RGT
- BDE
- DIV
- FLT
- SQN
- GRP
- WNG

[enum] UnitCategory:
- COMB
- BATT
- TF
- MECH
- INF
- MOT
- REC
- UAV
- UAVA
- UAVR
- UGV
- SIG
- ENG
- ART
- MORT
- MRL
- ARM
- CAV
- MED
- SUP
- LOG
- HQ
- NBC
- MP
- AIR
- SOF
- NAV
- AMP
- ADA
- EW
- ISR
- CBT
- CSS
- COM
- DET
- RES
- TRG

[facets] all Organizations:
- org class (OrgClass)
- echelon (ArmyEchelon or UnitSize)
- taskforce flag (bool)

## Collection

[variants] by purpose:
- CONVOY: Convoy
- FORMATION: Formation
- TASK_GROUP: TaskGroup
- SENSOR_NETWORK: SensorNetwork
- TARGET_DECK: TargetDeck
- MINEFIELD: Minefield

[enum] FormationType:
- Line
- Column
- Wedge
- Vee
- EchelonLeft
- EchelonRight
- Diamond
- StaggeredColumn
- Box
- File
- Herringbone
- Coil

Convoy [facets]:
- ordered member list
- route (path reference)
- spacing, speed

Formation [facets]:
- formation type (FormationType)
- members (ordered)
- spacing
- reference entity

## System

[variants] by function:
- WEAPON_SYSTEM: WeaponSystem
- COMMUNICATION_SYSTEM: CommunicationSystem
- SENSOR_SUITE: SensorSuite
- FIRE_CONTROL: FireControlSystem
- EW_SUITE: EWSuite
- NAVIGATION_SYSTEM: NavigationSystem
- C2_SYSTEM: C2System
- IADS: IntegratedAirDefenseSystem
- POWER_SYSTEM: PowerSystem

WeaponSystem [facets]:
- platform reference
- weapon reference
- fire control reference
- ammunition types
- max/min engagement range, rate of fire

## Site

[variants] by purpose:
- WAYPOINT: Waypoint
- CONTROL_POINT: ControlPoint
- GEOFENCE: Geofence
- CONTROL_AREA: ControlArea
- LANDING_ZONE: LandingZone
- DROP_ZONE: DropZone
- ASSEMBLY_POINT: AssemblyPoint
- FOB: ForwardOperatingBase
- OBSERVATION_POST: ObservationPost
- RALLY_POINT: RallyPoint
- ATTACK_POSITION: AttackPosition
- SBF_POSITION: SupportByFirePosition
- LOD: LineOfDeparture
- SUPPLY_POINT: SupplyPoint
- NAI: NamedAreaOfInterest
- TAI: TargetAreaOfInterest
- ACM: AirspaceCoordinatingMeasure
- BULLSEYE: Bullseye
- ENGAGEMENT_ZONE: EngagementZone
- HAZARD_AREA: HazardArea
- NO_FLY_ZONE: NoFlyZone
- AIRSPACE_VOLUME: AirspaceVolume
- TARGET_SET: TargetSet
- TARGET_BOX: TargetBox
- SPATIAL_FEATURE: SpatialFeature
- COMMAND_POST: CommandPost
- CHECKPOINT: SiteCheckpoint
- TRIGGER_POINT: TriggerPoint
- HIDE_POSITION: HidePosition
- PATROL_BASE: PatrolBase
- CORRIDOR: Corridor

[enum] GeofenceAction:
- KeepIn
- KeepOut
- Warn
- RTL
- Land
- Loiter
- Report
- Deny
- Brake
- Fence

[enum] ControlAreaType:
- KeepInZone
- KeepOutZone
- DitchZone
- LoiterZone

[enum] GeoType:
- General
- Hazard
- Emergency
- EngagementZone
- ControlArea
- Bullseye
- ACM

[enum] AirspaceClass:
- A
- B
- C
- D
- E
- F
- G

[enum] AirspaceType:
- Controlled
- Restricted
- Prohibited
- Danger
- Alert
- MOA
- Warning
- TFR
- CTR
- TMA
- FIR
- UIR
- ATZ
- ADIZ

[enum] AirspaceStatus:
- Active
- Inactive
- Scheduled
- Hot
- Cold

[enum] RallyPointType:
- ObjectiveRallyPoint
- InitialRallyPoint
- ActionPoint
- LinkupPoint
- AlternateRallyPoint

[enum] SupplyPointType:
- Depot
- ASP
- FARP
- Cache
- AidStation
- MaintenancePoint
- DistributionPoint

[enum] CommandPostType:
- Main
- Tactical
- Alternate
- Rear

[enum] FSCMType:
- FSCL
- CFL
- NFL
- RFL
- FFA
- NFA
- RFA
- ACA

Geofence [facets]:
- geometry (polygon)
- floor altitude, ceiling altitude
- action (GeofenceAction)
- enabled, priority

AirspaceVolume [facets]:
- geometry (polygon, horizontal)
- floor altitude, ceiling altitude
- class (AirspaceClass)
- type (AirspaceType)
- status (AirspaceStatus)
- schedule (time windows)

SupplyPoint [facets]:
- position
- type (SupplyPointType)
- capacity by supply class
- current inventory

NamedAreaOfInterest [facets]:
- geometry
- purpose
- indicators to watch

## Item

[variants] by purpose:
- RECORD: Record
- EQUIPMENT: Equipment
- COMPONENT: Component
- PAYLOAD: Payload

### Record
No further speciation yet.

### Equipment

[variants] by category:
- PERSONAL_WEAPON: PersonalWeapon
- OPTIC: Optic
- COMMS_GEAR: CommunicationsGear
- PROTECTIVE: ProtectiveGear
- NAV_EQUIPMENT: NavigationEquipment
- MUNITION: Munition
- LINK_HARDWARE: LinkHardware

[enum] WeaponCategory:
- Rifle
- Carbine
- Pistol
- MachineGun
- GrenadeLauncher
- AntiTank
- ManPAD
- Mortar
- Sniper
- Shotgun

[enum] MunitionStatus:
- NotPresent
- Present
- Ready
- Fault

Munition [facets]:
- type
- status (MunitionStatus)
- quantity

### Component

[enum] ComponentCategory:
- Motor
- ESC
- Battery
- FlightController
- Antenna
- Gimbal
- Servo
- Propeller
- Airframe
- LandingGear
- Parachute
- Transponder
- ADS_B
- IFF

### Payload

[variants] by category:
- EO_CAMERA: EOCamera
- IR_CAMERA: IRCamera
- MULTISPECTRAL: MultispectralCamera
- LIDAR: LIDARPayload
- SAR: SARPayload
- SIGINT_RECEIVER: SIGINTReceiver
- COMM_RELAY: CommRelayPayload
- CARGO: CargoPayload
- WEAPON: WeaponPayload
- JAMMER: JammerPayload
- ILLUMINATOR: Illuminator
- RWS: RemoteWeaponStation

[enum] PayloadOperationalState:
- Off
- NonOperational
- Degraded
- Operational
- OutOfService
- Unknown

[enum] GuidanceType:
- Unguided
- GPS
- INS
- LaserGuided
- IRHoming
- RadarHoming
- CommandGuided
- Wire
- FiberOptic
- Terminal_TV
- Vision

[facets] all Payloads:
- operational state (PayloadOperationalState)
- weight, power draw

WeaponPayload [facets]:
- weapon type
- guidance (GuidanceType)
- warhead type, max range

---

# Reference

## Frame

[enum] Local2D:
- LU
- LD
- RU
- RD

[enum] Local3D:
- FRD
- FLU
- NED
- ENU

[enum] GlobalFrame:
- WGS84
- ETRS89
- ECEF
- ECI
- TEME
- LVLH

[enum] AltitudeReference:
- AMSL
- HAE
- AGL
- Barometric
- StartRelative
- HAAT
- AboveSeaFloor
- BelowSeaSurface
- EGM96

[enum] BearingReference:
- TrueNorth
- MagneticNorth
- GridNorth
- RelativeToHeading

## Coordinate

[enum] CoordinateEncoding:
- Cartesian2D
- Cartesian3D
- LatLon
- UTM
- MGRS
- PlusCode
- ECI
- ENU
- Spherical

## Geometry

[enum] GeometryType:
- Point
- Line
- Path
- Polygon
- Volume
- Orientation
- Arc
- Ellipse
- Ellipsoid
- Frustum
- Corridor
- Annulus

## Time

[facets] Timestamp:
- value (epoch, integer)

[facets] TimeWindow:
- start time, end time

[facets] Duration:
- value (seconds or milliseconds)

[facets] PhaseTime:
- h-hour reference, offset

[enum] TimeSyncSource:
- GPS
- NTP
- PTP
- Manual
- RadioTimeSignal

## Type

[enum] PhysicalDomain:
- Land
- Air
- Sea
- Undersea
- Space

[enum] CombatDomain:
- Combat
- CombatSupport
- CombatSupportService

[enum] OpDomain:
- Land
- Air
- Sea
- Undersea
- Space
- Radio
- Psychological
- Cyber

[enum] Faction:
- UNKNOWN
- PENDING
- FRIENDLY
- SUSPECT
- HOSTILE
- NEUTRAL
- ASSUMED
- FAKER
- JOKER

[enum] Disposition:
- Unknown
- Friendly
- Hostile
- Suspicious
- AssumedFriendly
- Neutral
- Pending

[enum] ClassificationLevel:
- Unclassified
- ControlledUnclassified
- Confidential
- Secret
- TopSecret

[enum] ClassificationCaveat:
- NOFORN
- REL_TO
- FVEY
- NATO
- EU
- COSMIC
- ATOMAL

[enum] Nationality:
(100+ countries per Lattice — Albania through Zimbabwe, plus NATO, UN, InternationalRedCross)

[enum] MilitaryBranch:
- Army
- Navy
- AirForce
- Marines
- CoastGuard
- SpaceForce
- SpecialOperations
- Joint

[enum] EntityStatus:
- Active
- Inactive
- Unknown
- Offline
- Online
- Present
- Damaged
- Destroyed
- Lost
- Decoy

[enum] Priority:
- Routine
- Priority
- Immediate
- Flash
- FlashOverride
- CRITIC

[enum] PACE:
- Primary
- Alternate
- Contingency
- Emergency

[enum] ThreatLevel:
- Green
- Amber
- Red
- Black

[enum] DDILCondition:
- Normal
- Limited
- Intermittent
- Disrupted
- Denied

[enum] InteropLevel:
- Level1_IndirectRelay
- Level2_DirectReceipt
- Level3_PayloadControl
- Level4_FlightControl
- Level5_LaunchRecovery

## Structs

Reusable data shapes built on Reference primitives.
Ontologically part of Reference, not a separate root.

### Primitives

Vector2D [facets]:
- two-axis float vector (x, y)

Vector3D [facets]:
- three-axis float vector (x, y, z)

Quaternion [facets]:
- rotation quaternion (x, y, z, w)

EulerAngles [facets]:
- yaw, pitch, roll

### Measurement

Measurement [facets]:
- value (float)
- sigma / uncertainty (float, optional)

### Bearing

Bearing [facets]:
- value (degrees 0-360)
- reference (BearingReference)

### Geographic Positions

Position structs carry their own coordinate encoding and frame
as const metadata, so the consumer always knows how to interpret them.

LatLon [facets]:
- coordinate encoding (const, LatLon)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- latitude
- longitude

LLA [facets]:
- latitude, longitude
- altitude with reference (AltitudeReference)
- optional: altitude_hae, altitude_agl, altitude_asf, pressure_depth

MGRS [facets]:
- coordinate encoding (const, MGRS)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- grid zone, band, easting, northing

UTM [facets]:
- coordinate encoding (const, UTM)
- reference frame (GlobalFrame)
- geometry type (const, Point)
- zone, band, easting, northing

PlusCode [facets]:
- code string

ECI [facets]:
- x, y, z (doubles)

ENU [facets]:
- e, n, u (doubles) — used for velocity, acceleration

Spherical [facets]:
- azimuth, elevation, range

### Local Positions

LocalPosition [facets]:
- inherits Vector2D

### Lines

Line2D [facets]:
- start point (Vector2D), stop point (Vector2D)

Line3D [facets]:
- start point (Vector3D), stop point (Vector3D)

### Paths

Path2D [facets]:
- ordered list of Vector2D

Path3D [facets]:
- ordered list of Vector3D

LLAPath [facets]:
- ordered list of LLA
- loop (bool)

### Polygons and Shapes

Polygon [facets]:
- ordered list of LLA (closed ring)

GeoEllipse [facets]:
- semi-major axis, semi-minor axis, orientation, height

GeoEllipsoid [facets]:
- forward axis, side axis, up axis

### Bounding Boxes

Box2D [facets]:
- four corners (Vector2D)

Box3D [facets]:
- four corners (Vector3D)

### Error / Uncertainty

ErrorEllipse [facets]:
- probability
- semi-major axis, semi-minor axis, orientation

CovarianceMatrix3x3 [facets]:
- symmetric upper triangle (mxx, mxy, mxz, myy, myz, mzz)

### Pose

Pose [facets]:
- position (LLA)
- attitude (Quaternion) — body-to-ENU transform

### Range

FloatRange [facets]:
- lower bound, upper bound

UInt32Range [facets]:
- lower bound, upper bound

DoubleRange [facets]:
- min, max

DurationRange [facets]:
- min, max (Duration)

### Transforms

RigidTransform [facets]:
- rotation (Quaternion)
- translation (Vector3D)

### Content Address

ContentAddress [facets]:
- hash (SHA-256 bytes)
- size bytes
- MIME type

### Compact Encodings

CompactPosition [facets]:
- lat (int32 degE7), lon (int32 degE7), alt (int32 cm)

### Units

[enum] DistanceUnit:
- Meters
- Kilometers
- Feet
- Yards
- NauticalMiles
- StatuteMiles

[enum] SpeedUnit:
- MetersPerSecond
- Knots
- KilometersPerHour
- MilesPerHour

[enum] TemperatureUnit:
- Celsius
- Fahrenheit
- Kelvin

[enum] PressureUnit:
- Hectopascal
- Millibar
- InchesOfMercury

[enum] AngleUnit:
- Degrees
- Radians
- Mils_NATO
- Mils_Warsaw
- Gradians

[enum] MassUnit:
- Kilograms
- Pounds
- Tons_Metric
- Tons_Short

[enum] UnitOfMeasure:
- Each
- Kilogram
- Liter
- Round
- Box
- Case
- Pallet
- Meter
- SquareMeter
- CubicMeter
- Hour

---

# Control

## Directive

### Intent

[facets]:
- purpose (why)
- key tasks (what must happen)
- end state (what success looks like)

### Instruction

[variants] by form:
- OPORD: OPORD
- WARNO: WarningOrder
- FRAGO: FragmentaryOrder
- GENERAL_ORDER: GeneralOrder
- SOP: StandingOperatingProcedure
- STANDING_ORDER: StandingOrder

### Objective

[facets]:
- conditions: what must be true for success
- target reference (entity or point)

### Task

A Task has intent, actions, and an objective. It is not
a mode switch or a single command. "Fly to area X and loiter
for 30 minutes" is a task. "Take off" is a Command.

[variants] by purpose:
- MOVE: MoveTask
- PATROL: PatrolTask
- SEARCH: SearchTask
- OBSERVE: ObserveTask
- SURVEY: SurveyTask
- HOLD: HoldTask
- RELAY: RelayTask
- INVESTIGATE: InvestigateTask
- VISUAL_ID: VisualIdTask
- SHADOW: ShadowTask
- MONITOR: MonitorTask
- SCAN: ScanTask
- BDA: BDATask
- GIMBAL_POINT: GimbalPointTask
- GIMBAL_ZOOM: GimbalZoomTask
- TRANSIT: TransitTask
- MARSHAL: MarshalTask
- STRIKE: StrikeTask
- SMACK: SmackTask
- RELEASE_PAYLOAD: ReleasePayloadTask
- AREA_SEARCH: AreaSearchTask
- VOLUME_SEARCH: VolumeSearchTask
- IMPROVE_TRACK: ImproveTrackQualityTask
- MAP: MapTask
- LOITER: LoiterTask
- SET_LAUNCH_ROUTE: SetLaunchRouteTask
- FIRE_MISSION: FireMissionTask
- RESUPPLY: ResupplyMission
- MEDEVAC: MEDEVACMission
- EW_ACTION: EWActionTask
- ESCORT: EscortTask
- CAS: CloseAirSupportTask

[facets] all Tasks:
- priority
- specification (polymorphic payload — task-type specific data)
- relations (assignee, parent task)
- description
- scheduled time
- initial entities (objectives, zones)

[enum] TaskStatus:
- Created
- ScheduledInManager
- Sent
- MachineReceipt
- Ack
- Wilco
- Executing
- WaitingForUpdate
- DoneOk
- DoneNotOk
- Replaced
- CancelRequested
- CompleteRequested
- VersionRejected

[enum] TaskErrorCode:
- Cancelled
- Rejected
- Timeout
- Failed

Not tasks:
- Takeoff, Land, RTL → Commands
- Orbit, loiter patterns → Methods
- Track → method of observation, or sub-type of Observe

### Constraint

[variants] by domain:
- ROE: RulesOfEngagement
- EMCON: EMCONPolicy
- DECONFLICTION: DeconflictionRule
- AIRSPACE: AirspaceControlOrder
- WEATHER_LIMIT: WeatherLimits
- FLIGHT_RESTRICTION: FlightRestriction
- ABORT: AbortCriteria

[enum] WeaponsPosture:
- WeaponsFree
- WeaponsTight
- WeaponsHold

[enum] EMCONLevel:
- Full
- Limited
- Restricted
- Silent

[enum] EscalationLevel:
- ShowOfForce
- WarningShot
- Engage
- Destroy

[enum] DeconflictionType:
- Altitude
- Temporal
- Lateral
- Speed
- Route
- Frequency

[enum] AbortType:
- BatteryBingo
- FuelBingo
- CommsLost
- DamageSustained
- WeatherBelow
- MissionTimeout
- HostileContact
- GeofenceBreach
- ManualAbort
- EquipmentFailure

[enum] FailsafeAction:
- None
- RTL
- Land
- Loiter
- Descend
- Terminate
- Continue
- SmartRTL
- Brake
- Parachute
- HoldPosition

## Process

### Plan

[facets]:
- ordered actions
- task reference (what directive this fulfills)

[variants] by scope:
- MISSION_PLAN: MissionPlan
- ROUTE_PLAN: RoutePlan
- FIRE_SUPPORT_PLAN: FireSupportPlan
- COMMUNICATION_PLAN: CommunicationPlan
- LOGISTICS_PLAN: LogisticsPlan
- BRANCH_PLAN: BranchPlan
- SEQUEL_PLAN: SequelPlan

MissionPlan [facets]:
- name, uid, time, type
- formation parameters (h-sep, alt-sep, waves)
- phases: takeoff, assembly, ingress, survey, egress, landing
- assignments, flight plans, waypoints per phase

RoutePlan [facets]:
- route (ordered path segments)

### Method

[variants] by type:
- ORBIT: OrbitMethod
- SEARCH_PATTERN: SearchPattern
- MOVEMENT_TECHNIQUE: MovementTechnique
- ATTACK_METHOD: AttackMethod
- BREACH_METHOD: BreachMethod

[enum] OrbitPattern:
- Circle
- Racetrack
- FigureEight

[enum] OrbitDirection:
- Right
- Left

[enum] SearchPattern:
- Random
- Grid
- Spiral
- Sector
- Expanding

[enum] MovementTechnique:
- Traveling
- TravelingOverwatch
- BoundingOverwatch
- SuccessiveBounds
- AlternatingBounds

[enum] MovementFormation:
- Column
- StaggeredColumn
- Wedge
- Line
- Echelon
- Vee
- Diamond
- File
- Box
- Herringbone
- Coil

[enum] AttackType:
- Deliberate
- Hasty
- Spoiling
- Counterattack
- Raid
- Ambush
- Feint
- Demonstration

[enum] ApproachMethod:
- Frontal
- Flanking
- Envelopment
- TurningMovement
- Infiltration
- Penetration

### Action

[facets]:
- description
- status (LifecyclePhase)

### Interface
Physical actuation output, lowest layer.

[enum] InterfaceType:
- PWM — servo/ESC
- GPIO
- CAN — CAN bus
- Serial — serial actuator command
- RC — RC channel override

[facets]:
- channel/address
- output type

---

# Communication

## Node
Endpoint that transmits or receives.
An Entity can have multiple Nodes. Each Node has its own Transport(s).
Binding: Entity → Node → Transport.

[facets]:
- entity reference (what Entity this node belongs to)

[enum] NodeType:
- Sensor
- Effector
- C2
- Relay
- Gateway
- Observer
- All

## Transport

### Network

[enum] NetworkTopology:
- Mesh
- PointToPoint
- Broadcast
- StoreAndForward

[enum] MeshNodeRole:
- Router
- Endpoint
- Repeater
- Gateway
- BorderRouter

### Carrier

[variants] by medium:
- RADIO: RadioCarrier
- WIRE: WireCarrier
- IP: IPCarrier
- SATELLITE: SatelliteCarrier
- CELLULAR: CellularCarrier
- VOICE: VoiceCarrier — terminal, analog, no protocol

RadioCarrier [facets]:
- band (EMBand)
- frequency
- channel
- bandwidth
- waveform
- crypto type, crypto keys

WireCarrier [facets]:
- baud rate

SatelliteCarrier [facets]:
- band (SATCOMBand)
- orbit type (LEO, MEO, GEO)
- terminal type

[enum] EMBand:
- ELF
- SLF
- ULF
- VLF
- LF
- MF
- HF
- VHF
- UHF
- SHF
- EHF
- THF
- Infrared
- Visible

[enum] SATCOMBand:
- UHF
- SHF
- EHF
- Ka
- Ku
- X
- C
- L
- S

### Protocol

[enum] ProtocolType:
- MAVLink
- MAVLink_M
- MSPv2
- ROS
- STANAG4586
- CoT — Cursor on Target
- CustomSerial
- Meshtastic
- RTP_RTSP — video streaming
- SRT
- HLS
- WebRTC
- Link16
- VMF
- ADS_B
- XMPP
- DDS

[facets]:
- version
- serialization form (SerializationFormat)

[enum] SerializationFormat:
- Protobuf
- JSON
- XML
- CBOR
- MessagePack
- FlatBuffers
- Binary_Custom
- ASCII_Text

[enum] CompressionType:
- None
- GZIP
- LZ4
- Zstd
- Snappy

## Feed

[variants] by data flow shape:
- LINK: Link — discontinuous discrete packets
- STREAM: Stream — continuous indeterminate-size flow

Stream [variants] by content:
- VIDEO: VideoStream
- AUDIO: AudioStream
- SENSOR: SensorStream

[enum] StreamEncoding:
- H264
- H265
- VP8
- VP9
- AV1
- MJPEG
- RAW
- PCM
- AAC
- Opus

[enum] StreamTransport:
- RTP
- RTSP
- SRT
- HLS
- WebRTC
- MPEG_TS
- NDI
- RTMP

VideoStream [facets]:
- encoding (StreamEncoding)
- transport (StreamTransport)
- resolution, frame rate, bitrate, latency

## Message

[enum] MessageShape:
- Snapshot — whole state at a point in time
- Delta — only changes at a point in time
- History — only changes over time
- Log — whole state over time

[enum] DataFlowType:
- CommandDown — intent-bearing, reliable, ACK'd, small, infrequent
- StatusUp — task-coupled reporting, reliable, ACK'd, infrequent
- TelemetryUp — entity-state broadcast, lossy-tolerant, fire-and-forget, frequent

[enum] MessagePriority:
- Routine
- Priority
- Immediate
- Flash
- FlashOverride

[enum] AcknowledgmentPolicy:
- None
- OnReceipt
- OnProcessing
- OnExecution

[variants] by purpose:
- COMMAND: Command
- TELEMETRY: Telemetry
- OBSERVATION: Observation
- RESPONSE: Response

### Command
Directs or controls.

[variants] by target:
- NAVIGATION: NavigationCommand
- MODE: ModeCommand
- PARAMETER: ParameterCommand
- ACTUATOR: ActuatorCommand
- FIRE_SUPPORT: FireSupportCommand — immediate fire control only (adjust, cease, check); call-for-fire initiates FireMissionTask
- EW_COMMAND: EWCommand — immediate start/stop only (cease jam, start emission); sustained operations are EWActionTask
- COMMS_COMMAND: CommunicationCommand
- EMERGENCY: EmergencyCommand
- GIMBAL: GimbalCommand
- CAMERA: CameraCommand

[enum] GimbalMode:
- Stow
- Manual
- TrackEntity
- PointAtPosition
- PointAtAzEl
- ScanPattern
- StabilizedHold
- ReturnToCenter

[enum] CameraAction:
- TakePhoto
- StartRecording
- StopRecording
- SetZoom
- SetFocus
- SetExposure
- SetWhiteBalance
- SetPalette
- ToggleNightVision

### Telemetry
Reports the sender's own internal state.
Composes State data by reference — does not flatten fields.

[variants] by scope:
- VEHICLE: VehicleTelemetry
- HIGH_LATENCY: HighLatencyTelemetry — meta-telemetry for DDIL conditions

VehicleTelemetry [facets]:
- location (Location)
- kinematic state (Kinematic)
- battery (Battery)
- mission progress (MissionProgress)

HighLatencyTelemetry [facets]:
- position (compact)
- heading, target heading
- speed (air and ground)
- altitude, target altitude, climb rate
- battery remaining percent
- temperature
- current waypoint
- failure flags (bitmask)
- wind heading
- position uncertainty (ePH, ePV)

### Observation
Reports external objects, events, or environment.
Carries Intel data (Detection, Classification, Track).

### Response

[variants] by nature:
- ACK: Ack
- NACK: Nack
- RESULT: Result

### CoT Reply Codes (mapping to Response variants)

[enum] ReplyCode:
- Received
- Wilco
- Complete_Success
- Complete_Fail
- Fail_NoAssets
- Fail_BadRequest
- Fail_Denied
- Fail_InsufficientInfo
- Fail_Rejected
- Fail_RejectedByC2
- Fail_RejectedByPlatform
- Fail_Stale
- Status_Canceling
- Status_Executing
- Status_Review

### CoT Production Method (how data was produced)

[enum] ProductionMethod:
- Machine_GPS
- Machine_INS
- Machine_INS_GPS
- Machine_DGPS
- Machine_Mensurated
- Machine_Magnetic
- Machine_Simulated
- Machine_Configured
- Machine_Passed
- Machine_Fused
- Machine_Tracker
- Machine_Radio
- Machine_Radio_EPLRS
- Machine_Radio_PLRS
- Machine_Radio_Doppler
- Machine_Radio_VHF
- Machine_Radio_TADIL_A
- Machine_Radio_TADIL_B
- Machine_Radio_TADIL_J
- Human_Transcribed
- Human_Estimated
- Human_Calculated
- Human_Pasted
- Human_GIGO

### CoT Relation Types

[enum] RelationType:
- Parent
- Producer
- Owner
- Manager
- Leader
- Child
- Correlated
- Fused
- Composite
- Alternate
- Refinement
- Amplification
- RefinementURL
- TaskingBy
- TaskObject
- TaskIndirectObject
- TaskSubject
- TaskAt
- TaskBy
- TaskWith
- TaskFrom
- TaskRegarding

### CoT Operational Context

[enum] OperationalContext:
- Exercise
- Operational
- Simulated

---

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

[enum] AirRole:
- GroundAttack
- AntiAir
- Fighter
- Reconnaissance
- IMINT
- SIGINT
- Minelaying
- Cargo

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
- power watts
- consumed (mAh, mWh)

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

### Event
A discrete occurrence — something that happened at a point in time, whether planned or not.
Peer of State and Intel under Information. Not a sub-class of State.

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

##### Target Management (Assessment)

HighValueTarget [facets]:
- is high value (bool)
- priority (int, lower = higher)
- is high payoff (bool)
- target matches

TargetPriority [facets]:
- high value target info
- threat assessment (is_threat bool)

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

### Spatial

[variants]:
- POINTCLOUD: PointCloud
- MESH: Mesh
- SCAN: Scan

### Samples

[variants]:
- IQ: IQSamples — in-phase/quadrature
- ANALOG: AnalogSamples

---

# Weather [Data → State, of a Site or area]

[enum] PrecipitationType:
- None
- Rain
- Snow
- Sleet
- Hail
- FreezingRain
- Drizzle

[enum] CloudCover:
- Clear
- Few
- Scattered
- Broken
- Overcast

[enum] IcingIntensity:
- None
- Light
- Moderate
- Severe

[enum] TurbulenceIntensity:
- None
- Light
- Moderate
- Severe
- Extreme

[enum] FlightCategory:
- VFR
- MVFR
- IFR
- LIFR

[enum] WeatherSource:
- METAR
- TAF
- PIREP
- SIGMET
- AIRMET
- Radar
- Satellite
- ModelForecast

[enum] WeatherHazardType:
- Thunderstorm
- Icing
- Turbulence
- Fog
- Dust
- VolcanicAsh
- Windshear
- Sandstorm

WeatherCondition [facets]:
- temperature + unit
- wind (speed, gust, direction)
- pressure + unit
- humidity
- visibility + unit
- precipitation type + rate
- cloud coverage + ceiling + layers
- dew point
- icing intensity + altitude range
- turbulence intensity

---

# Terrain [Data → Properties, of a Site]

[enum] TerrainType:
- Urban
- Suburban
- Rural
- Forest
- Jungle
- Desert
- Mountain
- Tundra
- Marsh
- Farmland
- Water
- Coastal
- Arctic
- Steppe
- Savanna

[enum] TerrainSurface:
- Paved
- Unpaved
- Grass
- Sand
- Mud
- Rock
- Snow
- Ice
- Water
- Gravel

[enum] TerrainFeatureType:
- Ridge
- Valley
- Saddle
- Hill
- Depression
- Cliff
- River
- Lake
- Road
- Bridge
- Building
- Treeline
- Clearing
- UrbanArea
- Pass
- Ford
- Dam

[enum] ObstacleType:
- Wire
- Tower
- Building
- Terrain
- Vegetation
- Water
- Minefield
- Barrier
- Ditch

[enum] Traversability:
- Passable
- Restricted
- Impassable

[enum] MobilityClass:
- Unrestricted
- SlowGo
- NoGo

[enum] DTEDLevel:
- DTED0
- DTED1
- DTED2
- DTED3

---

# Supply Chain [Control → Directive + Data → State]

[enum] SupplyClass:
- I_Subsistence
- II_ClothingEquipment
- III_FuelPOL
- IV_Construction
- V_Ammunition
- VI_PersonalItems
- VII_MajorEndItems
- VIII_Medical
- IX_RepairParts
- X_Miscellaneous

[enum] SupplyPriority:
- Routine
- Priority
- Immediate
- Emergency

---

# Personnel [Data → State of Person]

[enum] PersonnelStatusType:
- Present
- Absent
- WIA
- KIA
- MIA
- Captured
- Evacuated
- OnLeave
- Detached
- Hospitalized
- RTD

[enum] CasualtyCause:
- Combat
- NonCombat
- Accident
- Disease
- FriendlyFire

[enum] InjurySeverity:
- Minor
- Serious
- VSI
- Critical
- Fatal

[enum] TreatmentStatus:
- Untreated
- FirstAid
- Stabilized
- Evacuated
- Hospitalized
- RTD
- Deceased

---

# MEDEVAC [Control → Directive]

[enum] PrecedenceCategory:
- Urgent
- UrgentSurgical
- Priority
- Routine
- Convenience

[enum] SpecialEquipment:
- None
- Hoist
- ExtractionEquipment
- Ventilator

[enum] PatientType:
- Litter
- Ambulatory

[enum] SecurityAtPickup:
- NoEnemy
- PossibleEnemy
- EnemyInArea
- EnemyContact

[enum] MarkingMethod:
- Panels
- PyroSignal
- Smoke
- None
- Other
- IRStrobe
- VSPanel

[enum] CBRNEContamination:
- None
- Chemical
- Biological
- Radiological
- Nuclear

---

# Fire Support [Control → Directive + Communication → Command]

[enum] EngagementMethod:
- PointTarget
- AreaTarget
- Suppression
- Destruction
- Neutralization
- Illumination
- Smoke
- Marking

[enum] FireType:
- Immediate
- Planned
- OnCall

[enum] WeaponType:
- Mortar
- Howitzer
- Rocket
- MLRS
- Missile
- DirectFire
- AirDelivered
- Naval

[enum] AmmunitionType:
- HE
- WP
- Illumination
- Smoke
- DPICM
- Thermobaric
- HEAT
- Frag
- AP
- Incendiary
- Guided

[enum] ShellTrajectory:
- Low
- High
- Vertical

[enum] FireMissionStatus:
- Requested
- Approved
- Denied
- ShotOut
- SplashOver
- RoundsComplete
- EndOfMission
- Cancelled
- CheckFiring

[enum] EffectAchieved:
- Destroyed
- Neutralized
- Suppressed
- NoEffect
- Unknown

---

# EW [Control → Process + Data → Intel]

[enum] EWActionType:
- Jam
- Spoof
- Deceive
- Intercept
- DirectionFind
- Monitor
- Deny

[enum] JamType:
- Noise
- Barrage
- Spot
- Sweep
- Responsive
- Follower

[enum] EWEffectType:
- SignalDegraded
- SignalDenied
- TargetDecoyed
- CommunicationsDisrupted
- NoEffect

[enum] EPType:
- FrequencyHopping
- SpreadSpectrum
- Encryption
- PowerControl
- DirectionalAntenna
- BurstTransmission

---

# Signal [Data → Sensory]

Signal [facets]:
- center frequency
- frequency range
- bandwidth
- SNR
- line of bearing
- emitter notations (list with confidence)
- pulse width
- pulse repetition interval
- scan characteristics (ScanType, period)

[enum] ScanType:
- Circular
- BidirectionalHorizontalSector
- BidirectionalVerticalSector
- NonScanning
- Irregular
- Conical
- LobeSwitching
- Raster
- CircularVerticalSector
- CircularConical
- SectorConical
- AgileBeam
- UnidirectionalVerticalSector
- UnidirectionalHorizontalSector
- UnidirectionalSector
- BidirectionalSector

---

# Transponder / IFF [Data → Properties]

TransponderCodes [facets]:
- mode 1, mode 2, mode 3 (squawk codes)
- mode 4 interrogation response
- mode 5 (response, code, platform ID)
- mode S (id string, ICAO address)

[enum] InterrogationResponse:
- Correct
- Incorrect
- NoResponse

---

# Provenance [cross-cutting]

Provenance [facets]:
- integration name (source system)
- data type
- source ID
- source update time
- source description

[enum] ProvenanceAction:
- Originated
- Relayed
- Fused
- Transformed
- Enriched
- Filtered

---

# Autonomy [Control → Process]

[enum] BehaviorNodeType:
- Sequence
- Selector
- Parallel
- Condition
- Action
- Decorator
- SubTree

[enum] BehaviorNodeStatus:
- Success
- Failure
- Running

---

# Maintenance [Data → State]

[enum] MaintenanceType:
- Preventive
- Corrective
- Inspection
- Calibration
- SoftwareUpdate
- BatteryReplacement
- PartReplacement

---

# Symbology [Data → Properties]

MilStd2525C [facets]:
- SIDC (symbol identification coding string)

---

# Pipeline Trace: VehicleTelemetry

How a telemetry message carrying position, altitude, attitude,
waypoint, battery, sats, and ground speed builds through the pipeline.

    Ontology (clades):
      Communication → Message → Telemetry
      Data → State → {Location, Kinematic, Resources, Mission}
      Reference → {Frame, Coordinate, Geometry}

    Typology (specialization):
      [enum]     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType
      [variants] Telemetry → VEHICLE: VehicleTelemetry
      [variants] Resources → BATTERY: Battery
      [facets]   LLA needs: lat, lon, altitude, altitude_reference
      [facets]   Location needs: position, altitude, sats, velocity_enu, uncertainty
      [facets]   Kinematic needs: attitude, ground speed, heading, climb rate
      [facets]   Battery needs: voltage, current, remaining pct, temperature
      [facets]   MissionProgress needs: waypoint index, total
      [facets]   VehicleTelemetry needs: location, kinematic, battery, mission

    Schema (definition, in YAML):
      enums:     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType, ...
      structs:   LLA{lat,lon,alt,ref,...} → Location{position,alt,...}
                 Quaternion{x,y,z,w} → Kinematic{attitude,speed,...}
                 Battery{voltage,pct,...} MissionProgress{idx,total}
                 → VehicleTelemetry{location,kinematic,battery,mission}

Each stage consumes the one above. No stage is skipped.
