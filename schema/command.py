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

class DirectControlMode(IntEnum):
    MANUAL_AXIS = 0
    ATTITUDE_THRUST = auto()

### Models

class Command(Control):
    'An immediate imperative requiring execution without interpretation'
    __occid_model_id__: ClassVar[int] = 45

class FlightCommand(Command):
    'Immediate aircraft operation such as arming, takeoff, landing, or recovery; distinct from navigation, mode selection, direct control, and Task/Plan lifecycle semantics'
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

class SetTakeoffAltitudeCommand(FlightCommand):
    __occid_model_id__: ClassVar[int] = 54
    relative_altitude_m: builtins.float

class NavigationCommand(Command):
    'Immediate navigation operation that changes a destination, waypoint, or selected onboard mission without implying a higher-level Task or Plan lifecycle'
    __occid_model_id__: ClassVar[int] = 290

class GoToCommand(NavigationCommand):
    __occid_model_id__: ClassVar[int] = 53
    position: GlobalPosition
    yaw_rad: builtins.float | None = None

class SetWaypointCommand(NavigationCommand):
    'Write one endpoint mission waypoint while preserving its explicit OCCID waypoint representation'
    __occid_model_id__: ClassVar[int] = 291
    waypoint: AutopilotMissionWaypoint

class SelectMissionCommand(NavigationCommand):
    'Select an already-present onboard mission sequence; mission upload/generation remains runtime policy outside the OCCID SDK'
    __occid_model_id__: ClassVar[int] = 55
    sequence: builtins.int

class ModeCommand(Command):
    'Immediate activation or deactivation of a flight-controller mode; imperative actions such as takeoff, land, and return use their own command families'
    __occid_model_id__: ClassVar[int] = 292

class SetModeCommand(ModeCommand):
    'Select a portable standard mode or an endpoint-native mode; exactly one semantic/native selector must be usable by the endpoint and enabled controls activation versus deactivation'
    __occid_model_id__: ClassVar[int] = 52
    standard_mode: StandardFlightMode | None = None
    native_mode_name: builtins.str | None = None
    native_mode_code: builtins.int | None = None
    enabled: builtins.bool = True

class DirectControlCommand(Command):
    'Lifecycle command for a direct-control session; high-rate control samples themselves are Input models and are not Commands'
    __occid_model_id__: ClassVar[int] = 293

class BeginDirectControlCommand(DirectControlCommand):
    'Begin delivery of a declared direct-control input form; endpoint runtimes own native offboard/manual-control/override lifecycle'
    __occid_model_id__: ClassVar[int] = 294
    mode: DirectControlMode

class EndDirectControlCommand(DirectControlCommand):
    'End the active direct-control session and relinquish its endpoint-specific control mechanism'
    __occid_model_id__: ClassVar[int] = 295

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
