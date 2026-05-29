"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class CommandMessage(Message):
    'Message whose payload directs action'
    __occid_model_id__: ClassVar[int] = 133
    command: SerializeAsAny[Command | FlightCommand | ArmCommand | DisarmCommand | TakeoffCommand | LandCommand | ReturnToLaunchCommand | SetModeCommand | GoToCommand | SetTakeoffAltitudeCommand | SelectMissionCommand | StartOffboardCommand | StopOffboardCommand | TaskCommand | TrackerCommand]

class HumanTextMessage(Message):
    __occid_model_id__: ClassVar[int] = 134
    sender_id: StringID | None = None
    sender_name: builtins.str | None = None
    destination_id: StringID | None = None
    destination_group: builtins.str | None = None
    kind: builtins.str | None = None
    message: builtins.str
    position: GlobalPosition | None = None
    targets: list[MessageTarget]
