"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .core import Root

### Enums

class Data_type(IntEnum):
    INFORMATION = 0
    SENSORY = auto()

### Models

class Data(Root):
    'Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects'
