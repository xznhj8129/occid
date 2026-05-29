"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .control import Control

### Models

class Reference(Control):
    'Control-side referent such as mark, path, region, boundary, target, waypoint, route, or area'
    __occid_model_id__: ClassVar[int] = 111

class Mark(Reference):
    __occid_model_id__: ClassVar[int] = 112

class ReferencePath(Reference):
    __occid_model_id__: ClassVar[int] = 113

class Region(Reference):
    __occid_model_id__: ClassVar[int] = 114

class Boundary(Reference):
    __occid_model_id__: ClassVar[int] = 115

class FlightLevelBand(Region):
    __occid_model_id__: ClassVar[int] = 116
    altitude_range_m: NumericRange
    alt_sep_m: builtins.float

class MissionPoi(Mark):
    __occid_model_id__: ClassVar[int] = 117
    uid: StringID
    name: builtins.str
    pos: GlobalPosition
    origin: builtins.str
    cot: builtins.str | None = None
    added_ts: builtins.float | None = None
    stale_after_s: builtins.float | None = None
    url: builtins.str | None = None

class AutopilotMissionWaypoint(Mark):
    __occid_model_id__: ClassVar[int] = 118
    waypoint_index: builtins.int
    action_code: builtins.int | None = None
    position: GlobalPosition
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None

class PlannerMissionPoint(Mark):
    __occid_model_id__: ClassVar[int] = 119
    num: builtins.int
    point_type: PlannerPointType
    category: PlannerPointCategory
    pos: GlobalPosition

class LoiterOrbit(ReferencePath):
    __occid_model_id__: ClassVar[int] = 120
    orbit_direction: builtins.int
    orbit_radius: builtins.int
    loiter_time: builtins.int

class MissionRouteGeometry(ReferencePath):
    __occid_model_id__: ClassVar[int] = 121
    route_in: GeoPath
    survey: GeoPath
    survey_area: GeoArea
    route_out: GeoPath

class PlannedRoutePoints(ReferencePath):
    __occid_model_id__: ClassVar[int] = 122
    start: PlannerMissionPoint
    route_in: list[PlannerMissionPoint]
    survey: list[PlannerMissionPoint]
    survey_area: list[PlannerMissionPoint]
    route_out: list[PlannerMissionPoint]
    end: PlannerMissionPoint
