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

### Models

class Command(Control):
    'An immediate imperative requiring execution without interpretation'
    __occid_model_id__: ClassVar[int] = 45

class FlightCommand(Command):
    __occid_model_id__: ClassVar[int] = 46

class ArmCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 47

class DisarmCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 48

class TakeoffCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 49

class LandCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 50

class ReturnToLaunchCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 51

class SetModeCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 52
    mode: FlightMode

class GoToCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 53
    position: GlobalPosition
    yaw_deg: builtins.float

class SetTakeoffAltitudeCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 54
    altitude_m: builtins.float

class SelectMissionCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 55
    sequence: builtins.int

class StartOffboardCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 56

class StopOffboardCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 57

class TaskCommand(Command):
    __occid_model_id__: ClassVar[int] = 58
    task: SerializeAsAny[Task | Mission | IsrTask | MoveTask | HoldTask | ResupplyTask]

class ApplyPlanCommand(Command):
    'Direct an executor to apply an approved plan'
    __occid_model_id__: ClassVar[int] = 286
    plan: SerializeAsAny[Plan | AutopilotFlightPlan | GroupFlightPlan | UnitFlightPlan | MissionPlan]

class TrackerCommand(Command):
    __occid_model_id__: ClassVar[int] = 59
    lock: builtins.bool | None = None
    reset: builtins.bool | None = None
    slew: LocalDirection | None = None
    search_box_size: builtins.int | None = None
    shutdown: builtins.bool | None = None
