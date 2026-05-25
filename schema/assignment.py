"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import Assignment, Lifecycle

### Models

class TaskDelta(Assignment):
    task_id: str
    task_rev: int = 0
    phase: TaskPhase
    progress: float | None = None
    owner: str | None = None
    updated_ts: float

class FlightAssignment(Assignment):
    num: int
    unit_id: str | None = None
    callsign: str | None = None
    objective_assign: int | None = None
    wave_n: int = 0
    formation_n: int = 0
    takeoff_time: float = 0.0

class TaskStatusEntry(Lifecycle):
    ts: float
    status: TaskStatus
    command_result: CommandResult | None = None
    reply_ack: ReplyAck | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase | None = None
    detail: str | None = None
    source: str | None = None
