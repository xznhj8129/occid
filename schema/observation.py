"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class Observation_type(IntEnum):
    DETECTION = 0
    CLASSIFICATION = auto()
    TRACK = auto()
    ASSESSMENT = auto()

### Models

class Observation(Data):
    'External detection, classification, track, signal, spot report, threat, or assessment data'

class Classification(Observation):
    pass

class Track(Observation):
    pass

class Assessment(Observation):
    pass

class Detection(Observation):
    'Assessment that something exists or occurred'

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
