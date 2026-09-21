"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class QuantityUnit(IntEnum):
    GRAM = 0
    KILOGRAM = auto()
    MILLILITER = auto()
    LITER = auto()
    METER = auto()
    KILOMETER = auto()
    SQUARE_METER = auto()
    CUBIC_METER = auto()
    SECOND = auto()
    MINUTE = auto()
    HOUR = auto()
    WATT_HOUR = auto()
    AMPERE_HOUR = auto()

### Models

class Struct(OCCIDModel):
    'Primitive reusable low-level struct families.'
    __occid_model_id__: ClassVar[int] = 314
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightLevelBand', 'SuccessCriterion', 'PlanContingency', 'IsrParameters', 'ResourceRequirement', 'OrgComposition', 'MilitaryStrength', 'PayloadAllocation', 'PayloadPlan', 'PayloadMount', 'Record', 'SpatialStruct', 'ID', 'Text', 'Vector', 'Measurement', 'Bearing', 'GeoPos', 'LocalPos', 'Line', 'StructPath', 'Shape', 'Bounding', 'Uncertainty', 'Pose', 'Range', 'Transform', 'Orbital', 'ItemCount', 'Effects', 'TargetPriority', 'TargetKinematics', 'TargetSet', 'Fires', 'SplashCorrection', 'TargetHandover', 'BattleDamageAssessment', 'EsadState', 'EsadArming', 'RwsPose', 'RwsState', 'MunitionAllocation', 'CombatTaskProfile')

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IntID', 'UID')

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 155
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 351
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Text(OCCIDModel):
    'Human-authored textual content whose encoding is not itself domain meaning'
    __occid_model_id__: ClassVar[int] = 339
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('PlainText', 'MarkdownText')

class PlainText(OCCIDValue[builtins.str]):
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Text'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class MarkdownText(OCCIDValue[builtins.str]):
    __occid_model_id__: ClassVar[int] = 185
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Text'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 357
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalVector', 'VelocityVector', 'AngularVelocityVector')

class Measurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 186
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SignalQuality', 'DeliveryQuality', 'LinkCounters', 'Airspeed', 'AltitudeState', 'Quantity', 'Distance', 'AreaMeasure', 'Angle', 'Ratio', 'Frequency', 'ElectricPotential', 'ElectricCurrent', 'ElectricPower', 'ElectricCharge', 'Energy', 'Temperature', 'Time', 'Duration', 'Timestamp')

class Quantity(OCCIDModel):
    'Amount of something, either discrete or expressed in a declared unit'
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Count', 'ByteCount', 'UnitQuantity')

class Count(OCCIDValue[builtins.int]):
    'Discrete non-negative quantity; validity constraints are imposed by the consuming semantic model'
    __occid_model_id__: ClassVar[int] = 66
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ByteCount(OCCIDValue[builtins.int]):
    'Quantity of octets'
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UnitQuantity(OCCIDModel):
    'Scalar quantity with an explicit unit vocabulary'
    __occid_model_id__: ClassVar[int] = 355
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    value: builtins.float
    unit: QuantityUnit

class Distance(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 81
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DistanceMeters',)

class DistanceMeters(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 83
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Distance'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class AreaMeasure(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AreaSquareMeters',)

class AreaSquareMeters(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AreaMeasure'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Angle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 13
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AngleDegrees', 'AngleRadians')

class AngleDegrees(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 14
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Angle'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class AngleRadians(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 15
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Angle'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Ratio(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('NormalizedRatio',)

class NormalizedRatio(OCCIDValue[builtins.float]):
    'Dimensionless ratio conventionally interpreted on the closed interval zero through one'
    __occid_model_id__: ClassVar[int] = 222
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Ratio'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Frequency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 120
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Hertz',)

class Hertz(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 146
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Frequency'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricPotential(OCCIDModel):
    'Electric potential difference'
    __occid_model_id__: ClassVar[int] = 92
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Volts',)

class Volts(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 367
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricPotential'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricCurrent(OCCIDModel):
    'Electric current'
    __occid_model_id__: ClassVar[int] = 91
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Amperes',)

class Amperes(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 12
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricCurrent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricPower(OCCIDModel):
    'Electrical power'
    __occid_model_id__: ClassVar[int] = 93
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Watts',)

class Watts(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 369
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricPower'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricCharge(OCCIDModel):
    'Electric charge expressed as a storage or consumption quantity'
    __occid_model_id__: ClassVar[int] = 90
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AmpereHours',)

class AmpereHours(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 11
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricCharge'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Energy(OCCIDModel):
    'Energy quantity'
    __occid_model_id__: ClassVar[int] = 96
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('WattHours',)

class WattHours(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 368
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Energy'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Temperature(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 338
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DegreesCelsius',)

class DegreesCelsius(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 74
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Temperature'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 31
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalDirection',)

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 132
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GlobalPosition',)

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 176
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 168
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 315
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoPath', 'GeoMultiPath')

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 299
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoArea', 'GeoCircle', 'GeoMultiPoint', 'GeoMultiArea', 'GeoGeometryCollection')

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 35
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('BoundingBox',)

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 352
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocationUncertainty',)

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 253
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EulerAngles',)

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 268
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TimeRange', 'NumericRange')

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 347
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 232
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 340
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.int

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 86
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
    __occid_model_id__: ClassVar[int] = 343
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.float
    tz: builtins.int

class TimeRange(OCCIDModel):
    'Closed or open temporal extent expressed by semantic timestamps'
    __occid_model_id__: ClassVar[int] = 341
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    start_ts: Semantic[Timestamp] | None = None
    end_ts: Semantic[Timestamp] | None = None

class ItemCount(OCCIDModel):
    'Quantity of an identified item or resource definition; the item is referenced semantically rather than named ad hoc'
    __occid_model_id__: ClassVar[int] = 163
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    item_uid: Semantic[UID]
    qty: Semantic[Count]

class NumericRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 223
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
