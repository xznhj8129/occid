"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Cue(OCCIDModel):
    'Spatial cue toward a target or point of interest, distinct from vehicle guidance, navigation, and control state'
    __occid_model_id__: ClassVar[int] = 47
    __occid_semantic_role__: ClassVar[str] = 'type'
    source_uid: UID | None = None
    target_uid: UID | None = None
    bearing_rad: builtins.float | None = None
    elevation_rad: builtins.float | None = None
    distance_m: builtins.float | None = None
    label: builtins.str | None = None
