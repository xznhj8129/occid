"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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
