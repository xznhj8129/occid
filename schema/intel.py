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
    'Effect-side data that something happened or changed external to the sender object'

class Classification(Intel):
    pass

class Track(Intel):
    pass

class Assessment(Intel):
    pass
