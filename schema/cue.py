"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Cue(OCCIDModel):
    'Spatial cue toward a target or point of interest, distinct from vehicle guidance, navigation, and control state'
    __occid_model_id__: ClassVar[int] = 52
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_uid: Semantic[UID] | None = None
    target_uid: Semantic[UID] | None = None
    bearing_rad: builtins.float | None = None
    elevation_rad: builtins.float | None = None
    distance_m: builtins.float | None = None
    label: builtins.str | None = None
