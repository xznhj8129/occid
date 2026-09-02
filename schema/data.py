"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Version(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 266
    __occid_semantic_role__: ClassVar[str] = 'representation'
    major: builtins.int
    minor: builtins.int
    patch: builtins.int
