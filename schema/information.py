"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class InformationType(IntEnum):
    PROPERTIES = 0
    STATE = auto()
    EVENT = auto()
    INTEL = auto()

### Models

class Information(Data):
    pass
