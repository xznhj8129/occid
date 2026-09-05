"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Struct(OCCIDModel):
    'Primitive reusable low-level struct families.'
    __occid_model_id__: ClassVar[int] = 249
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SuccessCriterion', 'PlanStep', 'PlanContingency', 'FlightLevelBand', 'AutopilotMissionWaypoint', 'PlannerMissionPoint', 'LoiterOrbit', 'MissionRouteGeometry', 'PlannedRoutePoints', 'IsrParameters', 'Record', 'SpatialStruct', 'ID', 'Vector', 'Measurement', 'Bearing', 'GeoPos', 'LocalPos', 'Line', 'StructPath', 'Shape', 'Bounding', 'Uncertainty', 'Pose', 'Range', 'Transform', 'Orbital', 'PayloadAllocation', 'PayloadPlan', 'PayloadMount', 'Effects', 'TargetPriority', 'TargetKinematics', 'TargetSet', 'Fires', 'SplashCorrection', 'TargetHandover', 'BattleDamageAssessment', 'EsadState', 'EsadArming', 'RwsPose', 'RwsState', 'OrgComposition', 'MunitionAllocation', 'CombatTaskProfile')

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 112
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IntID', 'UID')

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 118
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 279
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 284
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalVector', 'VelocityVector', 'AngularVelocityVector')

class Measurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 146
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SignalQuality', 'DeliveryQuality', 'LinkCounters', 'Airspeed', 'AltitudeState', 'Time', 'Duration', 'Timestamp', 'ItemCount')

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 21
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalDirection',)

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 97
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GlobalPosition',)

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 137
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 130
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 250
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoPath',)

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 240
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoArea',)

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 24
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('BoundingBox',)

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 280
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocationUncertainty',)

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 203
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EulerAngles',)

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 216
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('NumericRange',)

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 275
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 186
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 270
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.int

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 66
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
    __occid_model_id__: ClassVar[int] = 271
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.float
    tz: builtins.int

class ItemCount(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 125
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    item_type: builtins.str
    qty: builtins.int = 0

class NumericRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 179
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
