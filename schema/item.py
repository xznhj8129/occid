"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .object import Object

### Enums

class Item_type(IntEnum):
    RECORD = 0
    EQUIPMENT = auto()
    COMPONENT = auto()
    PAYLOAD = auto()

### Models

class Item(Object):
    pass

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
