"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class AlertLevel(IntEnum):
    ADVISORY = 0
    CAUTION = auto()
    WARNING = auto()

class HealthStatus(IntEnum):
    HEALTHY = 0
    WARN = auto()
    FAIL = auto()
    OFFLINE = auto()
    NOT_READY = auto()

class HumanHealthStatus(IntEnum):
    HEALTHY = 0
    TIRED = auto()
    SICK = auto()
    WOUNDED_LIGHT = auto()
    WOUNDED_CRITICAL = auto()
    DEAD = auto()
    MISSING = auto()
    CAPTURED = auto()

class ResourceStatus(IntEnum):
    UNKNOWN = 0
    NOMINAL = auto()
    DEGRADED = auto()
    FAILED = auto()
    OFFLINE = auto()

class SystemError(IntEnum):
    NO_ERROR = 0
    NOT_FOUND = auto()
    DEVICE_UNAVAILABLE = auto()
    HARDWARE_ERROR = auto()
    SOFTWARE_ERROR = auto()
    DATABASE_ERROR = auto()
    NETWORK_ERROR = auto()

class MaintenanceState(IntEnum):
    UNKNOWN = 0
    READY = auto()
    DUE = auto()
    IN_PROGRESS = auto()
    GROUNDED = auto()
    FAILED = auto()

### Models

class Health(OCCIDModel):
    'Integrity, damage, faults, and readiness state'
    __occid_model_id__: ClassVar[int] = 108
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('HealthAlert', 'LinkState', 'SubsystemHealth', 'HealthSnapshot', 'MaintenanceStatus', 'NavReadinessState')

class HealthAlert(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    alert_ref: builtins.str | None = None
    level: AlertLevel
    condition: builtins.str
    acknowledged: builtins.bool = False

class LinkState(OCCIDModel):
    'Time-varying condition and observed quality of a communication link'
    __occid_model_id__: ClassVar[int] = 134
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeshLink',)
    link_uid: Semantic[UID] | None = None
    condition: LinkCondition | None = None
    connection_status: ConnectionStatus | None = None
    signal: Semantic[SignalQuality] | None = None
    delivery: Semantic[DeliveryQuality] | None = None
    counters: Semantic[LinkCounters] | None = None

class SubsystemHealth(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 251
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subsystem_ref: builtins.str
    state: HealthStatus
    fault_count: builtins.int = 0
    note: builtins.str | None = None

class HealthSnapshot(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 110
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    overall_state: HealthStatus
    link_state: LinkCondition | None = None
    power_state: ResourceStatus | None = None
    temp_state: ResourceStatus | None = None
    fault_count: builtins.int = 0
    updated_ts: Semantic[Timestamp] | None = None
    subsystems: list[Semantic[SubsystemHealth]]
    alerts: list[Semantic[HealthAlert]]

class MaintenanceStatus(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 144
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    state: MaintenanceState
    last_service_ts: Semantic[Timestamp] | None = None
    next_service_ts: Semantic[Timestamp] | None = None
    note: builtins.str | None = None

class NavReadinessState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 173
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Health'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    gyro_ok: builtins.bool | None = None
    accel_ok: builtins.bool | None = None
    mag_ok: builtins.bool | None = None
    local_position_ok: builtins.bool | None = None
    global_position_ok: builtins.bool | None = None
    home_position_ok: builtins.bool | None = None
    armable: builtins.bool | None = None
    arm_ready: builtins.bool | None = None
    takeoff_ready: builtins.bool | None = None
    ekf_using_gps: builtins.bool | None = None
    can_arm_or_run: builtins.bool | None = None
    mode_name: builtins.str | None = None
    mode_problems: list[builtins.str]
    health_problems: list[builtins.str]
