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

