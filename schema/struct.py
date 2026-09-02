"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'type'

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'type'

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 259
    __occid_semantic_role__: ClassVar[str] = 'type'

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 249
    __occid_semantic_role__: ClassVar[str] = 'type'
    utime: builtins.int

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 108
    __occid_semantic_role__: ClassVar[str] = 'representation'

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 258
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'representation'

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'representation'

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 126
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 119
    __occid_semantic_role__: ClassVar[str] = 'representation'

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 229
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 220
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 23
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 188
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 200
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 254
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 171
    __occid_semantic_role__: ClassVar[str] = 'representation'

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 56
    __occid_semantic_role__: ClassVar[str] = 'representation'
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 250
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
    __occid_model_id__: ClassVar[int] = 166
    __occid_semantic_role__: ClassVar[str] = 'representation'
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
