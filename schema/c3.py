"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class CommandMessage(Message):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 136
    command: SerializeAsAny[Command | FlightCommand | ArmCommand | DisarmCommand | TakeoffCommand | LandCommand | ReturnToLaunchCommand | SetTakeoffAltitudeCommand | NavigationCommand | GoToCommand | SetWaypointCommand | SelectMissionCommand | ModeCommand | SetModeCommand | DirectControlCommand | BeginDirectControlCommand | EndDirectControlCommand | TaskCommand | ApplyPlanCommand | TrackerCommand]

class HumanTextMessage(Message):
    __occid_model_id__: ClassVar[int] = 137
    sender_id: StringID | None = None
    sender_name: builtins.str | None = None
    destination_id: StringID | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
