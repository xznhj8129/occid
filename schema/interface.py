"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Interface(OCCIDModel):
    'System or protocol interface through which a component communicates with another endpoint'
    __occid_model_id__: ClassVar[int] = 119
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Communication'
    __occid_children__: ClassVar[tuple[str, ...]] = ('RemoteControl', 'ObserverSource')
