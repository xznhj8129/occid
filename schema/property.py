"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class MetadataValue(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 145
    __occid_semantic_role__: ClassVar[str] = 'representation'
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: builtins.float | None = None
    bool: builtins.bool | None = None
