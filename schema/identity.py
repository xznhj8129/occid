"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Identity(OCCIDModel):
    'Identity bindings and identity-related properties'
    __occid_model_id__: ClassVar[int] = 104
    __occid_semantic_role__: ClassVar[str] = 'type'

class StringName(OCCIDValue[builtins.str]):
    'Human-readable reference for something'
    __occid_model_id__: ClassVar[int] = 233
    __occid_semantic_role__: ClassVar[str] = 'representation'

class IdentityBootstrap(OCCIDModel):
    "Stable Node-centered binding of one deployed Node to the Entity it serves and that Entity's Organization"
    __occid_model_id__: ClassVar[int] = 105
    __occid_semantic_role__: ClassVar[str] = 'representation'
    node_uid: UID
    node_id: Annotated[IntID, IDNamespace('Node')]
    entity_uid: UID
    entity_id: Annotated[IntID, IDNamespace('Entity')]
    organization_uid: UID
    organization_id: Annotated[IntID, IDNamespace('Organization')]
