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
    __occid_model_id__: ClassVar[int] = 173
    __occid_semantic_role__: ClassVar[str] = 'type'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None

class Group(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 96
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None

class Unit(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 260
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Organization')]
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    orglevel: OrgLevel = OrgLevel.UNIT
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
