"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Attribute(OCCIDModel):
    'Fundamental characteristics, type, form'
    __occid_model_id__: ClassVar[int] = 15
    __occid_semantic_role__: ClassVar[str] = 'type'

class Symbology(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 236
    __occid_semantic_role__: ClassVar[str] = 'representation'
    sidc: builtins.str | None = None
    cot: builtins.str | None = None

class DisplayMeta(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 55
    __occid_semantic_role__: ClassVar[str] = 'representation'
    icon_code: builtins.str | None = None
    tint: builtins.str | None = None
    short_label: builtins.str | None = None
