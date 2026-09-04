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

class EntityState(OCCIDModel):
    'Time-indexed mutable condition reported for an entity independently of its identity and specification'
    __occid_model_id__: ClassVar[int] = 62
    __occid_semantic_role__: ClassVar[str] = 'type'
    record: Record
    subject_uid: UID
    timestamp: builtins.float
    position: LocationState | None = None
    motion: VelocityVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    airspeed: Airspeed | None = None
    flight_control: FlightControlState | None = None
    power: PowerStateSchema | None = None
    operational_status: EntityOperationalState | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    health: HealthSnapshot | None = None
    resources: SuppliesSchema | None = None
    link_states: dict[builtins.str, LinkState]
    control_state: ControlLevel | None = None
    source_observation_ts: builtins.float | None = None
    source_time_basis: ObservationTimeBasis | None = None
    received_ts: builtins.float | None = None
    published_ts: builtins.float | None = None
