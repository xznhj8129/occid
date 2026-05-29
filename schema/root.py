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
    __occid_model_id__: ClassVar[int] = 0
