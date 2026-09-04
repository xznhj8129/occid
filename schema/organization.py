"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

### Models

class Organization(OCCIDModel):
    'A structured collection of organized entities and/or subordinate organizations with common command and control'
    __occid_model_id__: ClassVar[int] = 176
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[UID]
    roster: Roster
    leases: list[AttachmentLease]

class Group(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 97
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[UID]
    roster: Roster
    leases: list[AttachmentLease]
    orglevel: OrgLevel = OrgLevel.GROUP

class Unit(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 266
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    org_level: OrgLevel
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[UID]
    roster: Roster
    leases: list[AttachmentLease]
    orglevel: OrgLevel = OrgLevel.UNIT

class OrgRole(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 175
    __occid_semantic_role__: ClassVar[str] = 'representation'
    role: builtins.str
    authority: CommandAuthority | Lease | AttachmentLease | ControlLease
    assignment: Assignment
    rank: builtins.int

class Roster(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 217
    __occid_semantic_role__: ClassVar[str] = 'representation'
    roster: dict[UID, OrgRole]
