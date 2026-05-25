"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .intel import Intel

### Enums

class DetectionBoxSpace(IntEnum):
    IMAGE_PIXEL = 0
    IMAGE_NORMALIZED = auto()
    BODY_ANGULAR = auto()
    WORLD = auto()

### Models

class Detection(Intel):
    pass

class VisionBox(Detection):
    space: DetectionBoxSpace
    bounds: BoundingBox

class VisionDetection(Detection):
    detection_id: str | None = None
    label: str | None = None
    class_id: int | None = None
    confidence: float | None = None
    box: VisionBox | None = None
    bearing: LocalDirection | None = None
    position: GlobalPosition | None = None
    source_frame_id: str | None = None
    attributes: list[MetadataEntry]

class VisionDetectionFrame(Detection):
    frame_id: str | None = None
    sensor_id: str | None = None
    timestamp_us: int | None = None
    detections: list[VisionDetection]

class EmitterNotationSchema(Detection):
    emitter_name: str | None = None
    emitter_class: str | None = None
    platform_class: str | None = None

class SignalMeasurement(Detection):
    value: float | None = None
    unit: str | None = None
    confidence: ConfidenceLevel | None = None

class LineOfBearingSchema(Detection):
    bearing_deg: float | None = None
    bearing_error_deg: float | None = None

class AngleOfArrivalSchema(Detection):
    azimuth_deg: float | None = None
    elevation_deg: float | None = None
    azimuth_error_deg: float | None = None
    elevation_error_deg: float | None = None

class PulseRepetitionIntervalSchema(Detection):
    pri_us: float | None = None
    jitter_us: float | None = None

class ScanCharacteristicsSchema(Detection):
    period_s: float | None = None
    frame_time_s: float | None = None

class SignalSchema(Detection):
    signal_id: str
    source_id: str | None = None
    emitter: EmitterNotationSchema | None = None
    frequency: FrequencyRange | None = None
    strength: SignalMeasurement | None = None
    line_of_bearing: LineOfBearingSchema | None = None
    angle_of_arrival: AngleOfArrivalSchema | None = None
    pulse_interval: PulseRepetitionIntervalSchema | None = None
    scan: ScanCharacteristicsSchema | None = None
    fixed_position_id: str | None = None
