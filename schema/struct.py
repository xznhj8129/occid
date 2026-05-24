"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Models

class Time(OCCIDModel):
    utime: int

class Duration(OCCIDModel):
    ms: float | None = None
    seconds: float | None = None
    minutes: float | None = None
    hours: float | None = None
    days: float | None = None
    weeks: float | None = None
    months: float | None = None
    years: float | None = None

class Timestamp(OCCIDModel):
    ms: float
    seconds: float
    minutes: float
    hours: float
    day: float
    month: float
    year: float
    tz: float

class AlternateId(OCCIDModel):
    id_type: AlternateIdType
    value: str

class ItemCount(OCCIDModel):
    item_type: str
    qty: int = 0

class NumericRange(OCCIDModel):
    min_value: float | None = None
    max_value: float | None = None

class MetadataValue(OCCIDModel):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class MetadataEntry(OCCIDModel):
    key: str
    value: MetadataValue

class SymbologySchema(OCCIDModel):
    sidc: str | None = None
    cot: str | None = None

class FirmwareInfo(OCCIDModel):
    name: str | None = None
    version: str | None = None
    build: str | None = None

class FuelState(OCCIDModel):
    fuel_type: FuelType
    capacity: float | None = None
    remaining: float | None = None

class SuppliesSchema(OCCIDModel):
    fuel: FuelState | None = None
    stores: list[ItemCount]

class DisplayMeta(OCCIDModel):
    icon_code: str | None = None
    tint: str | None = None
    short_label: str | None = None

class RelationSchema(OCCIDModel):
    src_id: str
    dst_id: str
    rel_kind: str
    since_ts: float | None = None
    until_ts: float | None = None
    confidence: ConfidenceLevel | None = None
    source: str | None = None
