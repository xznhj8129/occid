"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State
from .struct import Measurement

### Enums

class AirspeedReference(IntEnum):
    UNSPECIFIED = 0
    INDICATED = auto()
    CALIBRATED = auto()
    TRUE = auto()
    EQUIVALENT = auto()

### Models

class Kinematic(State):
    'Motion and derived movement state.'
    __occid_model_id__: ClassVar[int] = 162
    __occid_semantic_role__: ClassVar[str] = 'specialization'

class ImuSample(Kinematic):
    __occid_model_id__: ClassVar[int] = 163
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    acceleration: LocalVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    magnetic_field: LocalVector | None = None
    temperature_deg_c: builtins.float | None = None
    timestamp_us: builtins.int | None = None
    frame: BodyReferenceFrame | None = None

class Airspeed(Measurement):
    'Air-relative vehicle speed with explicit interpretation when known'
    __occid_model_id__: ClassVar[int] = 323
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    speed_ms: builtins.float
    reference: AirspeedReference = AirspeedReference.UNSPECIFIED
