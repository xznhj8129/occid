"""Generated from core/schemav2."""
from __future__ import annotations
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

class PowerStatus(IntEnum):
    UNKNOWN = 0
    NOT_PRESENT = auto()
    OPERATING = auto()
    DISABLED = auto()
    ERROR = auto()

class PowerType(IntEnum):
    UNKNOWN = 0
    GAS = auto()
    BATTERY = auto()
    SOLAR = auto()
    NUCLEAR = auto()

### Models

class HealthAlert(OCCIDModel):
    alert_id: str | None = None
    level: AlertLevel
    condition: str
    acknowledged: bool = 'false'

class SubsystemHealth(OCCIDModel):
    subsystem_id: str
    state: HealthStatus
    fault_count: int = '0'
    note: str | None = None

class HealthSnapshot(OCCIDModel):
    overall_state: HealthStatus
    link_state: LinkCondition | None = None
    power_state: ResourceStatus | None = None
    temp_state: ResourceStatus | None = None
    fault_count: int = '0'
    updated_ts: float | None = None
    subsystems: list[SubsystemHealth] = Field(default_factory=list)
    alerts: list[HealthAlert] = Field(default_factory=list)

class MaintenanceStatus(OCCIDModel):
    state: MaintenanceState
    last_service_ts: float | None = None
    next_service_ts: float | None = None
    note: str | None = None

class PowerSourceSchema(OCCIDModel):
    source_id: str
    power_type: PowerType
    status: PowerStatus
    remaining_pct: float | None = None

class PowerStateSchema(OCCIDModel):
    status: PowerStatus
    sources: list[PowerSourceSchema] = Field(default_factory=list)
