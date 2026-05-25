"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

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

class Condition(State):
    pass

class HealthAlert(Condition):
    alert_id: str | None = None
    level: AlertLevel
    condition: str
    acknowledged: bool = False

class SubsystemHealth(Condition):
    subsystem_id: str
    state: HealthStatus
    fault_count: int = 0
    note: str | None = None

class HealthSnapshot(Condition):
    overall_state: HealthStatus
    link_state: LinkCondition | None = None
    power_state: ResourceStatus | None = None
    temp_state: ResourceStatus | None = None
    fault_count: int = 0
    updated_ts: float | None = None
    subsystems: list[SubsystemHealth]
    alerts: list[HealthAlert]

class MaintenanceStatus(Condition):
    state: MaintenanceState
    last_service_ts: float | None = None
    next_service_ts: float | None = None
    note: str | None = None

class VehicleReadinessState(Condition):
    gyro_ok: bool | None = None
    accel_ok: bool | None = None
    mag_ok: bool | None = None
    local_position_ok: bool | None = None
    global_position_ok: bool | None = None
    home_position_ok: bool | None = None
    armable: bool | None = None
    arm_ready: bool | None = None
    takeoff_ready: bool | None = None
    ekf_using_gps: bool | None = None
    can_arm_or_run: bool | None = None
    mode_name: str | None = None
    mode_problems: list[str]
    health_problems: list[str]
