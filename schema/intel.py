"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .information import Information

### Enums

class Intel_type(IntEnum):
    DETECTION = 0
    CLASSIFICATION = auto()
    TRACK = auto()
    ASSESSMENT = auto()

### Models

class Intel(Information):
    pass

class Classification(Intel):
    pass

class Track(Intel):
    pass

class Assessment(Intel):
    pass
