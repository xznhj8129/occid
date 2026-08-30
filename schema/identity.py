"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Identity(Property):
    'Identity bindings and identity-related properties'
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class IdentityBootstrap(Identity):
    "Stable Node-centered binding of one deployed Node to the Entity it serves and that Entity's Organization"
    __occid_model_id__: ClassVar[int] = 97
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    node_uid: UID
    node_id: builtins.int
    entity_uid: UID
    entity_id: builtins.int
    organization_uid: UID
    organization_id: builtins.int
