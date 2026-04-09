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

