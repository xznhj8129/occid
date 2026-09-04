"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Version(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'representation'
    major: builtins.int
    minor: builtins.int
    patch: builtins.int

class FirmwareInfo(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 73
    __occid_semantic_role__: ClassVar[str] = 'representation'
    name: builtins.str
    version: Version
    build: builtins.str | None = None

class MetadataValue(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 146
    __occid_semantic_role__: ClassVar[str] = 'representation'
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: Timestamp
    bool: builtins.bool | None = None
