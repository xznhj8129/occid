"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .information import Information

### Enums

class Event_type(IntEnum):
    FLIGHT = 0
    MISSION = auto()

### Models

class Event(Information):
    pass

class FlightEvent(Event):
    pass

class MissionEvent(Event):
    pass
