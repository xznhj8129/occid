"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .information import Information

### Enums

class AirMissionPhase(IntEnum):
    ONLINE = 0
    PREPARING = auto()
    TAKEOFF = auto()
    ASSEMBLY = auto()
    HOLDING = auto()
    ENROUTE = auto()
    INITIAL = auto()
    OBJECTIVE = auto()
    EGRESS = auto()
    RETURN = auto()
    APPROACH = auto()
    LANDING = auto()
    SHUTDOWN = auto()

class AirMissionEvent(IntEnum):
    ONLINE = 0
    PREPARED = auto()
    LOADED = auto()
    READY_TAKEOFF = auto()
    TAKEOFF_COMPLETE = auto()
    ASSEMBLY = auto()
    ENROUTE = auto()
    HOLDING = auto()
    ACTING = auto()
    PROCEEDING = auto()
    RESUMING = auto()
    BINGO = auto()
    RTB = auto()
    LANDING = auto()
    LANDED = auto()
    SHUTDOWN = auto()
    ABORTING = auto()
    FAILING = auto()

class State_type(IntEnum):
    KINEMATIC = 0
    INTERNAL = auto()
    POSITION = auto()
    GUIDANCE = auto()
    SENSOR = auto()
    INPUT = auto()
    RESOURCES = auto()
    CONDITION = auto()
    LIFECYCLE = auto()
    ASSIGNMENT = auto()

### Models

class State(Information):
    'Telemetric, changing data describing the own state or condition of an object at a given time'

class Kinematic(State):
    pass

class TelemetryState(State):
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    mission_phase: AirMissionPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: float | None = None
    link_rssi: float | None = None
