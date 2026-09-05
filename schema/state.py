"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class ObservationTimeBasis(IntEnum):
    UNKNOWN = 0
    UNIX = auto()
    BOOT = auto()

### Models

class State(OCCIDModel):
    'Changing condition of an object, node, link, task, system, or process'
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Lifecycle', 'Activation', 'Cue', 'GNC', 'Health', 'Input', 'Internal', 'Kinematic', 'Resource', 'SensorState', 'EntityState', 'Validation', 'Position')

class EntityState(OCCIDModel):
    'Time-indexed mutable condition reported for an entity independently of its identity and specification'
    __occid_model_id__: ClassVar[int] = 73
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: builtins.float
    position: Semantic[LocationState] | None = None
    motion: Semantic[VelocityVector] | None = None
    angular_velocity: Semantic[AngularVelocityVector] | None = None
    airspeed: Semantic[Airspeed] | None = None
    flight_control: Semantic[FlightControlState] | None = None
    power: Semantic[PowerState] | None = None
    operational_status: EntityOperationalState | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    health: Semantic[HealthSnapshot] | None = None
    resources: Semantic[Supplies] | None = None
    link_states: dict[builtins.str, Semantic[LinkState]]
    control_state: ControlLevel | None = None
    source_observation_ts: Semantic[Timestamp] | None = None
    source_time_basis: ObservationTimeBasis | None = None
    received_ts: Semantic[Timestamp] | None = None
    published_ts: Semantic[Timestamp] | None = None
