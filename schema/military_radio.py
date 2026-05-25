"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .radio import RadioProfile

### Models

class MilitaryRadioProfile(RadioProfile):
    bands: list[NATORadioBands]
