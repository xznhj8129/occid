"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .data import Data

### Enums

class Property_type(IntEnum):
    IDENTITY = 0
    ATTRIBUTES = auto()
    PARAMETERS = auto()
    RELATIONSHIP = auto()

### Models

class Property(Data):
    'Mostly stable identity, attribute, configuration, classification, display, provenance, and relationship data'

class FeaturePropertyValue(Property):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class FeatureProperty(Property):
    key: str
    value: FeaturePropertyValue

class Attributes(Property):
    'Fundamental characteristics, type, form'

class MetadataValue(Attributes):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class MetadataEntry(Attributes):
    key: str
    value: MetadataValue

class SymbologySchema(Attributes):
    sidc: str | None = None
    cot: str | None = None

class DisplayMeta(Attributes):
    icon_code: str | None = None
    tint: str | None = None
    short_label: str | None = None

class ClassificationSchema(Attributes):
    level: ClassificationLevel
    codewords: list[str]
    release_to: list[str]

class SensorFieldOfView(Attributes):
    horizontal: NumericRange | None = None
    vertical: NumericRange | None = None

class Identity(Property):
    'Fundamental identity, name, ID'

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

class Relationship(Property):
    'Nature of relations, ownership, provenance, link'

class RelationSchema(Relationship):
    src_id: str
    dst_id: str
    rel_kind: str
    since_ts: float | None = None
    until_ts: float | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None

class EntityComponentRef(Relationship):
    component_id: str
    component_type: str | None = None
    label: str | None = None
