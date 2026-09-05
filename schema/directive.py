"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Directive(OCCIDModel):
    'Directed work or an immediate imperative issued under control authority'
    __occid_model_id__: ClassVar[int] = 62
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Control'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Command', 'Task')
