"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Parameter(OCCIDModel):
    'Current operating configuration or control regime'
    __occid_model_id__: ClassVar[int] = 190
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VideoConfig', 'ReceiverConfig', 'ChannelMapEntry', 'ModeRange', 'RobotController')
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
