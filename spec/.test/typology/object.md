# Object

[variants] by class:
- ENTITY: Entity
- ORGANIZATION: Organization
- COLLECTION: Collection
- SYSTEM: System
- SITE: Site
- ITEM: Item

## Collection

[variants] by purpose:
- CONVOY: Convoy
- FORMATION: Formation
- TASK_GROUP: TaskGroup
- SENSOR_NETWORK: SensorNetwork
- TARGET_DECK: TargetDeck
- MINEFIELD: Minefield

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

### Equipment

[variants] by category:
- PERSONAL_WEAPON: PersonalWeapon
- OPTIC: Optic
- COMMS_GEAR: CommunicationsGear
- PROTECTIVE: ProtectiveGear
- NAV_EQUIPMENT: NavigationEquipment
- MUNITION: Munition
- LINK_HARDWARE: LinkHardware

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

