"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Control(OCCIDModel):
    'Desired outcomes and directed work'
    __occid_model_id__: ClassVar[int] = 44
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Assignment', 'Authority', 'Constraint', 'Directive', 'Objective', 'Plan', 'OrgRole', 'Roster')
