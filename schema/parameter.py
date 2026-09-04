"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Parameter(OCCIDModel):
    'Current operating configuration or control regime'
    __occid_model_id__: ClassVar[int] = 177
    __occid_semantic_role__: ClassVar[str] = 'type'
    key: builtins.str | None = None
    value: MetadataValue | None = None
