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
    'Immediate flight-domain command; distinct from Task and Plan lifecycle semantics'
    __occid_model_id__: ClassVar[int] = 46

class LowLevelFlightCommand(FlightCommand):
    'Direct flight-control imperative mapped by an endpoint adapter to MAVLink, MSP, or another native flight-controller protocol'
    __occid_model_id__: ClassVar[int] = 287

class ArmCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 47

class DisarmCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 48

class TakeoffCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 49

class LandCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 50

class ReturnToLaunchCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 51

class SetModeCommand(LowLevelFlightCommand):
    'Select a portable standard mode or an endpoint-native mode; at least one selector must be provided and adapters must reject unsupported or ambiguous selections'
    __occid_model_id__: ClassVar[int] = 52
    standard_mode: StandardFlightMode | None = None
    native_mode_name: builtins.str | None = None
    native_mode_code: builtins.int | None = None

class GoToCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 53
    position: GlobalPosition
    yaw_rad: builtins.float | None = None

class SetTakeoffAltitudeCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 54
    relative_altitude_m: builtins.float

class SelectMissionCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 55
    sequence: builtins.int

class StartOffboardCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 56

class StopOffboardCommand(LowLevelFlightCommand):
    __occid_model_id__: ClassVar[int] = 57

class SetControlAttitudeCommand(LowLevelFlightCommand):
    'Apply an attitude and thrust setpoint; endpoint adapters map the semantic setpoint to the native flight-controller mechanism'
    __occid_model_id__: ClassVar[int] = 288
    setpoint: ControlAttitudeSetpoint

class SetControlOverrideCommand(LowLevelFlightCommand):
    'Apply normalized direct control-axis overrides through the endpoint adapter'
    __occid_model_id__: ClassVar[int] = 289
    override: ControlOverride

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
