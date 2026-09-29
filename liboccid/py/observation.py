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
    __occid_model_id__: ClassVar[int] = 225
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Classification', 'Track', 'Assessment', 'Detection', 'IsrObservation', 'TrackUpdate')

class Classification(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 45
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Track(OCCIDModel):
    'Persistent maintained identity for one correlated observed object or phenomenon'
    __occid_model_id__: ClassVar[int] = 343
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    subject_uid: Semantic[ID] | None = None

class Assessment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 21
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IsrResult',)

class Detection(OCCIDModel):
    'Assessment that something exists or occurred'
    __occid_model_id__: ClassVar[int] = 78
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VisionBox', 'VisionDetection', 'VisionDetectionFrame')

class VisionBox(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 363
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    space: DetectionBoxSpace
    bounds: Semantic[BoundingBox]

class VisionDetection(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 364
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    label: builtins.str | None = None
    class_index: builtins.int | None = None
    confidence: builtins.float | None = None
    box: Semantic[VisionBox] | None = None
    bearing: Semantic[LocalDirection] | None = None
    position: Semantic[GlobalPosition] | None = None
    attributes: dict[builtins.str, Semantic[MetadataValue]]

class VisionDetectionFrame(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 365
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Detection'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    media_uid: Semantic[ID] | None = None
    observer_entity_uid: Semantic[ID] | None = None
    sensor_uid: Semantic[ID] | None = None
    timestamp_us: builtins.int | None = None
    detections: list[Semantic[VisionDetection]]

class IsrObservation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 158
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    side: Semantic[ID] | None = None
    identity: StandardIdentity
    symbology: Semantic[Symbology] | None = None
    track_uid: Semantic[ID] | None = None
    subject_uid: Semantic[ID] | None = None
    observer_entity_uid: Semantic[ID] | None = None
    sensor_uid: Semantic[ID] | None = None
    evidence_media_uids: list[Semantic[ID]]
    obs_ts: Semantic[Timestamp]
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: Semantic[SpotterOrigin] | None = None
    position: Semantic[GlobalPosition] | None = None
    uncertainty: Semantic[LocationUncertainty] | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 159
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
    __occid_model_id__: ClassVar[int] = 344
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Observation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    track_uid: Semantic[ID]
    track_state: TrackState | None = None
    updated_ts: Semantic[Timestamp]
    confidence: ConfidenceLevel | None = None

class IsrResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 160
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Assessment'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    detections: list[Semantic[IsrObservation]]
    track_updates: list[Semantic[TrackUpdate]]
    media: list[Semantic[MediaItem]] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[Semantic[IsrObservation]]
