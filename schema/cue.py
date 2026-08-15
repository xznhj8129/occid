"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Cue(State):
    'Directional cue toward a target or point of interest, distinct from vehicle guidance, navigation, and control state'
    __occid_model_id__: ClassVar[int] = 322
    source_id: StringID | None = None
    target_id: StringID | None = None
    bearing_rad: builtins.float
    elevation_rad: builtins.float | None = None
    distance_m: builtins.float | None = None
    label: builtins.str | None = None
