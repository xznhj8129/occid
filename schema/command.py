"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Command_type(IntEnum):
    VEHICLE = 0
    TASK = auto()
    TRACKER = auto()

### Models

class Command(Control):
    'An immediate imperative requiring execution without interpretation'
    command_id: str
    target_ref: str

class VehicleCommand(Command):
    command_type: FlightCommandType

class TaskCommand(Command):
    task: SerializeAsAny[Task | Mission | Plan | AutopilotFlightPlan | GroupFlightPlan | UnitFlightPlan | IsrTask]

class TrackerCommand(Command):
    lock: bool | None = None
    reset: bool | None = None
    slew: LocalDirection | None = None
    search_box_size: int | None = None
    shutdown: bool | None = None
