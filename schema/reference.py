"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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
    alt_sep_m: builtins.float

class MissionPoi(Mark):
    uid: StringID
    name: builtins.str
    pos: GlobalPosition
    origin: builtins.str
    cot: builtins.str | None = None
    added_ts: builtins.float | None = None
    stale_after_s: builtins.float | None = None
    url: builtins.str | None = None

class AutopilotMissionWaypoint(Mark):
    waypoint_index: builtins.int
    action_code: builtins.int | None = None
    position: GlobalPosition
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None

class PlannerMissionPoint(Mark):
    num: builtins.int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class LoiterOrbit(ReferencePath):
    orbit_direction: builtins.int
    orbit_radius: builtins.int
    loiter_time: builtins.int

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
