"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .properties import Identity

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

class Identifier(Identity):
    id_type: IdentifierType
    value: str

class HardwareIdentity(Identity):
    hardware_uid: str | None = None
    legacy_uid: str | None = None
    vendor_id: int | None = None
    vendor_name: str | None = None
    product_id: int | None = None
    product_name: str | None = None
    board_info: str | None = None

class FlightControllerIdentity(Identity):
    api_version: Version
    controller_variant: str | None = None
    hardware: HardwareIdentity | None = None
    flight_software: FirmwareInfo | None = None
    os_software: FirmwareInfo | None = None
