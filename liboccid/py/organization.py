"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain

### Enums

class OrgLevel(IntEnum):
    UNIT = 0
    GROUP = auto()

class OrgType(IntEnum):
    CIV = 0
    COMMERCIAL = auto()
    NGO = auto()
    GOVT = auto()

class OrgTopology(IntEnum):
    NONE = 0
    HIERARCHICAL = auto()
    CELLULAR = auto()
    NETWORKED = auto()

class OrganizationOperationalState(IntEnum):
    UNKNOWN = 0
    FORMING = auto()
    READY = auto()
    ACTIVE = auto()
    DEGRADED = auto()
    REORGANIZING = auto()
    RECONSTITUTING = auto()
    INACTIVE = auto()
    DISBANDED = auto()

class ReadinessLevel(IntEnum):
    UNKNOWN = 0
    UNAVAILABLE = auto()
    LIMITED = auto()
    READY = auto()
    FULL = auto()

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
    COR = auto()
    ARM = auto()
    AGP = auto()
    THR = auto()
    CMD = auto()

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

class OrgLayout(IntEnum):
    FREEFORM = 0
    ORBAT = auto()

class ReinforcementStatus(IntEnum):
    NONE = 0
    REINFORCED = auto()
    REDUCED = auto()
    REINFORCED_REDUCED = auto()

class StrengthCondition(IntEnum):
    UNKNOWN = 0
    FULL = auto()
    SUBSTANTIAL = auto()
    REDUCED = auto()
    SEVERELY_REDUCED = auto()
    INEFFECTIVE = auto()

### Mappings

UNIT_SIZE_LABELS: dict[OOBSize, builtins.str] = {
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
    OOBSize.COR: 'Corps',
    OOBSize.ARM: 'Army',
    OOBSize.AGP: 'Army Group/Front',
    OOBSize.THR: 'Region/Theater',
    OOBSize.CMD: 'Command',
}

UNIT_SIZE_SHORT: dict[OOBSize, builtins.str] = {
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
    OOBSize.COR: 'Corps',
    OOBSize.ARM: 'Army',
    OOBSize.AGP: 'Army Group/Front',
    OOBSize.THR: 'Region/Theater',
    OOBSize.CMD: 'Command',
}

UNIT_CATEGORY_LABELS: dict[NATOUnitCategory, builtins.str] = {
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

UNIT_CATEGORY_NAMES: dict[NATOUnitCategory, builtins.str] = {
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

UNIT_SIZE_LEVELS_LAND: dict[OOBSize, builtins.int] = {
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
    OOBSize.COR: 10,
    OOBSize.ARM: 11,
    OOBSize.AGP: 12,
    OOBSize.THR: 13,
    OOBSize.CMD: 14,
}

UNIT_SIZE_LEVELS_AIR: dict[OOBSize, builtins.int] = {
    OOBSize.IND: 0,
    OOBSize.TEM: 1,
    OOBSize.FLT: 2,
    OOBSize.SQN: 3,
    OOBSize.GRP: 4,
    OOBSize.WNG: 5,
}

CALLSIGN_TEMPLATES: dict[OOBSize, builtins.str] = {
    OOBSize.SQD: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.SEC: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.PLT: '<coy_callsign>-<plt_num>',
    OOBSize.COY: '<coy_callsign>-<btn_num>BTN',
    OOBSize.BTN: '<btn_num>BTN-<rgt_num>RGT',
    OOBSize.RGT: '<rgt_num>RGT-<bde_num>BDE',
    OOBSize.BDE: '<bde_num>BDE',
}

ENEMY_CALLSIGN_TEMPLATES: dict[OOBSize, builtins.str] = {
    OOBSize.SQD: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.SEC: '<coy_callsign>-<plt_num>-<s_num>',
    OOBSize.PLT: '<coy_callsign>-<plt_num>',
    OOBSize.COY: '<coy_callsign>-<btn_num>BTN',
    OOBSize.BTN: '<btn_num>BTN-<rgt_num>RGT',
    OOBSize.RGT: '<rgt_num>RGT-<bde_num>BDE',
    OOBSize.BDE: '<bde_num>BDE',
}

### Models

class Organization(OCCIDModel):
    'A structured collection of organized entities and/or subordinate organizations with common command and control'
    __occid_model_id__: ClassVar[int] = 268
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Set'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Group', 'Unit', 'MilitaryOrg')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None

class Group(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 156
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Organization'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None

class Unit(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 399
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Organization'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel = OrgLevel.UNIT
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None

class OrgTemplate(OCCIDModel):
    'Reusable definition or template for an organization, distinct from a concrete Organization and its changing state'
    __occid_model_id__: ClassVar[int] = 267
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryOrgTemplate',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OrgTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    topology: OrgTopology | None = None
    resource_requirements: list[Semantic[ResourceRequirement]]

class OrgComposition(OCCIDModel):
    'Required or doctrinal quantity of subordinate organizations defined by reusable organization definitions'
    __occid_model_id__: ClassVar[int] = 265
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    org_template_uid: Semantic[UID]
    quantity: Semantic[Count]

class MilitaryOrgTemplate(OCCIDModel):
    'Reusable military organizational definition or template, including doctrinal structure and authorized resources'
    __occid_model_id__: ClassVar[int] = 233
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OrgTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OrgTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    topology: OrgTopology | None = None
    resource_requirements: list[Semantic[ResourceRequirement]]
    category: NATOUnitCategory
    size: OOBSize
    op_domain: OperationalDomain
    tactical_elements: list[Semantic[OrgComposition]]
    support_elements: list[Semantic[OrgComposition]]

class Side(OCCIDModel):
    'Named operational side or alignment grouping; relative friendly/hostile identity is modeled separately from side membership'
    __occid_model_id__: ClassVar[int] = 339
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Set'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Coalition',)
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Side')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    member_uids: list[Semantic[UID]]

class Coalition(OCCIDModel):
    'Operational side composed of multiple organizations or other sides acting together'
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Side'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Side')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    member_uids: list[Semantic[UID]]

class OrgRole(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 266
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    role: Semantic[Role]
    authority: Semantic[Authority]
    assignment: Semantic[Assignment]

class Roster(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 325
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    roster: dict[Semantic[UID], Semantic[OrgRole]]

class OrganizationState(OCCIDModel):
    'Time-indexed mutable organizational condition, membership, location, readiness, holdings, and roster separated from organization identity'
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SubjectState'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryOrganizationState',)
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    position: Semantic[LocationState] | None = None
    operational_status: OrganizationOperationalState | None = None
    readiness: ReadinessLevel | None = None
    inventory: Semantic[InventoryState] | None = None
    health: Semantic[HealthSnapshot] | None = None

class MilitaryOrg(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 232
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Organization'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FlyingOrg', 'OrbatOrg')
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None
    category: NATOUnitCategory | None = None
    resource_requirements: list[Semantic[ResourceRequirement]]

class FlyingOrg(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 126
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MilitaryOrg'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None
    category: NATOUnitCategory
    resource_requirements: list[Semantic[ResourceRequirement]]
    op_domain: OperationalDomain = OperationalDomain.AIR

class OrbatOrg(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MilitaryOrg'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GroundOrbatOrg',)
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_type: OrgType | None = None
    topology: OrgTopology = OrgTopology.HIERARCHICAL
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None
    category: NATOUnitCategory
    resource_requirements: list[Semantic[ResourceRequirement]]
    org_layout: OrgLayout = OrgLayout.ORBAT
    size: OOBSize
    op_domain: OperationalDomain
    taskforce: builtins.bool | None = None
    spacing: Semantic[DistanceMeters]

class GroundOrbatOrg(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 154
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OrbatOrg'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_type: OrgType | None = None
    topology: OrgTopology = OrgTopology.HIERARCHICAL
    definition_uid: Semantic[UID] | None = None
    member_uids: list[Semantic[UID]] | None = None
    roster: Semantic[Roster] | None = None
    category: NATOUnitCategory
    resource_requirements: list[Semantic[ResourceRequirement]]
    org_layout: OrgLayout = OrgLayout.ORBAT
    size: OOBSize
    op_domain: OperationalDomain = OperationalDomain.LAND
    taskforce: builtins.bool | None = None
    spacing: Semantic[DistanceMeters]
    combat_domain: OperationalDomain

class MilitaryStrength(OCCIDModel):
    'Reported qualitative military strength when exact resource holdings are unavailable or inappropriate; exact counts remain ResourceHolding data'
    __occid_model_id__: ClassVar[int] = 236
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    overall: StrengthCondition | None = None
    personnel: StrengthCondition | None = None
    equipment: StrengthCondition | None = None

class MilitaryOrganizationState(OCCIDModel):
    'Military-specific changing organization state layered on generic OrganizationState'
    __occid_model_id__: ClassVar[int] = 234
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OrganizationState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    subject_uid: Semantic[UID]
    timestamp: Semantic[Timestamp]
    position: Semantic[LocationState] | None = None
    operational_status: OrganizationOperationalState | None = None
    readiness: ReadinessLevel | None = None
    inventory: Semantic[InventoryState] | None = None
    health: Semantic[HealthSnapshot] | None = None
    reinforcement_status: ReinforcementStatus | None = None
    strength: Semantic[MilitaryStrength] | None = None
