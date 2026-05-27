"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class ClassificationLevel(IntEnum):
    UNCLASSIFIED = 0
    CONTROLLED = auto()
    CONFIDENTIAL = auto()
    SECRET = auto()
    TOP_SECRET = auto()

class IdentifierType(IntEnum):
    UNIT_CODE = 0
    CALLSIGN = auto()
    SERIAL_NUMBER = auto()
    DB_ID = auto()
    TRACK_ID = auto()
    ASSET_ID = auto()
    REGISTRATION = auto()

class DetectionBoxSpace(IntEnum):
    IMAGE_PIXEL = 0
    IMAGE_NORMALIZED = auto()
    BODY_ANGULAR = auto()
    WORLD = auto()

class MediaType(IntEnum):
    IMAGE = 0
    VIDEO = auto()
    AUDIO = auto()
    DOCUMENT = auto()
    BINARY = auto()

class PowerStatus(IntEnum):
    UNKNOWN = 0
    NOT_PRESENT = auto()
    OPERATING = auto()
    DISABLED = auto()
    ERROR = auto()

class PowerType(IntEnum):
    UNKNOWN = 0
    GAS = auto()
    BATTERY = auto()
    SOLAR = auto()
    NUCLEAR = auto()

class Data_type(IntEnum):
    PROPERTY = 0
    STATE = auto()
    EVENT = auto()
    OBSERVATION = auto()
    MEDIA = auto()
    EFFECT = auto()

### Models

class Data(Root):
    'Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects'

class Version(Data):
    major: int
    minor: int
    patch: int
