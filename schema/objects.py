"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class ObjectType(IntEnum):
    ENTITY = 0
    ORGANIZATION = auto()

class Object_type(IntEnum):
    ENTITY = 0
    SET = auto()
    ITEM = auto()
    WORLD = auto()

class Set_type(IntEnum):
    ORGANIZATION = 0
    COLLECTION = auto()
    CLUSTER = auto()
    SYSTEM = auto()

class Item_type(IntEnum):
    RECORD = 0
    EQUIPMENT = auto()
    COMPONENT = auto()
    PAYLOAD = auto()

class World_type(IntEnum):
    FEATURE = 0
    LOCATION = auto()
    SITE = auto()

### Models

class Object(Root):
    'Atoms'
    object_type: ObjectType

class Set(Object):
    pass

class Collection(Set):
    pass

class Cluster(Set):
    pass

class System(Set):
    pass

class Item(Object):
    'A discrete bounded non-agent object'

class Record(Item):
    pass

class Equipment(Item):
    pass

class Component(Item):
    pass

class Payload(Item):
    pass

class SensorSchema(Payload):
    name: str
    model: str
    type: SensorType
    serial_uid: str = ''
    effect_domain: EffectDomain
    max_range: float
    ptz: bool
    spectrum: SensorSpectrum
    night_vision: bool
    all_weather: bool
    weather_limits: WeatherLimits
    error_margin: float
    error_type: SensorErrorType
    data_formats: list[SensorDataFormat]
    ai: list[SensorAICapability]
    datalink: str
    field_of_view: SensorFieldOfView | None = None
    zoom_range: NumericRange | None = None
    run_state: SensorRunState | None = None
    mode: SensorMode | None = None
    sensor_family: str | None = None
    frustum_shape: SensorFrustumShape | None = None
    field_of_regard: SensorFieldOfView | None = None
    gimbal_state: GimbalState | None = None
    freq_span: NumericRange | None = None
    chan_bw: float | None = None
    emit_profile: str | None = None
    quality_hint: MeasurementQuality | None = None

class World(Object):
    pass

class Feature(World):
    pass

class Location(World):
    pass

class Site(World):
    pass

class GeoJsonFeature(Feature):
    type: Literal['Feature'] = Field(default='Feature', frozen=True)
    geometry: GeoJsonGeometry
    properties: list[FeatureProperty]
    id: (str | int) | None = None
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(Collection):
    type: Literal['FeatureCollection'] = Field(default='FeatureCollection', frozen=True)
    features: list[GeoJsonFeature]
    bbox: BoundingBox | None = None
