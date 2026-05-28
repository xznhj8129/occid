"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Enums

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

### Models

class Command(Control):
    'An immediate imperative requiring execution without interpretation'

class FlightCommand(Command):
    command_type: FlightCommandType

class TaskCommand(Command):
    task: SerializeAsAny[Task | Mission | Plan | AutopilotFlightPlan | GroupFlightPlan | UnitFlightPlan | IsrTask]

class TrackerCommand(Command):
    lock: builtins.bool | None = None
    reset: builtins.bool | None = None
    slew: LocalDirection | None = None
    search_box_size: builtins.int | None = None
    shutdown: builtins.bool | None = None
