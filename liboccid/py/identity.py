"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Identity(OCCIDModel):
    'Identity bindings and identity-related properties'
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('StringName', 'IdentityBootstrap')

class StringName(OCCIDValue[builtins.str]):
    'Human-readable reference for something'
    __occid_model_id__: ClassVar[int] = 312
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Identity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class IdentityBootstrap(OCCIDModel):
    "Stable Node-centered binding of one deployed Node to the Entity it serves and that Entity's Organization"
    __occid_model_id__: ClassVar[int] = 149
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Identity'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    node_uid: Semantic[ID]
    entity_uid: Semantic[ID]
    organization_uid: Semantic[ID]
