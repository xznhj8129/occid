"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class IntelCategory(IntEnum):
    IMINT = 0
    ELINT = auto()
    SIGINT = auto()
    MASINT = auto()

class ObservationKind(IntEnum):
    DETECTION = 0
    TRACK = auto()
    IDENTIFICATION = auto()
    CLASSIFICATION = auto()

class ObservedObjectType(IntEnum):
    PERSONNEL = 0
    VEHICLES = auto()
    AIRCRAFT = auto()
    INSTALLATION = auto()
    WATERCRAFT = auto()
    ROUTE = auto()
    TRACE_SIGNATURE = auto()

class IsrFocusType(IntEnum):
    POINT = 0
    AREA = auto()
    TRACK = auto()
    ROUTE = auto()
    TARGET = auto()

class EvidenceLevel(IntEnum):
    SUSPECTED = 0
    DETECTED = auto()
    OBSERVED = auto()
    CONFIRMED = auto()
    POSITIVE_ID = auto()

class TrackState(IntEnum):
    NEW = 0
    ACTIVE = auto()
    STALE = auto()
    LOST = auto()

class DetectionBoxSpace(IntEnum):
    IMAGE_PIXEL = 0
    IMAGE_NORMALIZED = auto()
    BODY_ANGULAR = auto()
    WORLD = auto()

class Observation_type(IntEnum):
    DETECTION = 0
    CLASSIFICATION = auto()
    TRACK = auto()
    ASSESSMENT = auto()
    ISR = auto()

class Track_type(IntEnum):
    UPDATE = 0
    INTEL_TRACK_SCHEMA = auto()

class Assessment_type(IntEnum):
    ISR_RESULT = 0

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

class IsrObservation(Observation):
    obs_id: str
    track_id: str | None = None
    sensor_id: str | None = None
    obs_ts: float
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    focus_type: IsrFocusType | None = None
    focus_point: GlobalPosition | None = None
    dwell_s: float | None = None
    revisit_s: float | None = None
    sensor_types: list[SensorType]
    sensor_modes: list[SensorMode]
    effect_domains: list[EffectDomain]
    evidence_level: EvidenceLevel | None = None

class TrackUpdate(Track):
    track_id: str
    track_state: TrackState | None = None
    updated_ts: float
    confidence: ConfidenceLevel | None = None

class IsrResult(Assessment):
    detections: list[IsrObservation]
    track_updates: list[TrackUpdate]
    media: list[MediaItemSchema] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[IsrObservation]

class IntelTrackSchema(Track):
    schema_id: str
    schema_type: str = 'INTEL_TRACK'
    created_ts: float | None = None
    updated_ts: float | None = None
    origin_system: str | None = None
    trust_score: ConfidenceLevel | None = None
    alt_ids: list[Identifier]
    entity_flags: list[str]
    faction: str | None = None
    spotted_time: float
    updated_time: float
    stale_time: float
    track_state: TrackState = TrackState.NEW
    category: IntelCategory | None = None
    sensor_id: str | None = None
    spotter_last: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    error_m: float | None = None
    latest_observation: IsrObservation | None = None
    observations: list[IsrObservation]
