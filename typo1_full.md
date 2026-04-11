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

Indicators [facets]:
- simulated flag
- exercise flag
- emergency flag
- c2 flag
- egressable flag
- starred flag

Override [facets]:
- field path being overridden
- override value
- status (OverrideStatus)
- type (OverrideType)
- expiry time

[enum] OverrideType:
- Live
- PostExpiry

[enum] CorrelationType:
- Manual
- Automated

[enum] CorrelationReplicationMode:
- Local
- Global

Correlation [facets]:
- primary entity
- secondary entities
- correlation type (CorrelationType)
- replication mode (CorrelationReplicationMode)

Decorrelation [facets]:
- decorrelated entity references
- reason
- timestamp

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

[enum] AgentInferenceType:
- Text
- Vision
- Multimodal
- ToolUse
- Code

[enum] AgentSessionState:
- Active
- Suspended
- Terminated

AgentCapability [facets]:
- inference types (AgentInferenceType)
- context capacity
- response latency target

AgentConfiguration [facets]:
- model identifier
- prompt / instruction set reference
- tool manifest
- temperature
- constraints

AgentSession [facets]:
- session identifier
- agent reference
- start time
- token count
- session state (AgentSessionState)

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
- RELAY_STATION: RelayStation
- CHARGING_STATION: ChargingStation
- LAUNCH_PAD: LaunchPad
- RECOVERY_SYSTEM: RecoverySystem
- GCS: GroundControlStation
- COMMAND_POST: MobileCommandPost
- SENSOR_PLATFORM: SensorPlatform
- OPERATOR_STATION: OperatorStation

GroundControlStation [facets]:
- operator station count
- supported protocols
- mobile (bool)

MobileCommandPost [facets]:
- vehicle reference
- communications suite
- battle management system

RelayStation [facets]:
- coverage area
- supported carriers
- gain / amplification

ChargingStation [facets]:
- connector types
- max simultaneous clients
- power output

LaunchPad [facets]:
- supported launch methods
- max vehicle weight
- orientation

RecoverySystem [facets]:
- recovery method
- max vehicle weight
- cycle time

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
- national caveats
- interoperability level
- shared classification ceiling

Team [facets]:
- team identifier
- member entity references
- team lead entity reference
- purpose

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

TaskGroup [facets]:
- task reference
- members
- duration or validity window

SensorNetwork [facets]:
- sensor members
- coverage area
- fusion method

TargetDeck [facets]:
- ordered target references
- target priorities
- engagement status

[enum] MinefieldMarkingStatus:
- Marked
- Unmarked
- Mixed

Minefield [facets]:
- boundary
- mine type
- density
- marking status (MinefieldMarkingStatus)

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

CommunicationSystem [facets]:
- node references
- transport references
- coverage capability

SensorSuite [facets]:
- sensor references
- fusion capability
- primary mode

FireControlSystem [facets]:
- sensor reference
- weapon reference
- tracking mode
- engagement capability

EWSuite [facets]:
- sensors
- jammers
- direction finders
- controller

NavigationSystem [facets]:
- primary source
- backup sources
- accuracy class

C2System [facets]:
- battle management platform
- communications
- displays
- personnel

IntegratedAirDefenseSystem [facets]:
- radars
- launchers
- C2 node
- engagement zones

PowerSystem [facets]:
- sources
- distribution
- total capacity
- current load

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
- ASSAULT_POSITION: AssaultPosition
- BREACH_POINT: BreachPoint
- HLZ: HelicopterLandingZone
- PICKUP_ZONE: PickupZone
- AMMUNITION_SUPPLY_POINT: AmmunitionSupplyPoint
- GRAPHIC_CONTROL_MEASURE: GraphicControlMeasure

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
- response on violation
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

ObservationPost [facets]:
- position
- sector of observation
- manned by

SiteCheckpoint [facets]:
- position
- manning
- purpose

AttackPosition [facets]:
- position
- concealment rating
- sector of fire
- assigned unit or entity

SupportByFirePosition [facets]:
- position
- sector of fire
- weapons emplaced

LineOfDeparture [facets]:
- geometry
- H-hour reference
- unit crossing order

DropZone [facets]:
- boundary
- surface
- approach heading
- wind limits
- marking

AssaultPosition [facets]:
- position
- covered approach
- distance to objective

[enum] BreachMethod:
- Deliberate
- Hasty
- InStride
- Covert

BreachPoint [facets]:
- position
- obstacle type
- breach method (BreachMethod)

HelicopterLandingZone [facets]:
- position
- size
- surface
- obstacles
- approach / departure headings
- marking

PickupZone [facets]:
- position
- size
- surface
- obstacles
- approach / departure headings
- load plan

AmmunitionSupplyPoint [facets]:
- position
- stored supply classes
- security

[enum] GCMType:
- PhaseLine
- ObjectiveArea
- AssemblyArea
- AttackPosition
- SBFPosition
- Boundary
- Checkpoint
- ContactPoint
- CoordinationPoint
- FinalCoordinationLine
- LimitOfAdvance
- FLOT
- FEBA
- MainSupplyRoute
- AlternateSupplyRoute
- Route
- Axis
- DirectionOfAttack
- PassagePoint
- ReleasePoint
- StartPoint
- TriggerLine

GraphicControlMeasure [facets]:
- control measure type (GCMType)
- geometry
- name
- applies to
- effective time

## Item

[variants] by purpose:
- RECORD: Record
- EQUIPMENT: Equipment
- COMPONENT: Component
- PAYLOAD: Payload

### Record
No further speciation yet.

Media [facets]:
- media items (list)
- source entity reference

MediaItem [facets]:
- media type (MediaType)
- URI / reference
- timestamp
- source entity reference
- metadata (resolution, duration, etc.)

[enum] MediaType:
- Image
- Video

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

[enum] OpticType:
- RedDot
- LPVO
- FixedMagnification
- Binoculars
- Rangefinder
- ThermalSight
- NightVision
- LaserDesignator

[enum] ProtGearType:
- BodyArmor
- Helmet
- CBRN_Suit
- EyeProtection
- HearingProtection

[enum] NavEquipType:
- GPS_Receiver
- Compass
- Map
- Altimeter
- DAGR
- PLGR
- ATAK_Device

PersonalWeapon [facets]:
- category (WeaponCategory)
- caliber
- effective range
- rate of fire
- weight

Optic [facets]:
- optic type (OpticType)
- magnification range
- field of view
- night capable

CommunicationsGear [facets]:
- radio type
- frequency range
- power output
- crypto capable
- weight

ProtectiveGear [facets]:
- protection type (ProtGearType)
- protection level

NavigationEquipment [facets]:
- equipment type (NavEquipType)
- accuracy

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

ComponentHealth [facets]:
- component reference
- operational
- hours since maintenance
- hours total
- next maintenance due
- firmware version

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
- CHEMICAL_DETECTOR: ChemicalDetectorPayload
- RADIATION_DETECTOR: RadiationDetectorPayload
- LOUDSPEAKER: LoudspeakerPayload
- LEAFLET: LeafletPayload

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

EOCamera [facets]:
- resolution
- frame rate
- field of view
- zoom range
- stabilized

IRCamera [facets]:
- resolution
- frame rate
- field of view
- zoom range
- stabilized
- palette

MultispectralCamera [facets]:
- resolution
- frame rate
- field of view
- zoom range
- spectral bands

LIDARPayload [facets]:
- range
- points per second
- field of view

SARPayload [facets]:
- resolution
- swath width
- operating modes

CommRelayPayload [facets]:
- supported protocols
- range extension
- added latency

ChemicalDetectorPayload [facets]:
- detectable agent classes
- response time

RadiationDetectorPayload [facets]:
- detectable radiation classes
- dose rate range

LoudspeakerPayload [facets]:
- output power
- intelligibility range

LeafletPayload [facets]:
- payload count
- release mechanism

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

Staleness [facets]:
- age in seconds
- stale threshold

## Type

[enum] PhysicalDomain:
- Land
- Air
- Sea
- Undersea
- Space

[enum] Environment:
- Unknown
- Air
- Surface
- SubSurface
- Land
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

[enum] UnitFunction:
- Maneuver
- FireSupport
- AirDefense
- Aviation
- Engineer
- Signal
- MilitaryIntelligence
- MilitaryPolice
- CBRN
- Logistics
- Medical
- CivilAffairs
- PsyOps
- SOF

[enum] WarfareType:
- Conventional
- Unconventional
- Guerrilla
- Hybrid
- Asymmetric
- Information
- Cyber
- Electronic

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

Heading [facets]:
- value (degrees 0-360)
- reference (BearingReference)

Course [facets]:
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

AzimuthElevation [facets]:
- azimuth
- elevation
- reference (BearingReference)

MagneticDeclination [facets]:
- declination value
- validity date
- location reference

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

Arc [facets]:
- center
- radius
- start angle
- end angle

Annulus [facets]:
- center
- inner radius
- outer radius

Frustum [facets]:
- apex
- direction (AzimuthElevation)
- horizontal field of view
- vertical field of view
- near range
- far range

Sector [facets]:
- center
- radius
- start bearing
- end bearing

OrbitGeometry [facets]:
- center
- radius
- altitude
- direction
- speed

RacetrackGeometry [facets]:
- point A
- point B
- width
- altitude
- direction

CorridorGeometry [facets]:
- centerline
- width
- floor altitude
- ceiling altitude

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

[enum] AccuracyMethod:
- Calculated
- Estimated
- Measured
- Surveyed
- Unknown

CEP [facets]:
- radius
- probability basis

LEP [facets]:
- linear error
- probability basis

SEP [facets]:
- spherical error
- probability basis

DRMS [facets]:
- distance root mean square

PositionAccuracy [facets]:
- horizontal accuracy
- vertical accuracy
- accuracy method (AccuracyMethod)

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

TransformMatrix [facets]:
- 2x2 matrix (TMat2)
- 3x3 matrix (TMat3)
- 4x4 matrix (TMat4f)

### Compact Encodings

CompactPosition [facets]:
- lat (int32 degE7), lon (int32 degE7), alt (int32 cm)

### Orbital Mechanics

OrbitMeanElements [facets]:
- metadata (epoch, theory)
- mean elements (MeanKeplerianElements)
- TLE parameters (optional)

OrbitMeanElementsMetadata [facets]:
- epoch
- mean element theory (MeanElementTheory)

MeanKeplerianElements [facets]:
- semi-major axis
- eccentricity
- inclination
- right ascension
- argument of perigee
- mean anomaly
- mean motion
- eccentric anomaly

TleParameters [facets]:
- line 1 data
- line 2 data
- epoch
- mean motion derivative
- drag term

[enum] MeanElementTheory:
- SGP4

[enum] EciReferenceFrame:
- TEME

### Additional Coordinate / Geometry Shapes

ThetaPhi [facets]:
- theta (azimuth angle)
- phi (elevation angle)

AERPolygon [facets]:
- ordered list of azimuth-elevation-range points

LLAPolygon [facets]:
- ordered list of LLA points (closed ring)

LLAPath [facets]:
- ordered list of LLA
- loop (bool)

### Vector Variants

Vec2 [facets]:
- x, y (float)

Vec2f [facets]:
- x, y (float, explicit)

Vec3 [facets]:
- x, y, z (float)

Vec3f [facets]:
- x, y, z (float, explicit)

YawPitch [facets]:
- yaw, pitch

YPR [facets]:
- yaw, pitch, roll

### Color

Color [facets]:
- red, green, blue, alpha

[enum] MilColor:
- Red
- Blue
- Green
- Yellow
- Orange
- Purple
- White
- Black
- Brown
- Pink

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

[enum] VolumeUnit:
- Liters
- Gallons_US
- Gallons_Imperial
- CubicMeters

[enum] ForceUnit:
- Newtons
- PoundsForce

[enum] PowerUnit:
- Watts
- Kilowatts
- Horsepower

[enum] FrequencyUnit:
- Hertz
- Kilohertz
- Megahertz
- Gigahertz

[enum] DataRateUnit:
- BitsPerSecond
- KilobitsPerSecond
- MegabitsPerSecond
- GigabitsPerSecond

Color [facets]:
- red
- green
- blue
- alpha

[enum] MilColor:
- Red
- Blue
- Green
- Yellow
- Orange
- Purple
- White
- Black
- Brown
- Pink

[enum] MarkerColor:
- Red
- Green
- Yellow
- White
- IR
- Orange
- Violet
- Blue

---

# Control

## Directive

[variants] by kind:
- INTENT: Intent
- OBJECTIVE: Objective
- TASK: Task
- INSTRUCTION: Instruction
- COMMAND: Command

### Intent

[facets]:
- purpose (why)
- key tasks (what must happen)
- end state (what success looks like)

### Objective

[facets]:
- conditions: what must be true for success
- target reference (entity or point)

### Task

A Task has intent, actions, and an objective. It is not
a mode switch or a single command. "Move to area X, hold
presence for 30 minutes, and observe" is a task. "Take off"
is a Command.

[enum] TaskLevel:
- Technical
- Tactical
- Operational
- Strategic

[enum] TaskSubject:
- Maneuver
- ISR
- Effects
- Support
- EW

[variants] by subject:
- MANEUVER: ManeuverTask
- ISR: ISRTask
- EFFECTS: EffectsTask
- SUPPORT: SupportTask
- EW: EWTask

ManeuverTask [variants] by purpose:
- MOVE: MoveTask
- PATROL: PatrolTask
- HOLD: HoldTask
- TRANSIT: TransitTask
- MARSHAL: MarshalTask
- ESCORT: EscortTask
- SET_LAUNCH_ROUTE: SetLaunchRouteTask

ISRTask [variants] by purpose:
- SEARCH: SearchTask
- OBSERVE: ObserveTask
- SURVEY: SurveyTask
- INVESTIGATE: InvestigateTask
- VISUAL_ID: VisualIdTask
- SHADOW: ShadowTask
- MONITOR: MonitorTask
- SCAN: ScanTask
- AREA_SEARCH: AreaSearchTask
- VOLUME_SEARCH: VolumeSearchTask
- IMPROVE_TRACK: ImproveTrackQualityTask
- MAP: MapTask
- BDA: BDATask

EffectsTask [variants] by purpose:
- STRIKE: StrikeTask
- SMACK: SmackTask
- FIRE_MISSION: FireMissionTask
- RELEASE_PAYLOAD: ReleasePayloadTask
- CAS: CloseAirSupportTask

SupportTask [variants] by purpose:
- RELAY: RelayTask
- RESUPPLY: ResupplyMission
- MEDEVAC: MEDEVACMission

EWTask [variants] by purpose:
- EW_ACTION: EWActionTask

[facets] all Tasks:
- physical domain (PhysicalDomain)
- combat domain (CombatDomain, optional; absent for non-combat tasks)
- operational sphere (OpDomain)
- level (TaskLevel)
- subject (TaskSubject)
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

StrikeParameters [facets]:
- target reference
- weapon payload reference
- release constraints
- engagement parameters

StrikeReleaseConstraint [facets]:
- release authority
- release conditions
- abort conditions

PayloadConfiguration [facets]:
- payload reference
- operational state
- configuration parameters

ReleasePayload [facets]:
- payload configuration
- release conditions

DeliveryState [facets]:
- delivery status (DeliveryStatus)
- delivery error code (DeliveryErrorCode)
- delivery constraints

DeliveryConstraints [facets]:
- timeout
- retry strategy
- delivery deadline

RetryStrategy [facets]:
- max retries
- retry delay
- backoff multiplier

[enum] DeliveryStatus:
- Delivered
- PendingExecute
- PendingCancel
- PendingComplete

[enum] DeliveryErrorCode:
- Unavailable
- Timeout
- Rejected

Not tasks:
- Takeoff, Land, RTL, Arm, Disarm, SetMode → Commands
- Gimbal point / zoom / stow / track / recenter → GimbalCommand or CameraCommand
- Orbit, loiter patterns → Sequences
- Track → method of observation, or sub-type of Observe

### Instruction

[variants] by subject:
- MOVEMENT: MovementInstruction
- COLLECTION: CollectionInstruction
- EFFECTS: EffectsInstruction
- SUPPORT: SupportInstruction
- EW: EWInstruction

[facets] all Instructions:
- task reference (optional)
- prescribed method / procedure
- execution parameters
- control measures
- trigger or start condition
- termination condition

[enum] InstructionProductType:
- StandingOrder
- SOP
- WARNO
- FRAGO

InstructionProduct [facets]:
- instruction product type (InstructionProductType)
- issuing authority
- applies to
- effective time
- version or order number

### Command
Directs or controls immediately.

[variants] by target:
- FLIGHT: FlightCommand
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

[enum] OODACycle:
- Observe
- Orient
- Decide
- Act

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

FlightCommand [variants] by action:
- ARM: ArmCommand
- DISARM: DisarmCommand
- TAKEOFF: TakeoffCommand
- LAND: LandCommand
- RTL: ReturnToLaunchCommand
- SET_TAKEOFF_ALTITUDE: SetTakeoffAltitudeCommand

SetTakeoffAltitudeCommand [facets]:
- target altitude

NavigationCommand [variants] by action:
- GO_TO: GoToCommand
- SET_WAYPOINT: SetWaypointCommand
- SELECT_MISSION: SelectMissionCommand

[enum] WaypointActionType:
- Transit
- Flyover
- Flyby
- Takeoff
- Land
- Loiter
- Orbit
- Hold
- ReturnToLaunch
- PayloadAction
- SensorAction
- Photo
- Survey
- Delivery
- Relay
- Rendezvous
- Custom

GoToCommand [facets]:
- destination position
- target altitude
- target yaw

SetWaypointCommand [facets]:
- sequence index
- waypoint action (WaypointActionType)
- destination position
- target altitude
- action parameters
- flags

SelectMissionCommand [facets]:
- mission sequence index

ModeCommand [variants] by action:
- SET_MODE: SetModeCommand

SetModeCommand [facets]:
- mode identifier
- enabled state

## Execution

[variants] by kind:
- PLAN: Plan
- SEQUENCE: Sequence
- ACTION: Action

### Plan

Plan [facets]:
- fulfills task reference
- phases
- ordered instructions
- assignments
- timing / trigger structure
- branches and sequels
- coordination / deconfliction measures
- go / no-go or abort criteria

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

ObstaclePlan [facets]:
- planned obstacles
- breach plan

BranchPlan [facets]:
- parent plan reference
- trigger condition
- actions on branch
- probability assessment

SequelPlan [facets]:
- follows plan reference
- transition conditions
- sequel actions

### Sequence

Sequence [facets]:
- implements instruction reference
- ordered commands
- trigger conditions
- transition conditions
- timing / dwell / duration
- path / waypoint chain
- sensor, payload, and mode changes bound to steps

[variants] by procedure:
- ROUTE: RouteSequence
- SEARCH: SearchSequence
- ORBIT: OrbitSequence
- ATTACK: AttackSequence
- BREACH: BreachSequence

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

[enum] MovementRate:
- Normal
- Deliberate
- Hasty
- Forced
- Administrative

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

[enum] DefenseType:
- AreaDefense
- MobileDefense
- Retrograde
- Delay
- Withdrawal
- Retirement

[enum] RouteSegmentType:
- GreatCircle
- Rhumbline
- Straight
- TurnArc
- Orbit
- Hold
- Approach
- Departure
- Missed
- Emergency

RouteSegment [facets]:
- route segment type (RouteSegmentType)
- start point
- end point
- altitude constraint
- speed constraint
- turn radius
- direction

Waypoint [facets]:
- position (LLA)
- altitude constraint (optional)
- speed constraint (optional)
- action (WaypointActionType)
- action parameters
- dwell time (optional)

Route [facets]:
- ordered waypoints
- constraints (area, altitude)
- launch tracking mode

PathSegment [facets]:
- start waypoint
- end waypoint
- constraints

[enum] LaunchTrackingMode:
- GoToWaypoint
- TrackToWaypoint

[enum] LoiterType:
- Orbit
- Racetrack
- FigureEight
- Hold

[enum] OrbitDuration:
- UntilCommanded
- FixedTime
- FuelBased

ISRParameters [facets]:
- loiter type (LoiterType)
- loiter duration (OrbitDuration)
- orbit direction (OrbitDirection)
- orbit pattern (OrbitPattern)
- gimbal point
- zoom settings
- scan parameters

GimbalPoint [facets]:
- target entity reference (optional)
- target position reference (optional)
- azimuth-elevation point (optional)
- frame point (optional)

AzimuthElevationPoint [facets]:
- azimuth
- elevation

FramePoint [facets]:
- frame reference
- x offset
- y offset

GimbalZoom [facets]:
- zoom level
- field of view

AreaConstraints [facets]:
- minimum altitude
- maximum altitude
- boundary geometry

AltitudeConstraint [facets]:
- minimum altitude
- maximum altitude
- reference datum

AnglePair [facets]:
- minimum angle
- maximum angle

### Action

Action [facets]:
- resolves command reference
- description
- executor
- resulting state change or effect
- status (LifecyclePhase)

## Constraint

[variants] by kind:
- RESTRICTION: Restriction
- LIMITATION: Limitation
- CONDITION: Condition

### Restriction

[variants] by domain:
- ROE: RulesOfEngagement
- EMCON: EMCONPolicy

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

### Limitation

[variants] by domain:
- DECONFLICTION: DeconflictionRule
- AIRSPACE: AirspaceControlOrder
- WEATHER_LIMIT: WeatherLimits
- FLIGHT_RESTRICTION: FlightRestriction

[enum] DeconflictionType:
- Altitude
- Temporal
- Lateral
- Speed
- Route
- Frequency

### Condition

[variants] by purpose:
- ABORT: AbortCriteria
- TRIGGER: TriggerCondition
- CONDITIONAL_EXECUTION: ConditionalExecution

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

[enum] TriggerType:
- TimeReached
- PositionReached
- EventOccurred
- ThresholdExceeded
- ConditionMet
- OrderReceived
- EnemyAction
- FriendlyAction

TriggerCondition [facets]:
- trigger type
- parameters
- evaluation method

ConditionalExecution [facets]:
- condition
- if true
- if false (optional)

## Interface
The translation of an action into the terms of the executing layer.

[variants] by type:
- PWM: PWMInterface
- GPIO: GPIOInterface
- CAN: CANInterface
- SERIAL: SerialInterface
- RC: RCInterface

[enum] InterfaceType:
- PWM — servo/ESC
- GPIO
- CAN — CAN bus
- Serial — serial actuator command
- RC — RC channel override

PWMInterface [facets]:
- channel
- min, center, max range
- function

GPIOInterface [facets]:
- pin
- polarity / mode

CANInterface [facets]:
- arbitration id
- data length
- bus address

SerialInterface [facets]:
- baud, parity, stop bits, data bits
- command bytes

RCInterface [facets]:
- channels
- mapping
- range / calibration

---

# Communication

## Node
Endpoint that transmits or receives.
An Entity can have multiple Nodes. Each Node has its own Transport(s).
Binding: Entity → Node → Transport.

[facets]:
- entity reference (what Entity this node belongs to)
- node capabilities

[enum] NodeType:
- Sensor
- Effector
- C2
- Relay
- Gateway
- Observer
- All

NodeCapabilities [facets]:
- can transmit
- can receive
- can relay
- can process

NetworkInterface [facets]:
- node reference
- carrier reference
- address
- port
- state

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

[enum] MeshRoutingProtocol:
- AODV
- OLSR
- Babel
- Batman
- Custom

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

[enum] DataLinkType:
- CDL
- TCDL
- SADL
- Link16
- Link22
- JREAP
- BACN
- BLOS
- DAMA
- HaveQuick
- SINCGARS
- ARC_210

### Protocol

[enum] ProtocolType:
- MAVLink
- MAVLink_M
- MSPv2
- ROS
- STANAG4586
- CoT
- CustomSerial
- Meshtastic
- RTP_RTSP
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
- Avro
- BSON
- Binary_Custom
- ASCII_Text

[enum] CompressionType:
- None
- GZIP
- LZ4
- Zstd
- Snappy
- Deflate

[enum] Endianness:
- LittleEndian
- BigEndian
- NetworkOrder

[enum] QoSReliability:
- BestEffort
- AtLeastOnce
- ExactlyOnce
- Guaranteed

[enum] RoutingMode:
- Unicast
- Multicast
- Broadcast
- Anycast
- PubSub
- RequestReply
- StoreAndForward

QoS [facets]:
- max latency
- minimum bandwidth
- reliability (QoSReliability)
- priority

Topic [facets]:
- namespace
- name

Subscription [facets]:
- subscriber
- topic
- filter
- QoS

COMSEC [facets]:
- encryption algorithm
- key material reference
- key changeover schedule

TRANSEC [facets]:
- frequency hopping set
- hop rate
- synchronization method

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

SensorStream [facets]:
- stream purpose
- encoding
- transport
- source entity

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

MessageClassification [facets]:
- classification level
- caveats
- releasability

MessageEnvelope [facets]:
- message identifier
- timestamp
- source node
- destination nodes
- priority
- classification
- TTL
- sequence number
- correlation identifier
- retry count
- acknowledgment policy

DeliveryReceipt [facets]:
- message identifier
- receiving node
- received time
- receipt status

TransmissionResult [facets]:
- target count
- bytes sent

[variants] by purpose:
- COMMAND: Command
- TELEMETRY: Telemetry
- OBSERVATION: Observation
- RESPONSE: Response

### Command
Directs or controls.

[variants] by target:
- FLIGHT: FlightCommand
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

[enum] OODACycle:
- Observe
- Orient
- Decide
- Act

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

FlightCommand [variants] by action:
- ARM: ArmCommand
- DISARM: DisarmCommand
- TAKEOFF: TakeoffCommand
- LAND: LandCommand
- RTL: ReturnToLaunchCommand
- SET_TAKEOFF_ALTITUDE: SetTakeoffAltitudeCommand

SetTakeoffAltitudeCommand [facets]:
- target altitude

NavigationCommand [variants] by action:
- GO_TO: GoToCommand
- SET_WAYPOINT: SetWaypointCommand
- SELECT_MISSION: SelectMissionCommand

[enum] WaypointActionType:
- Transit
- Flyover
- Flyby
- Takeoff
- Land
- Loiter
- Orbit
- Hold
- ReturnToLaunch
- PayloadAction
- SensorAction
- Photo
- Survey
- Delivery
- Relay
- Rendezvous
- Custom

GoToCommand [facets]:
- destination position
- target altitude
- target yaw

SetWaypointCommand [facets]:
- sequence index
- waypoint action (WaypointActionType)
- destination position
- target altitude
- action parameters
- flags

SelectMissionCommand [facets]:
- mission sequence index

ModeCommand [variants] by action:
- SET_MODE: SetModeCommand

SetModeCommand [facets]:
- mode identifier
- enabled state

### Telemetry
Reports the sender's own internal state.
Composes State data by reference — does not flatten fields.

[variants] by scope:
- UAV: UAVTelemetry

UAVTelemetry [facets]:
- location (Location) — position, altitude, fix quality, satellite count, uncertainty, home/global validity
- navigation state (Navigation) — nav mode, source selection, fix source, validity, GNSS diagnostic statistics
- kinematic state (Kinematic) — attitude, angular rates, ground speed, ground course, airspeed, climb rate, heading, throttle
- sensor state (Sensor) — IMU sample, sensor readiness, calibration / availability state
- input state (Input) — RC channels, receiver config, channel map, mode ranges
- resource state (Battery, Fuel, Consumable as applicable) — battery / analog power telemetry, remaining, consumed, temperature
- parameters (Robot Parameters) — flight mode, armed, in-air, active modes, override active, failsafe state
- internal state (Internal) — FC connectivity, CPU load, cycle time, software / board / build identity
- condition (Condition) — sensor readiness, armable status, fault / warning indicators
- mission progress (MissionProgress) — current waypoint, total waypoints, mission validity

### Observation
Reports external objects, events, or environment.
Carries Intel data (Detection, Classification, Track).

CoTEvent [facets]:
- UID
- CoT type
- production method
- callsign
- event time
- start time
- stale time
- geographic position
- CE
- LE
- detail XML
- source host
- source port
- targets

MarkerMessage [facets]:
- UID
- callsign
- marker CoT type
- geographic position
- CE
- LE
- stale period
- targets

GeoChatMessage [facets]:
- UID
- message text
- sender callsign
- recipient team
- geographic position
- CE
- LE
- targets

ParseErrorMessage [facets]:
- error text

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

Heartbeat [facets]:
- node reference
- timestamp
- uptime
- status summary
- interval configuration

HeartbeatConfig [facets]:
- interval
- timeout
- jitter

[enum] ScheduleType:
- ZoneEnabled
- ZoneTempEnabled

Schedule [facets]:
- schedule type (ScheduleType)
- cron windows
- enabled state
- validity window

CronWindow [facets]:
- cron expression
- timezone
- active from
- active until

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

SupplyRequest [facets]:
- requested supply classes or items
- requested quantities
- destination
- required by time
- requesting unit

SupplyRoute [facets]:
- route geometry
- supported load classes
- threat level
- availability window

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

PersonnelStatus [facets]:
- personnel status type
- effective time
- duty state

CasualtyReport [facets]:
- casualty cause
- injury severity
- treatment status
- evacuation status

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

MEDEVACRequest [facets]:
- pickup zone
- patient precedence
- special equipment
- security at pickup
- marking method
- contamination state

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

CallForFire [facets]:
- target reference or position
- engagement method
- requested munition
- fire type
- observer

FireMission [facets]:
- target reference
- engagement method
- weapon type
- ammunition type
- mission status

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

EWAction [facets]:
- EW action type
- target emitter or band
- start condition
- stop condition

DirectionFindingResult [facets]:
- emitter reference
- line of bearing
- confidence

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

PathLoss [facets]:
- frequency
- distance
- environment

LinkMargin [facets]:
- link budget reference
- actual SNR
- required SNR
- margin
- link quality

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

[enum] PermissionLevel:
- None
- Read
- Write
- Execute
- Admin
- Owner

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

[enum] AuditAction:
- Created
- Updated
- Deleted
- Accessed
- Shared
- Classified
- Declassified
- Approved
- Denied
- Exported
- Imported

Notification [facets]:
- notification type
- severity
- subject reference
- message
- timestamp
- acknowledged

[enum] NotificationType:
- Alert
- StatusChange
- TaskUpdate
- Threshold
- Geofence
- CommLoss
- BatteryLow
- MissionComplete
- Hostile
- Emergency

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

MaintenanceAction [facets]:
- maintenance type
- entity reference
- component reference
- scheduled time
- completed time
- performed by
- notes

---

# Symbology [Data → Properties]

MilStd2525C [facets]:
- SIDC (symbol identification coding string)

[enum] Severity:
- Info
- Low
- Medium
- High
- Critical
- Emergency

[enum] GeofenceResponse:
- None
- Report
- Warn
- Loiter
- RTL
- Land
- Brake
- MissionPause
- Fence

[enum] FailsafeType:
- RCLost
- DataLinkLost
- BatteryLow
- BatteryCritical
- GPSLost
- GeofenceBreach
- MotorFailure
- IMUFailure
- BarometerFailure
- TerrainFollowLost
- MissionInvalid
- CommunicationLost
- HighWind
- Crash

GimbalState [facets]:
- current azimuth
- current elevation
- current horizontal field of view
- current vertical field of view
- stabilized
- mode
- tracking entity reference

CameraState [facets]:
- recording
- photos taken
- storage remaining percentage
- current zoom
- current field of view
- resolution
- frame rate

SequenceGap [facets]:
- source reference
- expected sequence
- received sequence
- gap count
- detection time

CompressionPolicy [facets]:
- algorithm
- compression level
- minimum message size

CompactTelemetry [facets]:
- short entity identifier
- compact position
- heading
- speed
- battery percentage
- status flags

---

# Pipeline Trace: UAVTelemetry

How a telemetry message carrying position, altitude, attitude,
waypoint, battery, sats, and ground speed builds through the pipeline.

    Ontology (clades):
      Communication → Message → Telemetry
      Data → State → {Location, Kinematic, Resources, Mission}
      Reference → {Frame, Coordinate, Geometry}

    Typology (specialization):
      [enum]     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType
      [variants] Telemetry → UAV: UAVTelemetry
      [variants] Resources → BATTERY: Battery
      [facets]   LLA needs: lat, lon, altitude, altitude_reference
      [facets]   Location needs: position, altitude, sats, velocity_enu, uncertainty
      [facets]   Kinematic needs: attitude, ground speed, heading, climb rate
      [facets]   Battery needs: voltage, current, remaining pct, temperature
      [facets]   MissionProgress needs: waypoint index, total
      [facets]   UAVTelemetry needs: location, kinematic, battery, mission

    Schema (definition, in YAML):
      enums:     AltitudeReference, GlobalFrame, CoordinateEncoding, GPSFixType, ...
      structs:   LLA{lat,lon,alt,ref,...} → Location{position,alt,...}
                 Quaternion{x,y,z,w} → Kinematic{attitude,speed,...}
                 Battery{voltage,pct,...} MissionProgress{idx,total}
                 → UAVTelemetry{location,kinematic,battery,mission}

Each stage consumes the one above. No stage is skipped.
