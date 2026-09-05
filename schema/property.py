"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Property(OCCIDModel):
    'A generally fixed characteristic, classification, disposition, or capability that defines an object, but is not merely its momentary condition'
    __occid_model_id__: ClassVar[int] = 209
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Attribute', 'Capability', 'Identity', 'Parameter', 'Version', 'FirmwareInfo', 'MetadataValue', 'Relationship')

class Version(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 287
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    major: builtins.int
    minor: builtins.int
    patch: builtins.int

class FirmwareInfo(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 82
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    name: builtins.str
    version: Semantic[Version]
    build: builtins.str | None = None

class MetadataValue(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 158
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MeasurementQuality',)
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: Semantic[Timestamp]
    bool: builtins.bool | None = None
