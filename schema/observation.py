"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class Observation(OCCIDModel):
    'External detection, classification, track, signal, spot report, threat, or assessment data'
    __occid_model_id__: ClassVar[int] = 182
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Classification', 'Track', 'Assessment', 'Detection', 'IsrObservation', 'TrackUpdate')

class Classification(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 31
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Track(OCCIDModel):
    'Persistent maintained identity for one correlated observed object or phenomenon'
    __occid_model_id__: ClassVar[int] = 272
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Track')]

class Assessment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 12
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IsrResult',)

class Detection(OCCIDModel):
    'Assessment that something exists or occurred'
    __occid_model_id__: ClassVar[int] = 60
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VisionBox', 'VisionDetection', 'VisionDetectionFrame')

class VisionBox(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 289
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    space: DetectionBoxSpace
    bounds: Semantic[BoundingBox]

class VisionDetection(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 290
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    detection_id: Annotated[IntID, IDNamespace('Detection')]
    label: builtins.str | None = None
    class_index: builtins.int | None = None
    confidence: builtins.float | None = None
    box: Semantic[VisionBox] | None = None
    bearing: Semantic[LocalDirection] | None = None
    position: Semantic[GlobalPosition] | None = None
    source_frame_uid: Semantic[UID] | None = None
    attributes: dict[builtins.str, Semantic[MetadataValue]]

class VisionDetectionFrame(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 291
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    frame_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    timestamp_us: builtins.int | None = None
    detections: list[Semantic[VisionDetection]]

class IsrObservation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 121
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Observation')]
    track_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    obs_ts: Semantic[Timestamp]
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: Semantic[SpotterOrigin] | None = None
    position: Semantic[GlobalPosition] | None = None
    uncertainty: Semantic[LocationUncertainty] | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 122
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    focus_type: IsrFocusType | None = None
    focus_point: Semantic[GlobalPosition] | None = None
    dwell_s: builtins.float | None = None
    revisit_s: builtins.float | None = None
    sensor_types: list[SensorType]
    sensor_modes: list[SensorMode]
    effect_domains: list[EffectDomain]
    evidence_level: EvidenceLevel | None = None

class TrackUpdate(OCCIDModel):
    'State update about an existing Track; does not define Track identity'
    __occid_model_id__: ClassVar[int] = 273
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    track_uid: Semantic[UID]
    track_state: TrackState | None = None
    updated_ts: Semantic[Timestamp]
    confidence: ConfidenceLevel | None = None

class IsrResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 123
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Assessment'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    detections: list[Semantic[IsrObservation]]
    track_updates: list[Semantic[TrackUpdate]]
    media: list[Semantic[MediaItem]] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[Semantic[IsrObservation]]
