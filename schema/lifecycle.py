"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import AckMode, ConflictPolicy, DeliveryState, QosTier, RouteMode
from .state import State

### Models

class Lifecycle(State):
    'Current stage in existence or execution.'
    __occid_model_id__: ClassVar[int] = 161

class TaskAssignment(Lifecycle):
    __occid_model_id__: ClassVar[int] = 162
    task_id: StringID
    ts: builtins.float
    status: TaskStatus
    unit_code: builtins.str | None = None
    capability: Capability | None = None
    command_result: CommandResult | None = None
    reply_ack: ReplyAck | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase | None = None
    geometry_id: StringID | None = None
    remarks: builtins.str | None = None
    last_update: builtins.float | None = None
    issued_by: builtins.str | None = None
    accepted_by: builtins.str | None = None
    assigned_assets: list[builtins.str]
    attempt_idx: builtins.int = 0
    dispatch_state: DeliveryState = DeliveryState.QUEUED
    dispatch_error: builtins.str | None = None
    time_window: TaskTimeWindow | None = None
    qos: QosTier = QosTier.ROUTINE
    ack_mode: AckMode = AckMode.RECEIPT
    route_mode: RouteMode = RouteMode.DIRECT
    conflict_policy: ConflictPolicy = ConflictPolicy.VECTOR_CLOCK
    objective: Objective | None = None
    detail: builtins.str | None = None
    source: builtins.str | None = None
