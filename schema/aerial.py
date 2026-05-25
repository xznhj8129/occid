"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class TaskAir(IntEnum):
    FLY = 0
    AIR_DROP = auto()
    RECOVERY = auto()

class AirMissionType(IntEnum):
    SURVEY = 0
    SEARCH = auto()
    DELIVERY = auto()

class AirMoveTask(IntEnum):
    FLY = 0
    RELOCATION = auto()

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

class PlannerPointType(IntEnum):
    HOME = 0
    TAKEOFF = auto()
    LANDING = auto()
    HOLD = auto()
    WAYPOINT = auto()
    ASSEMBLY = auto()
    POI = auto()
    ROI = auto()
    SURVEY = auto()

class PlannerPointCategory(IntEnum):
    ROUTE_IN = 0
    SURVEY = auto()
    SURVEY_AREA = auto()
    ROUTE_OUT = auto()

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

class AirGroupFormation3DType(IntEnum):
    NONE = 0
    BOX = auto()
    SEP_2D_PER_FL = auto()
    SEP_2D_SPACED = auto()

class AirGroupFormation2DType(IntEnum):
    NONE = 0
    LINE = auto()
    ECHELON = auto()
    TRAIL = auto()
    SQUARE = auto()
    DIAMOND = auto()
    VEE = auto()
    HEAVY_LEFT = auto()
    HEAVY_RIGHT = auto()
    ECHELON_LEFT = auto()
    ECHELON_RIGHT = auto()
    STAGG_TRAIL_LEFT = auto()
    STAGG_TRAIL_RIGHT = auto()

### Models

class LoiterOrbit(OCCIDModel):
    orbit_direction: int
    orbit_radius: int
    loiter_time: int

class WeatherLimits(OCCIDModel):
    ifr: bool | None = None
    night: bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: bool | None = None

class TelemetryState(OCCIDModel):
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    mission_phase: AirMissionPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: float | None = None
    link_rssi: float | None = None

class FlightLevelBand(OCCIDModel):
    altitude_range_m: NumericRange
    alt_sep_m: float

class FlightPhasePlan(OCCIDModel):
    phase: AirMissionPhase
    flight_level: FlightLevelBand | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: float | None = None
    delay_s: float | None = None
    airspeed: float | None = None
    path_offset: LocalDirection | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class MissionRouteGeometry(OCCIDModel):
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class MissionPoi(OCCIDModel):
    uid: str
    name: str
    pos: GlobalPosition
    origin: str
    cot: str | None = None
    added_ts: float | None = None
    stale_after_s: float | None = None
    url: str | None = None

class AutopilotMissionWaypoint(OCCIDModel):
    waypoint_index: int
    action_code: int | None = None
    position: GlobalPosition
    param1: int | None = None
    param2: int | None = None
    param3: int | None = None
    flag: int | None = None

class MissionProgress(OCCIDModel):
    waypoint_count: int | None = None
    current_waypoint_index: int | None = None
    mission_valid: bool | None = None

class PlannerMissionPoint(OCCIDModel):
    num: int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class PlannedRoutePoints(OCCIDModel):
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint

class FlightAssignment(OCCIDModel):
    num: int
    unit_id: str | None = None
    callsign: str | None = None
    objective_assign: int | None = None
    wave_n: int = 0
    formation_n: int = 0
    takeoff_time: float = 0.0

class PlannedUnitMission(OCCIDModel):
    unit_num: int
    callsign: str
    fl: float
    route_in: GeoPath
    objective: PlannerMissionPoint
    route_out: GeoPath
    home: GlobalPosition
    land_pos: GlobalPosition
    ip_wait_delay: float = 0.0
    wp: GeoPath

class AirMissionSchema(OCCIDModel):
    mission_name: str
    mission_uid: str
    mission_time: float
    mission_type: TaskType
    takeoff: FlightPhasePlan
    assembly_point: FlightPhasePlan
    route: FlightPhasePlan
    ingress: FlightPhasePlan
    survey_area: FlightPhasePlan
    egress: FlightPhasePlan
    landing: FlightPhasePlan
    pois: list[MissionPoi]
    assignments: dict[str, FlightAssignment]
    unit_plans: dict[str, PlannedUnitMission]
    routes: MissionRouteGeometry
    route_points: PlannedRoutePoints
