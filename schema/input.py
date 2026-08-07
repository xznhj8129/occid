"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Input(State):
    'Current operator or receiver input state and control mapping.'
    __occid_model_id__: ClassVar[int] = 152

class ControlAxisSet(Input):
    'Normalized control-axis values independent of the native receiver or flight-controller representation'
    __occid_model_id__: ClassVar[int] = 153
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[builtins.float]

class ControlChannelValue(Input):
    __occid_model_id__: ClassVar[int] = 154
    channel_index: builtins.int
    value: builtins.float | None = None

class ControlOverride(Input):
    'Normalized direct control override; endpoint adapters define the exact native mapping and reject unsupported axes'
    __occid_model_id__: ClassVar[int] = 155
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[ControlChannelValue]

class ControlAttitudeSetpoint(Input):
    'Attitude and normalized thrust setpoint using radians; frame metadata is optional in the record but control code that depends on frame semantics must require it explicitly'
    __occid_model_id__: ClassVar[int] = 156
    roll_rad: builtins.float
    pitch_rad: builtins.float
    yaw_rad: builtins.float
    thrust_normalized: builtins.float
    body_frame: BodyReferenceFrame | None = None
    reference_frame: InertialReferenceFrame | None = None
