"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class Root_type(IntEnum):
    DEFINITION = 0
    STRUCT = auto()
    OBJECT = auto()
    CONTROL = auto()
    COMMUNICATION = auto()
    DATA = auto()

### Models

class Root(OCCIDModel):
    pass
