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
    __occid_model_id__: ClassVar[int] = 189
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
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[Semantic[UID]]
    roster: Semantic[Roster]
    leases: list[Semantic[AttachmentLease]]

class Group(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 106
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
    org_level: OrgLevel
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[Semantic[UID]]
    roster: Semantic[Roster]
    leases: list[Semantic[AttachmentLease]]
    orglevel: OrgLevel = OrgLevel.GROUP

class Unit(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 281
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
    org_level: OrgLevel
    org_rank: builtins.int
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    elements: list[Semantic[UID]]
    roster: Semantic[Roster]
    leases: list[Semantic[AttachmentLease]]
    orglevel: OrgLevel = OrgLevel.UNIT

class OrgRole(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 188
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    role: builtins.str
    authority: Semantic[Authority]
    assignment: Semantic[Assignment]
    rank: builtins.int

class Roster(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 231
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    roster: dict[Semantic[UID], Semantic[OrgRole]]
