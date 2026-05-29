"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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

### Models

class Observation(Data):
    'External detection, classification, track, signal, spot report, threat, or assessment data'
    __occid_model_id__: ClassVar[int] = 85

class Classification(Observation):
    __occid_model_id__: ClassVar[int] = 86

class Track(Observation):
    __occid_model_id__: ClassVar[int] = 87

class Assessment(Observation):
    __occid_model_id__: ClassVar[int] = 88

class Detection(Observation):
    'Assessment that something exists or occurred'
    __occid_model_id__: ClassVar[int] = 89

class VisionBox(Detection):
    __occid_model_id__: ClassVar[int] = 90
    space: DetectionBoxSpace
    bounds: BoundingBox

class VisionDetection(Detection):
    __occid_model_id__: ClassVar[int] = 91
    detection_id: StringID | None = None
    label: builtins.str | None = None
    class_id: builtins.int | None = None
    confidence: builtins.float | None = None
    box: VisionBox | None = None
    bearing: LocalDirection | None = None
    position: GlobalPosition | None = None
    source_frame_id: StringID | None = None
    attributes: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]

class VisionDetectionFrame(Detection):
    __occid_model_id__: ClassVar[int] = 92
    frame_id: StringID | None = None
    sensor_id: StringID | None = None
    timestamp_us: builtins.int | None = None
    detections: list[VisionDetection]

class IsrObservation(Observation):
    __occid_model_id__: ClassVar[int] = 93
    obs_id: StringID
    track_id: StringID | None = None
    sensor_id: StringID | None = None
    obs_ts: builtins.float
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 94
    focus_type: IsrFocusType | None = None
    focus_point: GlobalPosition | None = None
    dwell_s: builtins.float | None = None
    revisit_s: builtins.float | None = None
    sensor_types: list[SensorType]
    sensor_modes: list[SensorMode]
    effect_domains: list[EffectDomain]
    evidence_level: EvidenceLevel | None = None

class TrackUpdate(Track):
    __occid_model_id__: ClassVar[int] = 95
    track_id: StringID
    track_state: TrackState | None = None
    updated_ts: builtins.float
    confidence: ConfidenceLevel | None = None

class IsrResult(Assessment):
    __occid_model_id__: ClassVar[int] = 96
    detections: list[IsrObservation]
    track_updates: list[TrackUpdate]
    media: list[MediaItemSchema] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[IsrObservation]

class IntelTrackSchema(Track):
    __occid_model_id__: ClassVar[int] = 97
    schema_id: StringID
    schema_type: builtins.str = 'INTEL_TRACK'
    created_ts: builtins.float | None = None
    updated_ts: builtins.float | None = None
    origin_system: builtins.str | None = None
    trust_score: ConfidenceLevel | None = None
    alt_ids: list[StringID]
    entity_flags: list[builtins.str]
    faction: builtins.str | None = None
    spotted_time: builtins.float
    updated_time: builtins.float
    stale_time: builtins.float
    track_state: TrackState = TrackState.NEW
    category: IntelCategory | None = None
    sensor_id: StringID | None = None
    spotter_last: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    error_m: builtins.float | None = None
    latest_observation: IsrObservation | None = None
    observations: list[IsrObservation]
