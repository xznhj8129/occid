"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data
from .struct import Struct

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
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Classification(Observation):
    __occid_model_id__: ClassVar[int] = 86
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Track(Observation):
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Assessment(Observation):
    __occid_model_id__: ClassVar[int] = 88
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Detection(Observation):
    'Assessment that something exists or occurred'
    __occid_model_id__: ClassVar[int] = 89
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class VisionBox(Detection):
    __occid_model_id__: ClassVar[int] = 90
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    space: DetectionBoxSpace
    bounds: BoundingBox

class VisionDetection(Detection):
    __occid_model_id__: ClassVar[int] = 91
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    detection_id: builtins.str | None = None
    label: builtins.str | None = None
    class_id: builtins.int | None = None
    confidence: builtins.float | None = None
    box: VisionBox | None = None
    bearing: LocalDirection | None = None
    position: GlobalPosition | None = None
    source_frame_id: builtins.str | None = None
    attributes: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]

class VisionDetectionFrame(Detection):
    __occid_model_id__: ClassVar[int] = 92
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    frame_id: builtins.str | None = None
    sensor_id: UID | None = None
    timestamp_us: builtins.int | None = None
    detections: list[VisionDetection]

class IsrObservation(Observation):
    __occid_model_id__: ClassVar[int] = 93
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    obs_id: UID
    track_id: UID | None = None
    sensor_id: UID | None = None
    obs_ts: builtins.float
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(Struct):
    __occid_model_id__: ClassVar[int] = 94
    __occid_semantic_role__: ClassVar[str] = 'specialization'
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
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    track_id: UID
    track_state: TrackState | None = None
    updated_ts: builtins.float
    confidence: ConfidenceLevel | None = None

class IsrResult(Assessment):
    __occid_model_id__: ClassVar[int] = 96
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    detections: list[IsrObservation]
    track_updates: list[TrackUpdate]
    media: list[MediaItemSchema] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[IsrObservation]
