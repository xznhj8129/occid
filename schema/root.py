"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class RootFlagExample(IntFlag):
    SOMETHING = 2
    OTHER = 4

### Models

class Root(OCCIDModel):
    'Any distinct part of the overall framework that can be identified, described, or referenced'
    __occid_model_id__: ClassVar[int] = 230
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = None
    __occid_children__: ClassVar[tuple[str, ...]] = ('Communication', 'Control', 'Data', 'Definition', 'Object', 'Struct')
