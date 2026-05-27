"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .organization import OrgTopology, Organization

### Enums

class OOBSize(IntEnum):
    IND = 0
    TEM = auto()
    SQD = auto()
    SEC = auto()
    PLT = auto()
    COY = auto()
    BTN = auto()
    RGT = auto()
    BDE = auto()
    DIV = auto()
    FLT = auto()
    SQN = auto()
    GRP = auto()
    WNG = auto()

class OOBSizeLabel(str, Enum):
    IND = 'Individual'
    TEM = 'Team'
    SQD = 'Squad'
    SEC = 'Section'
    PLT = 'Platoon'
    COY = 'Company'
    BTN = 'Battalion'
    RGT = 'Regiment'
    BDE = 'Brigade'
    DIV = 'Division'
    FLT = 'Flight'
    SQN = 'Squadron'
    GRP = 'Group'
    WNG = 'Wing'

class NATOUnitCategory(IntEnum):
    COMB = 0
    BATT = auto()
    TF = auto()
    MECH = auto()
    INF = auto()
    MOT = auto()
    REC = auto()
    UAV = auto()
    UAVA = auto()
    UAVR = auto()
    UGV = auto()
    SIG = auto()
    ENG = auto()
    ART = auto()
    MORT = auto()
    MRL = auto()
    ARM = auto()
    CAV = auto()
    MED = auto()
    SUP = auto()
    LOG = auto()
    HQ = auto()
    NBC = auto()
    MP = auto()
    AIR = auto()
    SOF = auto()
    NAV = auto()
    AMP = auto()
    ADA = auto()
    EW = auto()
    ISR = auto()
    CBT = auto()
    CSS = auto()
    COM = auto()
    DET = auto()
    RES = auto()
    TRG = auto()

class NATOUnitCategoryLabel(str, Enum):
    COMB = 'Combined Arms'
    BATT = 'Battery'
    TF = 'Task Force'
    MECH = 'Mechanized Infantry'
    INF = 'Light Infantry'
    MOT = 'Motorized Infantry'
    REC = 'Reconnaissance'
    UAV = 'Unmanned Aerial Systems'
    UAVA = 'UAV Attack'
    UAVR = 'UAV Recon'
    UGV = 'Unmanned Ground Systems'
    SIG = 'Signal'
    ENG = 'Engineer'
    ART = 'Artillery'
    MORT = 'Mortar'
    MRL = 'Rocket Artillery'
    ARM = 'Armored'
    CAV = 'Cavalry'
    MED = 'Medical'
    SUP = 'Supply'
    LOG = 'Logistics'
    HQ = 'Headquarters'
    NBC = 'Nuclear, Biological, and Chemical Defense'
    MP = 'Military Police'
    AIR = 'Airborne Infantry'
    SOF = 'Special Operations Forces'
    NAV = 'Naval Infantry'
    AMP = 'Amphibious Infantry'
    ADA = 'Air Defense Artillery'
    EW = 'Electronic Warfare'
    ISR = 'Intelligence, Surveillance, and Reconnaissance'
    CBT = 'Combat Support'
    CSS = 'Combat Service Support'
    COM = 'Command'
    DET = 'Detachment'
    RES = 'Reserve'
    TRG = 'Training'

class OrgLayout(IntEnum):
    FREEFORM = 0
    ORBAT = auto()

class MilitaryOrg_type(IntEnum):
    FLYING_ORG = 0
    ORBAT_ORG = auto()

class OrbatOrg_type(IntEnum):
    GROUND = 0

### Mappings

UNIT_SIZE_LABELS: dict[OOBSize, str] = {
    OOBSize.IND: 'Individual',
    OOBSize.TEM: 'Team',
    OOBSize.SQD: 'Squad',
    OOBSize.SEC: 'Section',
    OOBSize.PLT: 'Platoon',
    OOBSize.COY: 'Company',
    OOBSize.BTN: 'Battalion',
    OOBSize.RGT: 'Regiment',
    OOBSize.BDE: 'Brigade',
    OOBSize.DIV: 'Division',
    OOBSize.FLT: 'Flight',
    OOBSize.SQN: 'Squadron',
    OOBSize.GRP: 'Group',
    OOBSize.WNG: 'Wing',
}

UNIT_SIZE_SHORT: dict[OOBSize, str] = {
    OOBSize.IND: 'Individual',
    OOBSize.TEM: 'Team',
    OOBSize.SQD: 'Squad',
    OOBSize.SEC: 'Section',
    OOBSize.PLT: 'Platoon',
    OOBSize.COY: 'Company',
    OOBSize.BTN: 'Battalion',
    OOBSize.RGT: 'Regiment',
    OOBSize.BDE: 'Brigade',
    OOBSize.DIV: 'Division',
    OOBSize.FLT: 'Flight',
    OOBSize.SQN: 'Squadron',
    OOBSize.GRP: 'Group',
    OOBSize.WNG: 'Wing',
}

UNIT_CATEGORY_LABELS: dict[NATOUnitCategory, str] = {
    NATOUnitCategory.COMB: 'Combined Arms',
    NATOUnitCategory.BATT: 'Battery',
    NATOUnitCategory.TF: 'Task Force',
    NATOUnitCategory.MECH: 'Mechanized Infantry',
    NATOUnitCategory.INF: 'Light Infantry',
    NATOUnitCategory.MOT: 'Motorized Infantry',
    NATOUnitCategory.REC: 'Reconnaissance',
    NATOUnitCategory.UAV: 'Unmanned Aerial Systems',
    NATOUnitCategory.UAVA: 'UAV Attack',
    NATOUnitCategory.UAVR: 'UAV Recon',
    NATOUnitCategory.UGV: 'Unmanned Ground Systems',
    NATOUnitCategory.SIG: 'Signal',
    NATOUnitCategory.ENG: 'Engineer',
    NATOUnitCategory.ART: 'Artillery',
    NATOUnitCategory.MORT: 'Mortar',
    NATOUnitCategory.MRL: 'Rocket Artillery',
    NATOUnitCategory.ARM: 'Armored',
    NATOUnitCategory.CAV: 'Cavalry',
    NATOUnitCategory.MED: 'Medical',
    NATOUnitCategory.SUP: 'Supply',
    NATOUnitCategory.LOG: 'Logistics',
    NATOUnitCategory.HQ: 'Headquarters',
    NATOUnitCategory.NBC: 'Nuclear, Biological, and Chemical Defense',
    NATOUnitCategory.MP: 'Military Police',
    NATOUnitCategory.AIR: 'Airborne Infantry',
    NATOUnitCategory.SOF: 'Special Operations Forces',
    NATOUnitCategory.NAV: 'Naval Infantry',
    NATOUnitCategory.AMP: 'Amphibious Infantry',
    NATOUnitCategory.ADA: 'Air Defense Artillery',
    NATOUnitCategory.EW: 'Electronic Warfare',
    NATOUnitCategory.ISR: 'Intelligence, Surveillance, and Reconnaissance',
    NATOUnitCategory.CBT: 'Combat Support',
    NATOUnitCategory.CSS: 'Combat Service Support',
    NATOUnitCategory.COM: 'Command',
    NATOUnitCategory.DET: 'Detachment',
    NATOUnitCategory.RES: 'Reserve',
    NATOUnitCategory.TRG: 'Training',
}

UNIT_CATEGORY_NAMES: dict[NATOUnitCategory, str] = {
    NATOUnitCategory.COMB: 'Combined Arms',
    NATOUnitCategory.BATT: 'Battery',
    NATOUnitCategory.TF: 'Task Force',
    NATOUnitCategory.MECH: 'Mechanized Infantry',
    NATOUnitCategory.INF: 'Light Infantry',
    NATOUnitCategory.MOT: 'Motorized Infantry',
    NATOUnitCategory.REC: 'Reconnaissance',
    NATOUnitCategory.UAV: 'Unmanned Aerial Systems',
    NATOUnitCategory.UAVA: 'UAV Attack',
    NATOUnitCategory.UAVR: 'UAV Recon',
    NATOUnitCategory.UGV: 'Unmanned Ground Systems',
    NATOUnitCategory.SIG: 'Signal',
    NATOUnitCategory.ENG: 'Engineer',
    NATOUnitCategory.ART: 'Artillery',
    NATOUnitCategory.MORT: 'Mortar',
    NATOUnitCategory.MRL: 'Rocket Artillery',
    NATOUnitCategory.ARM: 'Armored',
    NATOUnitCategory.CAV: 'Cavalry',
    NATOUnitCategory.MED: 'Medical',
    NATOUnitCategory.SUP: 'Supply',
    NATOUnitCategory.LOG: 'Logistics',
    NATOUnitCategory.HQ: 'Headquarters',
    NATOUnitCategory.NBC: 'Nuclear, Biological, and Chemical Defense',
    NATOUnitCategory.MP: 'Military Police',
    NATOUnitCategory.AIR: 'Airborne Infantry',
    NATOUnitCategory.SOF: 'Special Operations Forces',
    NATOUnitCategory.NAV: 'Naval Infantry',
    NATOUnitCategory.AMP: 'Amphibious Infantry',
    NATOUnitCategory.ADA: 'Air Defense Artillery',
    NATOUnitCategory.EW: 'Electronic Warfare',
    NATOUnitCategory.ISR: 'Intelligence, Surveillance, and Reconnaissance',
    NATOUnitCategory.CBT: 'Combat Support',
    NATOUnitCategory.CSS: 'Combat Service Support',
    NATOUnitCategory.COM: 'Command',
    NATOUnitCategory.DET: 'Detachment',
    NATOUnitCategory.RES: 'Reserve',
    NATOUnitCategory.TRG: 'Training',
}

UNIT_SIZE_LEVELS_LAND: dict[OOBSize, int] = {
    OOBSize.IND: 0,
    OOBSize.TEM: 1,
    OOBSize.SQD: 2,
    OOBSize.SEC: 3,
    OOBSize.PLT: 4,
    OOBSize.COY: 5,
    OOBSize.BTN: 6,
    OOBSize.RGT: 7,
    OOBSize.BDE: 8,
    OOBSize.DIV: 9,
}

UNIT_SIZE_LEVELS_AIR: dict[OOBSize, int] = {
    OOBSize.IND: 0,
    OOBSize.TEM: 1,
    OOBSize.FLT: 2,
    OOBSize.SQN: 3,
    OOBSize.GRP: 4,
    OOBSize.WNG: 5,
}

CALLSIGN_TEMPLATES: dict[OOBSize, str] = {
    OOBSize.SQD: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.SEC: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.PLT: '<coy_callsign>-<plt_num>',
    OOBSize.COY: '<coy_callsign>-<btn_num>BTN',
    OOBSize.BTN: '<btn_num>BTN-<rgt_num>RGT',
    OOBSize.RGT: '<rgt_num>RGT-<bde_num>BDE',
    OOBSize.BDE: '<bde_num>BDE',
}

ENEMY_CALLSIGN_TEMPLATES: dict[OOBSize, str] = {
    OOBSize.SQD: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.SEC: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.PLT: '<coy_callsign>-<plt_num>',
    OOBSize.COY: '<coy_callsign>-<btn_num>BTN',
    OOBSize.BTN: '<btn_num>BTN-<rgt_num>RGT',
    OOBSize.RGT: '<rgt_num>RGT-<bde_num>BDE',
    OOBSize.BDE: '<bde_num>BDE',
}

### Models

class OrgComposition(OCCIDModel):
    category: NATOUnitCategory | None = None
    label: str | None = None
    qty: int = 0

class MilitaryOrg(Organization):
    sidc: str | None = None
    category: NATOUnitCategory | None = None
    link_loadout: list[ItemCount]

class FlyingOrg(MilitaryOrg):
    category: NATOUnitCategory
    op_domain: OperationalDomain = OperationalDomain.AIR
    air_units: list[ItemCount]

class OrbatOrg(MilitaryOrg):
    org_layout: OrgLayout = OrgLayout.ORBAT
    topology: OrgTopology = OrgTopology.HIERARCHICAL
    category: NATOUnitCategory
    size: OOBSize
    op_domain: OperationalDomain
    taskforce: bool | None = None
    links: dict[str, LinkSchema]
    tac_elements: list[OrgComposition]
    sup_elements: list[OrgComposition]
    tac_e_comp: list[ItemCount]
    sup_e_comp: list[ItemCount]
    personnel: list[ItemCount]
    vehicles: list[ItemCount]
    equipment: list[ItemCount]
    spacing: float = 0.0

class GroundOrbatOrg(OrbatOrg):
    category: NATOUnitCategory
    op_domain: OperationalDomain = OperationalDomain.LAND
    combat_domain: OperationalDomain
    ammo: list[ItemCount]
    weapons: list[ItemCount]
    air_units: list[ItemCount]
