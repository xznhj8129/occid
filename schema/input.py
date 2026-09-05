"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Input(OCCIDModel):
    'Current operator or receiver input state and control mapping.'
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ControlAxisSet', 'ControlChannelValue', 'ControlOverride', 'ControlAttitudeSetpoint')

class ControlAxisSet(OCCIDModel):
    'Normalized control-axis values in the signed range -1.0 to +1.0, independent of the native receiver or flight-controller representation'
    __occid_model_id__: ClassVar[int] = 45
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Input'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[builtins.float]

class ControlChannelValue(OCCIDModel):
    'One normalized auxiliary/control channel value in the signed range -1.0 to +1.0 when present'
    __occid_model_id__: ClassVar[int] = 46
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Input'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    channel_index: builtins.int
    value: builtins.float | None = None

class ControlOverride(OCCIDModel):
    'Normalized direct control override in the signed range -1.0 to +1.0; endpoint adapters define the exact native mapping and reject unsupported axes'
    __occid_model_id__: ClassVar[int] = 48
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Input'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    roll: builtins.float | None = None
    pitch: builtins.float | None = None
    yaw: builtins.float | None = None
    throttle: builtins.float | None = None
    aux: list[Semantic[ControlChannelValue]]

class ControlAttitudeSetpoint(OCCIDModel):
    'Attitude and normalized thrust setpoint using radians; frame metadata is optional in the record but control code that depends on frame semantics must require it explicitly'
    __occid_model_id__: ClassVar[int] = 44
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Input'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    roll_rad: builtins.float
    pitch_rad: builtins.float
    yaw_rad: builtins.float
    thrust_normalized: builtins.float
    body_frame: BodyReferenceFrame | None = None
    reference_frame: InertialReferenceFrame | None = None
