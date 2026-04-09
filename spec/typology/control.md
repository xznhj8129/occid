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

