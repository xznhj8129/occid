"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Lifecycle(OCCIDModel):
    'Current stage in existence or execution.'
    __occid_model_id__: ClassVar[int] = 128
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
