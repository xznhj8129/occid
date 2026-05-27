"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

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

class Reference_type(IntEnum):
    MARK = 0
    PATH = auto()
    REGION = auto()
    BOUNDARY = auto()

class MissionPoi_type(IntEnum):
    MILITARY = 0

### Models

class Reference(Control):
    'Control-side structural wrapper binding spatial definitions and structs into control-usable referents'

class Mark(Reference):
    pass

class ReferencePath(Reference):
    pass

class Region(Reference):
    pass

class Boundary(Reference):
    pass

class LoiterOrbit(ReferencePath):
    orbit_direction: int
    orbit_radius: int
    loiter_time: int

class FlightLevelBand(Region):
    altitude_range_m: NumericRange
    alt_sep_m: float

class MissionRouteGeometry(ReferencePath):
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class MissionPoi(Mark):
    uid: str
    name: str
    pos: GlobalPosition
    origin: str
    cot: str | None = None
    added_ts: float | None = None
    stale_after_s: float | None = None
    url: str | None = None

class AutopilotMissionWaypoint(Mark):
    waypoint_index: int
    action_code: int | None = None
    position: GlobalPosition
    param1: int | None = None
    param2: int | None = None
    param3: int | None = None
    flag: int | None = None

class PlannerMissionPoint(Mark):
    num: int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class PlannedRoutePoints(ReferencePath):
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint
