"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Attribute(Property):
    'Fundamental characteristics, type, form'
    __occid_model_id__: ClassVar[int] = 133
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class SymbologySchema(Attribute):
    __occid_model_id__: ClassVar[int] = 134
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    sidc: builtins.str | None = None
    cot: builtins.str | None = None

class DisplayMeta(Attribute):
    __occid_model_id__: ClassVar[int] = 135
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    icon_code: builtins.str | None = None
    tint: builtins.str | None = None
    short_label: builtins.str | None = None
