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
    org_uid: StringID
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    position: GlobalPosition | None = None
    control_level: ControlLevel | None = None
    link_condition: LinkCondition | None = None

class Group(Organization):
    __occid_model_id__: ClassVar[int] = 99
    orglevel: OrgLevel = OrgLevel.GROUP

class Unit(Organization):
    __occid_model_id__: ClassVar[int] = 100
    orglevel: OrgLevel = OrgLevel.UNIT
