"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Enums

class Data_type(IntEnum):
    PROPERTY = 0
    STATE = auto()
    EVENT = auto()
    OBSERVATION = auto()
    MEDIA = auto()

### Models

class Data(Root):
    'Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects'

class Version(Data):
    major: builtins.int
    minor: builtins.int
    patch: builtins.int
