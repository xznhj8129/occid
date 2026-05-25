"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

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
