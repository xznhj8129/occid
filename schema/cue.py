"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Cue(State):
    'Spatial cue toward a target or point of interest, distinct from vehicle guidance, navigation, and control state'
    __occid_model_id__: ClassVar[int] = 322
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    source_id: UID | None = None
    target_id: UID | None = None
    bearing_rad: builtins.float | None = None
    elevation_rad: builtins.float | None = None
    distance_m: builtins.float | None = None
    label: builtins.str | None = None
