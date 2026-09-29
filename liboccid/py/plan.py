"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class PlanApprovalState(IntEnum):
    DRAFT = 0
    PROPOSED = auto()
    APPROVED = auto()
    REJECTED = auto()
    SUPERSEDED = auto()

class PlanStepStatus(IntEnum):
    PENDING = 0
    READY = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    FAILED = auto()
    SKIPPED = auto()

class WaypointRole(IntEnum):
    HOME = 0
    TAKEOFF = auto()
    LANDING = auto()
    HOLD = auto()
    WAYPOINT = auto()
    ASSEMBLY = auto()
    POI = auto()
    ROI = auto()
    SURVEY = auto()
    INGRESS = auto()
    EGRESS = auto()

class OrbitPattern(IntEnum):
    CIRCLE = 0
    RACETRACK = auto()
    FIGURE_EIGHT = auto()

### Models

class Plan(OCCIDModel):
    'Proposed or approved method for accomplishing one or more tasks using actors, resources, sequencing, routes, constraints, and contingencies'
    __occid_model_id__: ClassVar[int] = 245
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('OperationalPlan', 'RoutePlan')
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class OperationalPlan(OCCIDModel):
    'Task-based'
    __occid_model_id__: ClassVar[int] = 228
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    objective_uids: list[Semantic[ID]]
    task_uids: list[Semantic[ID]]
    actor_uids: list[Semantic[ID]]
    resource_uids: list[Semantic[ID]]
    assignment_uids: list[Semantic[ID]]
    constraints: list[Semantic[Constraint]]
    contingencies: list[Semantic[PlanContingency]]

class RoutePlan(OCCIDModel):
    'Plan of routed movement along an ordered sequence of movement points'
    __occid_model_id__: ClassVar[int] = 284
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GroupFlightPlan',)
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    waypoints: list[Semantic[Waypoint]]

class Waypoint(OCCIDModel):
    'A point of movement on a route, with its role and movement constraints'
    __occid_model_id__: ClassVar[int] = 365
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    position: Semantic[GlobalPosition]
    role: WaypointRole = WaypointRole.WAYPOINT
    capture_radius: Semantic[DistanceMeters] | None = None
    hold_time: Semantic[Duration] | None = None
    heading_rad: builtins.float | None = None
    speed_ms: builtins.float | None = None
    velocity: Semantic[VelocityVector] | None = None
    orbit: Semantic[LoiterOrbit] | None = None
    area: Semantic[GeoArea] | None = None

class LoiterOrbit(OCCIDModel):
    'Embedded orbit geometry and timing value'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    orbit_direction_ccw: builtins.bool
    orbit_radius: Semantic[DistanceMeters]
    loiter_time: Semantic[Duration]
    pattern: OrbitPattern

class PlanContingency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition]
    task_uids: list[Semantic[ID]]
