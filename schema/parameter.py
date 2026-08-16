"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Parameter(Property):
    'Current operating configuration or control regime'
    __occid_model_id__: ClassVar[int] = 171
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
