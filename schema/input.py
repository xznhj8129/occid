"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Input(State):
    'Current operator or receiver input state and control mapping.'

class ControlAxisSet(Input):
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[builtins.float]

class ControlChannelValue(Input):
    channel_index: builtins.int
    value: builtins.float | None = None

class ControlOverride(Input):
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[ControlChannelValue]

class ControlAttitudeSetpoint(Input):
    roll_deg: builtins.float
    pitch_deg: builtins.float
    yaw_deg: builtins.float
    thrust_value: builtins.float
