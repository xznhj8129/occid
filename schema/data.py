"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .root import Root

### Models

class Data(Root):
    'Concrete typed structures describing objects, their characteristics, condition, intentions, actions, or effects'
    __occid_model_id__: ClassVar[int] = 3

class Version(Data):
    __occid_model_id__: ClassVar[int] = 4
    major: builtins.int
    minor: builtins.int
    patch: builtins.int
