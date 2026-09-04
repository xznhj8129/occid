"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class AirspeedReference(IntEnum):
    UNSPECIFIED = 0
    INDICATED = auto()
    CALIBRATED = auto()
    TAS = auto()
    EQUIVALENT = auto()

### Models

class Kinematic(OCCIDModel):
    'Motion and derived movement state.'
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'type'

class ImuSample(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 107
    __occid_semantic_role__: ClassVar[str] = 'representation'
    acceleration: LocalVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    magnetic_field: LocalVector | None = None
    temperature_deg_c: builtins.float | None = None
    timestamp_us: builtins.int | None = None
    frame: BodyReferenceFrame | None = None

class Airspeed(OCCIDModel):
    'Air-relative vehicle speed with explicit interpretation when known'
    __occid_model_id__: ClassVar[int] = 8
    __occid_semantic_role__: ClassVar[str] = 'representation'
    speed_ms: builtins.float
    reference: AirspeedReference = AirspeedReference.UNSPECIFIED
