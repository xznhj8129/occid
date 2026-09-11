"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class SymbologyStandard(IntEnum):
    MIL_STD_2525D = 0
    MIL_STD_2525E = auto()
    APP_6D = auto()

class StandardIdentity(IntEnum):
    PENDING = 0
    UNKNOWN = auto()
    ASSUMED_FRIEND = auto()
    FRIEND = auto()
    NEUTRAL = auto()
    SUSPECT = auto()
    HOSTILE = auto()
    JOKER = auto()
    FAKER = auto()

### Mappings

SIDC_FACTION: dict[builtins.str, builtins.str] = {
    'UNKNOWN': 'U',
    'PENDING': 'P',
    'FRIENDLY': 'F',
    'SUSPECT': 'S',
    'HOSTILE': 'H',
    'NEUTRAL': 'N',
}

SIDC_DOMAIN: dict[builtins.str, builtins.str] = {
    'ground': 'G',
    'air': 'A',
    'sea': 'S',
    'sub': 'U',
}

SIDC_STATUS: dict[builtins.str, builtins.str] = {
    'anticipated': 'A',
    'present': 'P',
    'present-capable': 'C',
    'present-damaged': 'D',
    'present-destroyed': 'X',
}

SIDC_AIR_A5: dict[builtins.str, builtins.str] = {
    'track': '-',
    'military': 'M',
    'civilian': 'C',
}

SIDC_AIR_A6: dict[builtins.str, builtins.str] = {
    'fixed-wing': 'F',
    'rotary': 'H',
    'weapon': 'W',
}

SIDC_AIR_MILITARY: dict[builtins.str, builtins.str] = {
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

SIDC_GROUND_A5: dict[builtins.str, builtins.str] = {
    'track': '-',
    'unit': 'U',
}

SIDC_GROUND_A6: dict[builtins.str, builtins.str] = {
    'combat': 'C',
    'combat-support': 'U',
    'service-support': 'S',
}

SIDC_COMBAT_GROUND: dict[builtins.str, builtins.str] = {
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

SIDC_COMBAT_GROUND_INFANTRY: dict[builtins.str, builtins.str] = {
    'light': 'L',
    'motorized': 'M',
    'mechanized': 'Z',
    'ifv': 'I',
    'air-assault': 'A',
}

SIDC_AIR_WEAPON_MISSILE: dict[builtins.str, builtins.str] = {
    'ssm': 'S*APWMSS----',
    'sam': 'S*APWMSA----',
    'aam': 'S*APWMAA----',
    'asm': 'S*APWMAS----',
    'land-attack': 'S*APWML----',
}

SIDC_GROUND_ARTILLERY: dict[builtins.str, builtins.str] = {
    'spg': 'S*GPUCFHE---',
    'light_towed': 'S*GPUCFHL---',
    'medium_towed': 'S*GPUCFHM---',
    'heavy_towed': 'S*GPUCFHH---',
    'sp_mrl': 'S*GPUCFRMS--',
    'towed_mortar': 'S*GPUCFMT---',
    'ssm': 'S*GPUCMMT---',
}

SIDC_UNIT_SIZE: dict[builtins.str, builtins.str] = {
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

SIDC_CODES: dict[builtins.str, Any] = {
    'friendly': {'land': {'default': 'S*GP--------', 'unit': 'S*GPUC------', 'infantry': 'S*GPUCI-----', 'armor': 'S*GPUCA-----', 'recon': 'S*GPUCR-----', 'artillery': 'S*GPUCF-----', 'hq': 'S*GPUH----A-', 'tfhq': 'S*GPUH----B-', 'tf': 'S*GPUH----E-'}, 'air': {'default': 'S*APM-------'}},
    'hostile': {'land': {'default': 'SHGPU-------'}, 'air': {'default': 'SHAPM-------'}},
}

### Models

class Attribute(OCCIDModel):
    'Fundamental characteristics, type, form'
    __occid_model_id__: ClassVar[int] = 26
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Symbology', 'GroundNavigation', 'AirNavigation', 'SensorFieldOfView')

class Symbology(OCCIDModel):
    'Semantic family for symbolic codings associated with an operational subject; concrete standards are represented by children'
    __occid_model_id__: ClassVar[int] = 364
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ('CoTSymbology', 'MilitarySymbology')

class CoTSymbology(OCCIDModel):
    'Cursor-on-Target symbolic type coding retained as an explicit external-standard representation'
    __occid_model_id__: ClassVar[int] = 50
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Symbology'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    cot: builtins.str

class SIDC(OCCIDModel):
    'Standard identity and symbol code encoded according to an explicitly declared military symbology standard'
    __occid_model_id__: ClassVar[int] = 331
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    value: builtins.str
    standard: SymbologyStandard

class MilitarySymbology(OCCIDModel):
    'Military symbolic coding of an operational subject'
    __occid_model_id__: ClassVar[int] = 239
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Symbology'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    sidc: Semantic[SIDC]
