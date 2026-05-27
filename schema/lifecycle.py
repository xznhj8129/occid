"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

### Models

class Lifecycle(State):
    'Current stage in existence or execution'

class TaskStatusEntry(Lifecycle):
    ts: float
    status: TaskStatus
    command_result: CommandResult | None = None
    reply_ack: ReplyAck | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase | None = None
    detail: str | None = None
    source: str | None = None
