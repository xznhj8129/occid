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

