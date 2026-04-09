# CONCEPTS — Raw Concept Dump

Everything found across HiveOS, Sigma SDK, ConstellationOverwatch, Lattice, CoT/TAK, frogcnclib, BMS planner, HiveLink notes, and MAVLink-M. Organized loosely by ontology root. Not structured into final typology yet — this is the pile.

Source key: `[HV]` HiveOS, `[HL]` HiveLink, `[SG]` Sigma SDK, `[CO]` ConstellationOverwatch, `[LA]` Lattice, `[CT]` CoT/TAK, `[FC]` frogcnclib, `[BM]` BMS planner, `[ML]` MAVLink-M

---

# OBJECT

## Entity

### Actor
- Person [LA: User principal, FC: commander field, CT: operator]
- Agent [LA: Agent in task system, SG: Agent actor variant]
- AI agent as commander [FC: commander = "AI"]
- Commander role [LA: Status.role = "Commander", "Team Member"]
- Platform activity as role descriptor [LA: Status.platform_activity = "RECONNAISSANCE", "INTERDICTION", "RTB", "PREPARING FOR LAUNCH"]

### Machine
- Vehicle [SG: Vehicle variant, CO: GROUND_VEHICLE_WHEELED, GROUND_VEHICLE_TRACKED]
- Robot [SG: Robot variant with autonomy field]
  - AirRobot / UAV / UAS [CO: AIRCRAFT_FIXED_WING, AIRCRAFT_MULTIROTOR, AIRCRAFT_VTOL, AIRCRAFT_HELICOPTER, AIRCRAFT_AIRSHIP]
  - LandRobot / UGV
  - SeaRobot / USV [CO: SURFACE_VESSEL_USV]
  - SubseaRobot / UUV [CO: UNDERWATER_VEHICLE]
  - SpaceRobot
- Platform [SG: Platform variant]
  - Launcher [FC: has_launchers, launcher field]
  - Charger
  - Relay
  - SensorPlatform [CO: SENSOR_PLATFORM]
  - PayloadSystem [CO: PAYLOAD_SYSTEM]
  - OperatorStation [CO: OPERATOR_STATION]
  - RemoteWeaponSystem [ML: RWS with pose, arming state, weapon type]

Machine domains: Land, Air, Sea, Undersea, Space [SG: MachineDomain, LA: Environment enum]

Land propulsion: Wheeled, Tracked, Bipedal, Legged [SG: LandPropulsion]

Autonomy levels: Remote, Assisted, SemiAutonomous, Supervised, Autonomous [SG: AutonomyClass]

Machine model/specs (from FC/AirUnitSchema):
- model, type, serial_uid
- propulsion type
- reusable (bool)
- has_warhead, warhead type
- pylons, pylon_format
- flight_type (fixed_wing, multirotor, vtol, etc.)
- launch_domain, effect_domain
- rc_link, vid_link, ctrl_video_sep
- guidance type
- navigation type, navaids
- autopilot, autopilot_model, autopilot_fw
- fuel_type, fuel_config, fuel_consumption
- control_modes (list)
- max_range, max_flight_time, max_speed, cruise_speed, max_altitude
- start_flight_time
- maintenance_status
- weather_limits (IFR, rain, snow, temp range, wind, vis, icing)
- roles (list of AirRole)
- attack_modes

Air roles [FC: AirRole enum]:
- Ground Attack (G)
- Anti-Air/Air Defense (AA)
- Fighter (F)
- Reconnaissance (R)
- IMINT (I)
- SIGINT (S)
- Minelaying (L)
- Cargo (C)

Ground unit specifics (FC/GroundUnitSchema):
- model, role, serial_uid
- propulsion, max_range, max_speed
- has_launchers, attack_modes, pylons
- navigation, navaids
- control_modes

Machine dimensions [LA: Dimensions — physical dimensions of the entity]

Machine indicators [LA: Indicators]:
- simulated (bool) — entity is from a simulation
- exercise (bool) — entity is part of an exercise
- emergency (bool)
- c2 (bool) — entity is a C2 node
- egressable (bool) — should be shared to external systems
- starred (bool) — arbitrary importance flag

### Organization
- Group (contains subordinate orgs) [SG: Group variant]
- Unit (leaf org, entities only) [SG: Unit variant]
- Fleet [CO: Fleet — id, name, org_id, swarm_ids, status]
- Swarm [CO: Swarm — id, name, org_id, fleet_id, entity_ids, type/role]
- Team [LA: Team in GroupDetails]
- Echelon [LA: ArmyEchelon — fire_team through army]

Organization types: Military, Civilian, Commercial, NGO [CO: OrgType]

Organization hierarchy (FC):
- parent, parent_num
- grandparent, grandparent_num
- attached, attached_to
- attachments (non-integral)
- tac_elements, sup_elements (tactical/support sub-elements)
- tac_e_comp, sup_e_comp (composition counts)
- levels_up, orglevel, sizelevel

Unit sizes — ground [FC: UnitSize enum]:
- IND (Individual), TEM (Team), SQD (Squad), SEC (Section), PLT (Platoon)
- COY (Company), BTN (Battalion), RGT (Regiment), BDE (Brigade), DIV (Division)

Unit sizes — air [FC: UnitSize enum]:
- FLT (Flight), SQN (Squadron), GRP (Group), WNG (Wing)

Echelon levels [LA: ArmyEchelon]:
- FIRE_TEAM, SQUAD, PLATOON, COMPANY, BATTALION, REGIMENT, BRIGADE, DIVISION, CORPS, ARMY

Unit power model (FC): 2^n from Individual(1) to Division(256)

Unit categories [FC: UnitCategory enum, 33 types]:
- COMB (Combined Arms), BATT (Battery), TF (Task Force)
- MECH (Mechanized Infantry), INF (Light Infantry), MOT (Motorized Infantry)
- REC (Reconnaissance), UAV (Unmanned Aerial Systems), UAVA (UAV Attack), UAVR (UAV Recon)
- UGV (Unmanned Ground Systems)
- SIG (Signal), ENG (Engineer)
- ART (Artillery), MORT (Mortar), MRL (Rocket Artillery)
- ARM (Armored), CAV (Cavalry)
- MED (Medical), SUP (Supply), LOG (Logistics)
- HQ (Headquarters), NBC (CBRN Defense), MP (Military Police)
- AIR (Airborne Infantry), SOF (Special Operations Forces)
- NAV (Naval Infantry), AMP (Amphibious Infantry)
- ADA (Air Defense Artillery), EW (Electronic Warfare)
- ISR (Intelligence, Surveillance, and Reconnaissance)
- CBT (Combat Support), CSS (Combat Service Support)
- COM (Command), DET (Detachment), RES (Reserve), TRG (Training)

Taskforce flag changes classification [FC: taskforce bool]

Organization composition aggregation (FC):
- get_orbat: recursive aggregation of personnel, infantry, vehicles, weapons, air_units
- get_uav_orbat: recursive aggregation of air_units and links
- Centroid computation from unit positions

### Collection
- No further speciation found yet

### System
- No further speciation found yet

### Site
- Waypoint [CO: WAYPOINT, CT: b-m-p-w, LA: Waypoint in RoutePlan]
- ControlPoint [CT: b-m-p-c route control point]
- NoFlyZone [CO: NO_FLY_ZONE]
- Geofence [CO: GEOFENCE, CT: geofence schema with elevation monitoring, trigger, tracking, bounding sphere, min/max elevation]
- ControlArea [LA: ControlArea — KEEP_IN_ZONE, KEEP_OUT_ZONE, DITCH_ZONE, LOITER_ZONE]
- LandingZone [LA: ACM_DETAIL_TYPE_LANDING_ZONE]
- Bullseye [LA: GEO_TYPE_BULLSEYE, CT: bullseye schema]
- EngagementZone [LA: GEO_TYPE_ENGAGEMENT_ZONE]
- HazardArea [LA: GEO_TYPE_HAZARD]
- EmergencyArea [LA: GEO_TYPE_EMERGENCY]
- GeoGeneral [LA: GEO_TYPE_GENERAL]
- ACM (Airspace Coordinating Measure) [LA: GEO_TYPE_ACM with ACMDetails]
- AssemblyPoint [BM: assembly point with azimuth, distance]
- IngressPoint [BM: ingress with dist, azimuth, alt, airspeed]
- EgressPoint [BM: egress with alt, dist, azimuth, airspeed]
- InitialPoint [BM: IP with distance from target]
- ReleasePoint [from Skynet notes: release point in mission planning]
- TargetSet [ML: TARGET_SET_COORD — circular area grouping targets with validity window]
- TargetBox [ML: TARGET_BOX_COORD — quadrilateral target area, four WGS84 corners]
- SpatialFeature [FC: spatial_feature — name, uid, domain, status, category (object/topography/landmark/polygon), type (bridge/building/base), cot, sidc, position, polygon]

### Item
- Record [SG: Record variant]
- Equipment [SG: Equipment variant]
- Component [SG: Component variant]
- Payload [SG: Payload variant, LA: Payload with operational state, PayloadConfiguration]
  - PayloadOperationalState: Off, NonOperational, Degraded, Operational, OutOfService, Unknown [LA]
- Sensor [LA: Sensor with type, mode, FoV, RF config; FC: SensorSchema]
  - SensorType: Radar, Camera, Transponder, RF, GPS, PTU_Pos, Perimeter, Sonar [LA]
  - SensorMode: Search, Track, WeaponSupport, Auto, Mute [LA]
  - OperationalState: Off, NonOperational, Degraded, Operational, Denied [LA]
- Munition [LA: Munition in Supplies, ML: ESAD with munition_status]
  - MunitionStatus: NotPresent, Present, Ready, Fault [ML: MAVLINK_M_ESAD_MUNITION_STATUS]
- Weapon [ML: RWS_STATE — weapon_string, weapon_type, arming_state]
- Link hardware (FC/LinkSchema):
  - uuid, name, link_type, net_type, io, data_type, rxtx
  - bands, waveform, bandwidth, speed
  - user_capacity, freq_set, ch, ch_set
  - crypto_type, crypto_set, crypto_keys
  - net_set, ip
- ESAD (Electronic Safe and Arm Device) [ML: arming, munition, ignition states, fault flags, challenge hash auth]

---

# REFERENCE

## Frame
Local 2D: LU, LD, RU, RD
Local 3D: FRD, FLU, NED, ENU [LA: ENU type, ML: NED in target coords]
Global Geodetic: WGS84, ETRS89
Global EarthFixed: ECEF
Global Orbital: ECI, TEME, LVLH [LA: ECI, TEME reference frames]
Altitude references: AMSL (MSL), HAE (WGS84), Barometric, StartRelative, HAAT [LA: ALTITUDE_REFERENCE enum, CO: altitude_msl, altitude_relative, altitude_terrain]
Lattice altitude references [LA: AltitudeReference]:
- HEIGHT_ABOVE_WGS84 (HAE)
- HEIGHT_ABOVE_EGM96 (geoid)
- UNKNOWN
- BAROMETRIC
- ABOVE_SEA_FLOOR
- BELOW_SEA_SURFACE
MAV_FRAME [ML: coordinate_frame enum on RWS_POSE]

## Coordinate
- LatLonAlt (lat, lon, alt) [everywhere — HV, CO, CT, LA, FC, BM]
  - Lattice Position: lat_degrees, lon_degrees, altitude_hae_meters, altitude_agl_meters, altitude_asf_meters, pressure_depth_meters [LA: 4 altitude refs]
  - CoT EventPoint: lat, lon, hae, ce (circular error), le (linear error) on WGS-84 [CT]
  - HiveOS: LatDeg, LonDeg, AbsAltM, RelAltM [HV]
  - CO GlobalPosition: lat, lon, altitude_msl, altitude_relative, altitude_terrain, accuracy_h, accuracy_v [CO]
  - degE7 encoding (int32 scaled by 1e7) [ML: lat/lon in MAVLink messages]
- Cartesian XYZ [CO: LocalPosition x,y,z, LA: Vec3]
- MGRS (zone, band, easting, northing) [from Russian F2T2EA: 18W298732 7832232]
- UTM (zone, band, easting, northing)
- PlusCode (str)
- LLA [LA: LLA type with altitude_reference]
- ECI [LA: ECI type]
- ENU [LA: ENU type — used for velocity, acceleration in entity location]
- Spherical [LA: Spherical type]
- ThetaPhi [LA: angles]

## Geometry
- Vector2D (x, y) [LA: Vec2, Vec2f]
- Vector3D (x, y, z) [LA: Vec3, Vec3f]
- Line2D (start, stop)
- Line3D (start, stop)
- Path2D: list[Vector2D]
- Path3D: list[Vector3D]
- Quaternion (x, y, z, w) [LA: Quaternion, CO: QuaternionAttitude q1-q4]
- EulerAngles / YPR (yaw, pitch, roll) [LA: YPR, YawPitch, CO: EulerAttitude roll/pitch/yaw]
- Pose [LA: Pose type — position + orientation quaternion, body-to-ENU transform]
- RigidTransform [LA: RigidTransform]
- TMat2, TMat3, TMat4f [LA: transformation matrices]
- TMat3 symmetric upper triangle (mxx, mxy, mxz, myy, myz, mzz) [LA: for covariance matrices]
- BoundingBox (x1, y1, x2, y2) [CO: BoundingBox]
- GeoPoint [LA: GeoPoint]
- GeoLine [LA: GeoLine]
- GeoPolygon [LA: GeoPolygon, LinearRing]
- GeoEllipse [LA: GeoEllipse]
- GeoEllipsoid [LA: GeoEllipsoid]
- LLAPolygon [LA: LLAPolygon]
- LLAPath [LA: LLAPath]
- AERPolygon [LA: AERPolygon]
- ErrorEllipse [LA: ErrorEllipse — position uncertainty probability ellipse]
- Circle [CT: circle schema]
- Rectangle [CT: rectangle schema]
- Freeform shape [CT: freeform schema]
- ShapeEllipse [CT: ellipse in geofence shape]
- ShapeLink [CT: link in geofence shape]
- AreaOfOperations [FC: shape, points, size]
- CylindricalVolume [CT: EventPoint CE+LE define a cylinder around a point]

## Time
- Timestamp (int64 / unix epoch) [everywhere]
- Timestamp microseconds (uint64 usec) [ML: time_usec field on all MAVLink-M messages]
- Duration
- TimeRange [LA: TimeRange in task queries — update_start_time, update_end_time]
- DurationRange [LA: DurationRange]
- CronWindow [LA: CronWindow — cron_expression, duration_millis]
- StaleTime [CT: stale attribute on CoT events — expiry of information validity]
- DTG (Date-Time Group, military format)
- ValidityWindow [ML: time_start, time_end on target sets — area/info validity period]
- Epoch [SG: Epoch with offset_s from Unix epoch]

## Type — Enums and Classifications

### Physical Domain
Land, Air, Sea, Undersea, Space [SG, LA: Environment enum]
LA Environment values: UNKNOWN, AIR, SURFACE, SUB_SURFACE, LAND, SPACE

### Combat Domain
Combat, CombatSupport, CombatSupportService

### Operational Domain
Land, Air, Sea, Undersea, Space, Radio, Psychological, Cyber

### Faction / Disposition
UNKNOWN, PENDING, FRIENDLY, SUSPECT, HOSTILE, NEUTRAL, ASSUMED, FAKER, JOKER [SG: Faction]
Lattice: DISPOSITION_UNKNOWN, FRIENDLY, HOSTILE, SUSPICIOUS, ASSUMED_FRIENDLY, NEUTRAL, PENDING
CoT maps: a-f- (friendly), a-h- (hostile), a-u- (unknown), a-n- (neutral), a-s- (suspect), a-j- (joker), a-k- (faker)
MAVLink-M: UNKNOWN, NEUTRAL, FRIENDLY, FOE, EXTRATERRESTRIAL [ML: TARGET_FORCE]

### Nationality
Full ISO-style country list [LA: Nationality enum, 100+ countries including NATO, UN, International Red Cross]

### Classification (security)
UNCLASSIFIED, CONTROLLED_UNCLASSIFIED, CONFIDENTIAL, SECRET, TOP_SECRET [LA: ClassificationLevels]
Per-field classification [LA: FieldClassificationInformation]

### MilStd2525 / SIDC
Symbol identification codes [LA: MilStd2525C, Symbology; FC: sidc field; CT: marker2525 schema]
CoT type hierarchy: a-{faction}-{domain}-{category}-... [CT: full type tree]

### Entity Status
ACTIVE, INACTIVE, UNKNOWN, OFFLINE, ONLINE [CO: EntityStatus]
Present, Damaged, Destroyed, Lost, Decoy/Fake [FC: status field]

### Priority
LOW, NORMAL, HIGH, CRITICAL [CO: PriorityLevel]

### Event Types
CREATED, UPDATED, DELETED, STATUS_CHANGED, ALERT [CO: EventType]
LA entity: EVENT_TYPE_CREATED, UPDATE, DELETED, PREEXISTING, POST_EXPIRY_OVERRIDE
LA task: EVENT_TYPE_CREATED, UPDATE, PREEXISTING

### Entity Types (CoT top-level)
- a: Atom (physical thing with position)
  - a-.-A: Air track
  - a-.-G: Ground track
  - a-.-S: Sea surface
  - a-.-U: Subsurface
  - a-.-P: Space
- b: Bits (information/data)
  - b-i: Image
  - b-m-r: Route
  - b-m-p: Map point (targeted, waypoint, click, SPI, VPOI)
  - b-m-p-c: Control point
  - b-m-p-w: Waypoint
  - b-m-g-o: Grid
  - b-d: Detection (acoustic, motion, seismic, radiation, CBRNE, launch, impact)
  - b-l: Alarm (CBRNE, environmental, fire)
- c: Capability
  - c-c: Communications
  - c-f: Fires (direct, indirect)
  - c-l: Logistics/supply (fuel)
  - c-r: Rescue
  - c-s: Surveillance
- t: Tasking
  - t-a: Air (CAS, air drop, EW, strike, recovery, SEAD)
  - t-k: Strike (destroy, investigate, target)
  - t-m: Mensurate
  - t-s: ISR (BFT, imagery EO/IR, radar, video EO/IR)
  - t-u: Update (status query, cancel)
  - t-r: Relocate
  - t-q: Query capable

### Template Types [LA]
TRACK, SENSOR_POINT_OF_INTEREST, ASSET, GEO, SIGNAL_OF_INTEREST

### Alternate ID Types [LA: AltIdType, with detailed descriptions]
- TRACK_ID_1, TRACK_ID_2 — Anduril track identifiers
- SPI_ID — Sensor Point of Interest ID
- NITF_FILE_TITLE — imagery file reference
- TRACK_REPO_ALERT_ID
- ASSET_ID — Anduril AssetId v2
- LINK16_TRACK_NUMBER — Link 16 track number (non-JTIDS)
- LINK16_JU — Link 16 JTIDS Unit identifier
- NCCT_MESSAGE_ID
- CALLSIGN — TAK or aircraft callsign
- MMSI_ID — Maritime Mobile Service Identity
- VMF_URN — VMF network URN
- IMO_ID — International Maritime Organization number
- VMF_TARGET_NUMBER
- SERIAL_NUMBER — permanent unique ID (VIN, hull number)
- REGISTRATION_ID — reassignable local/national ID (license plate, tail number)
- IBS_GID — Integrated Broadcast Service GID
- DODAAC — DoD Activity Address Code
- UIC — Unit Identification Code
- NORAD_CAT_ID — 9-digit satellite catalog number
- UNOOSA_NAME — UN space object name
- UNOOSA_ID — international spacecraft designator (YYYYNNNP{PP})

### Target Classification [ML: MAVLINK_M_TARGET_CLASS]
- MBT_1 through MBT_9 — Main Battle Tank types
- IFV_1 through IFV_9 — Infantry Fighting Vehicle types
- ROAD — road or linear infrastructure
- STRUCTURE — structure or building

### Media Types [LA: MediaType, ML: MATCH_MEDIA_TYPE]
- IMAGE, VIDEO [LA]
- Still image, Video clip, IR image, SAR image [ML: match media for target identification]

### Schema Template Types [FC: SchemaKind]
- BASIC_UNIT, GROUND_ORG, AIR_ORG, AIR_UNIT, GROUND_UNIT, INTEL_TRACK, LINK, SENSOR

---

# CONTROL

## Directive

### Intent
- Commander's intent [from Planning process notes: clear, concise statement of what force must do, purpose, conditions for end state]
- Mission-type tactics [from notes: objective + high-level details + forces needed; subordinates decide methods]

### Instruction
- Five Paragraph Order / OPORD [from notes: Situation, Mission, Execution, Admin/Logistics, Command/Signal]
- General Order [FC/CNC: AI generates general order to all units]
- Task order per subordinate [FC/CNC: short message to each element by callsign]

### Objective
- Objective [LA: Objective with Point target]
- Conditions for success
- Goal: desired end-state/outcome [from notes]

### Task
Task types from Lattice (v2 task definitions):
- **ISR tasks:**
  - Investigate [LA: Investigate]
  - VisualId [LA: VisualId]
  - Map [LA: Map]
  - Loiter [LA: Loiter with LoiterType, OrbitType, OrbitDuration]
  - AreaSearch [LA: AreaSearch]
  - VolumeSearch [LA: VolumeSearch]
  - ImproveTrackQuality [LA]
  - Shadow [LA: Shadow]
  - Monitor [LA: Monitor]
  - Scan [LA: Scan]
  - BattleDamageAssessment [LA: BDA]
  - GimbalPoint [LA: GimbalPoint, AzimuthElevationPoint, FramePoint]
  - GimbalZoom [LA]
- **Maneuver tasks:**
  - Marshal [LA: Marshal]
  - Transit [LA: Transit with RoutePlan]
  - SetLaunchRoute [LA: SetLaunchRoute]
- **Strike tasks:**
  - Smack [LA: Smack]
  - Strike [LA: Strike with StrikeParameters, StrikeReleaseConstraint, PayloadConfiguration]
  - ReleasePayload [LA]

From existing typology:
- Move: reposition to location
- Patrol: maintain presence along route/area
- Search: find something in area
- Observe: gather information on target/area
- Survey: systematic coverage for documentation
- Hold: maintain position for duration
- Relay: provide comms relay

From CoT tasking:
- Close Air Support (t-a-c)
- Air Drop (t-a-d)
- Electronic Warfare (t-a-e)
- Strike / Destroy / Target (t-k)
- ISR (t-s) — imagery, radar, video, BFT
- SEAD (t-a-s) — Suppression of Enemy Air Defenses
- Mensurate (t-m)
- Relocate (t-r)
- Recovery (t-a-r)

Mission types [from Skynet notes]:
- Vertical drop (one-way kamikaze)
- One-way (one-way with payload delivery)
- Search-Destroy-Return (polygon, circle, rectangle):
  - Random search pattern
  - Grid search pattern
  - Spiral search pattern (circle only)
- Search-Destroy-Attack (as above, doesn't return)

Task lifecycle (Lattice):
- STATUS_CREATED → SCHEDULED_IN_MANAGER → SENT → MACHINE_RECEIPT → ACK → WILCO → EXECUTING → WAITING_FOR_UPDATE → DONE_OK / DONE_NOT_OK
- REPLACED, CANCEL_REQUESTED, COMPLETE_REQUESTED, VERSION_REJECTED
- Error codes: CANCELLED, REJECTED, TIMEOUT, FAILED
- Delivery status: DELIVERED, PENDING_EXECUTE, PENDING_CANCEL, PENDING_COMPLETE
- Delivery errors: UNAVAILABLE, TIMEOUT, REJECTED

Task structure (Lattice):
- Task has: specification (Any), author (Principal), relations, description, display_name
- Principal: System or User
- Relations: parent task, assignee
- Owner: Team or Agent
- Allocation: Team or Agent
- TaskEntity: entity references (objective entity, keep-in-zone entity, etc.)
- DeliveryState, DeliveryConstraints, RetryStrategy (FixedRetry)
- Replication scope
- TaskVersion: definition_version, status_version
- TaskView: MANAGER vs AGENT view
- is_executed_elsewhere flag (for external system integration)
- TaskCatalog [LA: catalog of tasks an entity can perform]

Military hierarchy [from notes]:
- Operation (Task Force+): Attack the area
- Mission (Battalion): Take this village
- Assignment (Company): Take sector A
- Tactical Task (Platoon): Take building 42
- Tactical Plan (Platoon): Plan of maneuver
- Action: Move up to sides of building

Decision frameworks:
- OODA Loop: Observe → Orient → Decide → Act [from notes]
- F2T2EA: Find → Fix → Track → Target → Engage → Assess [from notes]
- FFFFF: Find → Fix → Fire → Finish → Feedback [from notes]
- Intelligence Cycle: Direct → Collect → Process → Disseminate [from notes]

## Process

### Plan
- Mission plan [BM: mission_data structure]
  - mission_name, mission_uid, mission_time, mission_type
  - formation parameters (hor_sep, min_alt, max_alt, alt_sep, waves_n)
  - takeoff (home_pos, wave_delay)
  - assembly point (azimuth, dist)
  - route (step_m, airspeed, alt)
  - ingress (dist, azimuth, alt, airspeed)
  - survey area (IP dist, simultaneous, airspeed, hover_wait)
  - egress (alt, dist, azimuth, airspeed)
  - landing (sep, delay, pos)
  - assignments, flight_plans
  - points: route_in, survey, survey_area, route_out
  - n_points per phase

- Flight plan [BM: blank_flight_plan]
  - num (unit index)
  - id (assigned unit UID)
  - callsign
  - wave_n
  - formation_n
  - takeoff_time

- RoutePlan [LA: RoutePlan with Route, PathSegment, Waypoint]
- RouteDetails [LA: entity route metadata]
- Route [CT: route schema — ordered waypoints with link attrs]
  - RouteDirection: Infil, Exfil [CT: RouteFil enum]
  - RouteMethod: Driving, Walking, Flying, Swimming, Watercraft [CT: RouteMethod enum]
  - RouteType: Primary, Secondary [CT: RouteRoutetype enum]
  - RouteOrder: Ascending/Descending Check Points [CT: RouteOrder enum]

- OpPlan rendering [BM: render_opplan generates HTML from mission_data]
- MAVLink mission export [BM: export_mavlink_missions]

Go/No-Go parameters [Skynet notes]:
- Unit failure handling
- Abort criteria
- Battery bingo (minimum battery level)

Mission planning parameters [Skynet notes]:
- Multi-target, multi-unit
- Takeoff point, assembly point, initial point, release point
- Release mode, altitude deconfliction
- Loiter time

### Method
- Orbit patterns: Circle, Racetrack, FigureEight [LA: OrbitPattern]
- Orbit direction: Right, Left [LA: OrbitDirection]
- LaunchTrackingMode: GoToWaypoint, TrackToWaypoint [LA]
- ISRParameters [LA: gimbal, zoom, scan params]
- Search patterns: Random, Grid, Spiral [Skynet notes]
- Terrain analysis [from notes: topography, roads/fields, obstacles, central points, cardinal directions]

### Action
- HiveOS UAV actions:
  - Arm, Disarm
  - SetTakeoffAltitude (meters), Takeoff, Land, RTL
  - SetMode (mode name + enabled bool)
  - GoTo (lat, lon, alt, yaw)
  - SetWaypoint (index, action, lat, lon, alt, param1-3, flag) — writes to FC mission table
  - SelectMission (sequence index)
- HiveOS ATAK actions:
  - SendEvent (full CoT event with uid, type, how, position, callsign, detail XML, targets array)
  - SendMarker (callsign, uid, cot_type, position, ce, le, stale_seconds, targets)
  - SendGeoChat (message, to_team, position)
- Lattice task actions:
  - ExecuteRequest (contains Task)
  - CancelRequest (task_id, assignee)
  - CompleteRequest (task_id)
- MAVLink-M fire actions:
  - FIRES (fire mission order: target lat/lon/alt, time_impact, effector_id, sequence, cep_expected)
  - ESAD_ARMING (arm/disarm with challenge hash authentication)

### Interface
- PWM (servo/ESC)
- GPIO
- CAN bus
- Serial actuator command
- RC channels [HV: RcChannels, RxConfig (rxMinUsec/rxMaxUsec/rxCenterUsec), ChannelMap, ModeRanges]
- Actuator servos [CO: ActuatorState — servos list]

---

# COMMUNICATION

## Node
- Entity reference (what entity this node belongs to)
- CO: source field on EntityState
- LA: Provenance on Entity (integration_name, data_type, source_id, source_update_time, source_description)

## Transport

### Network
Topologies: Mesh, PointToPoint, Broadcast, StoreAndForward

### Carrier
- Radio (HF, VHF, UHF, SHF, EHF)
- Wire/Serial (baud)
- IP
- Satellite
- Cellular
- Voice (terminal/analog)
- Meshtastic [noted in ontology]
- LoRa

Radio specifics (FC/LinkSchema):
- bands, waveform, bandwidth, speed
- frequency, channel
- crypto_type, crypto_set, crypto_keys

### Protocol
- MAVLink (v1, v2) [HV: UAV protocol is MAVLink-derived]
- MAVLink-M (custom dialect 0, v1) [ML: military targeting/fires extension]
- MSPv2 [HV: MSP support]
- ROS (1, 2)
- STANAG4586
- CoT / Cursor on Target [HV: ATAK protocol, CT: full CoT schema]
- Meshtastic
- RTP/RTSP/SRT/HLS [CO: VideoProtocol — RTSP, RTMP, SRT, HLS]
- Custom/Serial
- Link16 [LA: LINK16_TRACK_NUMBER, LINK16_JU alt IDs]
- VMF [LA: VMF_URN, VMF_TARGET_NUMBER]
- ADS-B [LA: transponder codes, Mode 1/2/3/4/5/S]
- XMPP [CT: xmpp_username in contact]

CoT "How" field — production method [CT/HV]:
- Machine-generated, human-entered, etc. Describes how the data was produced.

Signal characteristics (Lattice):
- EmitterNotation
- Frequency, FrequencyRange
- LineOfBearing (relative position of track to tracker), AngleOfArrival
- Fixed (location)
- PulseRepetitionInterval
- ScanCharacteristics with ScanType enum [LA: 16 scan types]:
  - Circular, BidirectionalHorizontalSector, BidirectionalVerticalSector
  - NonScanning, Irregular, Conical, LobeSwitching, Raster
  - CircularVerticalSector, CircularConical, SectorConical
  - AgileBeam, UnidirectionalVerticalSector, UnidirectionalHorizontalSector
  - UnidirectionalSector, BidirectionalSector
- Bandwidth, BandwidthRange
- RFConfiguration
- Measurement (generic measurement wrapper)

## Feed

### Link
- Discontinuous packet data
- Transport metrics [HV: ATAK RxCount, TxCount, RxParseErrors]
- Tx result [HV: ATAK LastResult — TargetCount, Bytes]

### Stream
- Video [CO: VideoFrame, VideoConfig, VideoProtocol]
- Audio
- SensorFeed

Video specifics (CO):
- VideoFrame: entity_id, frame_id, timestamp, sequence_num, camera_id, stream_id, width, height, format (jpeg/h264/raw), encoding (base64/binary), data (bytes), detections, priority, quality
- VideoDetectionBBox: class_id, class_name, confidence, x, y, width, height, track_id
- VideoConfig: protocol, port, stream_url, overlay_url, webrtc_url, overlay_webrtc_url, hls_url

## Message

### Message envelope concepts
- MessageType: Snapshot, Delta, History, Log
- CoT event envelope: uid, type, how, time, start, stale, point (lat/lon/hae/ce/le), detail [CT/HV]
- CoT detail: arbitrary XML payload (DetailXml field)
- HiveOS message key pattern: Protocol.Category.Domain.MessageName
- Sigma: message_id, unit_id
- Targets array: directed list of destination endpoints [HV: ATAK SendEvent/SendMarker targets]
- MAVLink message envelope: message_id, message_type, system_id, component_id, data [CO: MAVLinkTelemetry]

### Command
- Navigation command (GoTo, SetWaypoint, SelectMission) [HV]
- Mode change (SetMode, Arm, Disarm) [HV]
- Parameter set
- Actuator command
- Flight commands: Takeoff, Land, RTL [HV]
- Task execution: ExecuteRequest, CancelRequest, CompleteRequest [LA]
- Fire mission order [ML: FIRES — coordinate, time of impact, effector, CEP]
- ESAD arming command [ML: arm/disarm with challenge hash]
- Target handover [ML: transfer tracking responsibility with kinematic state, classification, media, authorization]
- Splash correction [ML: post-impact observation for fire correction]
- Target designation [ML: TARGET_COORD — position, velocity, covariance, CEP, class, force]

### Telemetry
- Heartbeat / status [HV: FcConnected, CpuLoad, CycleTime, FlightMode]
- FC system info [HV: FcInfo — ApiVersion, FcVariant, BoardInfo, HardwareUid, LegacyUid, VendorId/Name, ProductId/Name, software versions (FlightSw/OsSw major/minor/patch/GitHash)]
- Navigation state [HV: NavState code, IsGlobalPositionOk, IsHomePositionOk]
- Position [HV: Position, RawGps (with GroundSpeedMS, GroundCourseDeg, Hdop, Vdop, YawDeg); CO: GlobalPosition, LocalPosition]
- Altitude [HV: AltitudeM separate scalar]
- Attitude [HV: AttitudeRad, AngVelRadS; CO: EulerAttitude (with rates), QuaternionAttitude]
- Battery / power [HV: Battery (VoltageV, CurrentA, PowerW, ConsumedMah/MWh/Ah, RemainingPct, RemainingCapacity, TemperatureDegC, BatteryId, Rssi), Analog (vbat, amperage, powerDraw, mAhDrawn, mWhDrawn, percentageRemaining, remainingCapacity, rssi); CO: PowerState]
- IMU [HV: Imu — AccelXYZ, GyroRadSXYZ, MagXYZ, TemperatureDegC, TimestampUs, Frame]
- Sensor config readiness [HV: SensorConfig — GyroOk, AccelOk, MagOk, LocalPositionOk, GlobalPositionOk, HomePositionOk, Armable]
- GPS info [HV: GpsInfo (FixType, NumSat, lastMessageDt, errors, timeouts, hdop, eph, epv), GpsStatistics]
- VFR state [CO: VFRState — airspeed, groundspeed, heading, climb_rate, throttle, altitude]
- Mission progress [HV: WaypointInfo (WaypointCount, CurrentWaypointIndex, MissionValid); CO: MissionState]
- MAVLink raw telemetry [CO: MAVLinkTelemetry — message_id, message_type, system_id, component_id, data map]
- Vehicle status [CO: VehicleStatusState — armed, mode, custom_mode, autopilot, system_status, vehicle_type, landed_state, vtol_state, load, sensors_enabled/health]
- Actuator state [CO: ActuatorState — servos list]
- Environment [CO: EnvironmentState — pressure_abs, pressure_diff, temperature, humidity]
- RC override [HV: OverrideActive bool]
- Failsafe [HV: Failsafe bool]
- Active modes [HV: ActiveModes (array of raw IDs), ActiveModeNames (array of human-readable names)]
- ESAD telemetry [ML: arming_status, munition_status, ignition_status, fault_flags (bitmask: wiring/power_glitch/signal_integrity/sensor_acc/sensor_lidar), arming_challenge_hash, sw_version_hash, inputs]
- RWS pose [ML: RWS_POSE — position, velocity, covariance, mounting offset, orientation quaternion, accuracy roll/pitch/yaw, coordinate_frame]
- RWS state [ML: RWS_STATE — weapon_string, arming_state (safe/armed/fault), weapon_type]

Telemetry variants by domain [SG]:
- GroundTelemetry
- AirTelemetry
- SeaTelemetry
- SpaceTelemetry

### Observation
- CoT received event [HV: ATAK ReceivedEvent with SourceHost, SourcePort]
- CoT received marker [HV: ATAK ReceivedMarker]
- GeoChat [HV: ATAK ReceivedGeoChat — uid, from_callsign, to_team, message]
- Detection notification
- Track update
- Intel report
- SALUTE Report [from ISR notes]: Size, Activity, Location, Uniform, Time, Equipment
- Environment report [from ISR notes]
- Battle Damage Assessment [ML: BATTLE_DAMAGE_ASSESSMENT — position, velocity, covariance, destruction_pct, confidence_pct, target_class, target_force, authorization]
- Splash correction [ML: observed splash position, type_detected (unknown/smoke/explosion), CEP]
- Target handover observation [ML: full kinematic state + classification + media reference + confidence + authorization]

### Response
- Ack / Nack / Result
- CO: Response {success, data, error}
- CO: Error {code, message, details}
- HiveOS event pattern: Event.*.* (Armed, Disarmed, TakeoffDetected, Landed, FailsafeChanged, Mission.Aborted, Mission.Completed)
- TakeoffDetected carries altitude [HV: AltitudeM on event]
- Mission.Aborted carries reason [HV: Reason string]
- ATAK ParseError event [HV: Error string]
- ATAK link state [HV: TcpClientConnected bool]

---

# DATA

## Information

### Properties

#### Identity
- UID (uuid4) [everywhere]
- Name [everywhere]
- Callsign [FC, CT, HV, CO, LA: AltIdType CALLSIGN]
- Unit code [FC: randcode(8)]
- System ID, Component ID [CO: system_id, component_id; MAVLink concept]
- Device ID [CO: device_id]
- Entity ID (GUID) [LA: entity_id required field]
- Description [LA: entity description, human-readable for debugging]
- Alternate IDs [LA: AlternateId with AltIdType — 25+ types, see Reference/Type section]
- Aliases [LA: Aliases; CO: aliases map]
- Tags [CO: tags list]
- Subject [CO: subject string]
- NATO phonetic alphabet codenames [FC: NATO_ALPHABET tuple — ALPHA through ZULU]
- Callsign generation patterns [FC]:
  - Codename + number (BM: "DOG1", "MAVERICK2")
  - Hierarchical: parent-num format (e.g. "callsign-1-2" for squad/team)
  - Size-based naming: "2BTN-1RGT", "1BDE"
- Provenance [LA: Provenance — integration_name, data_type, source_id, source_update_time, source_description]

#### Attributes
- Faction / Disposition [SG: Faction; LA: Disposition; CT: a-f/h/u/n/s]
- Entity type / category [CO: EntityType; CT: CoT type hierarchy; FC: category]
- Domain (Air/Ground/Sea/Sub/Space) [LA: Environment; SG: MachineDomain]
- Organization class (Military/Civilian/Commercial/NGO) [CO: OrgType; SG: OrgClass]
- Unit size / echelon [FC: sizelevel, size; LA: ArmyEchelon]
- Taskforce flag [FC: taskforce bool]
- SIDC / MilStd2525 code [FC: sidc; LA: MilStd2525C; BM: info_points with SIDC]
- CoT type string [FC: cot; CT: type attribute]
- Classification level [LA: Classification, ClassificationLevels, per-field classification]
- Nationality [LA: Nationality enum — 100+ countries]
- Dimensions [LA: Dimensions — physical dimensions]
- Visual details / color [LA: VisualDetails, RangeRings (min_distance_m, max_distance_m, ring_count, ring_line_color), Color]
- Symbology [LA: Symbology, MilStd2525C]
- Ontology / MilView [LA: Ontology, MilView — entity categorization]

Machine-specific attributes (FC/AirUnitSchema):
- model, type, serial_uid
- propulsion, flight_type
- reusable, has_warhead, warhead
- guidance, navigation, navaids
- autopilot, autopilot_model
- fuel_type, fuel_config
- max_range, max_flight_time, max_speed, cruise_speed, max_altitude
- weather_limits (WeatherLimits: ifr, rain, snow, temp range, wind, vis, icing)
- roles, attack_modes
- sensors list, links, weapons, ammo, ordnance

Sensor attributes (FC/SensorSchema):
- name, model, type, serial_uid
- effect_domain, max_range
- ptz, spectrum, night_vision, all_weather
- weather_limits
- error_margin, error_type
- data_formats, AI capabilities
- datalink, fov, zoom_range

Organization attributes (FC/GroundOrganizationSchema):
- tac_e_comp, sup_e_comp (tactical/support element composition counts)
- links (link type → count)
- equipment, personnel, infantry
- vehicles, air_units (model → count maps)
- spacing
- weapons, ammo

#### Parameters
- Current autonomy mode (vs capability ceiling)
- Current control authority holder
- Flight mode [HV: FlightMode string]
- Armed state [HV: IsArmed; CO: VehicleStatusState.armed]
- Active modes [HV: ActiveModes array, ActiveModeNames array]
- In-air state [HV: IsInAir]
- Override active [HV: OverrideActive]
- Failsafe state [HV: Failsafe]
- Video config [CO: VideoConfig — protocol, port, URLs]
- Stream port [CO: stream_port]
- Fingerprinted [CO: fingerprinted bool]
- Simulated [LA: Indicators.simulated]
- Exercise [LA: Indicators.exercise]
- Egressable [LA: Indicators.egressable]
- Is live [LA: Entity.is_live, CO: EntityState.is_live]
- No expiry [LA: Entity.no_expiry — entity persists indefinitely]

#### Relationship
- ControlAuthority [SG: controller_id, authority_level]
- TaskAssignment [SG: task_id]
- Ownership [SG: owner_id]
- Composition [SG: part_id]
- Parent/child org hierarchy [FC: parent, grandparent, attached_to, attachments]
- Lattice relationships [LA: Relationships with RelationshipType]:
  - TrackedBy
  - GroupChild / GroupParent
  - MergedFrom
  - ActiveTarget
- Correlation [LA: Correlation, PrimaryCorrelation, SecondaryCorrelation]:
  - CorrelationType: MANUAL (higher precedence), AUTOMATED
  - CorrelationReplicationMode: LOCAL (higher precedence), GLOBAL
  - primary_entity_id, secondary_entity_ids
  - CorrelationMetadata
- Decorrelation [LA: Decorrelation — DecorrelatedAll, DecorrelatedSingle]
- Fleet → Swarm → Entity hierarchy [CO]
- Task relations: parent task, subtasks [LA: Relations — parent_task_id, assignee]
- Tracked reference [LA: Tracked — who is tracking this entity]

### State

#### Location
- Global position: lat, lon, alt (MSL), alt (relative), alt (terrain) [CO: GlobalPosition]
- Lattice position: lat_degrees, lon_degrees, altitude_hae_meters, altitude_agl_meters, altitude_asf_meters, pressure_depth_meters [LA: Position — 4 altitude references plus undersea depth]
- Local position: x, y, z, vx, vy, vz [CO: LocalPosition]
- Position accuracy: horizontal, vertical [CO: accuracy_h, accuracy_v]
- GPS quality: satellites_visible, fix_type [CO, HV]
- Home position validity [HV: IsHomePositionOk]
- Global position validity [HV: IsGlobalPositionOk]
- CoT position: lat, lon, HAE, CE (circular error), LE (linear error) [CT/HV]
- Location uncertainty [LA: LocationUncertainty]:
  - Position covariance matrix (ENU) [LA: TMat3 upper triangle]
  - Velocity covariance matrix (ENU) [LA: TMat3]
  - Error ellipse [LA: ErrorEllipse]
- Position + velocity covariance per-axis [ML: cov_pos_x/y/z, cov_vel_x/y/z on targets and BDA]
- Precision location source [CT: Precisionlocation]:
  - geopointsrc (how position was determined)
  - altsrc values: DTED0/1/2/3, LIDAR, USER, GPS, SRTM1, COT, CALC, ESTIMATED, RTK, DGPS, GPS_PPS
  - precise_image_file reference (x/y pixel coords in image)
- Pose [LA: position + orientation quaternion, body-to-ENU transform]
- Velocity in ENU [LA: Location.velocity_enu — meters/second]
- Speed magnitude [LA: Location.speed_mps]
- Acceleration in ENU [LA: Location.acceleration]
- Attitude as quaternion [LA: Location.attitude_enu — body frame to ENU]

#### Kinematic
- Euler attitude: roll, pitch, yaw [HV: AttitudeRad; CO: EulerAttitude with angular rates]
- Quaternion attitude: q1-q4 [CO: QuaternionAttitude]
- Angular velocity: x, y, z [HV: AngVelRadS; CO: rollspeed, pitchspeed, yawspeed]
- Ground speed [CO: VFRState.groundspeed, HV: RawGps.GroundSpeedMS]
- Ground course [HV: RawGps.GroundCourseDeg]
- Airspeed [CO: VFRState.airspeed]
- Climb rate [CO: VFRState.climb_rate]
- Heading [CO: VFRState.heading; FC: ang heading]
- Throttle [CO: VFRState.throttle]
- Velocity: horizontal speed, vertical speed [FC: vel (h_speed, v_speed)]
- IMU data: accel XYZ, gyro XYZ, mag XYZ, temperature, timestamp, frame [HV: Imu]
- CoT track detail: course, speed, slope [CT: Track detail]
- Radar cross section (RCS) in dBsm [LA: Tracked.radar_cross_section]
- Number of objects / strength estimate [LA: Tracked.number_of_objects — UInt32Range]

#### Resources
- Battery / Power:
  - Voltage, current, power (watts) [HV, CO]
  - Consumed (mAh, mWh, Ah) [HV]
  - Remaining % [HV, CO]
  - Remaining capacity [HV]
  - Temperature [HV, CO]
  - Cell voltages [CO: cells list]
  - Cell series count [SG]
  - Battery ID [HV]
  - RSSI [HV: on battery/analog — link quality proxy]
  - CoT status battery [CT: Status.battery int]
- Power source tracking [LA: PowerState.source_id_to_state map — multiple named power sources per entity]
  - PowerSource with PowerLevel
  - PowerType: Gas, Battery [LA]
  - PowerStatus: Unknown, NotPresent, Operating, Disabled, Error [LA]
- Fuel:
  - Volume (liters) [SG]
  - Remaining % [SG, LA: Fuel in Supplies]
- Supplies [LA: Supplies — Munition, Fuel]
- Resupply status [FC: resupply dict]
- Ammo counts [FC: ammo dict]
- Readiness [CT: Status.readiness bool]

#### Condition
- Readiness level
- Fault list
- Damage assessment
- Health status: Healthy, Warn, Fail, Offline, NotReady [LA: HealthStatus]
- Connection status: Online, Offline [LA: ConnectionStatus]
- Component health [LA: ComponentHealth, ComponentMessage]
- Alert: level (Advisory, Caution, Warning), conditions [LA: Alert, AlertCondition, AlertLevel]
- Power status: Unknown, NotPresent, Operating, Disabled, Error [LA: PowerStatus]
- Sensor readiness [HV: SensorConfig — gyro/accel/mag OK, armable]
- ESAD fault flags [ML: bitmask — wiring, power_glitch, signal_integrity, sensor_acc, sensor_lidar]
- FC system health [HV: CpuLoad, CycleTime]

#### Lifecycle
Phases: Planned, Active, Paused, Complete, Aborted, Failed [SG: LifecyclePhase]
Entity lifecycle: first_seen, last_seen, created_at, updated_at [CO]
Entity liveness: is_live, expiry_time, no_expiry [CO, LA]
Entity created_time [LA: when entity was first known to producer]
Override lifecycle [LA: OverrideStatus — Applied, Pending, Timeout, Rejected, DeletionPending]
Override types [LA: OverrideType — Live, PostExpiry]

#### Mission
- Current waypoint index, total waypoints [HV: WaypointInfo; CO: MissionState]
- Mission valid [HV]
- Operation, task, opord, plan, orders [FC: fields on CabalUnit]
- Assignments [BM: assignments dict]
- Flight plans [BM: flight_plans dict]

#### Event
- Flight events: Armed, Disarmed, TakeoffDetected (with altitude), Landed, FailsafeChanged [HV]
- Mission events: Aborted (with reason string), Completed [HV]
- Entity events: Created, Updated, Deleted, StatusChanged, Alert [CO]
- Task events: Created, Update, Preexisting [LA]
- Parse error events [HV: ATAK ParseError]

### Intel

#### Detection
- Position (where)
- Timestamp (when)
- Confidence
- CoT detections: acoustic (impulsive, voice, cyclostationary), motion, seismic, radiation, nuclear, CBRNE, launch (bullet, mortar), impact [CT: b-d-* tree]
- Video detections: class_id, class_name, confidence, bbox, track_id [CO: VideoDetectionBBox]
- Tracked objects: track_id, label, confidence, frame_count, bbox, center (cx,cy), velocity (dx,dy), first_seen, last_seen, avg_confidence, is_active, threat_level, suspicious_indicators [CO: TrackedObject]
- CEP (Circular Error Probable): desired and maximum acceptable [ML: TARGET_COORD.cep_desired, cep_max]
- Target set grouping: target_set_id, target_set_name, centroid, radius [ML]

#### Classification
- Detection reference
- Assessed type/category
- Confidence / confidence_score [ML: 0.0-1.0 on TARGET_HANDOVER]
- Classification information per field [LA: FieldClassificationInformation]
- Target class [ML: MBT types 1-9, IFV types 1-9, Road, Structure]
- Target force [ML: Unknown, Neutral, Friendly, Foe, Extraterrestrial]
- Match media reference [ML: match_media_url with type (image/video/IR/SAR)]

#### Track
- Track ID
- Position history / current estimated state
- Confidence
- Track quality score (0-15) [LA: Tracked.track_quality_wrapper]
- Sensor hits count [LA: Tracked.sensor_hits]
- Last measurement time [LA: Tracked.last_measurement_time]
- Line of bearing [LA: Tracked.line_of_bearing — relative position to tracker]
- Intel track (FC): faction, spotted_time, updated_time, spotter_origin (lat, lon, pitch, heading, bearing, elevation, range), spotter_last, history, error_m
- Observer template (BMS): objtype, type, active, pos, name, attitude (pitch/yaw/heading), fov, zoom, gimbal_axis/ang, video_res/type/addr, telem_type/port/baud, commands_allowed, metadata, simulated
- Threat intel [CO: ThreatIntelState — mission, analytics, threat_summary, threat_alerts]
- Threat summary [CO: ThreatSummary — total_threats, threat_distribution, alert_level]
- Target priority [LA: TargetPriority]:
  - HighValueTarget: is_high_value_target, target_priority (lower = higher), is_high_payoff_target, target_matches
  - Threat: is_threat
- Analytics [CO: AnalyticsState — total_unique_objects, total_frames_processed, active_objects_count, tracked_objects_count, label_distribution, threat_distribution, active_threat_count, active_track_ids, threat_alerts]
- BDA results [ML: destruction_pct (0-100%), confidence_pct (0-100%), with full kinematic state + authorization]
- Russian F2T2EA BDA color coding [from notes]:
  - Grey: good hit
  - Yellow: inconclusive
  - Green: confirmed destroyed (after daylight BDA)
  - Red: undamaged, needs re-engagement
- Target naming convention [from Russian F2T2EA]: date_unitnumber_targetnumber (e.g. "0708_114_1")
- Target handover [ML: full kinematic state + covariance + classification + media URL + confidence + authorization token + validity expiry]

## Sensory

### AV
- Video frame [CO: VideoFrame]
- Image [CT: b-i]
- Audio
- Telestration [CT: telestration schema — drawing/annotation overlay]
- Media items [LA: Media, MediaItem — associated images/videos/thumbnails]

### Spatial
- PointCloud
- Mesh
- Scan (radar, lidar)
- Field of view / projected frustum [LA: FieldOfView, ProjectedFrustum]
- FOV calculation: 2 * arctan(SensorSize / 2f) [from ISR notes]

### Samples
- IQ (in-phase/quadrature)
- Analog
- Signal [LA: Signal — EmitterNotation, Measurement, Frequency, LineOfBearing, AngleOfArrival, PulseRepetitionInterval, ScanCharacteristics, RFConfiguration, Bandwidth]

---

# CROSS-CUTTING CONCEPTS (not ontology nodes, but recurrent patterns)

## Pagination
- PaginationRequest: page, page_size, order_by, order [CO]
- PaginationResponse: items, page, page_size, total_items, total_pages [CO]
- Page token pagination [LA: page_token on QueryTasksRequest/Response]

## Health / Service
- HealthStatus: status, service, version, uptime, timestamp, details [CO]

## Metadata
- metadata: map[string, any] — appears on nearly everything [CO, LA]
- components: map[string, any] [CO]
- source: string [CO]
- created_by: string [CO]

## Filtering / Querying
- Predicate-based filtering [LA: Statement, Predicate, PredicateSet — complex boolean logic]:
  - Comparators: equality, in, less_than, greater_than, less_than_equal_to, greater_than_equal_to, within, exists, range_closed, case_insensitive_equality, case_insensitive_equality_in
  - Value types: Boolean, Numeric, String, Enum, List, Timestamp, Position, BoundedShape, Heading, Range
  - Boolean operations: AND, OR, NOT [LA: AndOperation, OrOperation, NotOperation]
  - List operations: ANY_OF [LA: ListComparator]
- Position-based filtering (within geo bounds) [LA: PositionType, BoundedShapeType]
- Heading-based filtering [LA: HeadingType]
- Status filter with inclusive/exclusive mode [LA: StatusFilter, FilterType]
- Task query by: parent_task_id, status, update_time_range, assignee, task_type_urls, task_type_prefix [LA]

## Rate Limiting
- RateLimit [LA: update_per_task_limit_ms — minimum interval between updates, must be >= 250ms]
- RateLimit [CO]

## Scheduling
- Schedule, CronWindow [LA: cron_expression in UTC quartz flavor, duration_millis]
- ScheduleType: zone_enabled, zone_temp_enabled [LA]

## Replication
- Replication scope [LA: Replication on Task]
- Correlation replication mode: Local (higher precedence), Global (last-write-wins) [LA]
- Override precedence: Manual > Automated; Local > Global [LA]

## Orbit / Space
- OrbitMeanElements, OrbitMeanElementsMetadata [LA]
- TleParameters [LA: SGP4 propagation]
- MeanKeplerianElements [LA]
- NORAD catalog IDs [LA: AltIdType]
- EciReferenceFrame: TEME [LA]
- MeanElementTheory: SGP4 [LA]

## Transponder / IFF
- TransponderCodes [LA]: Mode 1, 2, 3, 4, 5, S interrogations
- Mode 5: interrogation_response (Correct/Incorrect/NoResponse), mode5 code, platform_id [LA]
- Mode S: id (8 alphanumeric), ICAO address (1-16777214) [LA]
- InterrogationResponse: Correct, Incorrect, NoResponse [LA]

## Callsign Generation (FC pattern)
- Codename + number
- Hierarchical: parent-num format
- Size-based naming (BTN, RGT, BDE, DIV)
- NATO alphabet codenames [FC: NATO_ALPHABET]

## Formation / Wave Logic (BM)
- Vertical separation (alt_sep between wave members)
- Horizontal separation (dist_sep)
- Wave delay (time offset between waves)
- Flight level allocation (calculate available levels from alt range / alt_sep)
- Wave auto-calculation: waves_n = ceil(n_targets / available_levels)
- Assembly → Ingress → Survey → Egress → Landing sequence
- Route step distance (meters between waypoints)

## Chat / Messaging
- GeoChat [HV: ATAK geochat — message, to_team, position]
- Chat [CT: chat schema, chatreceipt, chatgrp]
- Target distribution via chat [Russian F2T2EA: target info posted in attack drone chat channel]

## Map Markers
- Marker [BMS: template_marker — name, dynamic, unitmarker, observer, type, markertype, lat, lon, angle, linked_track, comment, cot]
- Info point [BM: pos, name, origin, uid, cot, SIDC, added time, t_stale, url]
- Spot [CT: spot schema]
- Route [CT: route schema — ordered waypoints with infiltration/exfiltration direction]
- Markerset [CT: markerset schema]
- 2525 marker [CT: marker2525 schema]

## CV / Detection Pipeline
- Bounding box [BMS: template_box — linked_track, cv_algo, cv_class, rect]
- Track [BMS: template_track — files, dbid, id, image, type, lat, lon, alt, angle]
- Intel entry methods [ISR notes]: geopointing, click-drag box, manual (visual ident), semi (CV rec + manual mark), auto (CV rec + auto mark), manual entry from map
- IMINT pipeline [ISR notes]: mcvst/video → autocvimint → inteldb
- Sensor/track/object fusion [ISR notes: inteldb aggregator]

## Observer / Sensor Config
- Observer template [BMS: template_observer]:
  - objtype, type, active, pos, name
  - attitude: pitch, yaw, heading
  - fov (tuple), zoom, can_zoom
  - gimbal_axis (pitch/yaw/roll bools), gimbal_ang (pitch/yaw/roll floats)
  - video_res, video_type, video_addr
  - telem_type, telem_port, telem_baud
  - commands_allowed
  - metadata, simulated

## Geospatial Features
- spatial_feature (FC): name, uid, domain, status, category (object/topography/landmark/polygon), type (bridge/building/base), cot, sidc, position, polygon_shape, polygon
- Terrain analysis concerns [from notes]: topography, roads/open fields, obstacles (rivers/treelines/towns), central points (crossroads/large buildings/towns), cardinal direction analysis

## CBRNE
Full detection and alarm trees for: Biological, Chemical, Explosive, Nuclear, Radiological [CT: b-d-c-* and b-l-c-* trees]

## Capabilities (CoT)
- Communications, Fires (direct/indirect), Logistics/supply (fuel), Rescue, Surveillance [CT: c-* tree]

## Logistics / Maintenance [from CNC Notes]
- Logistics and Maintenance Management System:
  - Type data (model, serial number, type, role)
  - Components data (parts S/N, diffs, versions)
  - Flight logs (flight hours, used batteries)
  - Maintenance logs (changes, repairs, replacements)
  - Methodic configuration
- Logistics request → reply pattern
- Equipment serial tracking and assignment

## Spatial View / Situational Awareness (FC)
- spatial_view: given a unit, compute bearing/distance vectors to all friendlies, hostiles, and terrain features within max distance
- Returns: {friendly: {callsign: vector}, hostile: {code: vector}, feature: {code: vector}}
- find_closest_units: n-nearest units by geodesic distance

## Communication Formats / C3
- Command: functional exercise of authority based on knowledge [from notes]
- Control: process of verifying and correcting activity [from notes]
- Communications: necessary liaison to exercise command [from notes]
- Strategic vs Tactical: broad methods vs narrow methods en route to strategic goal [from notes]
- AI communications format [CNC notes]: AI generates plans, SYSTEM provides reports, AI generates orders per callsign

## Timetable / Timeline
- Immediate execution [FC: format_text_timeline]
- Phased execution [FC: timeline with T+hours phases]:
  - Phase goal, type ("from" = ongoing, other = until), time offset
  - Start time + DTG formatted timeline

## Authorization / Authentication
- Authorization token (opaque 8 bytes) [ML: on TARGET_HANDOVER and BDA]
- Arming challenge hash authentication [ML: ESAD arming requires matching challenge hash from telemetry]
- Crypto on links [FC: crypto_type, crypto_set, crypto_keys]

---

# INFERRED CONCEPTS — RECURSIVE EXPANSION

Everything below is inferred from use cases, not found in any source.
Each item is expanded into its constituent concepts, which are themselves
expanded until they bottom out into existing ontology/typology primitives
or self-evident leaf types.

Ontology placement noted in brackets where non-obvious.

---

## Weather [Data → State, of a Site or area]

### WeatherCondition (snapshot at a point in time and space)
- temperature (float) + TemperatureUnit
- wind: WindState
- pressure (float) + PressureUnit
- humidity: relative percentage (float 0-100)
- visibility: distance (float) + VisibilityUnit
- precipitation: PrecipitationType + rate (mm/h)
- cloud: CloudState
- dew_point: temperature
- icing: IcingIntensity + altitude range
- turbulence: TurbulenceIntensity

WindState:
- speed (float)
- gust (float, optional)
- direction (degrees, 0-360)
- SpeedUnit (used here and elsewhere)

CloudState:
- coverage: CloudCover
- ceiling: altitude (float + AltitudeReference — already exists)
- layers (optional list: altitude + CloudCover per layer)

TemperatureUnit [enum]: Celsius, Fahrenheit, Kelvin
SpeedUnit [enum]: MetersPerSecond, Knots, KilometersPerHour, MilesPerHour
PressureUnit [enum]: Hectopascal, Millibar, InchesOfMercury, MillimetersOfMercury
VisibilityUnit [enum]: Meters, StatuteMiles, NauticalMiles
PrecipitationType [enum]: None, Rain, Snow, Sleet, Hail, FreezingRain, Drizzle
CloudCover [enum]: Clear, Few, Scattered, Broken, Overcast (maps to oktas 0-8)
IcingIntensity [enum]: None, Light, Moderate, Severe
TurbulenceIntensity [enum]: None, Light, Moderate, Severe, Extreme

### FlightCategory [enum]
- VFR, MVFR, IFR, LIFR
- Derived from ceiling + visibility thresholds; not stored, but the enum must exist for constraint matching

### WeatherForecast
- conditions: ordered list of (time → WeatherCondition)
- valid_from, valid_to (timestamps)
- issuing_authority (string or Entity ref)
- source: WeatherSource

### WeatherSource [enum]
- METAR, TAF, PIREP, SIGMET, AIRMET, Radar, Satellite, ModelForecast

### WeatherLimits [Control → Directive, constraint on operations]
- min/max per WeatherCondition field
- Ties to existing FC WeatherLimits concept but generalized
- Expressed as: field → (min, max, unit)
- flight_category_minimum (FlightCategory)

### WeatherHazard
- type: WeatherHazardType
- severity (ordinal)
- area (Geometry — already exists)
- altitude_range (floor, ceiling)
- valid_time (TimeWindow)

WeatherHazardType [enum]: Thunderstorm, Icing, Turbulence, Fog, Dust, VolcanicAsh, Windshear, Sandstorm

---

## Terrain [Data → Properties, of a Site/area]

### TerrainType [enum]
- Urban, Suburban, Rural, Forest, Jungle, Desert, Mountain, Tundra, Marsh, Farmland, Water, Coastal, Arctic, Steppe, Savanna

### TerrainSurface [enum]
- Paved, Unpaved, Grass, Sand, Mud, Rock, Snow, Ice, Water, Gravel

### Slope
- gradient: degrees or percentage (float)
- aspect: compass heading (degrees)

### TerrainFeature [Object → Site specialization or Data → Properties of a Site]
- type: TerrainFeatureType
- position (Position — exists)
- geometry (Geometry — exists)
- elevation (altitude — exists)

TerrainFeatureType [enum]: Ridge, Valley, Saddle, Hill, Depression, Cliff, River, Lake, Road, Bridge, Building, Treeline, Clearing, UrbanArea, Pass, Ford, Dam

### Obstacle
- type: ObstacleType
- height_agl (float)
- position (Position)
- geometry (Geometry)
- traversability: Traversability

ObstacleType [enum]: Wire, Tower, Building, Terrain, Vegetation, Water, Minefield, Barrier, Ditch
Traversability [enum]: Passable, Restricted, Impassable

### CoverAndConcealment
- cover_rating (float 0-1) — protection from fire
- concealment_rating (float 0-1) — protection from observation
- directional (optional: map heading → rating)

### LineOfSight
- from_position (Position)
- to_position (Position)
- blocked (bool)
- obstruction_position (optional Position)
- max_effective_range (meters, float)

### TerrainGrid (reference to elevation data source)
- resolution_meters (float)
- bounds (Box2D or Polygon — exist)
- datum: GlobalFrame (exists)
- source_level: DTEDLevel

DTEDLevel [enum]: DTED0, DTED1, DTED2, DTED3 (already referenced in TAK altsrc)

---

## Airspace [Object → Site + Data → Properties]

### AirspaceClass [enum]
- A, B, C, D, E, F, G (ICAO standard)

### AirspaceType [enum]
- Controlled, Restricted, Prohibited, Danger, Alert, MOA, Warning, TFR, CTR, TMA, FIR, UIR, ATZ, ADIZ

### AirspaceVolume
- geometry: Polygon (horizontal) — exists
- floor_altitude (float + AltitudeReference — exists)
- ceiling_altitude (float + AltitudeReference)
- class: AirspaceClass
- type: AirspaceType

### AirspaceStatus [enum]
- Active, Inactive, Scheduled, Hot, Cold

### AirspaceSchedule
- volume_ref (AirspaceVolume)
- status (AirspaceStatus)
- active_times: list of TimeWindow
- NOTAM reference (optional)

### NOTAM
- type (string)
- effective_time, expiry_time (timestamps)
- description (text)
- affected_area (AirspaceVolume)

### FlightRestriction
- restriction_type: FlightRestrictionType
- value (float — altitude in meters, speed in m/s, etc.)
- applicable_to: entity type filter
- authority: issuing entity ref

FlightRestrictionType [enum]: AltitudeCeiling, AltitudeFloor, SpeedLimit, RouteRestriction, WeaponsFree, WeaponsHold

### Corridor
- geometry: Path3D with width (Path3D exists)
- floor, ceiling (altitudes)
- direction: CorridorDirection

CorridorDirection [enum]: OneWay, TwoWay

### AirspaceControlOrder (ACO)
- order_number
- effective_time, expiry_time
- sectors: list of (AirspaceVolume + assigned_to Entity/Organization ref)
- fire_support_coordination_measures: list of FSCM

FSCM (Fire Support Coordination Measure):
- type: FSCMType
- geometry (Line or Polygon)
- effective_time

FSCMType [enum]: FSCL (fire support coordination line), CFL (coordinated fire line), NFL (no-fire line), RFL (restrictive fire line), FFA (free-fire area), NFA (no-fire area), RFA (restrictive fire area), ACA (airspace coordination area)

---

## ROE / Rules of Engagement [Control → Directive]

### ROE
- rule_id (string)
- description (text)
- authority: Entity ref (who issued)
- effective_time, expiry_time

### ROESet
- rules: ordered list of ROE
- precedence_order (later rules override earlier if conflicting)

### WeaponsPosture [enum]
- WeaponsFree — engage any target not positively identified as friendly
- WeaponsTight — engage only targets positively identified as hostile
- WeaponsHold — engage only in self-defense or in response to formal order

### EngagementConstraint
- target_criteria: TargetCriteria
- weapon_constraints: list of WeaponType filter (which weapons may be used)
- authorization_level: WeaponsPosture
- collateral_distance_minimum (meters, optional)

### TargetCriteria
- faction_filter: list of Faction (exists)
- classification_filter: list of assessed types
- minimum_confidence (float 0-1)
- minimum_pid (bool — positive ID required)
- excluded_categories: list of types (hospitals, schools, etc.)

### EngagementAuthorization [Control → Directive, one-time permission]
- request_id
- target_ref (Track or Detection — exist)
- weapon_type
- authorized_by: Entity ref
- authorization_token (opaque, cf. ML auth tokens)
- expiry_time

### EscalationLevel [enum]
- ShowOfForce, WarningShot, Engage, Destroy

### ProportionalityAssessment [Data → Intel-adjacent]
- target_military_value (ordinal or score)
- collateral_damage_estimate: CollateralEstimate
- authorization_required (bool)

CollateralEstimate:
- civilian_casualties_estimate (int range)
- infrastructure_damage_estimate (DamageLevel — see BDA below)
- radius_of_effect (meters)

### PositiveIdentification (PID)
- required (bool)
- method: PIDMethod
- confidence_threshold (float 0-1)

PIDMethod [enum]: Visual, Electronic, Behavioral, Intelligence

Visual PID → observer_ref (Entity), description, confidence
Electronic PID → IFF_response (TransponderCodes — exists), emitter_match, confidence
Behavioral PID → observed_behavior_description, threat_indicators, confidence
Intelligence PID → intel_source_ref, corroboration_count, confidence

---

## EMCON / Emissions Control [Control → Directive, constraint on Communication]

### EMCONLevel [enum]
- Full — all emissions allowed
- Limited — restricted to specific carriers/protocols
- Restricted — only designated emissions
- Silent — no emissions whatsoever

### EMCONPolicy
- level: EMCONLevel
- exceptions: list of (CarrierType or ProtocolType — both exist) that are permitted
- effective_time, expiry_time
- area: Geometry (optional, geofenced EMCON)

### EmissionConstraint
- carrier_type (Carrier variant — exists)
- frequency_range: min_hz, max_hz (floats)
- power_limit_watts (float)
- allowed (bool)

### SignatureManagement [broader than just EM]
- radar: SignatureLevel
- infrared: SignatureLevel
- acoustic: SignatureLevel
- visual: SignatureLevel
- electromagnetic: EMCONLevel

SignatureType [enum]: Radar, Infrared, Acoustic, Visual, Electromagnetic, Cyber
SignatureLevel [enum]: Normal, Reduced, Minimal, Off

---

## Deconfliction [Control → Process, coordination to avoid conflict]

### DeconflictionType [enum]
- Altitude, Temporal, Lateral, Speed, Route, Frequency

### DeconflictionRule
- type: DeconflictionType
- parameters (type-specific, see below)
- applicable_to: entity/org filter
- authority: Entity ref
- effective_time, expiry_time

### AltitudeDeconfliction
- altitude_block_floor (altitude + ref)
- altitude_block_ceiling (altitude + ref)
- assigned_to: Entity ref
- time_window: TimeWindow

### TemporalDeconfliction
- time_window: TimeWindow
- area: Geometry
- assigned_to: Entity ref

### LateralDeconfliction
- corridor: Geometry (polygon or buffered path)
- buffer_distance (meters)
- assigned_to: Entity ref

### FrequencyDeconfliction
- frequency_band (carrier band — exists)
- channel_assignment
- assigned_to: Entity ref

### SeparationMinimum
- vertical_meters (float)
- horizontal_meters (float)
- temporal_seconds (float)
- applicable_between: pair of entity types or specific entity refs

### ConflictDetection [Data → Event-like]
- entities: pair of Entity refs
- conflict_type: DeconflictionType
- severity: ConflictSeverity
- predicted_time (timestamp)
- predicted_position (Position)

ConflictSeverity [enum]: Advisory, Caution, Warning, Critical

---

## BDA Results [Data → Intel]

### BDAResult
- target_ref (Track or Position — both exist)
- assessment_time (timestamp)
- assessor: Entity ref
- method: BDAMethod
- phase: BDAPhase
- damage: DamageAssessment
- imagery_ref (optional Media reference)
- restrike: RestrikeRecommendation (optional)

BDAMethod [enum]: Visual, ElectroOptical, Infrared, Radar, SignalIntel, HumanIntel
BDAPhase [enum]: Phase1_Initial, Phase2_Supplemental, Phase3_Restrike

### DamageAssessment
- damage_level: DamageLevel
- functional_impact: FunctionalImpact
- confidence (float 0-1)
- description (text)

DamageLevel [enum]: Undamaged, Light, Moderate, Heavy, Destroyed
FunctionalImpact [enum]: FullyOperational, Degraded, SignificantlyDegraded, NonOperational, Destroyed

### PhysicalDamage
- type: PhysicalDamageType
- extent: Geometry
- imagery_ref (optional)

PhysicalDamageType [enum]: Crater, Structural, Fire, Debris, Flooding

### RestrikeRecommendation
- recommended (bool)
- priority (int)
- weapon_type_suggested (optional)
- updated_target_position: Position (optional)
- justification (text)

### BDAStatusColor [enum — cf. Russian F2T2EA color coding]
- Grey (unknown/not assessed)
- Yellow (standby/awaiting assessment)
- Green (confirmed destroyed)
- Red (missed/restrike needed)

---

## Logistic Supply Chain [Control → Directive + Data → State + Object → Site]

### SupplyClass [enum — NATO supply classes]
- I (Subsistence/Rations)
- II (Clothing/Equipment)
- III (POL/Fuel)
- IV (Construction Materials)
- V (Ammunition)
- VI (Personal Items)
- VII (Major End Items — vehicles, weapons systems)
- VIII (Medical)
- IX (Repair Parts)
- X (Non-standard/Miscellaneous)

### SupplyItem
- supply_class: SupplyClass
- item_type (string — specific item name)
- quantity (float)
- unit_of_measure: UnitOfMeasure

UnitOfMeasure [enum — general purpose]:
- Each, Kilogram, Liter, Round, Box, Case, Pallet, Meter, SquareMeter, CubicMeter, Hour

### SupplyRequest [Control → Directive]
- requesting_unit: Organization ref
- items: list of SupplyItem
- priority: SupplyPriority
- delivery_location: Position
- required_by_time (timestamp)
- status: RequestStatus

SupplyPriority [enum]: Routine, Priority, Immediate, Emergency
RequestStatus [enum]: Submitted, Acknowledged, Approved, Denied, InTransit, Delivered, Cancelled

### SupplyPoint [Object → Site specialization]
- position: Position
- type: SupplyPointType
- capacity (by SupplyClass → max quantity)
- current_inventory: list of SupplyItem

SupplyPointType [enum]: Depot, ASP (ammo supply point), FARP (forward arming & refueling), Cache, AidStation, MaintenancePoint, DistributionPoint

### ConsumptionRate
- item_type (SupplyClass + specific type)
- rate_per_hour (float)
- unit_ref: Organization or Entity ref
- conditions (string — "combat", "garrison", etc.)

### SupplyRoute
- path: Path3D (exists)
- mode: RouteMethod (exists in CT)
- capacity_per_trip (weight or volume)
- security_level: ThreatLevel
- travel_time_estimate (duration)

ThreatLevel [enum]: Green (secure), Amber (possible threat), Red (active threat), Black (denied)

### ResupplyMission [Control → Task specialization]
- supply_request_ref
- assigned_to: Entity ref
- supply_point_ref
- delivery_window: TimeWindow
- status: LifecyclePhase (exists)

---

## Personnel / Casualty [Data → State of Person + Object → Entity → Actor → Person]

### PersonnelStatusType [enum]
- Present, Absent, WIA, KIA, MIA, Captured, Evacuated, OnLeave, Detached, Hospitalized, RTD (returned to duty)

### PersonnelStatus
- person_ref: Person ref
- status: PersonnelStatusType
- location: Position (optional)
- unit: Organization ref
- role (string)
- specialty (string — MOS/job code)

### CasualtyReport
- person_ref
- time (timestamp)
- location: Position
- cause: CasualtyCause
- severity: InjurySeverity
- treatment_status: TreatmentStatus
- evacuated_to (optional Site ref)

CasualtyCause [enum]: Combat, NonCombat, Accident, Disease, FriendlyFire
InjurySeverity [enum]: Minor, Serious, VSI (very seriously injured), Critical, Fatal
TreatmentStatus [enum]: Untreated, FirstAid, Stabilized, Evacuated, Hospitalized, RTD, Deceased

### PersonnelStrength
- unit_ref: Organization ref
- authorized (int)
- assigned (int)
- present (int)
- effective (int — present and fit for duty)
- casualties: CasualtyCount

### CasualtyCount
- KIA (int)
- WIA (int)
- MIA (int)
- captured (int)
- non_battle (int)

---

## MEDEVAC [Control → Directive + Control → Process → Plan]

Based on 9-line MEDEVAC request format.

### MEDEVACRequest
- request_id
- line1_location: Position
- line2_callsign (string), line2_frequency (float)
- line3_patients_by_precedence: map PrecedenceCategory → count
- line4_special_equipment: list of SpecialEquipment
- line5_patients_by_type: map PatientType → count
- line6_security: SecurityAtPickup
- line7_marking: MarkingMethod
- line8_nationality: Faction (exists) + nationality_string
- line9_cbrne: CBRNEContamination
- status: RequestStatus (from supply chain, reusable)

PrecedenceCategory [enum]: Urgent, UrgentSurgical, Priority, Routine, Convenience
SpecialEquipment [enum]: None, Hoist, ExtractionEquipment, Ventilator
PatientType [enum]: Litter, Ambulatory
SecurityAtPickup [enum]: NoEnemy, PossibleEnemy, EnemyInArea, EnemyContact
MarkingMethod [enum]: Panels, PyroSignal, Smoke, None, Other, IRStrobe, VSPanel
CBRNEContamination [enum]: None, Chemical, Biological, Radiological, Nuclear

### PatientInfo
- precedence: PrecedenceCategory
- type: PatientType
- nationality
- cbrne: CBRNEContamination
- injuries (text)

---

## Fire Support [Control → Directive → Task + Communication → Message → Command]

### CallForFire [Communication → Command specialization]
- observer_ref: Entity ref
- target_location: Position
- target_description (text)
- method_of_engagement: EngagementMethod
- fire_type: FireType
- danger_close (bool)
- target_number (string — alphanumeric ID)

EngagementMethod [enum]: PointTarget, AreaTarget, Suppression, Destruction, Neutralization, Illumination, Smoke, Marking
FireType [enum]: Immediate, Planned, OnCall

### AdjustFire / SpotCorrection
- direction: degrees or mils
- add_drop: meters (positive = add/long, negative = drop/short)
- left_right: meters (positive = right, negative = left)
- repeat (bool)
- fire_for_effect (bool)

Already partially modeled in ML SPLASH_CORRECTION. This is the reusable data shape.

### FireMission [Control → Task specialization]
- mission_id
- call_for_fire_ref
- assigned_unit: Organization ref
- weapon_type: WeaponType
- ammunition_type: AmmunitionType
- rounds_requested (int)
- trajectory: ShellTrajectory (optional)
- status: FireMissionStatus

WeaponType [enum]: Mortar, Howitzer, Rocket, MLRS, Missile, DirectFire, AirDelivered, Naval
AmmunitionType [enum]: HE, WP, Illumination, Smoke, DPICM, Thermobaric, HEAT, Frag, AP, Incendiary, Guided
ShellTrajectory [enum]: Low, High, Vertical

FireMissionStatus [enum]:
- Requested, Approved, Denied, ShotOut, SplashOver, RoundsComplete, EndOfMission, Cancelled, CheckFiring

### TargetList
- targets: list of TargetEntry

TargetEntry:
- target_id (alphanumeric)
- grid_reference: Position
- description (text)
- category (string)
- engagement_history: list of FireMission refs
- current_status: BDAStatusColor (from BDA section)

### EffectsAssessment
- fire_mission_ref
- effect_achieved: EffectAchieved
- BDA_ref (optional)

EffectAchieved [enum]: Destroyed, Neutralized, Suppressed, NoEffect, Unknown

---

## EW / Electronic Warfare [Control → Process → Action + Data → Intel]

### EWActionType [enum]
- Jam, Spoof, Deceive, Intercept, DirectionFind, Monitor, Deny

### EWAction
- type: EWActionType
- target_signal: Signal ref or frequency range
- platform_ref: Entity ref
- duration (seconds)
- area: Geometry (optional)
- power_watts (float, for active measures)
- status: LifecyclePhase (exists)

### JamType [enum]
- Noise, Barrage, Spot, Sweep, Responsive, Follower

### JamAction (specializes EWAction where type=Jam)
- jam_type: JamType
- frequency_range (min/max Hz)
- effectiveness_estimate (float 0-1)

### SpoofAction (specializes EWAction where type=Spoof)
- emulated_signal: Signal description
- intended_effect (text)

### DirectionFindingResult [Data → Intel]
- bearing_from_sensor (degrees)
- sensor_position: Position
- estimated_emitter_position: Position (optional — requires multiple bearings)
- confidence (float 0-1)
- signal_characteristics: Signal ref

### EWEffect [Data → Intel, assessment of effect]
- action_ref: EWAction
- observed_effect: EWEffectType
- confidence (float 0-1)
- duration_effective (seconds)

EWEffectType [enum]: SignalDegraded, SignalDenied, TargetDecoyed, CommunicationsDisrupted, NoEffect

### SpectrumAllocation [Control → Plan-adjacent]
- frequency_range: min_hz, max_hz
- assigned_to: Entity or Organization ref
- purpose (string)
- priority (int)
- time_window: TimeWindow
- exclusive (bool)

### ElectronicProtection
- measure_type: EPType
- applied_to: Carrier ref (exists)
- parameters (type-specific)

EPType [enum]: FrequencyHopping, SpreadSpectrum, Encryption, PowerControl, DirectionalAntenna, BurstTransmission

### ThreatEmitter [Data → Intel]
- emitter_notation: string (cf. LA EmitterNotation)
- location: Position
- signal_characteristics: Signal ref
- threat_assessment: ThreatLevel (reused from supply chain)
- associated_platform: Entity ref (optional)
- first_detected, last_detected (timestamps)

---

## Cyber [Data → State + Control → Process → Action]

### ConnectivityStatus [enum]
- Online, Degraded, Offline, Compromised, Unknown

### NetworkStatus [Data → State of a Node]
- node_ref: Node ref (exists)
- connectivity: ConnectivityStatus
- latency_ms (float)
- packet_loss_pct (float 0-100)
- throughput_bps (float)
- last_check_time (timestamp)

### CyberThreatType [enum]
- Intrusion, DenialOfService, Malware, Phishing, ManInTheMiddle, Spoofing, DataExfiltration, Ransomware

### ThreatSeverity [enum]
- Low, Medium, High, Critical

### CyberThreat [Data → Intel, detection of a cyber event]
- type: CyberThreatType
- severity: ThreatSeverity
- target: Node ref or network segment identifier
- time_detected (timestamp)
- indicator (string — IOC: IP, hash, signature, etc.)
- confidence (float 0-1)

### CyberActionType [enum]
- Defend, Exploit, Attack, Analyze, Recover, Isolate

### CyberAction [Control → Action specialization]
- type: CyberActionType
- target: Node ref or network segment
- operator: Entity ref
- status: LifecyclePhase (exists)
- description (text)

### CyberIncident [Data → Event]
- type: CyberThreatType
- affected_systems: list of Node refs
- impact_description (text)
- response_actions: list of CyberAction refs
- status: IncidentStatus

IncidentStatus [enum]: Detected, Investigating, Contained, Eradicated, Recovered, Closed

---

## ORBAT Aggregation [Data → Properties → Relationship + Object → Organization]

### ORBATNode (recursive tree)
- unit_ref: Organization ref
- parent_ref: Organization ref (optional — root has none)
- children: list of ORBATNode
- depth (int)
- echelon: Echelon

### Echelon [enum — NATO standard]
- FireTeam, Squad, Section, Platoon, Company, Battery, Troop,
  Battalion, Squadron, Regiment, Brigade, Division, Corps, Army,
  ArmyGroup, Theater
- Maps to existing UnitSize but with formal NATO naming

### ForceComposition (aggregate summary of a subtree)
- root: ORBATNode ref
- total_personnel: PersonnelStrength
- equipment_summary: list of EquipmentCount
- capability_summary: list of CapabilityEntry

### EquipmentCount
- equipment_type (string)
- operational (int)
- non_operational (int)
- in_maintenance (int)

### CapabilityEntry
- type: CapabilityType
- available (bool)
- capacity (float — subjective or numeric measure)
- readiness: ReadinessLevel

CapabilityType [enum]: DirectFire, IndirectFire, AirDefense, Reconnaissance, EW, Engineering, Medical, Logistics, Aviation, CBRN, Communications, CyberEW, AirAssault, Armor, Infantry, Artillery, SpecialOperations

ReadinessLevel [enum]: Full, Substantial, Marginal, NotReady

### TaskOrganization [Control → Directive-adjacent]
- effective_time (timestamp)
- purpose: Task or Mission ref
- organization: ORBATNode tree (the reorganized structure)
- attachments: list of UnitAttachment
- detachments: list of UnitAttachment

### UnitAttachment
- unit_ref: Organization ref
- from_parent: Organization ref
- to_parent: Organization ref
- attachment_type: AttachmentType
- effective_time, expiry_time

AttachmentType [enum]: Attached, OPCON, TACON, DS (direct support), GS (general support), Reinforcing, GSR (general support reinforcing)

---

## Simultaneous Control Capacity [Data → Properties → Parameters]

### ControlCapacity
- controller_ref: Entity ref (operator or GCS)
- max_simultaneous (int)
- current_count (int)
- link_type: ProtocolType (exists)
- bandwidth_per_unit (bps, float)
- latency_budget_ms (float)

### LinkBudget
- carrier_ref: Carrier ref (exists)
- total_bandwidth_bps (float)
- allocated_bandwidth_bps (float)
- available_bandwidth_bps (float)
- max_connections (int)
- current_connections (int)

### OperatorWorkload
- operator_ref: Person ref
- assigned_units: list of Entity refs
- workload_level: WorkloadLevel
- max_capacity (int)

WorkloadLevel [enum]: Idle, Low, Moderate, High, Saturated

### ControlHandoff [Control → Process → Action]
- from_controller: Entity ref
- to_controller: Entity ref
- unit: Entity ref
- handoff_time (timestamp)
- authorization_token (cf. ML auth tokens)
- status: HandoffStatus

HandoffStatus [enum]: Requested, Approved, InProgress, Complete, Rejected, Cancelled

---

## Mission Debrief / After Action [Data → Information → Properties of completed Task; also Item → Record]

### AfterActionReport
- mission_ref: Task ref
- time_prepared (timestamp)
- prepared_by: Entity ref
- classification (string)
- situation_summary (text)
- timeline: MissionTimeline
- assessment: PerformanceAssessment
- statistics: StatisticsBlock
- lessons: list of LessonLearned

### MissionTimeline
- events: chronologically ordered list of TimelineEvent

TimelineEvent:
- time (timestamp)
- description (text)
- event_type: TimelineEventType
- location: Position (optional)
- actor: Entity ref (optional)

TimelineEventType [enum]: Decision, Action, Contact, Casualty, EquipmentFailure, Communication, PhaseTransition, WeatherChange, Other

### PerformanceAssessment
- unit_ref: Organization ref
- mission_ref: Task ref
- objectives_achieved: list of ObjectiveResult
- overall_assessment (text)

ObjectiveResult:
- objective_ref: Objective ref (exists)
- achieved (bool)
- partial_completion (float 0-1, optional)
- notes (text)

### LessonLearned
- category (string)
- observation (text — what happened)
- discussion (text — why it matters)
- recommendation (text — what to change)
- assigned_to: Entity or Organization ref (optional)
- priority: LessonPriority

LessonPriority [enum]: Critical, Important, Routine

### StatisticsBlock
- sorties_flown (int)
- flight_hours (float)
- munitions_expended: list of (AmmunitionType, count)
- targets_engaged (int)
- targets_destroyed (int)
- targets_damaged (int)
- casualties_friendly: CasualtyCount
- casualties_enemy_estimate: CasualtyCount
- equipment_lost: list of EquipmentCount
- consumables_used: list of SupplyItem

---

## Sensor Fusion Rules [Control → Process → Method + Data → Intel]

### FusionMethod [enum]
- NearestNeighbor, Bayesian, DempsterShafer, KalmanFilter, CovarianceIntersection, Voting, WeightedAverage

### FusionRule
- name (string)
- inputs: list of sensor type or detection source identifiers
- method: FusionMethod
- output_type: (Track update, Classification update, or new Detection)
- confidence_adjustment_formula (text or reference)

### DetectionCorrelation [Data → Intel, association assessment]
- detection_a_ref: Detection ref (exists)
- detection_b_ref: Detection ref
- spatial_score (float 0-1) — proximity in space
- temporal_score (float 0-1) — proximity in time
- classification_score (float 0-1) — similarity of assessed type
- overall_correlation_score (float 0-1)
- correlated (bool)

### TrackAssociation
- track_ref: Track ref (exists)
- new_detection_ref: Detection ref
- association_score (float 0-1)
- gate_type: GateType
- within_gate (bool)

GateType [enum]: Rectangular, Ellipsoidal, Mahalanobis
— Gate uses position covariance (cf. LA TMat3 position_enu_cov)

### FusionPriority
- sensor_type (string)
- priority (int — lower is higher priority)
- reliability_score (float 0-1)
- freshness_weight (float — how fast confidence decays with age)
- positional_accuracy_meters (float)

### TrackManagement
- track_id
- state: TrackState
- tentative_hit_count (int)
- confirmed_threshold (int — hits required to promote from Tentative)
- coast_timeout_seconds (float — time with no updates before Coasting)
- max_coast_seconds (float — time before Dropped)
- last_update_time (timestamp)
- update_count (int)

TrackState [enum]: Tentative, Confirmed, Coasting, Dropped

### ConflictResolution (when sources disagree)
- conflicting_sources: list of (source_id, claimed_value, confidence)
- resolution_method: ResolutionMethod
- resolved_value
- resolution_confidence (float 0-1)

ResolutionMethod [enum]: HighestConfidence, MostRecent, WeightedAverage, ManualOverride, Voting

---

## OPORD / Orders Schema [Control → Directive + Item → Record]

### OPORD
- order_number (string)
- dtg: timestamp (date-time group)
- issuing_unit: Organization ref
- classification (string)
- references: list of document references
- paragraph_1: Situation
- paragraph_2: Mission
- paragraph_3: Execution
- paragraph_4: Sustainment
- paragraph_5: CommandAndSignal

### Paragraph 1 — Situation

Situation:
- enemy: EnemyAssessment
- friendly: FriendlyForces
- attachments_detachments: list of UnitAttachment (from ORBAT section)
- civil_considerations (text)
- terrain_weather: TerrainWeatherAssessment

EnemyAssessment:
- composition: ForceComposition (from ORBAT section)
- disposition (text — where they are and how arranged)
- strength_estimate (text)
- most_probable_coa: CourseOfAction
- most_dangerous_coa: CourseOfAction
- known_capabilities: list of CapabilityType (from ORBAT section)
- known_limitations (text)

CourseOfAction:
- name (string)
- description (text)
- objectives: list of Objective refs (exists)
- timeline: list of (phase_name, time_estimate)
- forces_required: ForceComposition (optional)
- indicators: list of (indicator description, how detected)

FriendlyForces:
- higher_unit: Organization ref
- higher_mission: text
- higher_intent: CommanderIntent
- adjacent_units: list of AdjacentUnit
- supporting_units: list of SupportingUnit

AdjacentUnit:
- unit_ref: Organization ref
- mission_summary (text)
- boundary: Geometry (line — shared boundary)
- contact_info: callsign, frequency

SupportingUnit:
- unit_ref: Organization ref
- support_type: AttachmentType (DS, GS, Reinforcing, etc.)
- capabilities: list of CapabilityType
- contact_info: callsign, frequency

TerrainWeatherAssessment:
- terrain_summary (text — OAKOC: Observation, Avenues of approach, Key terrain, Obstacles, Cover/concealment)
- weather_summary (text — from WeatherForecast)
- effects_on_friendly_operations (text)
- effects_on_enemy_operations (text)
- light_data: SunMoonData

SunMoonData:
- sunrise, sunset (timestamps)
- moonrise, moonset (timestamps)
- moon_phase (string)
- BMNT (begin morning nautical twilight)
- EENT (end evening nautical twilight)
- illumination_percent (float)

### Paragraph 2 — Mission

MissionStatement:
- who: Organization ref
- what: task verb + object (text)
- when: timestamp or condition
- where: Position or area (Geometry)
- why: purpose (text)
— Single sentence: "WHO does WHAT, WHEN, WHERE, in order to WHY"

### Paragraph 3 — Execution

Execution:
- intent: CommanderIntent
- concept_of_operations (text)
- scheme_of_maneuver (text)
- tasks_to_subordinates: list of SubordinateTask
- coordinating_instructions: CoordinatingInstructions
- fire_support_plan (optional, references FireMission list)

CommanderIntent:
- purpose (text — the "why")
- key_tasks: list of text (things that must happen)
- end_state (text — what the world looks like when we're done)

SubordinateTask:
- unit_ref: Organization ref
- task_description (text)
- purpose (text)
- priority (int)
- on_order (bool — execute on command vs. immediately)

CoordinatingInstructions:
- timeline: list of (phase_name, trigger or time)
- phase_lines: list of PhaseLine
- checkpoints: list of Checkpoint
- boundaries: list of Boundary
- fire_support_coordination: list of FSCM (from Airspace section)
- movement_instructions (text)
- rules_of_engagement: ROESet ref
- EMCON: EMCONPolicy ref
- risk_reduction_measures (text)

PhaseLine:
- name (string — typically a codename)
- geometry: Line (exists — on the map)
- significance (text)

Checkpoint:
- name (string)
- position: Position
- purpose (text)

Boundary:
- between: pair of Organization refs
- geometry: Line (exists)

### Paragraph 4 — Sustainment

Sustainment:
- logistics: LogisticsPlan
- maintenance: MaintenancePlan
- medical: MedicalPlan
- personnel: PersonnelPlan
- transportation: TransportationPlan

LogisticsPlan:
- supply_points: list of SupplyPoint refs (from supply chain section)
- supply_routes: list of SupplyRoute refs
- class_specific_instructions: map SupplyClass → text

MaintenancePlan:
- maintenance_collection_point: Position
- recovery_priorities: list of equipment types
- instructions (text)

MedicalPlan:
- casualty_collection_point: Position
- medevac_plan (text or MEDEVACRequest template)
- aid_station: Position
- evacuation_routes: list of SupplyRoute refs

PersonnelPlan:
- replacement_priorities (text)
- strength_reporting_schedule (text)

TransportationPlan:
- movement_priorities: list of Organization refs
- routes: list of SupplyRoute refs
- mode: RouteMethod (exists)

### Paragraph 5 — Command and Signal

CommandAndSignal:
- command_posts: list of CommandPost
- succession_of_command: ordered list of Entity refs (by rank/position)
- signal: CommunicationPlan

CommandPost:
- type: CommandPostType
- position: Position
- callsign (string)
- operational_time: TimeWindow

CommandPostType [enum]: Main, Tactical, Alternate, Rear

CommunicationPlan:
- primary_net: NetEntry
- alternate_net: NetEntry
- contingency_net: NetEntry
- emergency_net: NetEntry
- running_password (string)
- challenge_response: pair (challenge_word, response_word)
- codewords: map string → string (codeword → meaning)
- pyrotechnics: map color → meaning

NetEntry:
- frequency (float)
- callsign (string)
- protocol: ProtocolType (exists)
- encryption: bool
- backup_frequency (optional float)

---

# RECURRING INFERRED META-PATTERNS

Patterns that appear across multiple inferred concept trees above.
These are not new ontology nodes but structural observations that
the typology and schema stages must account for.

## Confidence (float 0-1)
Appears on: Detection, Classification, Track, DamageAssessment,
PositiveIdentification, DetectionCorrelation, TrackAssociation,
EWEffect, CyberThreat, ConflictResolution, FusionPriority.
Universal enough to be a named scalar type, not just raw float.

## TimeWindow
- start_time, end_time (timestamps)
- Appears on: AirspaceSchedule, DeconflictionRule, EMCONPolicy,
  SupplyRequest delivery, OperationalTime, ROE validity, SpectrumAllocation.
Already implied by Time in Reference but needs an explicit struct.

## RequestStatus lifecycle
- Submitted → Acknowledged → Approved/Denied → InTransit → Delivered/Cancelled
- Appears on: SupplyRequest, MEDEVACRequest, EngagementAuthorization, ControlHandoff.
- Superset of LifecyclePhase (which is Planned→Active→Complete) — needs a broader enum
  or LifecyclePhase needs extension.

## Severity / Intensity ordinal pattern
- Multiple enums follow the same None → Light → Moderate → Severe → Extreme/Critical pattern:
  IcingIntensity, TurbulenceIntensity, DamageLevel, ThreatSeverity, ConflictSeverity,
  InjurySeverity, WorkloadLevel, ReadinessLevel.
- These are NOT the same enum (they have different values), but the pattern is universal.

## Authorization pattern
- Request → Approval → Token → Expiry
- Appears on: EngagementAuthorization, ControlHandoff, ESAD arming (ML), TARGET_HANDOVER (ML).
- Structural: requester, authorizer, subject, token, expiry_time, status.

## Recursive tree pattern
- Parent → children → grandchildren with aggregation flowing upward
- Appears on: ORBATNode, TaskDecomposition, OPORD paragraphs, AirspaceVolume containment.
- Common operations: aggregate upward, filter by depth, find path to root.

## Reference-by-ID pattern
- Nearly every struct references others by ID rather than composition.
- Entity ref, Organization ref, Task ref, Detection ref, Track ref, etc.
- Implies a universal identifier type (uuid4 per Identity — already exists) and
  typed references (ref to what kind of thing).

---

# EXPANSION PASS 2 — FILLING GAPS

Everything below expands concepts that were thin, missing, or only
partially represented in the original dump. Same source key applies
where traceable; unmarked entries are inferred from domain knowledge.

---

## OBJECT — Gaps

### Entity → Actor → Agent (AI-specific)
- AgentType [enum]: LLM, VisionModel, PlanningAgent, ControlAgent, FusionAgent, ClassificationAgent
- AgentCapability: inference_types (list: text, vision, multimodal, tool_use, code), context_capacity, response_latency_ms
- AgentConfiguration: model_id, prompt/instruction_set_ref (Record ref), tool_manifest (list of available actions), temperature, constraints
- AgentSession: session_id, agent_ref, start_time, token_count, state (Active, Suspended, Terminated)

### Entity → Machine → Vehicle (missing domains)
Vehicle only has LandVehicle. Missing:
- AirVehicle (manned aircraft): FixedWing, RotaryWing, Tiltrotor, Lighter-Than-Air
- SeaVehicle: SurfaceVessel, Submarine (manned)
- SpaceVehicle: Spacecraft, SpaceStation, LaunchVehicle

AirVehicleClass [enum]: Fighter, Bomber, Transport, Tanker, Trainer, Reconnaissance, Helicopter, Tiltrotor, LighterThanAir
SeaVehicleClass [enum]: Frigate, Destroyer, Carrier, Submarine, Patrol, Amphibious, Auxiliary, Merchant

### Entity → Machine → Robot (airframe/hull specifics)
Missing airframe granularity for AirRobot:
- MultirotorConfig [enum]: Quad, Hex, Octo, Coaxial, Y6, X8
- FixedWingConfig [enum]: Conventional, FlyingWing, Canard, TandemWing, BlendedWingBody, Delta
- VTOLConfig [enum]: Tiltrotor, Tailsitter, LiftAndCruise, QuadPlane, CopterPlane
- PropulsionType [enum]: Electric, Gasoline, Diesel, Turbine, Hybrid, Hydrogen, Solar
- LaunchMethod [enum]: HTOL (horizontal takeoff/landing), VTOL, CATAPULT, HandLaunch, RailLaunch, TubeLaunch, DropLaunch, BalloonLaunch
- RecoveryMethod [enum]: HTOL, VTOL, Parachute, DeepStall, NetRecovery, SkyHook, BellyLand, Ditching

### Entity → Machine → Platform (missing variants)
- GroundControlStation (GCS): fixed or mobile, number of operator stations, supported protocols
- MobileCommandPost: vehicle_ref, communications_suite, battle_management_system
- RelayStation: coverage_area (Geometry), supported_carriers (list of Carrier), gain_dBm
- ChargingStation: connector_types, max_simultaneous, power_output_watts
- LaunchPad: supported_launch_methods, max_vehicle_weight_kg, orientation
- RecoverySystem: recovery_method, max_vehicle_weight_kg, cycle_time_seconds

### Organization (missing concepts)
- CommandRelationship [enum]: OPCON (operational control), TACON (tactical control), ADCON (administrative control), SUPCON (support), DIRLAUTH (direct liaison authority)
- SupportRelationship [enum]: DirectSupport, GeneralSupport, Reinforcing, GeneralSupportReinforcing
- CommandRelationshipEntry: subordinate (Organization ref), superior (Organization ref), type (CommandRelationship), effective_time, expiry_time
- Coalition/Alliance structure: national_caveats (text), interoperability_level, shared_classification_ceiling

### Collection (no speciation exists — adding)
- Convoy: ordered list of Entity refs, route (Path3D), spacing_meters, speed_kph, lead_vehicle_ref
- Formation (tactical): formation_type (FormationType), members (ordered Entity refs), spacing, reference_entity
- FormationType [enum]: Line, Column, Wedge, Vee, Echelon (Left/Right), Diamond, Staggered Column, Box, File, Herringbone, Coil
- TaskGroup: ad-hoc collection of assets assembled for a specific task, task_ref, members
- SensorNetwork: sensors (list of Entity refs with Sensor payloads), coverage_area, fusion_method
- TargetDeck: ordered list of target refs with priority and engagement status
- Minefield: boundary (Polygon), mine_type, density, marking_status (Marked, Unmarked, Mixed)

### System (no speciation exists — adding)
- WeaponSystem: platform_ref (Machine), weapon_ref (Item→Equipment), fire_control_ref, ammunition_types, max_effective_range, min_engagement_range, rate_of_fire
- CommunicationSystem: nodes (list of Node refs), transports (list of Transport refs), coverage_capability
- SensorSuite: sensors (list of Sensor refs), fusion_capability (bool), primary_mode
- FireControlSystem: sensor_ref, weapon_ref, tracking_mode, engagement_capability
- EWSuite: sensors, jammers, direction_finders, controller
- NavigationSystem: primary_source (GPS, INS, SLAM, VIO, Optical Flow), backup_sources, accuracy_class
- C2System: battle_management_platform, communications, displays, personnel
- IntegratedAirDefenseSystem (IADS): radars, launchers, C2 node, engagement_zones
- PowerSystem: sources (list of PowerSource), distribution, total_capacity, current_load

### Site (missing military site types)
- ForwardOperatingBase (FOB): perimeter (Polygon), facilities, garrison (Organization ref)
- ObservationPost (OP): position, sector_of_observation (arc geometry), manned_by (Entity ref)
- Checkpoint: position, manning (Entity ref), purpose (security, traffic control, liaison)
- RallyPoint: type (RallyPointType), position, purpose
- RallyPointType [enum]: ObjectiveRallyPoint (ORP), InitialRallyPoint, ActionPoint, LinkupPoint, AlternateRallyPoint
- AttackPosition: position, concealment_rating, sector_of_fire (arc geometry), assigned_to
- SupportByFirePosition: position, sector_of_fire, weapons_emplaced
- LineOfDeparture: geometry (Line), H_hour (timestamp), unit_crossing_order
- AssaultPosition: position, covered_approach (bool), distance_to_objective_m
- BreachPoint: position, obstacle_type, breach_method
- DropZone (DZ): boundary (Polygon), surface, approach_heading, wind_limits, marking
- HelicopterLandingZone (HLZ): position, size, surface, obstacles, approach/departure_headings, marking
- PickupZone (PZ): same structure as HLZ + load plan
- AmmunitionSupplyPoint (ASP): position, stored_classes (list of SupplyClass), security
- PatrolBase: position, perimeter, security_plan, duration
- HidePosition: position, concealment_rating, for_entity (Entity ref)
- TriggerPoint: position, event_on_reach (what action triggers)
- NamedAreaOfInterest (NAI): geometry (Polygon), purpose, observed_by, indicators_to_watch
- TargetAreaOfInterest (TAI): geometry (Polygon), target_types_expected, fire_support_plan_ref

### Item → Equipment (no speciation — adding)
- PersonalWeapon: type (WeaponCategory), caliber, effective_range_m, rate_of_fire, weight_kg
- WeaponCategory [enum]: Rifle, Carbine, Pistol, MachineGun, GrenadeLauncher, AntiTank, ManPAD, Mortar, Sniper, Shotgun
- Optic: type (OpticType), magnification_range, field_of_view, night_capable (bool)
- OpticType [enum]: RedDot, LPVO, FixedMagnification, Binoculars, Rangefinder, ThermalSight, NightVision (NVG), LaserDesignator
- CommunicationsGear: radio_type, frequency_range, power_watts, crypto_capable (bool), weight_kg
- ProtectiveGear: type (ProtGearType), protection_level
- ProtGearType [enum]: BodyArmor, Helmet, CBRN_Suit, EyeProtection, HearingProtection
- NavigationEquipment: type (NavEquipType), accuracy_m
- NavEquipType [enum]: GPS_Receiver, Compass, Map, Altimeter, DAGR (Defense Advanced GPS Receiver), PLGR, ATAK_Device

### Item → Payload (categories missing)
- PayloadCategory [enum]: EO_Camera, IR_Camera, Multispectral, LIDAR, SAR, SIGINT_Receiver, CommRelay, CargoDropper, Weapon, Jammer, Illuminator, ChemicalDetector, RadiationDetector, Loudspeaker, Leaflet
- CameraPayload: type (EO, IR, Multispectral), resolution, frame_rate, field_of_view, zoom_range, stabilized (bool), weight_kg, power_draw_watts
- LIDARPayload: range_m, points_per_second, field_of_view, weight_kg
- SARPayload: resolution_m, swath_width_m, modes (Spotlight, Stripmap, ScanSAR)
- CommRelayPayload: supported_protocols, range_extension_km, bandwidth_bps, latency_added_ms
- WeaponPayload: weapon_type, guidance_type (GuidanceType), warhead_type, weight_kg, max_range_m
- GuidanceType [enum]: Unguided, GPS, INS, LaserGuided, IRHoming, RadarHoming, CommandGuided, Wire, FiberOptic, Terminal_TV, Vision

### Item → Component (adding)
- ComponentCategory [enum]: Motor, ESC, Battery, FlightController, Antenna, Gimbal, Servo, Propeller, Airframe, LandingGear, Parachute, Transponder, ADS_B, IFF
- ComponentHealth: component_ref, operational (bool), hours_since_maintenance, hours_total, next_maintenance_due, firmware_version

---

## REFERENCE — Gaps

### Measurement Units (general purpose, missing)
DistanceUnit [enum]: Meters, Kilometers, Feet, Yards, NauticalMiles, StatuteMiles
MassUnit [enum]: Kilograms, Pounds, Ounces, Tons_Metric, Tons_Short
VolumeUnit [enum]: Liters, Gallons_US, Gallons_Imperial, CubicMeters
AngleUnit [enum]: Degrees, Radians, Mils_NATO (6400), Mils_Warsaw (6000), Gradians
ForceUnit [enum]: Newtons, PoundsForce
PowerUnit [enum]: Watts, Kilowatts, Horsepower
FrequencyUnit [enum]: Hertz, Kilohertz, Megahertz, Gigahertz
DataRateUnit [enum]: BitsPerSecond, KilobitsPerSecond, MegabitsPerSecond
PercentageUnit: always 0-100 float, but worth naming for clarity

### Angular types (missing from geometry)
- Bearing: value (float 0-360), reference (BearingReference)
- BearingReference [enum]: TrueNorth, MagneticNorth, GridNorth, RelativeToHeading
- Heading: value (float 0-360), reference (BearingReference) — direction of travel
- Course: value (float 0-360), reference (BearingReference) — intended/planned direction
- AzimuthElevation: azimuth (float 0-360), elevation (float -90 to +90), reference
- MagneticDeclination: value (degrees east/west), date_of_validity, location

### Accuracy / Precision (partially covered, needs structure)
- CEP: Circular Error Probable (meters) — 50% probability radius
- LEP: Linear Error Probable (meters) — vertical
- SEP: Spherical Error Probable (meters) — 3D
- Sigma1/Sigma2: 1-sigma (68%) and 2-sigma (95%) confidence radii
- DRMS: Distance Root Mean Square
- PositionAccuracy: horizontal_accuracy_m, vertical_accuracy_m, method (AccuracyMethod)
- AccuracyMethod [enum]: Calculated, Estimated, Measured, Surveyed, Unknown
- CovarianceMatrix3x3: already exists as TMat3, but worth noting it's used for position_enu_cov AND velocity_enu_cov

### Color (used in marking, symbology, visual)
- Color: r, g, b, a (uint8 each) [LA: Color type]
- MilColor [enum]: Red, Blue, Green, Yellow, Orange, Purple, White, Black, Brown, Pink — NATO standard map colors
- MarkerColor [enum]: for pyrotechnics and signals — Red, Green, Yellow, White, IR, Orange, Violet, Blue

### Geometric additions
- Arc: center (Position), radius_m, start_angle, end_angle — sector of fire/observation
- Annulus: center, inner_radius_m, outer_radius_m — range rings, engagement zones
- Corridor: centerline (Path3D), width_m, floor_altitude, ceiling_altitude
- Frustum: apex (Position), direction (AzimuthElevation), horizontal_fov, vertical_fov, near_range_m, far_range_m — sensor field of view
- Orbit: center (Position), radius_m, altitude, direction (CW/CCW), speed — loiter pattern
- Racetrack: point_a (Position), point_b (Position), width_m, altitude, direction
- Sector: center (Position), radius_m, start_bearing, end_bearing — sector of responsibility

### Time additions
- H_Hour: reference timestamp from which all phase times are offset (H+30 = H_hour + 30 min)
- PhaseTime: h_hour_ref, offset_minutes — "H+45" = 45 minutes after H
- Zulu/Local distinction: all timestamps are UTC (Zulu), local time derived from position
- TimeSyncSource [enum]: GPS, NTP, PTP (IEEE 1588), Manual, RadioTimeSignal
- Staleness: age_seconds since last update, threshold beyond which data is considered stale

### Type additions
- MilitaryBranch [enum]: Army, Navy, AirForce, Marines, CoastGuard, SpaceForce, SpecialOperations, Joint
- UnitFunction [enum]: Maneuver, FireSupport, AirDefense, Aviation, Engineer, Signal, Military Intelligence, Military Police, CBRN, Logistics, Medical, Civil Affairs, PsyOps, SOF
- WarfareType [enum]: Conventional, Unconventional, Guerrilla, Hybrid, Asymmetric, Information, Cyber, Electronic
- ThreatLevel already exists but broader: Green (secure), Amber (possible threat), Red (active threat), Black (denied/impassable)
- PACE [enum]: Primary, Alternate, Contingency, Emergency — used for comm plans, routes, anything with backup layers
- ClassificationCaveat [enum]: NOFORN, REL_TO (with country list), FVEY, NATO, EU, COSMIC, ATOMAL — caveats on classification

---

## CONTROL — Gaps

### Directive additions

#### Standing Orders / SOPs
- StandingOrder: applies_to (Organization ref), conditions (text), actions (text), authority (Entity ref), effective indefinitely until rescinded
- SOP (Standard Operating Procedure): procedure_id, title, applies_to, steps (ordered list of text), last_updated, version

#### Contingency Planning
- BranchPlan: parent_plan_ref, trigger_condition (text or Event ref), actions (Plan ref), probability_assessment (text)
- SequelPlan: follows_plan_ref, conditions_for_transition (text), actions (Plan ref)
- WARNO (Warning Order): order_number, issuing_unit, dtg, situation_summary, earliest_move_time, orders_group_time, initial_tasks
- FRAGO (Fragmentary Order): order_number, references_opord, changes_only (list of changed paragraphs), effective_time

#### Abort / Emergency
- AbortCriteria: conditions (list of AbortCondition), authority (Entity ref), automatic (bool)
- AbortCondition: type (AbortType), threshold, description
- AbortType [enum]: BatteryBingo, FuelBingo, CommsLost, DamageSustained, WeatherBelow, MissionTimeout, HostileContact, GeofenceBreach, ManualAbort, EquipmentFailure
- EmergencyProcedure: trigger (AbortType), immediate_action (text), subsequent_actions (text), rally_point (Position)

#### Trigger / Condition
- TriggerCondition: type (TriggerType), parameters, evaluation_method (Automatic, Manual)
- TriggerType [enum]: TimeReached, PositionReached, EventOccurred, ThresholdExceeded, ConditionMet, OrderReceived, EnemyAction, FriendlyAction
- ConditionalExecution: condition (TriggerCondition), if_true (Action/Task ref), if_false (Action/Task ref, optional)

### Process additions

#### Movement Techniques
- MovementTechnique [enum]: Traveling, TravelingOverwatch, BoundingOverwatch, SuccessiveBounds, AlternatingBounds
- MovementFormation [enum]: Column, Staggered Column, Wedge, Line, Echelon, Vee, Diamond, File, Box, Herringbone, Coil
- MovementRate [enum]: Normal, Deliberate, Hasty, Forced, Administrative

#### Approach / Attack Methods
- ApproachMethod [enum]: Frontal, Flanking, Envelopment, TurningMovement, Infiltration, Penetration
- AttackType [enum]: Deliberate, Hasty, Spoiling, Counterattack, Raid, Ambush, Feint, Demonstration
- DefenseType [enum]: AreaDefense, MobileDefense, Retrograde, Delay, Withdrawal, Retirement

#### Waypoint Types (missing detail)
- WaypointType [enum]: Flyover, Flyby, Loiter, Orbit, Landing, Takeoff, Photo, Survey, Delivery, Relay, Rendezvous, IP (Initial Point), CP (Contact Point), RP (Release Point), SP (Start Point), PP (Passage Point), LP (Linkup Point), TurnPoint, HoldPoint
- WaypointAction [enum]: None, TakePhoto, StartVideo, StopVideo, DropPayload, ActivateSensor, DeactivateSensor, ChangeAltitude, ChangeSpeed, Loiter, SetROI (region of interest), TriggerCamera, SetGimbal, SetRelay, RepeatServo

#### Coordination Measures
- GraphicControlMeasure: type (GCMType), geometry (Line or Polygon or Point), name, applies_to, effective_time
- GCMType [enum]: PhaseLine, ObjectiveArea, AssemblyArea, AttackPosition, SBFPosition, Boundary, Checkpoint, ContactPoint, CoordinationPoint, FinalCoordinationLine, LOA (limit of advance), LimitOfAdvance, LineOfDeparture, FLOT (forward line of own troops), FEBA (forward edge of battle area), MainSupplyRoute, AlternateSupplyRoute, Route, Axis, DirectionOfAttack, PassagePoint, ReleasePoint, StartPoint, TriggerLine

#### Obstacle Planning
- ObstaclePlan: obstacles (list of PlannedObstacle), breach_plan (optional BreachPlan)
- PlannedObstacle: type (ObstacleType — exists), position, geometry, intent (ObstacleIntent)
- ObstacleIntent [enum]: Disrupt, Turn, Fix, Block
- BreachPlan: breach_point, breach_method (BreachMethod), breach_force, support_force, assault_force
- BreachMethod [enum]: Deliberate, Hasty, InStride, Covert

### Interface additions
- MAVLink command ID mapping (specific actions to MAVLink CMD IDs)
- MSPv2 command mapping
- Meshtastic packet types
- SerialCommand: baud, parity, stop_bits, data_bits, command_bytes
- CANBusMessage: arbitration_id, data (bytes), dlc (data length code)
- PWMRange: min_us, center_us, max_us, channel_id, function

---

## COMMUNICATION — Gaps

### Serialization / Encoding
- SerializationFormat [enum]: Protobuf, JSON, XML, CBOR, MessagePack, FlatBuffers, Avro, BSON, Binary_Custom, ASCII_Text
- CompressionType [enum]: None, GZIP, LZ4, Zstd, Snappy, Deflate
- Endianness [enum]: LittleEndian, BigEndian, NetworkOrder

### Quality of Service
- QoS: latency_max_ms, bandwidth_min_bps, reliability (QoSReliability), priority (int)
- QoSReliability [enum]: BestEffort, AtLeastOnce, ExactlyOnce, Guaranteed
- DataPrecedence [enum]: Routine, Priority, Immediate, Flash, FlashOverride, CRITIC (military message precedence)

### Message Routing
- RoutingMode [enum]: Unicast, Multicast, Broadcast, Anycast, PubSub, RequestReply, StoreAndForward
- Topic: namespace, name — for publish/subscribe systems (MQTT, ROS, etc.)
- MessageQueue: topic, max_depth, overflow_policy (Drop, Block, DropOldest)
- Subscription: subscriber (Node ref), topic, filter (optional predicate), QoS

### Communication Security
- COMSEC: encryption_algorithm, key_material_ref, key_changeover_schedule
- TRANSEC: frequency_hopping_set, hop_rate, synchronization_method
- EMSEC: emission_limits, shielding_requirements
- EncryptionType [enum]: None, AES128, AES256, ChaCha20, Type1 (NSA approved), Type2, Type3, Custom
- KeyManagement: key_id, algorithm, effective_time, expiry_time, distribution_method (Manual, OTAR, OTAD)

### Data Link Types (specific)
- DataLinkType [enum]: CDL (Common Data Link), TCDL (Tactical CDL), SADL (Situational Awareness Data Link), Link16, Link22, JREAP, BACN, BLOS (Beyond Line of Sight), DAMA, HaveQuick, SINCGARS, ARC_210
- Link16Specifics: JTIDS_Unit_Number, net_number, time_slot_assignment, NPG (Network Participation Group)
- SATCOMBand [enum]: UHF, SHF, EHF, Ka, Ku, X, C, L, S
- SATCOMTerminal: terminal_type, supported_bands, data_rate_bps, antenna_diameter_m, orbit_type (LEO, MEO, GEO)

### Mesh Networking
- MeshNodeRole [enum]: Router, Endpoint, Repeater, Gateway, BorderRouter
- MeshRoutingProtocol [enum]: AODV, OLSR, Babel, Batman, Custom
- MeshMetrics: hop_count, route_metric, last_heard (timestamp), SNR_dB, RSSI_dBm

### Node additions
- NodeType [enum]: Sensor, Effector, C2, Relay, Gateway, Observer, All
- NodeCapabilities: can_transmit (bool), can_receive (bool), can_relay (bool), can_process (bool)
- NetworkInterface: node_ref, carrier_ref, address (string), port (int), state (Up, Down, Degraded)

### Feed additions
- StreamEncoding [enum]: H264, H265, VP8, VP9, AV1, MJPEG, RAW, PCM, AAC, Opus
- StreamTransport [enum]: RTP, RTSP, SRT, HLS, WebRTC, MPEG_TS, NDI, RTMP
- StreamMetadata: codec, resolution_w, resolution_h, fps, bitrate_bps, keyframe_interval, latency_ms, source_entity_ref

### Message additions
- MessagePriority [enum]: Routine, Priority, Immediate, Flash, FlashOverride — military precedence
- MessageClassification: level (ClassificationLevels — exists), caveats (list of ClassificationCaveat), releasability (text)
- MessageEnvelope: id, timestamp, source_node, destination_nodes (list), priority, classification, ttl_seconds, sequence_number, correlation_id (for request/reply), retry_count
- AcknowledgmentPolicy [enum]: None, OnReceipt, OnProcessing, OnExecution
- DeliveryReceipt: message_id, received_by (Node ref), time_received, status (Received, Processed, Failed, Rejected)

---

## DATA — Gaps

### Properties additions

#### Identity additions
- VisualMarkings: hull_number, tail_number, registration, tactical_markings, unit_markings, color_scheme
- ElectronicSignature: radar_cross_section_dBsm, IR_signature, acoustic_signature, EM_emissions_profile
- IFF_Codes: mode1, mode2, mode3 (squawk), mode4_crypto, mode5_crypto, mode_s_address, mode_s_id — current assigned codes

#### Attributes additions
- Capability: type (CapabilityType — from ORBAT section), description, max_range_m, min_range_m, rate (optional), ammunition_types (optional)
- WeaponMount: weapon_ref, mount_type (Fixed, Turret, Pintle, Coaxial, Wing, Pylon, Internal), traverse_limits (arc), elevation_limits (min/max degrees)
- ArmorProtection: type (ArmorType), level (ArmorLevel), coverage (front/side/rear/top/bottom)
- ArmorType [enum]: None, Ballistic, Composite, Reactive, Slat, Active, Cage
- ArmorLevel [enum]: None, SmallArms, HeavyMachineGun, Autocannon, ShapedCharge, KineticEnergy
- MobilityProfile: max_speed_kph, cruise_speed_kph, max_gradient_pct, max_side_slope_pct, max_fording_depth_m, turning_radius_m, ground_pressure_kpa

### State additions

#### System State (exists in ontology but completely absent from typology/concepts)
- SystemState: operational_mode (OperationalMode), submode, error_codes (list), cpu_load_pct, memory_used_pct, disk_used_pct, uptime_seconds, temperature_degc
- OperationalMode [enum]: Off, Startup, Nominal, Degraded, Emergency, Maintenance, Calibrating, Standby, Sleep
- SoftwareState: version, build_hash, last_updated, config_hash
- AutopilotState: mode (string), armed (bool), is_flying (bool), throttle_pct, nav_mode, geofence_active (bool), failsafe_active (bool)

#### Location additions
- IndoorPosition: building_ref (Site ref), floor_number, room_id, x_m, y_m (relative to building origin), method (IndoorPosMethod)
- IndoorPosMethod [enum]: WiFi, BLE_Beacon, UWB, RFID, Optical, DeadReckoning, Manual
- DeadReckoningState: last_fix_position, last_fix_time, estimated_position, drift_estimate_m, method (IMU, WheelOdometry, VisualOdometry, Combined)
- RelativePosition: reference_entity_ref, offset (Vector3D), frame (Local3D — exists)

#### Navigation State (not well represented)
- NavigationState: mode (NavMode), fix_type (GPSFixType), position_source (NavSource), heading_source (NavSource), altitude_source (NavSource)
- NavMode [enum]: Manual, Waypoint, RTL, Loiter, Guided, Land, Takeoff, Circle, Drift, PositionHold, Brake, Throw, ADSB, SmartRTL, FlowHold, Follow, Zigzag, SystemID, AutoRotate
- GPSFixType [enum]: NoFix, Fix2D, Fix3D, DGPS, RTK_Float, RTK_Fixed, Static, PPS
- NavSource [enum]: GPS, GLONASS, Galileo, BeiDou, INS, VIO (Visual Inertial Odometry), OpticalFlow, SLAM, Barometer, Radar, Altimeter, Fused

### Intel additions

#### Intelligence Types
- HUMINT: source_reliability (SourceReliability), information_credibility (InfoCredibility), source_id, handler_ref
- SourceReliability [enum]: A_CompletelyReliable, B_UsuallyReliable, C_FairlyReliable, D_NotUsuallyReliable, E_Unreliable, F_CannotBeJudged (NATO standard)
- InfoCredibility [enum]: 1_Confirmed, 2_ProbablyTrue, 3_PossiblyTrue, 4_Doubtful, 5_Improbable, 6_CannotBeJudged
- SIGINT: type (SIGINTType), intercept_time, emitter_ref, content_summary
- SIGINTType [enum]: COMINT (communications), ELINT (electronic/radar), FISINT (foreign instrumentation)
- OSINT: source_url, source_type (Social Media, News, Academic, Government, Commercial), access_time, relevance_score
- GEOINT: imagery_ref (Media), coverage_area (Geometry), resolution_m, collection_time, source_platform
- MASINT: measurement_type, sensor_type, data_ref, analysis_summary
- IntelReport: report_id, classification, source_type (HUMINT/SIGINT/OSINT/GEOINT/MASINT), dtg, content, reliability_rating, credibility_rating, dissemination_list

#### Intelligence Preparation of Battlefield (IPB)
- IPBProduct: type (IPBType), area_of_operations (Geometry), date_prepared, prepared_by
- IPBType [enum]: TerrainAnalysis, WeatherAnalysis, ThreatEvaluation, ThreatIntegration, CourseOfActionDevelopment
- ModifiedCombinedObstacleOverlay (MCOO): terrain_factors (list), avenues_of_approach (list of Path3D), key_terrain (list of Position), obstacles (list), cover_and_concealment (grid)
- AvenueOfApproach: path (Path3D), width_m, mobility_class (MobilityClass), suitable_for (list of entity types)
- MobilityClass [enum]: Unrestricted, SlowGo, NoGo

#### Situational Awareness Products
- CommonOperatingPicture (COP): timestamp, entities (list of entity snapshots), tracks, events, area_of_operations
- RecognizedAirPicture (RAP): timestamp, air_tracks (list of Track refs), airspace_status (list of AirspaceVolume + status)
- RecognizedMaritimePicture (RMP): similar to RAP for sea surface/subsurface
- ForceTracking: tracked_entities (list of Entity refs with Location), update_rate_seconds, coverage_area
- BlueForceSituation: friendly_positions (list), friendly_status (list), boundaries, phase_lines, unit_tasks_summary

#### Target Management
- HighValueTargetList (HVTL): targets (ordered list of HighValueTarget)
- HighValueTarget: entity_or_position_ref, category (string), priority (int), why_high_value (text), engagement_guidance
- HighPayoffTargetList (HPTL): targets (ordered list of HighPayoffTarget)
- HighPayoffTarget: hvt_ref, decision_criteria (when to engage), method_of_engagement, effect_desired, engagement_authority
- JointTargetList (JTL): targets (list), approval_authority, classification
- RestrictedTargetList (RTL): targets that require specific authorization before engagement
- NoStrikeList (NSL): entities/sites that must NOT be engaged under any circumstances, reason

### Sensory additions
- ThermalImage: temperature_range (min_kelvin, max_kelvin), palette (GrayScale, IronBow, Rainbow, WhiteHot, BlackHot)
- HyperspectralData: band_count, wavelength_range_nm (min, max), spatial_resolution_m
- SARImage: mode (SARMode), resolution_m, look_direction, incidence_angle, polarization
- SARMode [enum]: Spotlight, Stripmap, ScanSAR, ISAR, GMTI
- AcousticSignature: frequency_spectrum, source_level_dB, classification (if available)
- SeismicSignature: waveform, magnitude, bearing, estimated_distance

---

## CROSS-CUTTING — Gaps

### Access Control / Permissions
- AccessControlEntry: subject (Entity ref), resource (any ref), permission (PermissionLevel)
- PermissionLevel [enum]: None, Read, Write, Execute, Admin, Owner
- Role: name, permissions (list of AccessControlEntry), inherits_from (optional Role ref)
- DataPolicy: data_ref, classification, handling_instructions, releasability, retention_days

### Audit Trail
- AuditEntry: timestamp, actor (Entity ref), action (AuditAction), resource (any ref), old_value, new_value, reason
- AuditAction [enum]: Created, Updated, Deleted, Accessed, Shared, Classified, Declassified, Approved, Denied, Exported, Imported

### Versioning
- Version: major, minor, patch, build_hash — for software/firmware
- EntityVersion: entity_ref, version_number (incrementing), timestamp, changed_fields (list of field names), changed_by
- SchemaVersion: schema_id, version, migration_path

### Notification / Subscription
- Notification: type (NotificationType), severity, subject_ref, message, timestamp, acknowledged (bool)
- NotificationType [enum]: Alert, StatusChange, TaskUpdate, Threshold, Geofence, CommLoss, BatteryLow, MissionComplete, Hostile, Emergency
- AlertSubscription: subscriber (Entity ref), event_types (list), filter_conditions, delivery_method (Push, Poll, Stream)

### Data Quality
- DataQuality: freshness_seconds, accuracy_estimate, source_reliability (SourceReliability), completeness_pct, consistency_check_passed (bool)
- StalenessPolicy: max_age_seconds, action_when_stale (Warn, Drop, Extrapolate, Mark)

### Interoperability / Translation
- ProtocolBridge: source_protocol (ProtocolType), target_protocol (ProtocolType), translation_rules, data_loss_fields (list — fields that cannot be mapped)
- FormatConverter: input_format (SerializationFormat), output_format (SerializationFormat), schema_mapping
- InteroperabilityGateway: node_ref, supported_protocols (list of ProtocolType), translation_table

### Simulation / Exercise
- SimulationConfig: is_simulated (bool), time_acceleration_factor (float, 1.0=realtime), inject_entities (list), scenario_name
- ExerciseControl: exercise_id, name, start_time, end_time, participants (list of Organization refs), classification, inject_schedule (list of SimulationInject)
- SimulationInject: time, entity_ref, injected_state (State data), description

### Electronic Order of Battle (EOB)
- EOBEntry: emitter_ref, location, signal_characteristics (Signal ref), associated_platform_type, threat_level, first_detected, last_detected, active (bool)
- EOB: entries (list of EOBEntry), area_of_interest (Geometry), date_compiled, classification

### Phase Concepts
- OperationalPhase: name, phase_number, h_hour_offset, description, trigger_conditions, end_conditions
- PhaseTransition: from_phase, to_phase, trigger (TriggerCondition), authority (Entity ref)
- H_HourConcept: reference_time, phase_offsets (map phase_name → offset_minutes), current_phase

### Multi-Domain
- CrossDomainSolution: from_network (classification level), to_network (classification level), guard_type, allowed_data_types, review_method (Automatic, Manual, Both)
- DomainSynchronization: domains (list of OpDomain — exists), synchronization_point (time/event), deconfliction_measures

### ISR Management
- ISRRequest: requester (Organization ref), collection_type (CollectionType), priority (int), area (Geometry), time_window (TimeWindow), sensor_requirements, LTIOV (latest time info is of value)
- CollectionType [enum]: Visual, IR, Radar, SIGINT, HUMINT, OSINT, Multisource
- ISRSynchronizationMatrix: missions (list), NAIs (list of NAI refs), indicators_per_NAI, collection_assets_assigned, collection_times
- CollectionPlan: requests (list of ISRRequest), assets_available (list of Entity refs), schedule (time → asset → NAI mapping)

### Reporting Formats
- SALUTEReport: size, activity, location (Position), uniform (text), time (timestamp), equipment (text) — standard tactical report
- SPOTReport: observer (Entity ref), time, activity_observed, location (Position), number_of_personnel, actions_taken
- SITREPFormat: dtg, reporting_unit, enemy_situation, friendly_situation, combat_power, logistics_status, significant_events
- METREPFormat: reporting_station, dtg, surface_wind, visibility, weather_phenomena, cloud_layers, temperature, dewpoint, altimeter_setting
- INTSUMFormat: period_covered, area_of_interest, enemy_activity_summary, assessment, forecast, intelligence_gaps

### Rate / Frequency patterns
- UpdateRate: entity_ref, data_type, interval_ms, priority_multiplier
- HeartbeatConfig: interval_ms, timeout_ms (considered dead after this), jitter_ms
- ThrottlePolicy: max_updates_per_second, burst_limit, window_seconds

### Geofence (expanding from Site)
- GeofenceRule: geometry (Polygon), floor_altitude, ceiling_altitude, type (GeofenceAction), enabled (bool), priority
- GeofenceAction [enum]: KeepIn, KeepOut, Warn, RTL, Land, Loiter, Report, Deny
- GeofenceViolation [Data → Event]: entity_ref, geofence_ref, violation_type (Entered, Exited, AltitudeExceeded), position, timestamp, action_taken

### Handoff / Transfer patterns (generalized)
- Handoff: type (HandoffType), from_entity (Entity ref), to_entity (Entity ref), subject (Entity ref or Task ref), initiated_time, completed_time, status (HandoffStatus — exists), authorization_token
- HandoffType [enum]: ControlAuthority, TrackCustody, TaskAssignment, SensorCue, CommunicationRelay, LogisticResponsibility

### Map / Display concepts
- MapLayer: name, type (MapLayerType), visible (bool), opacity (float 0-1), z_order (int), source_url
- MapLayerType [enum]: Basemap, Satellite, Terrain, Overlay, EntityTrack, Route, Geofence, ThreatRings, SensorCoverage, Weather, SIGACTS, DrawingAnnotation
- MapAnnotation: geometry, style (color, stroke_width, fill_color, label), author (Entity ref), timestamp, category

### Connectivity / Reachability
- Reachability: from_node (Node ref), to_node (Node ref), reachable (bool), via_path (list of Node refs), latency_ms, bandwidth_bps, reliability_pct
- NetworkGraph: nodes (list of Node refs), edges (list of Reachability), last_updated
- LinkState: carrier_ref, connected (bool), rssi_dBm, snr_dB, packet_loss_pct, latency_ms, uptime_seconds

### Maintenance Management
- MaintenanceAction: type (MaintenanceType), entity_ref, component_ref (optional), scheduled_time, completed_time, performed_by, notes
- MaintenanceType [enum]: Preventive, Corrective, Inspection, Calibration, SoftwareUpdate, BatteryReplacement, PartReplacement
- MaintenanceSchedule: entity_ref, actions (list ordered by due time), next_due
- FlightLog: entity_ref, flight_id, start_time, end_time, duration_hours, pilot_ref, mission_ref, battery_id, start_voltage, end_voltage, distance_km, max_altitude_m, notes, anomalies

### Electromagnetic Spectrum (expanding Reference → Type)
- EMBand [enum]: ELF, SLF, ULF, VLF, LF, MF, HF, VHF, UHF, SHF, EHF, THF, Infrared, Visible, UV, XRay, Gamma
- FrequencyAllocation: band (EMBand), min_hz, max_hz, purpose, assigned_to, priority, exclusive (bool)
- SpectrumSnapshot: time, allocations (list of FrequencyAllocation), active_emitters (list of signal refs), interference_detected (list)

### Environmental Effects on Operations
- EnvironmentalEffect: factor (EnvironmentalFactor), impact_on (list of affected capabilities), severity (Severity enum), mitigation (text)
- EnvironmentalFactor [enum]: Rain, Snow, Fog, Dust, Smoke, Darkness, Wind, Heat, Cold, Humidity, Altitude, Vegetation, UrbanClutter, ElectromagneticInterference, SolarActivity
- OperationalImpact: capability_ref (CapabilityType), degradation_pct (float 0-100), compensating_measures (text)

### Decision Support
- DecisionPoint: name, trigger_conditions (list of TriggerCondition), options (list of CourseOfAction), deadline (timestamp or TriggerCondition), authority (Entity ref)
- RiskAssessment: hazard (text), probability (RiskProbability), severity (RiskSeverity), risk_level (derived), mitigation (text), residual_risk_level
- RiskProbability [enum]: Frequent, Likely, Occasional, Seldom, Unlikely
- RiskSeverity [enum]: Catastrophic, Critical, Marginal, Negligible
- RiskMatrix: probability × severity → risk level (Extremely High, High, Medium, Low)

### Entity Grouping / Tagging
- Tag: key (string), value (string) — generic key-value label applicable to any entity/object
- GroupMembership: entity_ref, group_ref (Collection ref), role_in_group (string), joined_time, left_time
- Filter: name, predicate (from Lattice filtering — exists), applies_to_type

### Energy / Power Management
- PowerBudget: entity_ref, total_available_watts, allocated (map component_ref → watts), reserve_pct
- EnergyEstimate: entity_ref, current_energy_wh, consumption_rate_w, estimated_endurance_minutes, point_of_no_return_position (Position)
- ChargingState: entity_ref, charging (bool), charge_rate_watts, estimated_full_time, charge_cycles_total

---

# ADDITIONAL RECURRING PATTERNS (extending meta-patterns)

## Lifecycle with Request/Approval
The existing LifecyclePhase (Planned→Active→Complete) and RequestStatus
(Submitted→Acknowledged→Approved→...) are two views of the same continuum.
Proposed unified superset:

UnifiedLifecycle [enum]:
- Draft, Submitted, Acknowledged, Approved, Denied,
- Planned, Scheduled, Queued,
- Active, Executing, Paused, Suspended, WaitingForInput,
- InTransit, Delivered,
- Complete, CompletedWithErrors, Failed, Aborted, Cancelled,
- Archived, Expired

Not every type uses every state. The subset used is determined by the struct.
But they must all draw from the same vocabulary.

## Status/Health pattern
Many things report health the same way:
- state: enum from {Nominal, Degraded, Failed, Unknown, Offline}
- last_check_time
- details (text or structured)

Appears on: Node, Carrier, Component, System, Sensor, PowerSource, Link.
Pattern, not a struct — but the schema should define a reusable shape.

## Bounded Range pattern
- min, max of the same type
- Used for: altitude ranges, frequency ranges, temperature ranges,
  speed ranges, time ranges, angle ranges, distance ranges
- Already partially exists (DurationRange, FrequencyRange, TimeRange in LA)
- Needs a generic parameterized shape or a set of typed range structs

## Ordered Priority List pattern
- Items ordered by priority (lower number = higher priority)
- Used for: target lists, supply priorities, evacuation priorities,
  engagement priorities, movement priorities, communication nets (PACE)
- Priority is always (int) with lower = more important

## Geospatial Constraint pattern
- geometry + altitude range + time window + who it applies to + action
- Used for: geofence, airspace, FSCM, deconfliction zone, NAI, TAI,
  keep-in/keep-out zones, engagement zones, drop zones, corridors
- Always the same structural bones: volume + time + scope + rule

## Observation-Assessment pair
- Raw detection/observation → human or AI assessment → classified/categorized result
- Used for: Detection→Classification→Track, BDA, PID, Weather observation→forecast
- Structural: observation_ref, assessor, method, confidence, result
- Confidence always 0-1 float, method always an enum

## Source Attribution
- Nearly every piece of data needs: who produced it, when, how, from where
- Lattice calls it Provenance. CoT calls it "how". HiveOS tracks source host/port.
- Structural: source_entity_ref, source_type, production_time, production_method, reliability

---

# EXPANSION PASS 3 — ATOMIC LEVEL

Sources: CoT full type tree, Lattice protobuf field-level detail, CJADC2 deep
research, stage1 architecture notes. Every field, every enum value, every
relation type. Nothing omitted.

---

## CoT TYPE TREE — COMPLETE DECOMPOSITION

### CoT Top-Level Branches
- `a` — Atom: physical thing with position (entities, tracks)
- `b` — Bits: information, data, detections, alarms, reports, weather, graphics
- `c` — Capability: what a unit can do
- `t` — Tasking: requests and orders
- `y` — Reply: acknowledgments and completion codes

### CoT Atom (a-) Domain Hierarchy
- `a-.-A` — Air track
  - `a-.-A-C` — Civil aircraft
    - `a-.-A-C-F` — Fixed wing
      - `a-.-A-C-F-q` — RPV/Drone/UAV (civil)
    - `a-.-A-C-H` — Rotary wing
    - `a-.-A-C-L` — Lighter than air
  - `a-.-A-M-F` — Military fixed wing
    - `a-.-A-M-F-g` — Gunship
    - `a-.-A-M-F-A` — Attack/Strike
    - `a-.-A-M-F-B` — Bomber
    - `a-.-A-M-F-C` — Cargo/Transport
      - `a-.-A-M-F-C-H` — Heavy cargo
  - `a-.-A-W` — Weapon (airborne)
    - `a-.-A-W-D` — Decoy
    - `a-.-A-W-M` — Missile in flight
      - `a-.-A-W-M-S` — SAM
- `a-.-G` — Ground track
  - `a-.-G-E` — Equipment
    - `a-.-G-E-S` — Sensor
      - `a-.-G-E-S-E` — Emplaced sensor
    - `a-.-G-E-V` — Vehicle
  - `a-.-G-I` — Installation/Structure
    - `a-.-G-I-c` — Civilian structure
      - `a-.-G-I-c-b` — Bridge
      - `a-.-G-I-c-bar` — Fence/Wall/Barrier
      - `a-.-G-I-c-can` — Canal
        - `a-.-G-I-c-can-l` — Canal lock
  - `a-.-G-U` — Ground unit
    - `a-.-G-U-C` — Combat
      - `a-.-G-U-C-A` — Armor
        - `a-.-G-U-C-A-A` — Anti-armor
          - `a-.-G-U-C-A-A-A` — Anti-armor armored
            - `a-.-G-U-C-A-A-A-S` — Anti-armor armored air assault
            - `a-.-G-U-C-A-A-A-T` — Anti-armor armored tracked
  - `a-.-G-U-i` — Incident Management resources
  - `a-.-G-O` — Ground obstacle
- `a-.-S` — Sea surface track
- `a-.-U` — Subsurface track
- `a-.-P` — Space track

Faction prefix replaces `-.-`:
- `a-f-` friendly, `a-h-` hostile, `a-u-` unknown, `a-n-` neutral
- `a-s-` suspect, `a-j-` joker, `a-k-` faker, `a-p-` pending, `a-a-` assumed

### CoT Bits (b-) Full Tree

#### Detections (b-d-)
- `b-d` — Detection (generic)
- `b-d-a` — Acoustic
  - `b-d-a-i` — Impulsive
  - `b-d-a-v` — Voice
  - `b-d-a-c` — Cyclostationary
- `b-d-m` — Motion
- `b-d-s` — Seismic
- `b-d-r` — Radiation (deprecated, use b-d-c-n-r)
- `b-d-n` — Nuclear (deprecated, use b-d-c-n-n)
- `b-d-c` — CBRNE
  - `b-d-c-b` — BioChem
    - `b-d-c-b-b` — Biological
    - `b-d-c-b-c` — Chemical
  - `b-d-c-e` — Explosive
    - `b-d-c-e-d` — Explosive device
  - `b-d-c-n` — Nuclear/Radiological
    - `b-d-c-n-n` — Nuclear
      - `b-d-c-n-n-b` — Nuclear bomb
      - `b-d-c-n-n-sm` — Special nuclear material
    - `b-d-c-n-r` — Radiological
      - `b-d-c-n-r-dd` — Dirty bomb (dispersal device)
- `b-d-l` — Launch
  - `b-d-l-b` — Bullet launch
  - `b-d-l-m` — Mortar launch
- `b-d-i` — Impact
  - `b-d-i-m` — Mortar impact

#### Alarms (b-l-)
- `b-l` — Alarm
- `b-l-c` — CBRNE alarm (mirrors detection tree)
  - `b-l-c-b` — BioChem alarm
    - `b-l-c-b-b` — Biological alarm
    - `b-l-c-b-c` — Chemical alarm
  - `b-l-c-e` — Explosive alarm
    - `b-l-c-e-d` — Explosive device alarm
  - `b-l-c-n` — Nuclear/Radiological alarm
    - `b-l-c-n-n` — Nuclear alarm
      - `b-l-c-n-n-b` — Nuclear bomb alarm
      - `b-l-c-n-n-sm` — SNM alarm
    - `b-l-c-n-r` — Radiological alarm
      - `b-l-c-n-r-dd` — Dirty bomb alarm
- `b-l-e` — Environmental alarm
  - `b-l-e-h` — Hazmat alarm
- `b-l-f` — Fire alarm
  - `b-l-f-a` — Audible fire alarm
    - `b-l-f-a-a` — Pump activated
    - `b-l-f-a-c` — Combustion
    - `b-l-f-a-d` — Duct detector
    - `b-l-f-a-f` — Flame detector
    - `b-l-f-a-h` — Heat
    - `b-l-f-a-p` — Pull station
    - `b-l-f-a-s` — Smoke
    - `b-l-f-a-w` — Waterflow

#### Weather / METOC (b-w-)
- `b-w` — METOC (Meteorological/Oceanographic)
- `b-w-A` — Atmospheric
  - `b-w-A-t` — Temperature
  - `b-w-A-T` — Turbulence
  - `b-w-A-I` — Icing
  - `b-w-A-W` — Winds
  - `b-w-A-C` — Cloud coverage
    - `b-w-A-C-t` — Cloud top
    - `b-w-A-C-b` — Cloud base
    - `b-w-A-C-c` — Cloud ceiling
    - `b-w-A-C-a` — Cloud total
  - `b-w-A-S-T` — Thunderstorm
  - `b-w-A-P` — Pressure systems
    - `b-w-A-P-L` — Low pressure center
    - `b-w-A-P-H` — High pressure center
    - `b-w-A-P-F` — Frontal systems
      - `b-w-A-P-F-C` — Cold front
        - `b-w-A-P-F-C-U` — Upper cold front

#### Reports (b-r-)
- `b-r-.-h-c` — Casualty report
- `b-r-.-I` — Signals intelligence
  - `b-r-.-I-P` — Space track
    - `b-r-.-I-P-S` — Signal intercept
      - `b-r-.-I-P-S-C` — Communications intercept
        - `b-r-.-I-P-S-C-D` — Satellite downlink
- `b-r-.-O` — MOOTW (Military Operations Other Than War)
  - `b-r-.-O-V` — Violent activities
    - `b-r-.-O-V-A` — Arson/Fire
    - `b-r-.-O-V-M` — Assassination/Murder/Execution
    - `b-r-.-O-V-B` — Bomb/Bombing
    - `b-r-.-O-V-Y` — Booby trap
    - `b-r-.-O-V-D` — Drive-by shooting
    - `b-r-.-O-V-S` — Sniping
    - `b-r-.-O-V-P` — Poisoning
- `b-r-F-C` — Fire coordination

#### Map/Spatial (b-m-)
- `b-m-r` — Route
- `b-m-p` — Map point
  - `b-m-p-t` — Targeted
  - `b-m-p-w` — Waypoint
  - `b-m-p-m-c` — Click (user placed)
  - `b-m-p-s-p-i` — SPI (Sensor Point of Interest)
  - `b-m-p-v-p-i` — VPOI (Video Point of Interest)
  - `b-m-p-r` — Reference point
  - `b-m-p-c` — Control point
- `b-m-g-o` — Grid
- `b-i` — Image
  - `b-i-e` — KML image
- `b-S` — Strike warning
- `b-t-f` — Free text (preferred over t-x-f)
- `b-x` — Non-CoT object

#### Tactical Graphics (b-g-, deprecated)
- `b-g-.-T` — Tasks
  - `b-g-.-T-B` — Block
  - `b-g-.-T-H` — Breach
  - `b-g-.-T-Y` — Bypass
  - `b-g-.-T-C` — Canalize
  - `b-g-.-T-X` — Clear
  - `b-g-.-T-J` — Contain
  - `b-g-.-T-K` — Counterattack
    - `b-g-.-T-K-F` — Counterattack by fire
- `b-g-.-G` — C2 and General Maneuver
  - `b-g-.-G-G-P` — Points
    - `b-g-.-G-G-P-U` — Undersea warfare
      - `b-g-.-G-G-P-U-U-D` — Datum
      - `b-g-.-G-G-P-U-U-B` — Brief contact
      - `b-g-.-G-G-P-U-U-L` — Lost contact
      - `b-g-.-G-G-P-U-U-S` — Sinker

### CoT Capability (c-) Tree
- `c-c` — Communications
- `c-f` — Fires
  - `c-f-d` — Direct fires
  - `c-f-i` — Indirect fires
- `c-l` — Logistics/Supply
  - `c-l-f` — Fuel
- `c-r` — Rescue
- `c-s` — Surveillance

### CoT Tasking (t-) Tree
- `t-a` — Air tasking
  - `t-a-c` — Close Air Support
  - `t-a-d` — Air drop
  - `t-a-e` — Electronic warfare
  - `t-a-k` — Strike (deprecated)
  - `t-a-r` — Recovery (deprecated)
  - `t-a-s` — SEAD (deprecated)
- `t-k` — Strike
  - `t-k-d` — Destroy
  - `t-k-i` — Investigate
  - `t-k-t` — Target
- `t-m` — Mensurate
- `t-p-s-i` — Imagery (WTP)
- `t-q` — Query capable
- `t-r` — Relocate
- `t-s` — ISR
  - `t-s-b` — BFT (Blue Force Tracking) info
  - `t-s-i` — Imagery desired
    - `t-s-i-e` — ISR EO
    - `t-s-i-i` — ISR IR
  - `t-s-r` — ISR Radar
  - `t-s-v` — ISR Video
    - `t-s-v-e` — ISR Video EO
    - `t-s-v-i` — ISR Video IR
- `t-u` — Update
  - `t-u-q` — Status query
  - `t-u-z` — Cancel
- `t-x` — Experimental
  - `t-x-i` — Data retrieval
    - `t-x-i-l` — Link dereference
  - `t-x-a-s` — App sync
    - `t-x-a-s-c` — Sync subscribe
  - `t-x-a-f` — App filter
  - `t-x-a-o` — App open
  - `t-x-a-c-c` — Comm check
  - `t-x-f` — Free text (deprecated, use b-t-f)
  - `t-x-v-m` — MEDEVAC (experimental)

### CoT Reply (y-) Tree
- `y-a` — Acknowledgment
  - `y-a-r` — Received (receipt)
  - `y-a-w` — Wilco (will comply)
- `y-c` — Tasking complete
  - `y-c-s` — Success
  - `y-c-f` — Fail
    - `y-c-f-a` — No assets
    - `y-c-f-b` — Bad request (CANTPRO)
    - `y-c-f-d` — Denied
    - `y-c-f-i` — Insufficient info
    - `y-c-f-r` — Rejected
      - `y-c-f-r-c` — Rejected by C2 element
      - `y-c-f-r-p` — Rejected by platform (CANTCO)
  - `y-c-f-s` — Stale
- `y-s-c` — Status: canceling
- `y-s-e` — Status: executing
- `y-s-r` — Status: review

### CoT Relation Types (link semantics between events)
Parent relations:
- `p` — parent (of this object)
- `p-p` — producer
- `p-o` — owner
- `p-m` — manager
- `p-l` — leader/commander

Child relations:
- `c` — child (of this object)
- `c-c` — correlated element
- `c-f` — fused element
- `c-p` — composite element
- `c-a` — alternate element

Refinement relations:
- `r` — refinement (of this object)
- `r-a` — amplification
- `r-u` — refinement URL

Tasking relations (grammatical structure):
- `t` — tasking (by this object)
- `t-o` — object of tasking
- `t-i` — indirect object
- `t-s` — subject of tasking
- `t-p` — preposition
  - `t-p-a` — at
  - `t-p-b` — by
  - `t-p-w` — with
  - `t-p-f` — from
  - `t-p-r` — regarding

### CoT "How" Field — Production Method Taxonomy
Machine-generated:
- `m-` — machine (generic)
- `m-g` — GPS
  - `m-g-n` — INS+GPS (fused)
  - `m-g-d` — DGPS
- `m-i` — mensurated (from imagery)
- `m-n` — INS (inertial only)
- `m-m` — magnetic
- `m-s` — simulated
- `m-c` — configured
- `m-p` — passed/propagated/relayed
- `m-f` — fused (multi-source)
- `m-a` — tracker (automatic)
- `m-r` — radio
  - `m-r-e` — EPLRS
  - `m-r-p` — PLRS
  - `m-r-d` — Doppler
  - `m-r-v` — VHF
  - `m-r-t` — TADIL
    - `m-r-t-a` — TADIL-A
    - `m-r-t-b` — TADIL-B
    - `m-r-t-j` — TADIL-J (Link 16)

Human-entered:
- `h-` — human (generic)
- `h-t` — transcribed/retyped
- `h-e` — estimated
- `h-c` — calculated
- `h-p` — pasted
- `h-g-i-g-o` — GIGO (non-CoT import, garbage-in-garbage-out)

### CoT QoS Predicates
Priority levels (first digit):
- 0-1: Routine
- 2-3: Priority
- 4-5: Immediate
- 6-7: Flash
- 8-9: Flash Override

Delivery class (second character):
- `g` — Guaranteed/Assured
- `d` — Deadline
- `c` — Congestion-managed

Replacement policy (third character):
- `r` — Replace (latest supersedes)
- `f` — Follow (append to queue)

### CoT Operational Context
- `e-` — Exercise
- `o-` — Operational
- `s-` — Simulated

### CoT Mayday
- `a-.-.*-9-1-1` — Mayday emergency signal (any faction, any domain)

---

## LATTICE PROTOBUF — ATOMIC FIELD DETAIL

### Entity Component Bag (complete field list on Entity proto)
A Lattice Entity is a composable bag of optional components:
- entity_id: string (required, GUID)
- description: string
- is_live: bool
- created_time: Timestamp
- expiry_time: Timestamp
- no_expiry: bool
- status: Status {platform_activity: string, role: string}
- location: Location
- location_uncertainty: LocationUncertainty
- geo_shape: GeoShape (oneof: point, line, polygon, ellipse, ellipsoid)
- geo_details: GeoDetails {type: GeoType, control_area, acm}
- aliases: Aliases {alternate_ids[], name}
- tracked: Tracked
- correlation: Correlation
- mil_view: MilView {disposition, environment, nationality}
- ontology: Ontology {platform_type, specific_type, template}
- sensors: Sensors {sensors[]}
- payloads: Payloads {payload_configurations[]}
- power_state: PowerState {source_id_to_state map}
- provenance: Provenance
- overrides: Overrides {override[]}
- indicators: Indicators {simulated, exercise, emergency, c2, egressable, starred}
- target_priority: TargetPriority
- signal: Signal
- transponder_codes: TransponderCodes
- data_classification: Classification
- task_catalog: TaskCatalog {task_definitions[]}
- media: Media {media[]}
- relationships: Relationships {relationships[]}
- visual_details: VisualDetails {range_rings}
- dimensions: Dimensions {length_m}
- route_details: RouteDetails {destination_name, estimated_arrival_time}
- schedules: Schedules {schedules[]}
- health: Health
- group_details: GroupDetails {team, echelon}
- supplies: Supplies {fuel[]}
- orbit: Orbit {orbit_mean_elements}
- symbology: Symbology {mil_std_2525_c: {sidc}}

### Location (atomic fields)
Position:
- latitude_degrees: double
- longitude_degrees: double
- altitude_hae_meters: DoubleValue (optional)
- altitude_agl_meters: DoubleValue (optional)
- altitude_asf_meters: DoubleValue (optional)
- pressure_depth_meters: DoubleValue (optional)

Location:
- position: Position
- velocity_enu: ENU {e, n, u} (meters/second)
- speed_mps: DoubleValue
- acceleration: ENU {e, n, u}
- attitude_enu: Quaternion {x, y, z, w} (body→ENU transform)

LocationUncertainty:
- position_enu_cov: TMat3 {mxx, mxy, mxz, myy, myz, mzz} (symmetric upper triangle, floats)
- velocity_enu_cov: TMat3
- position_error_ellipse: ErrorEllipse {probability, semi_major_axis_m, semi_minor_axis_m, orientation_d}

### Power (atomic fields)
PowerLevel:
- capacity: float
- remaining: float
- percent_remaining: float
- voltage: DoubleValue
- current_amps: DoubleValue
- run_time_to_empty_mins: DoubleValue
- consumption_rate_l_per_s: DoubleValue

PowerSource:
- power_status: PowerStatus (Unknown, NotPresent, Operating, Disabled, Error)
- power_type: PowerType (Unknown, Gas, Battery)
- power_level: PowerLevel
- messages: string[] (status messages)
- offloadable: BoolValue

PowerState:
- source_id_to_state: map<string, PowerSource>

### Fuel (atomic fields)
- fuel_id: string
- name: string
- reported_date: Timestamp
- amount_gallons: uint32
- max_authorized_capacity_gallons: uint32
- operational_requirement_gallons: uint32
- data_classification: Classification
- data_source: string

### Signal (atomic fields)
- frequency_center: Frequency {frequency_hz: Measurement}
- frequency_range: FrequencyRange {minimum_frequency_hz, maximum_frequency_hz}
- bandwidth_hz: DoubleValue
- signal_to_noise_ratio: DoubleValue
- line_of_bearing: LineOfBearing
- fixed: Fixed (marker, no fields)
- emitter_notations: EmitterNotation[] {emitter_notation: string, confidence: DoubleValue}
- pulse_width_s: DoubleValue
- pulse_repetition_interval: PulseRepetitionInterval {pulse_repetition_interval_s: Measurement}
- scan_characteristics: ScanCharacteristics {scan_type: ScanType, scan_period_s: DoubleValue}

Measurement (generic value+uncertainty):
- value: DoubleValue
- sigma: DoubleValue

LineOfBearing:
- angle_of_arrival: AngleOfArrival {relative_pose: Pose, bearing_elevation_covariance_rad2: TMat2}
- range_estimate_m: Measurement
- max_range_m: Measurement

### Sensor (atomic fields)
- sensor_id: string
- operational_state: OperationalState (Off, NonOperational, Degraded, Operational, Denied)
- sensor_type: SensorType (Radar, Camera, Transponder, RF, GPS, PTU_Pos, Perimeter, Sonar)
- sensor_description: string
- rf_configuration: RFConfiguration {frequency_range_hz[], bandwidth_range_hz[]}
- last_detection_timestamp: Timestamp
- fields_of_view: FieldOfView[]

FieldOfView:
- fov_id: int32
- mount_id: string
- projected_frustum: ProjectedFrustum {upper_left, upper_right, bottom_right, bottom_left: Position}
- projected_center_ray: Position
- center_ray_pose: Pose
- horizontal_fov: float (degrees)
- vertical_fov: float (degrees)
- range: FloatValue (meters)
- mode: SensorMode

### GeoShape (atomic fields)
GeoPoint: {position: Position}
GeoLine: {positions: Position[]}
GeoPolygon: {rings: LinearRing[], is_rectangle: bool}
LinearRing: {positions: GeoPolygonPosition[]}
GeoPolygonPosition: {position: Position, height_m: FloatValue}
GeoEllipse: {semi_major_axis_m, semi_minor_axis_m, orientation_d, height_m: DoubleValue each}
GeoEllipsoid: {forward_axis_m, side_axis_m, up_axis_m: DoubleValue each}

GeoDetails:
- type: GeoType (General, Hazard, Emergency, EngagementZone, ControlArea, Bullseye, ACM)
- control_area: ControlAreaDetails {type: ControlAreaType (KeepIn, KeepOut, Ditch, Loiter)}
- acm: ACMDetails {acm_type: ACMDetailType (LandingZone), acm_description: string}

### Override System (atomic fields)
Override:
- request_id: string
- field_path: string (dotted path to overridden component)
- masked_field_value: Entity (the override value)
- status: OverrideStatus (Applied, Pending, Timeout, Rejected, DeletionPending)
- provenance: Provenance
- type: OverrideType (Live, PostExpiry)
- request_timestamp: Timestamp

Precedence rules: Manual > Automated; Local > Global

### Correlation System (atomic fields)
PrimaryCorrelation: {secondary_entity_ids: string[]}
SecondaryCorrelation: {primary_entity_id: string, metadata: CorrelationMetadata}
CorrelationMetadata: {provenance, replication_mode (Local|Global), type (Manual|Automated)}
Decorrelation: {all: DecorrelatedAll | decorrelated_entities: DecorrelatedSingle[]}

### Tracked (atomic fields)
- track_quality_wrapper: Int32Value (0-15 quality score)
- sensor_hits: Int32Value
- number_of_objects: UInt32Range {lower_bound, upper_bound}
- radar_cross_section: DoubleValue (dBsm)
- last_measurement_time: Timestamp
- line_of_bearing: LineOfBearing

### Health (atomic fields)
Health:
- connection_status: ConnectionStatus (Online, Offline)
- health_status: HealthStatus (Healthy, Warn, Fail, Offline, NotReady)
- components: ComponentHealth[]
- update_time: Timestamp
- active_alerts: Alert[]

ComponentHealth:
- id: string
- name: string
- health: HealthStatus
- messages: ComponentMessage[] {status: HealthStatus, message: string}
- update_time: Timestamp

Alert:
- alert_code: string
- description: string
- level: AlertLevel (Advisory, Caution, Warning)
- activated_time: Timestamp
- active_conditions: AlertCondition[] {condition_code, description}

### Task v2 (atomic fields)
Task:
- version: TaskVersion {task_id, definition_version: uint32, status_version: uint32}
- specification: google.protobuf.Any (polymorphic task payload)
- created_by: Principal
- last_updated_by: Principal
- last_update_time: Timestamp
- status: TaskStatus
- scheduled_time: Timestamp
- relations: Relations {assignee: Principal, parent_task_id: string}
- description: string
- is_executed_elsewhere: bool
- create_time: Timestamp
- replication: Replication {stale_time: Timestamp}
- initial_entities: TaskEntity[]
- owner: Owner {entity_id}

TaskStatus:
- status: Status (Created, ScheduledInManager, Sent, MachineReceipt, Ack, Wilco, Executing, WaitingForUpdate, DoneOk, DoneNotOk, Replaced, CancelRequested, CompleteRequested, VersionRejected)
- task_error: TaskError {code: ErrorCode (Cancelled, Rejected, Timeout, Failed), message, error_details: Any}
- progress: Any (task-specific progress report)
- result: Any (task-specific result)
- start_time: Timestamp
- estimate: Any (task-specific completion estimate)
- allocation: Allocation {active_agents: Agent[]}

Principal (who initiated, oneof):
- system: System {service_name, entity_id, manages_own_scheduling}
- user: User {user_id}
- team: Team {entity_id, members: Agent[]}
- on_behalf_of: Principal (delegation chain)

TaskEntity:
- entity: Entity (full snapshot or reference)
- snapshot: bool (if true, entity is a frozen copy)

### ISR Task Fields (atomic)
ISRParameters:
- speed_m_s: FloatValue
- standoff_distance_m: FloatValue
- standoff_angle: FloatValue
- expiration_time_ms: UInt64Value

Investigate: {objective: Objective, parameters: ISRParameters}
VisualId: {objective: Objective, parameters: ISRParameters}
Shadow: {objective: Objective, parameters: ISRParameters}
Monitor: {objective: Objective}
Scan: {objective: Objective, parameters: ISRParameters}
Map: {objective, parameters, min_niirs: UInt32Value}
ImproveTrackQuality: {objective, termination_track_quality: uint32}
GimbalPoint: {look_at: Objective | celestial_location: AzimuthElevation | frame_location: FramePoint, parameters}
GimbalZoom: {set_horizontal_fov: DoubleValue | set_magnification: FloatValue}
BattleDamageAssessment: {objective, parameters}

Loiter: {objective, loiter_type: LoiterType {orbit_type: OrbitType}, parameters}
OrbitType: {direction: OrbitDirection (Right|Left), pattern: OrbitPattern (Circle|Racetrack|FigureEight), duration: OrbitDuration}
OrbitDuration: {duration_range: DurationRange {min, max: Duration} | num_of_orbits: uint64}

AreaSearch: {objective, priors: Prior[], participants: Agent[], control_areas: ControlArea[]}
VolumeSearch: {objective, priors: Prior[], participants: Agent[], control_areas: ControlArea[]}
Prior: {entity_id | point: Point}

### Strike Task Fields (atomic)
Strike: {objective, ingress_angle: AnglePair {min, max: double}, strike_release_constraint: StrikeReleaseConstraint, parameters: StrikeParameters}
StrikeParameters: {payloads_to_employ: PayloadConfiguration[], desired_impact_time: Duration, run_in_bearing: double, glide_slope_angle: double}
StrikeReleaseConstraint: {release_area: AreaConstraints {altitude_constraint: AltitudeConstraint {min, max: double}}}
Smack: {objective, parameters: StrikeParameters}
ReleasePayload: {payloads: PayloadConfiguration[], objective, precision_release: bool}
PayloadConfiguration: {capability_id: string, quantity: uint32}

### Maneuver Task Fields (atomic)
Transit: {plan: RoutePlan}
Marshal: {objective}
SetLaunchRoute: {plan: RoutePlan, tracking_mode: LaunchTrackingMode (GoToWaypoint|TrackToWaypoint)}
RoutePlan: {route: Route {path: PathSegment[]}}
PathSegment (oneof): {waypoint: Waypoint {lla_point: Point} | loiter: Loiter}
Point: {reference_name: string, lla: LLA, backing_entity_id: string}
Objective: {entity_id: string | point: Point}

### Entity Manager API (streaming/querying)
StreamEntityComponentsRequest:
- components_to_include: string[] (select which components to stream)
- include_all_components: bool
- filter: Statement (predicate tree)
- rate_limit: RateLimit {update_per_entity_limit_ms: uint32}
- heartbeat_period_millis: uint32
- preexisting_only: bool

EntityEvent: {event_type: EventType (Created, Update, Deleted, Preexisting, PostExpiryOverride), time, entity}

OverrideEntityRequest: {entity, field_path: string[], provenance}

### Filter System (predicate algebra)
Statement (recursive, oneof):
- and: AndOperation {predicate_set | statement_set}
- or: OrOperation {predicate_set | statement_set}
- not: NotOperation {predicate | statement}
- list: ListOperation {list_path, list_comparator (AnyOf), statement}
- predicate: Predicate {field_path, value, comparator}

Comparator enum: MatchAll, Equality, In, LessThan, GreaterThan, LessThanEqualTo, GreaterThanEqualTo, Within (geo), Exists, CaseInsensitiveEquality, CaseInsensitiveEqualityIn, RangeClosed

Value (oneof): boolean, numeric (double/float/int32/int64/uint32/uint64), string, enum (int32), timestamp, bounded_shape (GeoPolygon), position, heading, list (nested values), range (start/end numeric)

---

## CJADC2 / UC2 CONCEPTS — ARCHITECTURAL PATTERNS

### Three Data Flow Types [from stage1]
1. **Commands** — flow DOWN, intent-bearing, infrequent, MUST be reliable (ACK'd), small (~100-200 bytes), highest priority on constrained links
2. **Status** — flow UP, task-coupled reporting (accepted/executing/complete/failed), infrequent, MUST be reliable (ACK'd), directly coupled to commands
3. **Telemetry** — flow UP, entity-state broadcast, frequent, lossy-tolerant (missing updates OK), not tied to any command, fire-and-forget

Commands and Status are the C2 loop. Telemetry is situational awareness.
Different QoS: Commands/Status get ACK_REQUEST, Telemetry is best-effort.

### Auftragstaktik / Mission-Type Tactics
- Commander gives intent + constraints ("go here, observe, by this time")
- Status reports against intent ("accepted, executing, complete")
- Telemetry is NOT part of the order structure — it's self-awareness shared
- Commander gets mission reports, not GPS feeds. GPS is for the ops center map.

### DDIL Conditions (Denied, Disrupted, Intermittent, Limited)
- DDILCondition [enum]: Normal, Limited, Intermittent, Disrupted, Denied
- Link degradation affects what data can flow and at what rate
- Must gracefully degrade: full telemetry → meta-telemetry → status-only → autonomous

### Multi-Rate Meta-Telemetry Pattern
Three tiers keyed to available bandwidth:
1. Essential state (always, low-rate): position, heading, battery, armed, mode — cf. MAVLink HIGH_LATENCY2
2. Track updates (moderate-rate): targets, detections, tracks
3. Rich artifacts (opportunistic, cached): imagery, video, point clouds, maps

### Delay/Disruption Tolerant Networking (DTN)
- Bundle Protocol v7 (RFC 9171): store-carry-forward overlay
- Nodes cache bundles when no route exists, forward when connectivity returns
- Complements real-time mesh (OLSRv2 / batman-adv) at L2/L3
- BundleNode: node_ref, storage_capacity_bytes, custody_acceptance (bool), priority_scheme

### Conflict-Free Replicated Data Types (CRDTs)
- Enable partition-tolerant state: concurrent updates merge deterministically without coordination
- Strong eventual consistency: all replicas converge
- Use for: entity annotations, track correlation votes, shared map annotations, task status
- CRDTType [enum]: GCounter, PNCounter, GSet, ORSet, LWWRegister, MVRegister, RGA
- AnnotationLayer: layer_id, entity_ref, annotations (map field_path → CRDTValue), last_merged_time

### Behavior Trees (autonomy orchestration)
- Alternative to FSMs for mission autonomy
- BehaviorNode types [enum]: Sequence, Selector (Fallback), Parallel, Condition, Action, Decorator, SubTree
- BehaviorTree: root_node (BehaviorNode), tick_rate_hz
- BehaviorNodeStatus [enum]: Success, Failure, Running
- Composable: nodes are reusable, subtrees nestable
- Asynchronous actions first-class (for real hardware that doesn't complete instantly)
- BehaviorTreeLibrary: named_trees (map name → BehaviorTree), named_nodes (map name → BehaviorNode)

### UCI (Universal Command and Control Interface) / STANAG 4586
- Mission-level C2 messages (not stick control)
- Interoperability levels:
  - Level 1: Indirect receipt/transmission of UA data (relay through GCS)
  - Level 2: Direct receipt of UA data (sensor feeds)
  - Level 3: Control/monitoring of UA payload (sensor control)
  - Level 4: Control/monitoring of UA (flight control)
  - Level 5: Control/monitoring of UA launch and recovery
- InteropLevel [enum]: Level1_IndirectRelay, Level2_DirectReceipt, Level3_PayloadControl, Level4_FlightControl, Level5_LaunchRecovery

### Task Allocation (distributed)
- Auction-based: agents bid on tasks, highest bidder wins
- Market-based: economic models for resource allocation
- Factors: distance_to_task, fuel/battery, sensor_match, weapon_match, workload, priority
- AllocationBid: agent_ref, task_ref, score (float), factors (map factor_name → score)
- AllocationResult: task_ref, winning_agent, bids_received (int), allocation_time

### JDL Fusion Model (levels)
- Level 0: Source preprocessing (sensor-level)
- Level 1: Object assessment (single target estimation from multi-sensor)
- Level 2: Situation assessment (relationships, patterns, context)
- Level 3: Impact assessment (what does this mean for the mission)
- Level 4: Process refinement (optimize collection and processing)
- FusionLevel [enum]: L0_SourcePreprocessing, L1_ObjectAssessment, L2_SituationAssessment, L3_ImpactAssessment, L4_ProcessRefinement

### Content Addressing / Mesh CDN
- Artifacts (imagery, video, models) stored by content hash (SHA-256)
- Retrieved by fingerprint, not location
- Tiered lookup: local cache → peer mesh → gateway → cloud
- Enables deduplication across disconnected nodes that later reconnect
- ContentAddress: sha256_hash (bytes), size_bytes (uint64), mime_type (string)
- CacheEntry: content_address, local_path, cached_time, ttl_seconds, access_count

### Partial-State / Delta Updates
- JSON Patch (RFC 6902): targeted field-level updates
- Entity components are independently updatable — don't need to send full entity
- Enables bandwidth-efficient updates: only changed fields flow
- DeltaUpdate: entity_id, changed_components (list of component_name), patch_operations (list of JSONPatchOp)
- JSONPatchOp: op (add|remove|replace|move|copy|test), path (string), value (any)

### Provenance Standard
- W3C PROV model: Entity, Activity, Agent, derivedFrom, wasGeneratedBy, wasAttributedTo
- CoT flow-tags: ordered list of system names that processed an event
- Lattice Provenance: integration_name, data_type, source_id, source_update_time, source_description
- ProvenanceChain: entries (ordered list of ProvenanceEntry)
- ProvenanceEntry: system_name, processing_time, action (Originated|Relayed|Fused|Transformed|Enriched|Filtered)

### DDS QoS Policies (for pub-sub)
- Reliability: BestEffort, Reliable
- Durability: Volatile, TransientLocal, Transient, Persistent
- History: KeepLast(depth), KeepAll
- Liveliness: Automatic, ManualByParticipant, ManualByTopic
- Deadline: period (max time between samples)
- LatencyBudget: duration (acceptable delay)
- Ownership: Shared, Exclusive (single publisher wins)
- OwnershipStrength: int (priority among exclusive publishers)

### Coalition Interoperability
- MIP (Multilateral Interoperability Programme): NATO semantic reference for C2
- JC3IEDM: Joint C3 Information Exchange Data Model
- Semantic alignment: mapping local ontology to shared coalition ontology
- National caveats: restrictions on data sharing per nation
- Releasability: which nations/coalitions may see which data
- InteropProfile: partner (Nationality), shared_classification_ceiling, protocol_bridge_ref, data_filters

### Safety and Assurance
- Deconfliction: airspace separation between autonomous agents
- Fratricide prevention: positive ID before engagement
- Runtime assurance: verified safety properties enforced at execution time
- Safety backbone: assured control layer that can override autonomy
- SafetyConstraint: type (GeofenceViolation, CollisionRisk, ROEViolation, CommLoss, BatteryBingo), action (RTL, Land, Loiter, Hold, Alert), priority (int)
- RuntimeAssurance: constraints (list of SafetyConstraint), override_authority (Entity ref), active (bool)

---

## ADDITIONAL ATOMIC CONCEPTS (gap fills)

### Gimbal Control (missing from Control → Process → Action)
- GimbalCommand: mode (GimbalMode), target (Position or AzimuthElevation or FrameCoord or EntityRef)
- GimbalMode [enum]: Stow, Manual, TrackEntity, PointAtPosition, PointAtAzEl, ScanPattern, StabilizedHold, ReturnToCenter
- GimbalState: current_azimuth, current_elevation, current_fov_h, current_fov_v, stabilized (bool), mode, tracking_entity_ref (optional)
- GimbalLimits: min_azimuth, max_azimuth, min_elevation, max_elevation, max_slew_rate_deg_s

### Camera Control (missing)
- CameraCommand: action (CameraAction), parameters
- CameraAction [enum]: TakePhoto, StartRecording, StopRecording, SetZoom, SetFocus, SetExposure, SetWhiteBalance, SetPalette (IR), ToggleNightVision
- CameraState: recording (bool), photos_taken (int), storage_remaining_pct, current_zoom, current_fov, resolution, frame_rate

### Geofence Actions (expanding geofence trigger behavior)
- GeofenceResponse [enum]: None, Report, Warn, Loiter, RTL, Land, Brake, MissionPause, Fence (stop at boundary)
- Geofence now fully: geometry + floor + ceiling + type (KeepIn/KeepOut/Ditch/Loiter) + response + enabled + priority

### MAVLink HIGH_LATENCY2 Fields (meta-telemetry for degraded links)
The essential-state message for DDIL conditions:
- timestamp (ms since boot)
- type (aircraft type)
- autopilot
- heading (degrees/2)
- target_heading
- throttle (percent)
- airspeed, groundspeed (m/s * 5)
- altitude (meters)
- target_altitude
- climb_rate (m/s * 10)
- battery_remaining (percent)
- temperature_air (degrees)
- wp_num (current waypoint)
- failure_flags (bitmask: GPS, Gyro, Accel, Mag, Terrain, Battery, RC, Link, Mission, GeoFence, Estimator, VTOLTransition, AbsolutePressure, DifferentialPressure)
- target_distance (km/10)
- custom0, custom1, custom2 (application-specific int8)
- wind_heading (degrees/2)
- ePH, ePV (position uncertainty, cm)

### Failsafe Conditions (expanding from HiveOS)
- FailsafeType [enum]: RCLost, DataLinkLost, BatteryLow, BatteryCritical, GPSLost, GeofenceBreach, MotorFailure, IMUFailure, BarometerFailure, TerrainFollowLost, MissionInvalid, CommunicationLost, HighWind, Crash
- FailsafeAction [enum]: None, RTL, Land, Loiter, Descend, Terminate, Continue, SmartRTL, Brake, Parachute, HoldPosition

### NIIRS (National Imagery Interpretability Rating Scale)
- Rating 0-9, floating point for precision
- 0: Interpretability of imagery is precluded
- 1: Distinguish between major land use classes
- 3: Detect individual buildings
- 5: Identify vehicles by type
- 7: Identify equipment mounted on vehicles
- 9: Identify individual items on the ground (eg grenades)
- Used in: Map task min_niirs, ISR collection requirements

### Engagement Sequence (atomic steps from OODA/F2T2EA mapped to schema)
Find: Detection (Data → Intel)
Fix: Classification + Position refinement (Data → Intel)
Track: Track creation/update (Data → Intel)
Target: TargetEntry creation, engagement authorization request (Control → Directive)
Engage: Fire mission execution, weapon release (Control → Process → Action)
Assess: BDA result (Data → Intel)

### Link Budget Calculation (expanding comms)
- PathLoss: frequency_hz, distance_m, environment (FreeSpace, Urban, Suburban, Forest, Overwater)
- TransmitPower_dBm: float
- AntennaGain_dBi: transmit and receive
- ReceiverSensitivity_dBm: float
- SystemMargin_dB: float
- EffectiveRange_m: derived from above
- LinkMargin: link_budget_ref, actual_snr_dB, required_snr_dB, margin_dB, link_quality (Good, Marginal, Poor, NoLink)

### Video Pipeline (expanding from CO)
- VideoSource: entity_ref, camera_id, stream_id, encoding (StreamEncoding), transport (StreamTransport), resolution_w, resolution_h, fps, bitrate_bps
- VideoAnalyticsPipeline: source_ref, models_loaded (list of model_id), detection_classes (list), tracking_enabled (bool), classification_enabled (bool)
- VideoAnnotation: frame_id, timestamp, annotations (list of: bbox, label, confidence, track_id, action)
- VideoRecording: source_ref, start_time, end_time, storage_path, size_bytes, format

### Terrain Following / Avoidance
- TerrainFollowConfig: mode (TerrainFollowMode), clearance_m, lookahead_m, max_climb_rate_mps, max_descent_rate_mps
- TerrainFollowMode [enum]: Off, TerrainFollow, ObstacleAvoid, TerrainAndObstacle, ConstantAGL
- TerrainData: source (TerrainDataSource), resolution_m, coverage_area (Geometry)
- TerrainDataSource [enum]: DTED0, DTED1, DTED2, SRTM, LIDAR, Onboard, RealTime

### Swarm Concepts (expanding from CO)
- SwarmBehavior [enum]: Flock, Spread, Converge, Orbit, Search, Follow, Custom
- SwarmState: swarm_ref, behavior, centroid (Position), spread_radius_m, member_count, connectivity_pct
- SwarmCommand: behavior (SwarmBehavior), target (Position or Geometry or Entity ref), parameters (spacing_m, speed_mps, altitude_m)
- SwarmHealth: members_online, members_offline, members_degraded, lowest_battery_pct, average_battery_pct

### Time Synchronization (critical for fusion)
- TimeSync: source (TimeSyncSource — GPS, NTP, PTP, Manual), offset_from_utc_ns (int64), accuracy_ns (uint64), last_sync_time
- ClockDrift: estimated_drift_ppm (parts per million), last_calibration_time
- Timestamps across systems MUST be comparable — fusion, correlation, and track association all depend on temporal alignment

### Coordinate Transforms (what actually happens at boundaries)
When data crosses systems, coordinates must transform:
- WGS84 ↔ ECEF ↔ ENU ↔ Body frame
- Geodetic ↔ UTM ↔ MGRS
- HAE ↔ MSL (geoid separation model)
- True North ↔ Magnetic North ↔ Grid North (declination + convergence)
- CoordinateTransform: from_frame, to_frame, method (Analytical, LookupTable, Interpolated), accuracy_m

### Message Sequence Numbers and Ordering
- SequenceNumber: uint32 or uint64, monotonically increasing per source
- Used for: detecting gaps (missed messages), ordering (reconstruct sequence), deduplication (reject replays)
- SequenceGap: source_ref, expected_seq, received_seq, gap_count, time_detected

### Compression for Constrained Links
- CompressionPolicy: algorithm (None, LZ4, Zstd, GZIP), level (1-22 for Zstd), min_message_size_bytes (don't compress below this)
- On Meshtastic/LoRa: every byte matters. Position can be encoded in 8-12 bytes with delta compression vs 24+ bytes raw.
- DeltaCompression: reference_message_seq, changed_fields_bitmask, field_deltas (only changed values)

### Entity Lifecycle Events (complete list merging all sources)
EntityLifecycleEvent [enum]:
- FirstSeen (new entity detected/created)
- Updated (any component changed)
- LocationChanged (position moved beyond threshold)
- StatusChanged (operational status change)
- HealthChanged (health degradation or recovery)
- Correlated (merged with another entity)
- Decorrelated (split from another entity)
- Overridden (manual override applied)
- OverrideRemoved
- Expired (TTL exceeded, no updates)
- PostExpiryOverride (manually kept alive after TTL)
- Deleted (explicitly removed)
- Lost (comm lost, position stale beyond threshold)
- Recovered (comm restored after loss)
- Handed off (control transferred)
- TaskAssigned
- TaskCompleted

### Entity State Snapshot vs Delta
Two fundamental message shapes (already in typology as MessageShape):
- Snapshot: complete state at point in time. Used for: initial publish, periodic full-state refresh, entity creation
- Delta: only changed fields. Used for: efficient updates, bandwidth-constrained links
- Schema must support both: every struct must be fully optional (all fields nullable) so deltas can carry partial updates

### Route Segment Types (expanding path planning)
- RouteSegmentType [enum]: GreatCircle, Rhumbline, Straight (projected), TurnArc, Orbit, Hold, Approach, Departure, Missed, Emergency
- RouteSegment: type, start_point, end_point, altitude, speed, turn_radius_m (for arcs), direction (for orbits)
- AltitudeConstraintOnSegment: min_altitude, max_altitude, altitude_reference
- SpeedConstraintOnSegment: min_speed, max_speed, unit

### Notification / Alert Severity Levels (harmonizing across sources)
All systems use some form of severity. Mapping:
- Lattice AlertLevel: Advisory, Caution, Warning
- HiveOS: Failsafe bool (binary)
- CO: PriorityLevel (Low, Normal, High, Critical)
- Military: Routine, Priority, Immediate, Flash, Flash Override
- Generic: Info, Low, Medium, High, Critical, Emergency

### Cross-Domain Fire Integration
How fire support messages map to the schema:
- Call For Fire → Communication → Message → Command → NavigationCommand-adjacent but really a FireSupportCommand
- Fire mission → Control → Task (FireMission)
- Shot/Splash/Rounds Complete → Communication → Message → Response
- Adjust Fire → Communication → Message → Command (correction)
- BDA → Data → Intel → Detection/Classification
- End of Mission → Communication → Message → Response
- FireSupportCommand should be a Command variant alongside Navigation, Mode, Parameter, Actuator

### Missing Command Variants (corrected — Tasks vs Commands)

Commands are immediate, single-action directives. Tasks have intent, actions, and an objective.

Actual Commands (immediate control):
- FireSupport: adjust fire, cease fire, check fire (NOT call for fire — that initiates a FireMissionTask)
- EW: cease jamming, start/stop emission (NOT sustained jam/spoof/DF — those are EWActionTask)
- Communication: change frequency, switch net, relay command
- Emergency: abort, RTL, emergency land, eject payload, parachute deploy
- Gimbal/Camera: already exist as GimbalCommand, CameraCommand

NOT Commands — already Tasks:
- "sensor tasking" → ObserveTask, SurveyTask, ScanTask
- "collection cueing" → ImproveTrackQualityTask
- "call for fire" → FireMissionTask
- "jam/spoof/direction-find" (sustained) → EWActionTask
- "supply request" → ResupplyMission
- "evacuation request" → MEDEVACMission

---

# CONCEPTS ADDED FROM UNIFIED CJADC2 DEEP RESEARCH

## F2T2EA (Find, Fix, Track, Target, Engage, Assess)

The time-sensitive targeting workflow from US joint doctrine (JP 3-60). Maps to occid concepts:

- **Find** → Detection from sensors, ISRTask, initial Entity creation
- **Fix** → Geopositioning, Detection.confidence, Position component
- **Track** → TrackComponent fusion, ImproveTrackQualityTask, Correlated lifecycle event
- **Target** → TargetableTask routing, FireMissionTask, ObserveTask for BDA prep
- **Engage** → Task execution by weapon platform, TaskStatus transition
- **Assess** → BDA (battle damage assessment) via Detection/Classification on target post-engagement

## JDL Fusion Levels (Joint Directors of Laboratories model)

Fusion produces tiered information products, not raw streams [LA, SG, CT inference]:

- **Level 0 (Source Pre-processing)** → Raw sensor data, Detection.source_data (pixels, RF samples, point clouds)
- **Level 1 (Object Assessment)** → TrackComponent, fused position/velocity, uncertainty ellipse, Detection classification
- **Level 2 (Situation Assessment)** → RelationshipComponent between entities (hostile/friendly proximity, formation, formation patterns)
- **Level 3 (Impact Assessment)** → Threat assessment, priority escalation, Alert component
- **Level 4 (Process Refinement)** → Sensor management, adaptive tasking (SensorTask retargeting based on fusion quality)

## Covariance Intersection (Track-to-Track Fusion)

When fusing tracks from independent sources with unknown cross-correlation [LA inference, ISIF proceedings]:

- Never naively average or multiply covariances — leads to overconfident fusion
- Use covariance intersection: fused mean = ω·P₂·(ω·P₂ + (1-ω)·P₁)⁻¹·μ₁ + (1-ω)·P₁·(ω·P₂ + (1-ω)·P₁)⁻¹·μ₂ where ω minimizes trace
- Produces conservative (larger) covariance that is safe regardless of unknown correlation
- Relevant for multi-node fusion where track cross-correlation cannot be computed

## DDS / ROS 2 Quality of Service (QoS) Polices

Data-centric pub-sub with configurable delivery semantics [LA inference, Shield AI EdgeOS inference]:

**Reliability** [enum]:
- BestEffort — drop messages under congestion (high-rate telemetry, video frames)
- Reliable — guarantee delivery with retransmit (commands, task updates, entity state)

**Durability** [enum]:
- Volatile — late joiners get nothing (live sensor feeds)
- TransientLocal — late joiners get last value (entity state snapshot, config)

**History** [enum]:
- KeepLast(depth=N) — retain most recent N samples
- KeepAll — buffer all samples (risk of unbounded growth)

**Liveliness** [enum]:
- Automatic — publisher must write within lease_duration to be considered alive
- ManualByTopic — application explicitly asserts liveliness

**Deadline** — maximum acceptable period between samples; violation triggers callback

**Lifespan** — maximum age after which a sample is considered stale (distinct from entity TTL)

**Partition** — logical segmentation of topic namespace within same physical bus

## DDS-XRCE (Extremely Resource Constrained Environments)

Protocol for microcontrollers and constrained devices to participate in DDS domains via a broker agent [ML adjacency]:

- XRCE Agent runs on edge compute node, manages DDS participation
- XRCE Client runs on MCU/autopilot, sends compact publish/subscribe requests
- Eliminates need for full DDS stack on resource-constrained endpoints
- Maps to MAVLink→bridge→DDS pattern: autopilot publishes MAVLink, agent translates to DDS topics

## MANET Routing Patterns

Mesh networking for DDIL environments [HL, LA inference]:

**OLSRv2 (Optimized Link State Routing v2)** [RFC 7181]:
- Proactive routing — maintains routes before traffic needs them
- Multipoint relays (MPRs) reduce control overhead vs. flooding
- Suitable for moderately sized swarms (tens to hundreds of nodes)
- Convergence time: seconds, acceptable for COP but not tight control loops

**B.A.T.M.A.N. Advanced (batman-adv)** — Linux kernel module:
- Reactive routing — discovers routes on demand
- Originator messages at L2, no IP dependency
- Transparent bridge — applications see single L2 domain
- Trade-off: L2 broadcast domain scaling challenges; needs segmentation for large swarms

**Routing selection by traffic class**:
- Commands/tasking → OLSRv2 (proactive, low latency)
- Bulk artifacts → DTN overlay when MANET partitioned
- COP/telemetry → Either, with reliability policy from QoS layer

## DTN (Delay/Disruption Tolerant Networking) — BPv7

Store-carry-forward overlay for partitions and extreme delay [RFC 9171]:

- Bundle Protocol v7 operates as overlay above transport
- Nodes buffer bundles when no route exists, forward when contact available
- UAVs serve as opportunistic carriers when mobile
- Not for tight control loops; supports eventual delivery of:
  - Imagery/artifacts from disconnected nodes
  - Mission logs and audit trails
  - Fused track updates after prolonged partition
  - Entity updates with high TTL tolerance

## CRDTs (Conflict-free Replicated Data Types)

Eventually consistent data structures for decentralized COP [LA inference, ETH Zurich SSZ paper]:

- Allow concurrent updates from multiple nodes without coordination
- Commutative, associative, idempotent merge — any order produces same result
- Applicable types:
  - G-Counter (grow-only): entity sighting counts
  - PN-Counter: entity status vote tallies
  - OR-Set (observed-remove): entity component lists, task assignments
  - LWW-Register (last-writer-wins): single-value fields with timestamp tiebreaking
- Use when partition tolerance > strong consistency (DDIL environments)
- Not needed for real-time control loops; for COP state reconciliation after healing

## MIL-STD-2525 Symbology

Standardized warfighting symbology for map-centric COP [CT, LA]:

- SIDC (Symbol Identification Code) — 20-character alphanumeric code encoding:
  - Context (Reality, Simulation, Exercise, Future)
  - Standard identity (Friend, Hostile, Neutral, Unknown)
  - Hierarchy (from echelon down to equipment item)
  - Status (Active, Planned, Present, Anticipated, etc.)
  - Modifier fields (HQ staff fill, unique designation, speed, etc.)
- SIDC maps to Entity.type/identity fields in occid schema
- Provides common visual encoding across coalition partners
- APP-6(D) is NATO equivalent with minor differences

## Semantic Layer / Ontology as Bridge

Formal ontology layer between raw feeds and applications [LA, Palantir inference]:

**Object types** — Entity categories (Vehicle, Person, Installation, Sensor)

**Property types** — Typed attributes on objects (position, affiliation, status)

**Link types** — Relationships between objects (ReportsTo, LocatedAt, Commands, Threatens)

**Action types** — Permissible operations on objects (Assign, Revoke, Update, Correlate)

**Ontology mappings**:
- MIP Information Model (MIM) — semantic reference embodying JC3IEDM concepts
- Lattice Entity/Task/Object three-model system
- occid maps to this via Component system (properties) and Relationship structs (links)

**Design principle**: Raw feeds ingest into ontology objects; applications consume ontology objects, not raw feeds.

## Mesh CDN / Edge Object Store Caching

Tiered artifact availability across partitioned meshes [LA]:

**Local cache** — Object already on node (zero network cost)

**Mesh peer** — Artifact cached on reachable neighbor (one hop)

**Origin** — Artifact requires retrieval from source node (may be partitioned)

**Caching policy**:
- Checksum (SHA256) on every artifact upload — integrity verification on fetch
- TTL on cached copies — evict stale artifacts to free edge storage
- Tiered lookup: try local → mesh peer → origin → DTN bundle
- Thumbnail previews cached more aggressively than full-resolution

## W3 Event Model (What/Where/When)

CoT/TAK-style compact event schema for shared SA [CT]:

- **What** — Event type, platform type, activity classification
- **Where** — Position (lat/lon/alt), uncertainty ellipse
- **When** — Timestamp, TTL/stale time

- Core schema is minimal; detail goes in extensible XML/JSON extensions
- Maps naturally to:
  - Low-rate COP upkeep (periodic position broadcasts)
  - Airspace deconfliction overlays for swarms
  - Human-readable situation awareness on constrained displays

## Behavior Trees (Autonomy Runtime)

Deterministic execution model for onboard agent decision-making [SG, Shield AI inference]:

- Composable tree of behavior nodes: Sequence, Selector, Parallel, Decorator
- Leaf nodes: Actions (execute), Conditions (guarded), Services (async call)
- Returns: Success, Failure, Running (for long-running actions)
- Advantages over state machines:
  - Explicit priority ordering (selectors try children left-to-right)
  - Easy to insert/replace subtrees without breaking existing logic
  - Natural mapping from mission intent to execution sequence
- Safety runtime assurance wraps behavior trees:
  - Monitor node checks invariants (altitude floor, geofence, comm timeout)
  - Override transitions to safe state (RTL, hover, loiter) on violation

## Lattice Task Model (Reference)

Mission-level tasking primitives [LA] — maps to occid Task/Control/Route concepts:

**Deliberate tasks** — Planned, sequential actions executable by asset or team
- Task has intent (objective), routing (delivery path), lifecycle (state machine)
- Status propagation: Created → Assigned → InProgress → Completed/Failed/Cancelled

**Distributed and persisted** — Tasks survive across COP nodes mesh network
- Task state replicates via pub-sub with Reliable QoS
- Task execution tracked even if originating node goes offline

**Team-level tasks** — Single task routed to multiple assets with coordination
- Team task decomposes into individual sub-tasks
- Requires task allocation mechanism (auction, consensus, or centralized assignment)

## Multi-Rate Telemetry

Different data rates for different information classes under bandwidth constraints [LA, ML, CT inference]:

| Rate | Content | Protocol/Pattern |
|---|---|---|
| High-rate (10-50 Hz) | Flight control, gimbal, raw detections | DDS Reliable, MAVLink |
| Medium-rate (1-5 Hz) | Platform position, health, mode | DDS BestEffort + TransientLocal |
| Low-rate (0.1-1 Hz) | COP entity updates, W3 events | CoT/TAK, MAVLink HIGH_LATENCY2 |
| Event-driven | Alerts, state transitions, task updates | Reliable pub-sub, COMMAND_ACK |
| Opportunistic | Full artifacts, logs, high-res imagery | DTN / Mesh CDN when bandwidth available |

## Lattice Entity Component Indicators (additional)

From LA entity indicators model — flags that govern entity handling:

- **simulated** (bool) — entity originates from simulation, marked differently in COP
- **exercise** (bool) — entity is part of training exercise, not real-world
- **emergency** (bool) — entity is in emergency state, escalates priority
- **c2** (bool) — entity is a C2 node (command and control asset)
- **egressable** (bool) — entity should be shared to external/coalition systems
- **starred** (bool) — operator-flagged importance, persistent highlight in COP

## Provenance Chain-of-Processing (Flow-Tags)

Trace of how entity data was produced and transformed [LA, CT CoT flow-tags]:

- Each processing system appends its identifier to a provenance chain
- CoT flow-tags schema (DoD public release) adds system fingerprints to events
- Enables reconstruction of processing lineage: Sensor A → Detector B → Fusion C → COP D
- Lattice requires provenance.integration_name on every entity — not optional
- In occid: Detection.source_ref, TrackComponent.fused_from, Entity.provenance[]
- For coalition: provenance determines trust level and sharing eligibility

## DDIL Design Principle

Explicit design assumption for Denied, Disrupted, Intermittent, Limited-bandwidth environments:

- **Network is assumed unreliable** — services must degrade gracefully, not crash
- **Local operation is primary** — every node must function standalone when partitioned
- **Bandwidth is scarce** — delta updates, compression, multi-rate telemetry mandatory
- **Reconciliation is eventual** — CRDTs or last-writer-wins for COP state repair
- **No single point of failure** — mesh topology, distributed pub-sub, DTN fallback

## Time-Sensitive Targeting Metrics

Key performance indicators from F2T2EA workflow [LA, CT inference]:

- **Sensor-to-shooter time** — Time from first detection to weapon release decision
- **COP freshness** — Maximum age of position data for tracked entities
- **Decision latency** — Time from alert to operator action/task creation
- **Link availability** — Percentage of time communication paths are usable
- **Track quality** — Covariance/uncertainty metric for fused position estimate

## UxAS (Unmanned Systems Autonomy Services) — AFRL Reference Architecture

AFRL's published architecture for distributed autonomous teaming [AFRL paper]:

- **Architecture concept** — Service-oriented middleware where autonomy capabilities are exposed as composable services
- **Service orchestration** — Services register capabilities, subscribe to relevant data, and produce outputs consumed by other services
- **Decentralized execution** — Each UAV runs its own autonomy services; no single point of coordination failure
- **Service types include**:
  - Route planning and optimization
  - Task allocation and assignment
  - Sensor management and tasking
  - Collision avoidance and deconfliction
  - Energy management and refueling/recharging decisions
  - Health monitoring and fault management
- **Maps to occid**: Task system orchestration, autonomous Task routing, SensorTask management

## Gerkey Task Allocation Taxonomy Formalism

Formal classification of multi-robot task allocation problems [TAMU robotics paper]:

**Single-task robot (ST) vs Multi-task robot (MT)**:
- ST: Robot can execute only one task at a time (most UAVs)
- MT: Robot can execute multiple tasks concurrently (UAV with ISR + comms relay)

**Single-robot task (SR) vs Multi-robot task (MR)**:
- SR: One robot suffices to complete the task (single UAV recon)
- MR: Multiple robots required (coordinated perimeter, formation search)

**Four problem classes**:
- **ST-SR**: Simplest — one robot, one task. Assignment = matching problem.
- **ST-MR**: Complex — tasks need teams. Requires set-partitioning.
- **MT-SR**: Complex — robots juggle tasks. Requires scheduling.
- **MT-MR**: Most complex — teams and concurrent execution.

**Instantaneous assignment (IA) vs Time-extended assignment (TA)**:
- IA: Assign available tasks to available robots now (greedy/auction)
- TA: Plan assignments over time horizon considering future availability

**Occid relevance**:
- Most occid UAV operations fall into ST-SR (simple assign-then-execute)
- Swarm behaviors may be ST-MR (multiple UAVs needed for one task)
- Multi-payload platforms enable MT-SR (UAV doing ISR and comms relay simultaneously)
- Task allocation mechanism selection depends on classification

## Shield AI EdgeOS Runtime Primitives

Hivemind EdgeOS public framing of autonomy runtime platform [Shield AI]:

- **Discovery** — Nodes find each other on the network without central registry
- **Time synchronization** — Shared timebase across distributed nodes (critical for fusion)
- **Configurable QoS** — Per-topic delivery guarantees, not global best-effort
- **Network feedback** — Applications receive explicit link quality metrics
- **Deterministic messaging** — Predictable latency bounds for safety-critical paths
- **Runtime safety assurance** — Monitors enforce safety envelopes regardless of mission logic state
- **Operates without comms/GNSS/human input** — Designed for GPS-denied, comms-denied autonomous operation
- **Maps to occid**: TimeSync module, QoS layer, Discovery service, SafetyRuntimeMonitor

## Entity-Component Partial State Tolerance

Design pattern from Lattice's entity model — "bags of components" [LA]:

- **Every entity is identified by stable ID** — UUID or URN, not by completeness of data
- **Components are optional and independent** — Position, Classification, Motion, Health, etc.
- **Partial updates are first-class** — Never require full entity resend for single field change
- **Missing component is normal state** — Not every sensor provides every component
- **Expiry time on every component** — Different data ages out at different rates
  - Position: short TTL (seconds to minutes depending on platform)
  - Classification: medium TTL (valid until contradicted)
  - Identity: long TTL (stable identification)
- **Provenance.integration_name mandatory** — Every component update carries source
- **Partial-state tolerance enables**:
  - Incremental entity construction from heterogeneous sources
  - Efficient delta updates over constrained links
  - Degraded operation when some components become unavailable
  - Clean garbage collection when TTLs expire without full-entity deletion

**Occid implementation mapping**:
- Entity.components dict → component bag
- Component struct with updated_at, confidence, provenance, ttl → per-component lifecycle
- Entity update handler merges partial deltas → partial-state-tolerant reconciliation

## CoT/TAK Schema Details

Beyond W3 model, CoT defines extensible event structure:

**Core event fields**:
- uid — unique event identifier
- type — CoT event type string (e.g., "a-f-G-E-V-C" for ground vehicle friendly)
- how — how event was generated (h-g-i-g-o = manual, m-g = manual GPS, a-g = autonomous)
- time — event creation timestamp
- start — validity start
- stale — validity end (TTL)

**Detail extensions** (optional, extensible):
- contact — callsign, affiliation, role
- vitals — battery %, status, equipment state
- track — course, speed, heading, accuracy
- remarks — free-text annotations
- link — references to related UIDs (relates, parent, child)
- sensor — sensor cone geometry
- color — display tint
- file — associated file/artifact reference
- video — video stream URL (RTSP, WebRTC)

**Protocol transports**:
- Multicast UDP — LAN/broadcast distribution
- TCP/TLS — secure point-to-point
- HTTP/REST — API integration
- **occid already has Communication.Message which maps to CoT events**

## AfRL UCI (Unmanned Control Interface)

Messages for mission-level command and control interoperability [AFRL VDL]:

- **Mission-level abstraction** — Messages are independent of specific airframe/payload
- **Enables**: Any compliant UAV to receive and execute mission commands from any compliant C2 system
- **Message categories**:
  - Mission planning (route, objectives, constraints)
  - Task allocation (assign task to platform)
  - Payload control (sensor tasking, imagery requests)
  - Status reporting (platform health, task completion)
- **Maps to occid**: Task model, Control.Command variants, Platform.Status reporting

## Coalition Semantics and Interoperability

Mapping between different ontologies in coalition/interoperability scenarios:

**MIP (Multilateral Interoperability Programme) Information Model**:
- Semantic reference for C2 domain concepts
- Embodies JC3IEDM (Joint Command, Control, and Consultation Information Exchange Data Model) operational concepts
- Defines standard object types, relationships, and actions for military operations
- DELTA tested for interoperability within NATO environment via CWIX (Coalition Warrior Interoperability Exercise)

**Coalition mapping challenges**:
- Different nations use different entity classification schemes
- Symbology varies slightly between MIL-STD-2525 (US) and APP-6(D) (NATO)
- Coalition sharing requires egressable flag filtering (what gets shared vs retained)
- Trust levels vary — some coalition partners receive less detail (classification downgrading)
- **In occid**: Entity.indicators.egressable, CoalitionFilter for outbound sharing rules

## DELTA Mission Control Workflow

Ukrainian system's drone operations coordination pattern:

- **Crews must enter into system**: UAV type, planned route, mission objective
- **Creates unified reporting and visibility**: All drone operations visible in shared COP
- **Supports**: Planning and coordination of drone operations across units
- **Integration**: DELTA provides real-time situational awareness on soldiers' smartphones/tablets/laptops
- **Source integration**: Radars, sensors, GPS trackers, radio intercepts, satellite imagery, drone footage, human reporting
- **Access patterns**: Layered battlefield map with filters for different intelligence products

## Sensor-to-COP Ingestion Pipeline

Full flow from raw sensor to tracked entity in COP:

```
Physical Sensor → Detection → Local Track → Fused Track → COP Entity
     ↓               ↓            ↓              ↓            ↓
  Raw data    Position +      Local           Multi-      Shared
              classification  tracking        source      entity graph
              with            with            fusion      with
              uncertainty     uncertainty     with CI     full
              bounds          ellipse         covariance  ontology
                                                        mapping
```

**Key transitions**:
- Detection → Track: temporal association, track initiation logic (M/N detections to declare)
- Local Track → Fused Track: cross-platform correlation, covariance intersection fusion
- Fused Track → Entity: ontology mapping, relationship resolution, provenance chaining

## Artifact Types and Classification (expanding from LA Objects model)

From Lattice object model — artifacts that exist as independent objects:

- **Image files** — captured imagery with metadata (GPS, timestamp, sensor params)
- **Video streams** — live or recorded video with stream URL reference
- **Thumbnail previews** — compressed previews for constrained bandwidth display
- **Detection metadata** — AI model output: detections, classifications, confidence scores
- **3D models** — reconstructed terrain or structure models
- **Map tiles** — cached geographic tiles for offline operation
- **Mission logs** — audit trail of task execution, platform decisions
- **Flight paths** — recorded telemetry tracks for replay and analysis

**Artifact integrity**:
- SHA256 checksum on upload
- Checksum verification on fetch/integrity check
- TTL-based garbage collection for cached copies
- Access control based on classification level and coalition sharing rules

## Architecture Reference Diagram

Canonical layered architecture for C3ISR/CJADC2 edge systems:

**Edge Connectivity Layer**:
- Bearers: RF + LTE/5G + SATCOM + wired
- MANET/Mesh Routing (OLSRv2, L2 mesh)
- DTN Overlay (store-carry-forward, BPv7)

**Edge Nodes**:
- Sensor Nodes (radars, EO/IR, SIGINT)
- UAV Edge Nodes (flight control + mission compute)
- Edge C2 Nodes (tablet/laptop/tactical server)

**Edge Middleware**:
- Pub-Sub/Streaming Bus (DDS/ROS2-like QoS)
- Low-bandwidth Telemetry (MAVLink + microservices)
- Event Meta-telemetry (CoT/TAK-style W3 events)

**Semantics + Fusion**:
- Ontology/Data Model (objects, links, actions)
- Entity/Track Graph (partial-state, TTL, provenance)
- Sensor + Track Fusion (uncertainty-aware)

**Control + Autonomy**:
- Mission Tasking Layer (intent, routing, lifecycle)
- Onboard Autonomy Runtime (behavior trees, planners)
- Multi-agent Allocation (auctions/consensus)

**Artifacts**:
- Edge Object Store / Mesh CDN (cache, integrity, TTL)
- Artifacts: imagery, video clips, thumbnails, models, tiles

## Sensor-to-COP-to-Action Message Sequences

Sequence 1: Detection to Fused Track
```
Sensor/Detector → COP Entity Graph: Publish/Update Track Entity (partial components)
COP Entity Graph → Track Fusion Service: Stream track updates & metadata
Track Fusion Service → COP Entity Graph: Publish fused track entity + confidence/uncertainty
```

Sequence 2: Mission Tasking
```
Operator UI → Tasking Service: Create mission task (intent + parameters)
Tasking Service → Taskable Agent: Route task to agent/team
Taskable Agent → Tasking Service: Update task status (accept/execute/complete/error)
```

Sequence 3: Artifact Flow
```
Sensor → Object Store/Mesh CDN: Upload artifact (image/clip/thumbnail) with checksum + TTL
Object Store/Mesh CDN → Operator UI: On-demand artifact retrieval via cache/mesh
Operator UI → COP Entity Graph: Annotate entity (classification, priority) via partial update
```

## Coalesced Design Backbone

Core problems:
- Operate under DDIL networking and partitions while keeping a coherent shared picture
- Fuse heterogeneous sensing into stable tracks and higher-level assessments with uncertainty, avoiding overconfidence
- Provide a semantic layer (ontology) that aligns humans, services, and edge agents; support coalition semantics and symbology
- Scale tasking from one operator to many UAVs through mission-level intent, routing, lifecycle, and status
- Deliver meta-telemetry (multi-rate) plus artifact survivability through caching/CDN and integrity checks

Key architectural primitives:
- Entity/track graph with composable components, TTL/expiry, and mandatory provenance
- Ontology layer mapping data to object/link/action types; "digital twin" semantics
- Task model for mission-level sequential actions; task routing, persistence, and status propagation
- Object/artifact store with mesh caching, tiered lookup, integrity checks, and TTL
- Communications substrate with QoS-aware pub-sub + constrained endpoints via agent bridges
- Low-bandwidth vehicle telemetry with specialized high-latency profile and reliable command microservices
- Autonomy runtime primitives: deterministic messaging, discovery, time sync, QoS, and safety/runtime assurance
