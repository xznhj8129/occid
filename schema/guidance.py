"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Enums

class AirFailsafeMode(IntEnum):
    HOLD = 0
    RTB = auto()
    LAND = auto()
    LOITER = auto()
    CONTINUE_LAST = auto()

class FlightMode(IntEnum):
    ACRO = 0
    ANGLE = auto()
    POSHOLD = auto()
    GUIDED = auto()
    NAV_WP = auto()
    LOITER = auto()
    CRUSE = auto()
    RTH = auto()
    LANDING = auto()
    DISARMED = auto()

class FlightPhase(IntEnum):
    PREFLIGHT = 0
    TAKEOFF = auto()
    CRUISE = auto()
    LOITER = auto()
    PLAN_OPERATION = auto()
    RTB = auto()
    LANDING = auto()
    POSTFLIGHT = auto()
    ABORT = auto()

class GnssFixType(IntEnum):
    NONE = 0
    NO_FIX = auto()
    FIX_2D = auto()
    FIX_3D = auto()
    DGPS = auto()
    RTK_FLOAT = auto()
    RTK_FIXED = auto()

### Models

class Guidance(State):
    'Navigation, arming, mode, plan progress, readiness, failsafe, estimator, and control state'
    __occid_model_id__: ClassVar[int] = 135

class TelemetryState(Guidance):
    __occid_model_id__: ClassVar[int] = 136
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    plan_phase: FlightPlanPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: builtins.float | None = None
    link_rssi: builtins.float | None = None

class NavigationValidity(Guidance):
    __occid_model_id__: ClassVar[int] = 137
    local_position_ok: builtins.bool | None = None
    global_position_ok: builtins.bool | None = None
    home_position_ok: builtins.bool | None = None

class GnssSolution(Guidance):
    __occid_model_id__: ClassVar[int] = 138
    fix_type: GnssFixType | None = None
    fix_code: builtins.int | None = None
    satellites_used: builtins.int | None = None
    position: GlobalPosition | None = None
    altitude: AltitudeState | None = None
    ground_speed_ms: builtins.float | None = None
    ground_course_deg: builtins.float | None = None
    hdop: builtins.float | None = None
    vdop: builtins.float | None = None
    eph: builtins.float | None = None
    epv: builtins.float | None = None
    yaw_deg: builtins.float | None = None
    last_message_dt: builtins.float | None = None
    errors: builtins.float | None = None
    timeouts: builtins.float | None = None
