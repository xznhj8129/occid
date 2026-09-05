"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Attribute(OCCIDModel):
    'Fundamental characteristics, type, form'
    __occid_model_id__: ClassVar[int] = 15
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Symbology', 'DisplayMeta', 'GroundNavigation', 'AirNavigation', 'SensorFieldOfView')

class Symbology(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 254
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    sidc: builtins.str | None = None
    cot: builtins.str | None = None

class DisplayMeta(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 63
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Attribute'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    icon_code: builtins.str | None = None
    tint: builtins.str | None = None
    short_label: builtins.str | None = None
