"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class Control_type(IntEnum):
    REASONING = 0
    DIRECTIVE = auto()
    EXECUTION = auto()
    REFERENCE = auto()
    CONSTRAINT = auto()
    INTERFACE = auto()

### Models

class Control(Root):
    'Scale-invariant; the binding of agents to objectives through structured decomposition'
