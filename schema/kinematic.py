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
    __occid_model_id__: ClassVar[int] = 126
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ImuSample',)

class ImuSample(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Kinematic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    acceleration: Semantic[LocalVector] | None = None
    angular_velocity: Semantic[AngularVelocityVector] | None = None
    magnetic_field: Semantic[LocalVector] | None = None
    temperature_deg_c: builtins.float | None = None
    timestamp_us: builtins.int | None = None
    frame: BodyReferenceFrame | None = None

class Airspeed(OCCIDModel):
    'Air-relative vehicle speed with explicit interpretation when known'
    __occid_model_id__: ClassVar[int] = 8
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    speed_ms: builtins.float
    reference: AirspeedReference = AirspeedReference.UNSPECIFIED
