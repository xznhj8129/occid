"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class AirFailsafeMode(IntEnum):
    HOLD = 0
    RTB = auto()
    LAND = auto()
    LOITER = auto()
    CONTINUE_LAST = auto()

class StandardFlightMode(IntEnum):
    NON_STANDARD = 0
    POSITION_HOLD = auto()
    ORBIT = auto()
    CRUISE = auto()
    ALTITUDE_HOLD = auto()
    SAFE_RECOVERY = auto()
    MISSION = auto()
    LAND = auto()
    TAKEOFF = auto()
    EXTERNAL_CONTROL = auto()

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

class GNC(OCCIDModel):
    'Guidance, navigation, and control state including arming, mode, plan progress, readiness, failsafe, and estimator state'
    __occid_model_id__: ClassVar[int] = 85
    __occid_semantic_role__: ClassVar[str] = 'type'

class NavigationValidity(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 163
    __occid_semantic_role__: ClassVar[str] = 'representation'
    local_position_ok: builtins.bool | None = None
    global_position_ok: builtins.bool | None = None
    home_position_ok: builtins.bool | None = None

class GnssSolution(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 91
    __occid_semantic_role__: ClassVar[str] = 'representation'
    fix_type: GnssFixType | None = None
    satellites_used: builtins.int | None = None
    position: GlobalPosition | None = None
    altitude: AltitudeState | None = None
    ground_speed_ms: builtins.float | None = None
    ground_course_deg: builtins.float | None = None
    hdop: builtins.float | None = None
    vdop: builtins.float | None = None
    yaw_deg: builtins.float | None = None

class AutopilotMissionState(OCCIDModel):
    'State and storage capacity of an onboard autopilot waypoint mission; distinct from OCCID Task, Plan, Assignment, and Execution lifecycle state'
    __occid_model_id__: ClassVar[int] = 17
    __occid_semantic_role__: ClassVar[str] = 'representation'
    valid: builtins.bool | None = None
    current_waypoint_index: builtins.int | None = None
    waypoint_count: builtins.int | None = None
    max_waypoints: builtins.int | None = None
    waypoints_remaining: builtins.int | None = None
