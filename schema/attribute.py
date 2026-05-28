"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .property import Property

### Models

class Attribute(Property):
    'Fundamental characteristics, type, form'

class SymbologySchema(Attribute):
    sidc: builtins.str | None = None
    cot: builtins.str | None = None

class DisplayMeta(Attribute):
    icon_code: builtins.str | None = None
    tint: builtins.str | None = None
    short_label: builtins.str | None = None
