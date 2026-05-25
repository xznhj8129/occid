"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .objects import BaseObject, ObjectType

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

class BaseOrg(BaseObject):
    org_uid: str
    object_type: ObjectType = ObjectType.ORGANIZATION
    orglevel: OrgLevel = OrgLevel.GROUP
    org_type: OrgType | None = None
    topology: OrgTopology | None = None
    position: GlobalPosition | None = None
    control_level: ControlLevel | None = None
    link_condition: LinkCondition | None = None
