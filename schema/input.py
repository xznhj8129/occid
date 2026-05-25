"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

### Models

class Input(State):
    pass

class ControlAxisSet(Input):
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None
    throttle: float | None = None
    aux: list[float]

class ControlChannelValue(Input):
    channel_index: int
    value: float | None = None

class ControlOverride(Input):
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None
    throttle: float | None = None
    aux: list[ControlChannelValue]

class ControlAttitudeSetpoint(Input):
    roll_deg: float
    pitch_deg: float
    yaw_deg: float
    thrust_value: float
