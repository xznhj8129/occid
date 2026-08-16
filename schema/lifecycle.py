"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Lifecycle(State):
    'Current stage in existence or execution.'
    __occid_model_id__: ClassVar[int] = 164
    __occid_semantic_role__: ClassVar[str] = 'specialization'
