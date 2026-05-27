"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .constraint import Constraint
from .state import State

### Enums

class AirMissionPhase(IntEnum):
    ONLINE = 0
    PREPARING = auto()
    TAKEOFF = auto()
    ASSEMBLY = auto()
    HOLDING = auto()
    ENROUTE = auto()
    INITIAL = auto()
    OBJECTIVE = auto()
    EGRESS = auto()
    RETURN = auto()
    APPROACH = auto()
    LANDING = auto()
    SHUTDOWN = auto()

class AirMissionEvent(IntEnum):
    ONLINE = 0
    PREPARED = auto()
    LOADED = auto()
    READY_TAKEOFF = auto()
    TAKEOFF_COMPLETE = auto()
    ASSEMBLY = auto()
    ENROUTE = auto()
    HOLDING = auto()
    ACTING = auto()
    PROCEEDING = auto()
    RESUMING = auto()
    BINGO = auto()
    RTB = auto()
    LANDING = auto()
    LANDED = auto()
    SHUTDOWN = auto()
    ABORTING = auto()
    FAILING = auto()

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
    MISSION_OPERATION = auto()
    RTB = auto()
    LANDING = auto()
    POSTFLIGHT = auto()
    ABORT = auto()

class AirframeType(IntEnum):
    FIXED_WING = 0
    COPTER = auto()
    VTOL = auto()
    TAILSITTER = auto()
    FLYING_WING = auto()

class CopterType(IntEnum):
    X = 0
    Y = auto()
    HEXA = auto()
    OCTO = auto()
    DECA = auto()
    HELICOPTER = auto()

class VTOLType(IntEnum):
    NONE = 0
    QUADPLANE = auto()
    TILT = auto()
    VECTORING = auto()
    TAILSITTER = auto()

class NavAids(IntEnum):
    NONE = 0
    GNSS = auto()
    INS = auto()
    TERRAIN_MATCH = auto()
    CELESTIAL = auto()
    VISUAL = auto()

class GnssFixType(IntEnum):
    NONE = 0
    NO_FIX = auto()
    FIX_2D = auto()
    FIX_3D = auto()
    DGPS = auto()
    RTK_FLOAT = auto()
    RTK_FIXED = auto()

class AirNavigationSchema_type(IntEnum):
    MILITARY_AIR_NAVIGATION = 0

### Models

class TelemetryState(State):
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    mission_phase: AirMissionPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: float | None = None
    link_rssi: float | None = None

class Guidance(State):
    'Status and quality of the navigation solution, mode, source, and validity'

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

class GroundNavigationSchema(Guidance):
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    max_range: float
    max_spd: float

class AirNavigationSchema(Guidance):
    flight_type: AirframeType
    control_modes: list[FlightMode]
    failsafe_mode: AirFailsafeMode | None = None
    weather_limits: WeatherLimits
    ifr: bool | None = None
    propulsion: PropulsionType
    navigation: NavigationMode
    navaids: list[NavAids]
    fuel: FuelState | None = None
    max_range: float
    max_flight_t: float
    max_spd: float
    cruise_spd: float
    max_alt: float
    start_flight_time: float

class WeatherLimits(Constraint):
    ifr: bool | None = None
    night: bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: bool | None = None
