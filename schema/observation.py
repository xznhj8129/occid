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

class Classification(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 30
    __occid_semantic_role__: ClassVar[str] = 'type'

class Track(OCCIDModel):
    'Persistent maintained identity for one correlated observed object or phenomenon'
    __occid_model_id__: ClassVar[int] = 257
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Track')]

class Assessment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 12
    __occid_semantic_role__: ClassVar[str] = 'type'

class Detection(OCCIDModel):
    'Assessment that something exists or occurred'
    __occid_model_id__: ClassVar[int] = 52
    __occid_semantic_role__: ClassVar[str] = 'type'

class VisionBox(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 274
    __occid_semantic_role__: ClassVar[str] = 'representation'
    space: DetectionBoxSpace
    bounds: BoundingBox

class VisionDetection(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 275
    __occid_semantic_role__: ClassVar[str] = 'representation'
    detection_id: Annotated[IntID, IDNamespace('Detection')]
    label: builtins.str | None = None
    class_index: builtins.int | None = None
    confidence: builtins.float | None = None
    box: VisionBox | None = None
    bearing: LocalDirection | None = None
    position: GlobalPosition | None = None
    source_frame_ref: builtins.str | None = None
    attributes: dict[builtins.str, MetadataValue]

class VisionDetectionFrame(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 276
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    frame_ref: builtins.str | None = None
    sensor_uid: UID | None = None
    timestamp_us: builtins.int | None = None
    detections: list[VisionDetection]

class IsrObservation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 112
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Observation')]
    track_uid: UID | None = None
    sensor_uid: UID | None = None
    obs_ts: builtins.float
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 113
    __occid_semantic_role__: ClassVar[str] = 'representation'
    focus_type: IsrFocusType | None = None
    focus_point: GlobalPosition | None = None
    dwell_s: builtins.float | None = None
    revisit_s: builtins.float | None = None
    sensor_types: list[SensorType]
    sensor_modes: list[SensorMode]
    effect_domains: list[EffectDomain]
    evidence_level: EvidenceLevel | None = None

class TrackUpdate(OCCIDModel):
    'State update about an existing Track; does not define Track identity'
    __occid_model_id__: ClassVar[int] = 258
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    track_uid: UID
    track_state: TrackState | None = None
    updated_ts: builtins.float
    confidence: ConfidenceLevel | None = None

class IsrResult(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 114
    __occid_semantic_role__: ClassVar[str] = 'representation'
    detections: list[IsrObservation]
    track_updates: list[TrackUpdate]
    media: list[MediaItem] | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[IsrObservation]
