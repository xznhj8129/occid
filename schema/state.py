"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Enums

class ObservationTimeBasis(IntEnum):
    UNKNOWN = 0
    UNIX = auto()
    BOOT = auto()

### Models

class State(Data):
    'Changing condition of an object, node, link, task, system, or process'
    __occid_model_id__: ClassVar[int] = 123
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class EntityState(State):
    'Time-indexed mutable condition reported for an entity independently of its identity and specification'
    __occid_model_id__: ClassVar[int] = 280
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
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
    link_states: dict[builtins.str, SerializeAsAny[LinkState | MeshLink]]
    control_state: ControlLevel | None = None
    source_observation_ts: builtins.float | None = None
    source_time_basis: ObservationTimeBasis | None = None
    received_ts: builtins.float | None = None
    published_ts: builtins.float | None = None
