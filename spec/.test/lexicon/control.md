# Control 

## Autonomy

BehaviorNodeType:
- Sequence
- Selector
- Parallel
- Condition
- Action
- Decorator
- SubTree

BehaviorNodeStatus:
- Success
- Failure
- Running

## Control

TaskLevel:
- Technical
- Tactical
- Operational
- Strategic

TaskSubject:
- Maneuver
- ISR
- Effects
- Support
- EW

TaskStatus:
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

TaskErrorCode:
- Cancelled
- Rejected
- Timeout
- Failed

DeliveryStatus:
- Delivered
- PendingExecute
- PendingCancel
- PendingComplete

DeliveryErrorCode:
- Unavailable
- Timeout
- Rejected

InstructionProductType:
- StandingOrder
- SOP
- WARNO
- FRAGO

GimbalMode:
- Stow
- Manual
- TrackEntity
- PointAtPosition
- PointAtAzEl
- ScanPattern
- StabilizedHold
- ReturnToCenter

OODACycle:
- Observe
- Orient
- Decide
- Act

CameraAction:
- TakePhoto
- StartRecording
- StopRecording
- SetZoom
- SetFocus
- SetExposure
- SetWhiteBalance
- SetPalette
- ToggleNightVision

WaypointActionType:
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

OrbitPattern:
- Circle
- Racetrack
- FigureEight

OrbitDirection:
- Right
- Left

SearchPattern:
- Random
- Grid
- Spiral
- Sector
- Expanding

MovementTechnique:
- Traveling
- TravelingOverwatch
- BoundingOverwatch
- SuccessiveBounds
- AlternatingBounds

MovementRate:
- Normal
- Deliberate
- Hasty
- Forced
- Administrative

MovementFormation:
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

AttackType:
- Deliberate
- Hasty
- Spoiling
- Counterattack
- Raid
- Ambush
- Feint
- Demonstration

ApproachMethod:
- Frontal
- Flanking
- Envelopment
- TurningMovement
- Infiltration
- Penetration

DefenseType:
- AreaDefense
- MobileDefense
- Retrograde
- Delay
- Withdrawal
- Retirement

RouteSegmentType:
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

LaunchTrackingMode:
- GoToWaypoint
- TrackToWaypoint

LoiterType:
- Orbit
- Racetrack
- FigureEight
- Hold

OrbitDuration:
- UntilCommanded
- FixedTime
- FuelBased

WeaponsPosture:
- WeaponsFree
- WeaponsTight
- WeaponsHold

EMCONLevel:
- Full
- Limited
- Restricted
- Silent

EscalationLevel:
- ShowOfForce
- WarningShot
- Engage
- Destroy

DeconflictionType:
- Altitude
- Temporal
- Lateral
- Speed
- Route
- Frequency

AbortType:
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

FailsafeAction:
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

TriggerType:
- TimeReached
- PositionReached
- EventOccurred
- ThresholdExceeded
- ConditionMet
- OrderReceived
- EnemyAction
- FriendlyAction

InterfaceType:
- PWM 
- GPIO
- CAN 
- Serial 
- RC 

## Ew

EWActionType:
- Jam
- Spoof
- Deceive
- Intercept
- DirectionFind
- Monitor
- Deny

JamType:
- Noise
- Barrage
- Spot
- Sweep
- Responsive
- Follower

EWEffectType:
- SignalDegraded
- SignalDenied
- TargetDecoyed
- CommunicationsDisrupted
- NoEffect

EPType:
- FrequencyHopping
- SpreadSpectrum
- Encryption
- PowerControl
- DirectionalAntenna
- BurstTransmission

## Fire Support

EngagementMethod:
- PointTarget
- AreaTarget
- Suppression
- Destruction
- Neutralization
- Illumination
- Smoke
- Marking

FireType:
- Immediate
- Planned
- OnCall

WeaponType:
- Mortar
- Howitzer
- Rocket
- MLRS
- Missile
- DirectFire
- AirDelivered
- Naval

AmmunitionType:
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

ShellTrajectory:
- Low
- High
- Vertical

FireMissionStatus:
- Requested
- Approved
- Denied
- ShotOut
- SplashOver
- RoundsComplete
- EndOfMission
- Cancelled
- CheckFiring

EffectAchieved:
- Destroyed
- Neutralized
- Suppressed
- NoEffect
- Unknown

## Logistics

SupplyClass:
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

SupplyPriority:
- Routine
- Priority
- Immediate
- Emergency
