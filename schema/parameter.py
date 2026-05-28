"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Parameter(Property):
    'Current operating configuration or control regime'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
