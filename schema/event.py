"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class Event_type(IntEnum):
    FLIGHT = 0
    MISSION = auto()

### Models

class Event(Data):
    'A discrete occurrence, planned or unplanned, with subject, source, time, type, and event data'

class FlightEvent(Event):
    pass

class MissionEvent(Event):
    pass
