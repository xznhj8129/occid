"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Enums

class IdentifierType(IntEnum):
    UNIT_CODE = 0
    CALLSIGN = auto()
    SERIAL_NUMBER = auto()
    DB_ID = auto()
    TRACK_ID = auto()
    ASSET_ID = auto()
    REGISTRATION = auto()

### Models

class Identity(Property):
    'Fundamental identity, name, ID'

class StringID(Identity):
    id_type: IdentifierType
    value: builtins.str

class IntID(Identity):
    id_type: IdentifierType
    value: builtins.int

class HardwareIdentity(Identity):
    hardware_uid: StringID | None = None
    vendor_id: StringID | None = None
    product_id: StringID | None = None
    product_name: builtins.str | None = None
    board_info: StringID | None = None
