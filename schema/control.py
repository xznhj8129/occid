"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .root import Root

### Enums

class Capability(IntEnum):
    NONE = 0
    LOGISTICS_SUPPLY = auto()
    COMMUNICATIONS = auto()
    FUEL = auto()
    RESCUE = auto()

class TaskType(IntEnum):
    POSITIONING = 0
    CARGO = auto()
    HOLD = auto()
    SUPPORT = auto()
    MOVE = auto()
    RESUPPLY = auto()

class TaskLevel(IntEnum):
    MISSION = 0
    PLAN = auto()

class TaskPhase(IntEnum):
    CREATED = 0
    DISPATCHED = auto()
    ASSIGNED = auto()
    RUNNING = auto()
    DONE_OK = auto()
    DONE_FAIL = auto()
    CANCELLED = auto()

class TaskPriority(IntEnum):
    ROUTINE = 0
    HIGH = auto()
    IMMEDIATE = auto()

class TaskStatus(IntEnum):
    NEW = 0
    ACCEPTED = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    FAILED = auto()
    CANCELLED = auto()

class TaskAssignFail(IntEnum):
    FAIL = 0
    FAIL_NO_ASSETS = auto()
    FAIL_BAD_REQUEST_CANTPRO = auto()
    FAIL_DENIED = auto()
    FAIL_INSUFFICIENT_INFO = auto()
    FAIL_REJECTED = auto()
    FAIL_C2_ELEMENT = auto()
    FAIL_PLATFORM_CANTCO = auto()
    FAIL_STALE = auto()
    FAIL_CANCELLED = auto()

class CommandResult(IntEnum):
    ACCEPTED = 0
    TEMPORARILY_REJECTED = auto()
    DENIED = auto()
    UNSUPPORTED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()
    CANCELLED = auto()

class FlightCommandType(IntEnum):
    ARM = 0
    DISARM = auto()
    TAKEOFF = auto()
    LAND = auto()
    RETURN_TO_LAUNCH = auto()
    SET_MODE = auto()
    GOTO = auto()
    SET_TAKEOFF_ALTITUDE = auto()
    SELECT_MISSION = auto()
    START_OFFBOARD = auto()
    STOP_OFFBOARD = auto()

class TaskAir(IntEnum):
    FLY = 0
    AIR_DROP = auto()
    RECOVERY = auto()

class AirMoveTask(IntEnum):
    FLY = 0
    RELOCATION = auto()

class PlannerPointType(IntEnum):
    HOME = 0
    TAKEOFF = auto()
    LANDING = auto()
    HOLD = auto()
    WAYPOINT = auto()
    ASSEMBLY = auto()
    POI = auto()
    ROI = auto()
    SURVEY = auto()

class PlannerPointCategory(IntEnum):
    ROUTE_IN = 0
    SURVEY = auto()
    SURVEY_AREA = auto()
    ROUTE_OUT = auto()

class AirGroupFormation3DType(IntEnum):
    NONE = 0
    BOX = auto()
    SEP_2D_PER_FL = auto()
    SEP_2D_SPACED = auto()

class AirGroupFormation2DType(IntEnum):
    NONE = 0
    LINE = auto()
    ECHELON = auto()
    TRAIL = auto()
    SQUARE = auto()
    DIAMOND = auto()
    VEE = auto()
    HEAVY_LEFT = auto()
    HEAVY_RIGHT = auto()
    ECHELON_LEFT = auto()
    ECHELON_RIGHT = auto()
    STAGG_TRAIL_LEFT = auto()
    STAGG_TRAIL_RIGHT = auto()

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GUIDE = auto()
    FULL = auto()

class Control_type(IntEnum):
    OBJECTIVE = 0
    TASK = auto()
    COMMAND = auto()
    REFERENCE = auto()
    CONSTRAINT = auto()
    INTERFACE = auto()

### Models

class Control(Root):
    'Desired outcomes and directed work'
