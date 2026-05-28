"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Lifecycle(State):
    'Current stage in existence or execution.'

class TaskStatusEntry(Lifecycle):
    ts: builtins.float
    status: TaskStatus
    command_result: CommandResult | None = None
    reply_ack: ReplyAck | None = None
    assign_fail: TaskAssignFail | None = None
    phase: TaskPhase | None = None
    detail: builtins.str | None = None
    source: builtins.str | None = None
