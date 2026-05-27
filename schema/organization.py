"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .objects import ObjectType, Set

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

class Organization_type(IntEnum):
    GROUP = 0
    UNIT = auto()
    MILITARY_ORG = auto()

### Models

class Organization(Set):
    'A structured collection of organized entities and/or subordinate organizations with common command and control'
    org_uid: str
    object_type: ObjectType = ObjectType.ORGANIZATION
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    position: GlobalPosition | None = None
    control_level: ControlLevel | None = None
    link_condition: LinkCondition | None = None

class Group(Organization):
    orglevel: OrgLevel = OrgLevel.GROUP

class Unit(Organization):
    orglevel: OrgLevel = OrgLevel.UNIT
