"""Generated from core/schemav2."""
from __future__ import annotations
from enum import IntEnum as _StdIntEnum, IntEnum, auto, Enum
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field

SchemaVersion = tuple[int, int, int]

### Enums

class IntEnum(_StdIntEnum):
    @classmethod
    def _missing_(cls, value):
        if type(value) == str:
            return cls[value]
        return super()._missing_(value)

class ConfidenceLevel(IntEnum):
    UNKNOWN = 0
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CONFIRMED = auto()

class OperationalDomain(IntEnum):
    LAND = 0
    AIR = auto()
    SEA = auto()
    SUB = auto()
    SPACE = auto()
    CYBER = auto()
    ALL = auto()

class EffectDomain(IntEnum):
    LAND = 0
    AIR = auto()
    SEA = auto()
    SUB = auto()
    SPACE = auto()
    CYBER = auto()
    ALL = auto()

class SchemaKind(IntEnum):
    BASIC_UNIT = 0
    GROUND_ORG = auto()
    AIR_ORG = auto()
    AIR_UNIT = auto()
    GROUND_UNIT = auto()
    INTEL_TRACK = auto()
    LINK = auto()
    SENSOR = auto()
    INSTALLATION = auto()

class Faction(IntEnum):
    UNKNOWN = 0
    PENDING = auto()
    FRIENDLY = auto()
    SUSPECT = auto()
    HOSTILE = auto()
    NEUTRAL = auto()
    ASSUMED = auto()
    FAKER = auto()
    JOKER = auto()

class AlternateIdType(IntEnum):
    TRACK_ID = 0
    ASSET_ID = auto()
    CALLSIGN = auto()
    SERIAL_NUMBER = auto()
    REGISTRATION = auto()
    UNIT_CODE = auto()
    TRACK_NUMBER = auto()
    JU_NUMBER = auto()

class PriorityLevel(IntEnum):
    LOW = 0
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()

class PropulsionType(IntEnum):
    FOOT = 0
    WHEELED = auto()
    TRACKED = auto()
    ROTARY_WING = auto()
    FIXED_WING = auto()
    JET = auto()
    MARITIME = auto()
    STATIC = auto()

class NavigationMode(IntEnum):
    MANUAL = 0
    INS = auto()
    GNSS = auto()
    INS_GNSS = auto()
    VISUAL = auto()
    TERRAIN_FOLLOW = auto()

class FuelType(IntEnum):
    GASOLINE = 0
    DIESEL = auto()
    HEAVY_FUEL = auto()
    JET_FUEL = auto()
    BATTERY = auto()
    HYBRID = auto()

### Mappings

SIDC_FACTION: dict[str, str] = {
    'UNKNOWN': 'U',
    'PENDING': 'P',
    'FRIENDLY': 'F',
    'SUSPECT': 'S',
    'HOSTILE': 'H',
    'NEUTRAL': 'N',
}

SIDC_DOMAIN: dict[str, str] = {
    'ground': 'G',
    'air': 'A',
    'sea': 'S',
    'sub': 'U',
}

SIDC_STATUS: dict[str, str] = {
    'anticipated': 'A',
    'present': 'P',
    'present-capable': 'C',
    'present-damaged': 'D',
    'present-destroyed': 'X',
}

SIDC_AIR_A5: dict[str, str] = {
    'track': '-',
    'military': 'M',
    'civilian': 'C',
}

SIDC_AIR_A6: dict[str, str] = {
    'fixed-wing': 'F',
    'rotary': 'H',
    'weapon': 'W',
}

SIDC_AIR_MILITARY: dict[str, str] = {
    'fighter': 'F',
    'attack': 'A',
    'bomber': 'B',
    'utility': 'U',
    'drone': 'Q',
    'missile': 'M',
    'decoy': 'D',
    'recon': 'R',
    'ecm': 'J',
}

SIDC_GROUND_A5: dict[str, str] = {
    'track': '-',
    'unit': 'U',
}

SIDC_GROUND_A6: dict[str, str] = {
    'combat': 'C',
    'combat-support': 'U',
    'service-support': 'S',
}

SIDC_COMBAT_GROUND: dict[str, str] = {
    'air-defence': 'D',
    'armor': 'A',
    'ssm': 'M',
    'artillery': 'F',
    'infantry': 'I',
    'anti-tank': 'A',
    'recon': 'R',
    'hq': 'H',
    'engineer': 'E',
}

SIDC_COMBAT_GROUND_INFANTRY: dict[str, str] = {
    'light': 'L',
    'motorized': 'M',
    'mechanized': 'Z',
    'ifv': 'I',
    'air-assault': 'A',
}

SIDC_AIR_WEAPON_MISSILE: dict[str, str] = {
    'ssm': 'S*APWMSS----',
    'sam': 'S*APWMSA----',
    'aam': 'S*APWMAA----',
    'asm': 'S*APWMAS----',
    'land-attack': 'S*APWML----',
}

SIDC_GROUND_ARTILLERY: dict[str, str] = {
    'spg': 'S*GPUCFHE---',
    'light_towed': 'S*GPUCFHL---',
    'medium_towed': 'S*GPUCFHM---',
    'heavy_towed': 'S*GPUCFHH---',
    'sp_mrl': 'S*GPUCFRMS--',
    'towed_mortar': 'S*GPUCFMT---',
    'ssm': 'S*GPUCMMT---',
}

SIDC_UNIT_SIZE: dict[str, str] = {
    'single': '-',
    'team': 'A',
    'squad': 'B',
    'section': 'C',
    'platoon': 'D',
    'company': 'E',
    'battalion': 'F',
    'regiment': 'G',
    'brigade': 'H',
    'division': 'H',
}

SIDC_CODES: dict[str, Any] = {
    'friendly': {'land': {'default': 'S*GP--------', 'unit': 'S*GPUC------', 'infantry': 'S*GPUCI-----', 'armor': 'S*GPUCA-----', 'recon': 'S*GPUCR-----', 'artillery': 'S*GPUCF-----', 'hq': 'S*GPUH----A-', 'tfhq': 'S*GPUH----B-', 'tf': 'S*GPUH----E-'}, 'air': {'default': 'S*APM-------'}},
    'hostile': {'land': {'default': 'SHGPU-------'}, 'air': {'default': 'SHAPM-------'}},
}

### Models

class OCCIDModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    def model_dump(self, *, mode="python", **kwargs):
        def encode(value):
            if type(value) == dict:
                return {key: encode(item) for key, item in value.items()}
            if type(value) in (list, tuple):
                return [encode(item) for item in value]
            if issubclass(type(value), IntEnum):
                return value.name
            if issubclass(type(value), Enum):
                return value.value
            return value

        if mode == "json":
            data = super().model_dump(mode="python", **kwargs)
            return encode(data)
        data = super().model_dump(mode=mode, **kwargs)
        return data

class Time(SigmaModel):
    utime: int

class Duration(SigmaModel):
    ms: float | None = None
    seconds: float | None = None
    minutes: float | None = None
    hours: float | None = None
    days: float | None = None
    weeks: float | None = None
    months: float | None = None
    years: float | None = None

class Timestamp(SigmaModel):
    ms: float
    seconds: float
    minutes: float
    hours: float
    day: float
    month: float
    year: float
    tz: float

class AlternateId(SigmaModel):
    id_type: AlternateIdType
    value: str

class ItemCount(SigmaModel):
    item_type: str
    qty: int = '0'

class NumericRange(SigmaModel):
    min_value: float | None = None
    max_value: float | None = None

class MetadataValue(SigmaModel):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class MetadataEntry(SigmaModel):
    key: str
    value: MetadataValue

class SymbologySchema(SigmaModel):
    sidc: str | None = None
    cot: str | None = None

class FirmwareInfo(SigmaModel):
    name: str | None = None
    version: str | None = None
    build: str | None = None

class FuelState(SigmaModel):
    fuel_type: FuelType
    capacity: float | None = None
    remaining: float | None = None
    burn_rate_per_hour: float | None = None

class SuppliesSchema(SigmaModel):
    fuel: FuelState | None = None
    stores: list[ItemCount] = Field(default_factory=list)
