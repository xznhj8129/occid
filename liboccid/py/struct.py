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
    __occid_model_id__: ClassVar[int] = 346
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightLevelBand', 'SuccessCriterion', 'PlanContingency', 'IsrParameters', 'ColorComponent', 'ColorRGBA', 'StrokeStyle', 'FillStyle', 'TextStyle', 'GraphicStyle', 'AnnotationAnchor', 'RepresentationSource', 'LayerView', 'MapGrid', 'UTMZone', 'ResourceRequirement', 'OrgComposition', 'MilitaryStrength', 'PayloadAllocation', 'PayloadPlan', 'PayloadMount', 'Record', 'SpatialStruct', 'ID', 'Text', 'Vector', 'Measurement', 'Bearing', 'GeoPos', 'LocalPos', 'Line', 'StructPath', 'Shape', 'Bounding', 'Uncertainty', 'Pose', 'Range', 'Transform', 'Orbital', 'ItemCount', 'Effects', 'TargetPriority', 'TargetKinematics', 'TargetSet', 'Fires', 'SplashCorrection', 'TargetHandover', 'BattleDamageAssessment', 'EsadState', 'EsadArming', 'RwsPose', 'RwsState', 'MunitionAllocation', 'CombatTaskProfile')

class ID(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 161
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IntID', 'UID')

class IntID(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 169
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UID(OCCIDValue[Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]]):
    __occid_model_id__: ClassVar[int] = 388
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ID'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Text(OCCIDModel):
    'Human-authored textual content whose encoding is not itself domain meaning'
    __occid_model_id__: ClassVar[int] = 374
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('PlainText', 'MarkdownText')

class PlainText(OCCIDValue[builtins.str]):
    __occid_model_id__: ClassVar[int] = 273
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Text'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class MarkdownText(OCCIDValue[builtins.str]):
    __occid_model_id__: ClassVar[int] = 206
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Text'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Vector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 396
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalVector', 'VelocityVector', 'AngularVelocityVector')

class Measurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 207
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SignalQuality', 'DeliveryQuality', 'LinkCounters', 'GraphicLength', 'Airspeed', 'AltitudeState', 'Quantity', 'Distance', 'AreaMeasure', 'Angle', 'Ratio', 'Frequency', 'ElectricPotential', 'ElectricCurrent', 'ElectricPower', 'ElectricCharge', 'Energy', 'Temperature', 'Time', 'Duration', 'Timestamp')

class Quantity(OCCIDModel):
    'Amount of something, either discrete or expressed in a declared unit'
    __occid_model_id__: ClassVar[int] = 291
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Count', 'ByteCount', 'UnitQuantity')

class Count(OCCIDValue[builtins.int]):
    'Discrete non-negative quantity; validity constraints are imposed by the consuming semantic model'
    __occid_model_id__: ClassVar[int] = 71
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ByteCount(OCCIDValue[builtins.int]):
    'Quantity of octets'
    __occid_model_id__: ClassVar[int] = 39
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UnitQuantity(OCCIDModel):
    'Scalar quantity with an explicit unit vocabulary'
    __occid_model_id__: ClassVar[int] = 394
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Quantity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    value: builtins.float
    unit: QuantityUnit

class Distance(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DistanceMeters',)

class DistanceMeters(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 89
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Distance'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class AreaMeasure(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AreaSquareMeters',)

class AreaSquareMeters(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 22
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
    __occid_model_id__: ClassVar[int] = 297
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Opacity', 'NormalizedRatio')

class NormalizedRatio(OCCIDValue[builtins.float]):
    'Dimensionless ratio conventionally interpreted on the closed interval zero through one'
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Ratio'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Frequency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 128
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Hertz',)

class Hertz(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 159
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Frequency'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricPotential(OCCIDModel):
    'Electric potential difference'
    __occid_model_id__: ClassVar[int] = 98
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Volts',)

class Volts(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 406
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricPotential'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricCurrent(OCCIDModel):
    'Electric current'
    __occid_model_id__: ClassVar[int] = 97
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
    __occid_model_id__: ClassVar[int] = 99
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Watts',)

class Watts(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 408
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ElectricPower'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ElectricCharge(OCCIDModel):
    'Electric charge expressed as a storage or consumption quantity'
    __occid_model_id__: ClassVar[int] = 96
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
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('WattHours',)

class WattHours(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 407
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Energy'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Temperature(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 373
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DegreesCelsius',)

class DegreesCelsius(OCCIDValue[builtins.float]):
    __occid_model_id__: ClassVar[int] = 80
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Temperature'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Bearing(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 33
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocalDirection',)

class GeoPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 140
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GlobalPosition',)

class LocalPos(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 194
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Line(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 185
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class StructPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 347
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoPath', 'GeoMultiPath')

class Shape(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 330
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeoArea', 'GeoCircle', 'GeoMultiPoint', 'GeoMultiArea', 'GeoGeometryCollection')

class Bounding(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('BoundingBox',)

class Uncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 391
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LocationUncertainty',)

class Pose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 280
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EulerAngles',)

class Range(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 296
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TimeRange', 'NumericRange')

class Transform(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 384
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Orbital(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 257
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Time(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 377
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.int

class Duration(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 92
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
    __occid_model_id__: ClassVar[int] = 380
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    utime: builtins.float
    tz: builtins.int

class TimeRange(OCCIDModel):
    'Closed or open temporal extent expressed by semantic timestamps'
    __occid_model_id__: ClassVar[int] = 378
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    start_ts: Semantic[Timestamp] | None = None
    end_ts: Semantic[Timestamp] | None = None

class ItemCount(OCCIDModel):
    'Quantity of an identified item or resource definition; the item is referenced semantically rather than named ad hoc'
    __occid_model_id__: ClassVar[int] = 177
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    item_uid: Semantic[UID]
    qty: Semantic[Count]

class NumericRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 247
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Range'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    min_value: builtins.float | None = None
    max_value: builtins.float | None = None
