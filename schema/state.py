"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class State_type(IntEnum):
    KINEMATIC = 0
    INTERNAL = auto()
    POSITION = auto()
    GUIDANCE = auto()
    SENSOR = auto()
    INPUT = auto()
    RESOURCES = auto()
    CONDITION = auto()
    LIFECYCLE = auto()
    ASSIGNMENT = auto()

### Models

class State(Data):
    'Changing condition of an object, node, link, task, system, or process'
