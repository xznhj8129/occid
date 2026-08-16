"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .radio import RadioProfile

### Models

class MilitaryRadioProfile(RadioProfile):
    __occid_model_id__: ClassVar[int] = 232
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    bands: list[NATORadioBands]
