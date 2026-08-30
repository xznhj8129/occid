"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .object import Set

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

class Organization(Set):
    'A structured collection of organized entities and/or subordinate organizations with common command and control'
    __occid_model_id__: ClassVar[int] = 98
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    record: RecordMeta
    org_uid: UID
    organization_number: builtins.int | None = None
    name: builtins.str | None = None
    unit_code: builtins.str | None = None
    callsign: builtins.str | None = None
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None

class Group(Organization):
    __occid_model_id__: ClassVar[int] = 99
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    orglevel: OrgLevel = OrgLevel.GROUP

class Unit(Organization):
    __occid_model_id__: ClassVar[int] = 100
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    orglevel: OrgLevel = OrgLevel.UNIT
