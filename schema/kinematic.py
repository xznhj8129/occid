"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Kinematic(State):
    'Motion and derived movement state.'

class ImuSample(Kinematic):
    acceleration: LocalVector | None = None
    angular_velocity: AngularVelocityVector | None = None
    magnetic_field: LocalVector | None = None
    temperature_deg_c: builtins.float | None = None
    timestamp_us: builtins.int | None = None
    frame: BodyReferenceFrame | None = None
