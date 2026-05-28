"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Assignment(State):
    'Current task, owner, control lease, objective binding, dispatch state, phase, and status log.'

class TaskDelta(Assignment):
    task_id: StringID
    task_rev: builtins.int = 0
    phase: TaskPhase
    progress: builtins.float | None = None
    owner: builtins.str | None = None
    updated_ts: builtins.float

class FlightAssignment(Assignment):
    num: builtins.int
    unit_id: StringID | None = None
    callsign: builtins.str | None = None
    objective_assign: builtins.int | None = None
    wave_n: builtins.int = 0
    formation_n: builtins.int = 0
    takeoff_time: builtins.float = 0.0
