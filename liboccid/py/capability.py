"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Capability(OCCIDModel):
    'An ability an Object possesses or can provide; concrete capability schemas define the specific semantics and parameters'
    __occid_model_id__: ClassVar[int] = 41
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MediaProductionCapability',)

class MediaProductionCapability(OCCIDModel):
    'Ability of an Object to originate media in the declared modalities'
    __occid_model_id__: ClassVar[int] = 216
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Capability'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    content_types: list[MediaSpectrum]
