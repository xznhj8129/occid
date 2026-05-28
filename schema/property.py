"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Enums

class Property_type(IntEnum):
    IDENTITY = 0
    ATTRIBUTE = auto()
    PARAMETER = auto()
    RELATIONSHIP = auto()

### Models

class Property(Data):
    'A generally fixed characteristic, classification, disposition, or capability that defines an object, but is not merely its momentary condition'

class MetadataValue(Property):
    str: builtins.str | None = None
    int: builtins.int | None = None
    float: builtins.float | None = None
    bool: builtins.bool | None = None
