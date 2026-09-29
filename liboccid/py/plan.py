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

### Models

class Plan(OCCIDModel):
    'Proposed or approved method for accomplishing one or more tasks using actors, resources, sequencing, routes, constraints, and contingencies'
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AirPlan', 'OperationalPlan', 'RoutePlan')
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class OperationalPlan(OCCIDModel):
    'Task-based'
    __occid_model_id__: ClassVar[int] = 229
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
    'Plan of routed movement along waypoints or routes'
    __occid_model_id__: ClassVar[int] = 287
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Plan'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AutopilotMission',)
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class PlanContingency(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 247
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    condition: Semantic[Condition]
    task_uids: list[Semantic[ID]]

class AutopilotMission(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 27
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RoutePlan'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT
    waypoints: list[Semantic[AutopilotMissionWaypoint]]

class AutopilotMissionWaypoint(OCCIDModel):
    'Embedded autopilot waypoint value used by a plan or protocol mapping'
    __occid_model_id__: ClassVar[int] = 29
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialStruct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlightMissionPoint',)
    waypoint_index: builtins.int
    position: Semantic[GlobalPosition]
    action_code: builtins.int | None = None
    param1: builtins.int | None = None
    param2: builtins.int | None = None
    param3: builtins.int | None = None
    flag: builtins.int | None = None
