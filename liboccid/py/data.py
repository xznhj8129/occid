"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Data(OCCIDModel):
    'Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects'
    __occid_model_id__: ClassVar[int] = 77
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Root'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Condition', 'Context', 'Event', 'Execution', 'SpatialMeasurement', 'Media', 'Observation', 'Property', 'Representation', 'State')
