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
    'A discrete occurrence — something that happened at a point in time, whether planned or not'

class FlightEvent(Event):
    pass

class MissionEvent(Event):
    pass
