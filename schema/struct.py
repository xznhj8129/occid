"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Struct(OCCIDModel):
    'Primitive reusable low-level struct families.'
    __occid_model_id__: ClassVar[int] = 251
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightLevelBand', 'SuccessCriterion', 'PlanContingency', 'IsrParameters', 'Record', 'SpatialStruct', 'ID', 'Vector', 'Measurement', 'Bearing', 'GeoPos', 'LocalPos', 'Line', 'StructPath', 'Shape', 'Bounding', 'Uncertainty', 'Pose', 'Range', 'Transform', 'Orbital', 'PayloadAllocation', 'PayloadPlan', 'PayloadMount', 'Effects', 'TargetPriority', 'TargetKinematics', 'TargetSet', 'Fires', 'SplashCorrection', 'TargetHandover', 'BattleDamageAssessment', 'EsadState', 'EsadArming', 'RwsPose', 'RwsState', 'OrgComposition', 'MunitionAllocation', 'CombatTaskProfile')

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 114
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IntID', 'UID')

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 281
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 286
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalVector', 'VelocityVector', 'AngularVelocityVector')

class Measurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SignalQuality', 'DeliveryQuality', 'LinkCounters', 'Airspeed', 'AltitudeState', 'Time', 'Duration', 'Timestamp', 'ItemCount')

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 22
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalDirection',)

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 99
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GlobalPosition',)

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 139
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 132
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 252
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoPath',)

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 242
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoArea',)

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 25
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('BoundingBox',)

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 282
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocationUncertainty',)

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 204
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EulerAngles',)

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 217
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('NumericRange',)

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 277
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 188
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 272
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.int

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 67
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    seconds: builtins.float | None = None
    minutes: builtins.int | None = None
    hours: builtins.int | None = None
    days: builtins.int | None = None
    weeks: builtins.int | None = None
    months: builtins.int | None = None
    years: builtins.int | None = None

class Timestamp(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 273
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.float
    tz: builtins.int

class ItemCount(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 127
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 180
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
