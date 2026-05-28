"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class Reference_type(IntEnum):
    MARK = 0
    PATH = auto()
    REGION = auto()
    BOUNDARY = auto()

class MissionPoi_type(IntEnum):
    MILITARY = 0

### Models

class Reference(Control):
    'Control-side referent such as mark, path, region, boundary, target, waypoint, route, or area'

class Mark(Reference):
    pass

class ReferencePath(Reference):
    pass

class Region(Reference):
    pass

class Boundary(Reference):
    pass

class FlightLevelBand(Region):
    altitude_range_m: NumericRange
    alt_sep_m: float

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

class LoiterOrbit(ReferencePath):
    orbit_direction: int
    orbit_radius: int
    loiter_time: int

class MissionRouteGeometry(ReferencePath):
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class PlannedRoutePoints(ReferencePath):
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint
