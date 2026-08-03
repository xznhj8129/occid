"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Models

class State(Data):
    'Changing condition of an object, node, link, task, system, or process'
    __occid_model_id__: ClassVar[int] = 123

class EntityState(State):
    'Time-indexed mutable condition reported for an entity independently of its identity and specification'
    __occid_model_id__: ClassVar[int] = 280
    record: RecordMeta
    subject_id: StringID
    timestamp: builtins.float
    position: LocationState | None = None
    motion: VelocityVector | None = None
    operational_status: EntityOperationalState | None = None
    lifecycle_status: EntityLifecycleStatus | None = None
    health: HealthSnapshot | None = None
    resources: SuppliesSchema | None = None
    links: dict[builtins.str, LinkCondition]
    control_state: ControlLevel | None = None
