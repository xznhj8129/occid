"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Input(OCCIDModel):
    'Current operator or receiver input state and control mapping.'
    __occid_model_id__: ClassVar[int] = 108
    __occid_semantic_role__: ClassVar[str] = 'type'

class ControlAxisSet(OCCIDModel):
    'Normalized control-axis values in the signed range -1.0 to +1.0, independent of the native receiver or flight-controller representation'
    __occid_model_id__: ClassVar[int] = 40
    __occid_semantic_role__: ClassVar[str] = 'representation'
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[builtins.float]

class ControlChannelValue(OCCIDModel):
    'One normalized auxiliary/control channel value in the signed range -1.0 to +1.0 when present'
    __occid_model_id__: ClassVar[int] = 41
    __occid_semantic_role__: ClassVar[str] = 'representation'
    channel_index: builtins.int
    value: builtins.float | None = None

class ControlOverride(OCCIDModel):
    'Normalized direct control override in the signed range -1.0 to +1.0; endpoint adapters define the exact native mapping and reject unsupported axes'
    __occid_model_id__: ClassVar[int] = 43
    __occid_semantic_role__: ClassVar[str] = 'representation'
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[ControlChannelValue]

class ControlAttitudeSetpoint(OCCIDModel):
    'Attitude and normalized thrust setpoint using radians; frame metadata is optional in the record but control code that depends on frame semantics must require it explicitly'
    __occid_model_id__: ClassVar[int] = 39
    __occid_semantic_role__: ClassVar[str] = 'representation'
    roll_rad: builtins.float
    pitch_rad: builtins.float
    yaw_rad: builtins.float
    thrust_normalized: builtins.float
    body_frame: BodyReferenceFrame | None = None
    reference_frame: InertialReferenceFrame | None = None
