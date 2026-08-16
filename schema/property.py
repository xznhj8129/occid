"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Models

class Property(Data):
    'A generally fixed characteristic, classification, disposition, or capability that defines an object, but is not merely its momentary condition'
    __occid_model_id__: ClassVar[int] = 101
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class MetadataValue(Property):
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: builtins.float | None = None
    bool: builtins.bool | None = None
