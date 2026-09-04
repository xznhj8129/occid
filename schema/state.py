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
    __occid_model_id__: ClassVar[int] = 229
    __occid_semantic_role__: ClassVar[str] = 'type'

class EntityState(OCCIDModel):
    'Time-indexed mutable condition reported for an entity independently of its identity and specification'
    __occid_model_id__: ClassVar[int] = 64
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    subject_uid: UID
    timestamp: builtins.float
    position: LocationState | None = None
    motion: VelocityVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    airspeed: Airspeed | None = None
    flight_control: FlightControlState | None = None
    power: PowerState | None = None
    operational_status: EntityOperationalState | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    health: HealthSnapshot | None = None
    resources: Supplies | None = None
    link_states: dict[builtins.str, SerializeAsAny[LinkState | MeshLink]]
    control_state: ControlLevel | None = None
    source_observation_ts: Timestamp | None = None
    source_time_basis: ObservationTimeBasis | None = None
    received_ts: Timestamp | None = None
    published_ts: Timestamp | None = None
