"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class ControlType(IntEnum):
    REASONING = 0
    DIRECTIVE = auto()
    EXECUTION = auto()
    REFERENCE = auto()
    CONSTRAINT = auto()
    INTERFACE = auto()

### Models

class Control(Root):
    pass
