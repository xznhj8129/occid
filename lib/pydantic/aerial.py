"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .spatial import GeoArea, GeoPath

### Enums

class TaskAir(IntEnum):
    FLY = 0
    ISR = auto()
    CLOSE_AIR_SUPPORT = auto()
    AIR_DROP = auto()
    ELECTRONIC_WARFARE = auto()
    STRIKE = auto()
    RECOVERY = auto()
    SEAD = auto()

class AirRole(IntEnum):
    GROUND = 0
    AIR_DEFENSE = auto()
    FIGHTER = auto()
    GROUND_ATTACK = auto()
    ISR = auto()
    MINE = auto()
    CARGO = auto()

class AirMissionType(IntEnum):
    SURVEY = 0
    SEARCH = auto()
    ISR = auto()
    DELIVERY = auto()

class AirMoveTask(IntEnum):
    FLY = 0
    RELOCATION = auto()

class AirCombatTask(IntEnum):
    STRIKE = 0
    CAS = auto()
    CAP = auto()
    INTERCEPT = auto()
    HK = auto()

class AirISRType(IntEnum):
    OVERFLY = 0
    FLYBY = auto()
    ORBIT = auto()

class AirAttackMode(IntEnum):
    ONEWAY = 0
    DROPPER = auto()
    DIVE = auto()
    STRAFE = auto()
    STANDOFF_LAUNCH = auto()

class AirFailsafeMode(IntEnum):
    HOLD = 0
    RTB = auto()
    DROP = auto()
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
    TARGET = auto()
    DISPERSAL = auto()
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

### Mappings

AIR_ROLE_LABELS: dict[AirRole, str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

AIR_ROLE_NAMES: dict[AirRole, str] = {
    AirRole.GROUND: 'Ground',
    AirRole.AIR_DEFENSE: 'Air Defense',
    AirRole.FIGHTER: 'Fighter',
    AirRole.GROUND_ATTACK: 'Ground Attack',
    AirRole.ISR: 'ISR',
    AirRole.MINE: 'Mine',
    AirRole.CARGO: 'Cargo',
}

### Models

class LoiterOrbit(SigmaModel):
    orbit_direction: int
    orbit_radius: int
    loiter_time: int

class WeatherLimits(SigmaModel):
    ifr: bool | None = None
    night: bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: bool | None = None

class TelemetryState(SigmaModel):
    flight_mode: FlightMode | None = None
    flight_phase: FlightPhase | None = None
    mission_phase: AirMissionPhase | None = None
    attitude: EulerAngles | None = None
    velocity: VelocityVector | None = None
    battery_pct: float | None = None
    link_rssi: float | None = None

class FlightLevelBand(SigmaModel):
    altitude_range_m: NumericRange
    alt_sep_m: float

class FlightPhasePlan(SigmaModel):
    phase: AirMissionPhase
    flight_level: FlightLevelBand | None = None
    alt_frame: AltitudeDatum | None = None
    h_sep_m: float | None = None
    delay_s: float | None = None
    airspeed: float | None = None
    path_offset: LocalDirection | None = None
    formation_2d: AirGroupFormation2DType | None = None
    formation_3d: AirGroupFormation3DType | None = None

class MissionRouteGeometry(SigmaModel):
    route_in: GeoPath = Field(default_factory=GeoPath)
    survey: GeoPath = Field(default_factory=GeoPath)
    survey_area: GeoArea = Field(default_factory=GeoArea)
    route_out: GeoPath = Field(default_factory=GeoPath)

class MissionPoi(SigmaModel):
    uid: str
    name: str
    pos: GlobalPosition
    origin: str
    cot: str | None = None
    sidc: int | None = None
    added_ts: float | None = None
    stale_after_s: float | None = None
    url: str | None = None

class PlannerMissionPoint(SigmaModel):
    num: int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class PlannedRoutePoints(SigmaModel):
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint] = Field(default_factory=list)
    survey: list[PlannerMissionPoint] = Field(default_factory=list)
    survey_area: list[PlannerMissionPoint] = Field(default_factory=list)
    route_out: list[PlannerMissionPoint] = Field(default_factory=list)
    end: PlannerMissionPoint

class FlightAssignment(SigmaModel):
    num: int
    unit_id: str | None = None
    callsign: str | None = None
    objective_assign: int | None = None
    wave_n: int = '0'
    formation_n: int = '0'
    takeoff_time: float = '0.0'

class PlannedUnitMission(SigmaModel):
    unit_num: int
    callsign: str
    fl: float
    route_in: GeoPath = Field(default_factory=GeoPath)
    target: PlannerMissionPoint
    route_out: GeoPath = Field(default_factory=GeoPath)
    home: GlobalPosition
    land_pos: GlobalPosition
    ip_wait_delay: float = '0.0'
    wp: GeoPath = Field(default_factory=GeoPath)

class AirMissionSchema(SigmaModel):
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
    pois: list[MissionPoi] = Field(default_factory=list)
    assignments: dict[str, FlightAssignment] = Field(default_factory=dict)
    unit_plans: dict[str, PlannedUnitMission] = Field(default_factory=dict)
    routes: MissionRouteGeometry = Field(default_factory=MissionRouteGeometry)
    route_points: PlannedRoutePoints = Field(default_factory=PlannedRoutePoints)
