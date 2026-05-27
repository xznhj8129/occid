"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Execution_type(IntEnum):
    PLAN = 0
    SEQUENCE = auto()
    ACTION = auto()

class PlannedUnitMission_type(IntEnum):
    MILITARY = 0

### Models

class Execution(Control):
    'How directed activity is structured and carried out'

class Plan(Execution):
    pass

class Sequence(Execution):
    pass

class Action(Execution):
    pass

class FlightPhasePlan(Sequence):
    phase: AirMissionPhase
    flight_level: FlightLevelBand | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: float | None = None
    delay_s: float | None = None
    airspeed: float | None = None
    path_offset: LocalDirection | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class PlannedUnitMission(Plan):
    unit_num: int
    callsign: str
    fl: float
    route_in: GeoPath
    objective: PlannerMissionPoint
    route_out: GeoPath
    home: GlobalPosition
    land_pos: GlobalPosition
    ip_wait_delay: float = 0.0
    wp: GeoPath
