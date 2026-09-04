"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 103
    __occid_semantic_role__: ClassVar[str] = 'type'

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'type'

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 265
    __occid_semantic_role__: ClassVar[str] = 'type'

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 255
    __occid_semantic_role__: ClassVar[str] = 'type'
    utime: builtins.int

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'representation'

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 264
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'representation'

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 88
    __occid_semantic_role__: ClassVar[str] = 'representation'

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 127
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'representation'

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 234
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 225
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 23
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 191
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 203
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 260
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 173
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 57
    __occid_semantic_role__: ClassVar[str] = 'representation'
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 256
    __occid_semantic_role__: ClassVar[str] = 'representation'
    seconds: builtins.float
    minutes: builtins.int
    hours: builtins.int
    day: builtins.int
    month: builtins.int
    year: builtins.int
    tz: builtins.int

class ItemCount(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 115
    __occid_semantic_role__: ClassVar[str] = 'representation'
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 168
    __occid_semantic_role__: ClassVar[str] = 'representation'
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
