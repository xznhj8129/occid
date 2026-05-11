"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .tasks import BaseTask, TaskType

### Enums

class TaskISR(IntEnum):
    OBSERVE = 0
    SEARCH = auto()
    FIND = auto()
    SURVEY = auto()
    INVESTIGATE = auto()
    IMPROVE_TRACK = auto()
    IMAGERY = auto()

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
    DAMAGE_ASSESSMENT = auto()

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

class TrackImproveGoal(IntEnum):
    POSITION = 0
    IDENTITY = auto()
    ACTIVITY = auto()
    COMPOSITION = auto()
    DAMAGE = auto()

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

class ActivityType(IntEnum):
    STATIC = 0
    MOVING = auto()
    ENGAGING = auto()
    DIGGING_IN = auto()
    RESUPPLYING = auto()
    RETREATING = auto()

### Models

class IsrTask(BaseTask):
    task_type: TaskType = Field(default=TaskType.ISR, frozen=True)
    isr_task: TaskISR | None = None
    area: GeoArea
    dwell_seconds: float | None = None
    isr_params: IsrParameters | None = None
    isr_result: IsrResult | None = None

class IsrObservation(OCCIDModel):
    obs_id: str
    track_id: str | None = None
    sensor_id: str | None = None
    obs_ts: float
    observation_kind: ObservationKind | None = None
    category: IntelCategory | None = None
    spotter_origin: SpotterOrigin | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    signal: SignalSchema | None = None
    confidence: ConfidenceLevel | None = None

class IsrParameters(OCCIDModel):
    focus_type: IsrFocusType | None = None
    focus_point: GlobalPosition | None = None
    dwell_s: float | None = None
    revisit_s: float | None = None
    sensor_types: list[SensorType] = Field(default_factory=list)
    sensor_modes: list[SensorMode] = Field(default_factory=list)
    effect_domains: list[EffectDomain] = Field(default_factory=list)
    track_improve_goal: TrackImproveGoal | None = None
    bda_required: bool = 'false'
    evidence_level: EvidenceLevel | None = None

class TrackUpdate(OCCIDModel):
    track_id: str
    track_state: TrackState | None = None
    updated_ts: float
    confidence: ConfidenceLevel | None = None

class IsrResult(OCCIDModel):
    detections: list[IsrObservation] = Field(default_factory=list)
    track_updates: list[TrackUpdate] = Field(default_factory=list)
    media: MediaSchema | None = None
    confidence: ConfidenceLevel | None = None
    observations: list[IsrObservation] = Field(default_factory=list)

class IntelTrackSchema(OCCIDModel):
    schema_id: str
    schema_type: SchemaKind = SchemaKind.INTEL_TRACK
    created_ts: float | None = None
    updated_ts: float | None = None
    origin_system: str | None = None
    trust_score: ConfidenceLevel | None = None
    alt_ids: list[AlternateId] = Field(default_factory=list)
    entity_flags: list[str] = Field(default_factory=list)
    faction: Faction
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
    observations: list[IsrObservation] = Field(default_factory=list)

class BdaStrikeSummary(OCCIDModel):
    casualties: int = '0'
    destroyed: list[ItemCount] = Field(default_factory=list)
    damaged: list[ItemCount] = Field(default_factory=list)
    unknown: list[ItemCount] = Field(default_factory=list)

class BdaReportSchema(OCCIDModel):
    time: float
    uid: str
    unit_code: str
    spotter: str
    track: str
    sensor: str
    pos: GlobalPosition
    spotter_origin: SpotterOrigin | None = None
    confidence: ConfidenceLevel | None = None
    casualties: int = '0'
    assessment: BdaStrikeSummary = Field(default_factory=BdaStrikeSummary)
    summary: str | None = None

class SaluteReportSchema(OCCIDModel):
    time: float
    uid: str
    unit_code: str
    spotter: str
    sensor: str
    spotter_origin: SpotterOrigin
    activity: ActivityType | None = None
    pos: GlobalPosition
    equipment: list[ItemCount] = Field(default_factory=list)
    vehicles: list[ItemCount] = Field(default_factory=list)
    summary: str | None = None
