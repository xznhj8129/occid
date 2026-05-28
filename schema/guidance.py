"""Generated from core/schemav2."""
from __future__ import annotations
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

class Guidance_type(IntEnum):
    PLAN_PROGRESS = 0
    TELEMETRY_STATE = auto()
    NAVIGATION_VALIDITY = auto()
    GNSS_SOLUTION = auto()
    FLIGHT_CONTROL_STATE = auto()

### Models

class Guidance(State):
    'Navigation, arming, mode, plan progress, readiness, failsafe, estimator, and control state'

class PlanProgress(Guidance):
    waypoint_count: int | None = None
    current_waypoint_index: int | None = None
    plan_valid: bool | None = None

class TelemetryState(Guidance):
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    plan_phase: FlightPlanPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: float | None = None
    link_rssi: float | None = None

class NavigationValidity(Guidance):
    local_position_ok: bool | None = None
    global_position_ok: bool | None = None
    home_position_ok: bool | None = None

class GnssSolution(Guidance):
    fix_type: GnssFixType | None = None
    fix_code: int | None = None
    satellites_used: int | None = None
    position: GlobalPosition | None = None
    altitude: AltitudeState | None = None
    ground_speed_ms: float | None = None
    ground_course_deg: float | None = None
    hdop: float | None = None
    vdop: float | None = None
    eph: float | None = None
    epv: float | None = None
    yaw_deg: float | None = None
    last_message_dt: float | None = None
    errors: float | None = None
    timeouts: float | None = None
