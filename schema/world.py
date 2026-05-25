"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .object import Collection, Object

### Enums

class World_type(IntEnum):
    FEATURE = 0
    LOCATION = auto()
    SITE = auto()

### Models

class World(Object):
    pass

class Feature(World):
    pass

class Location(World):
    pass

class Site(World):
    pass

class GeoJsonFeature(Feature):
    type: Literal['Feature'] = Field(default='Feature', frozen=True)
    geometry: GeoJsonGeometry
    properties: list[FeatureProperty]
    id: (str | int) | None = None
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(Collection):
    type: Literal['FeatureCollection'] = Field(default='FeatureCollection', frozen=True)
    features: list[GeoJsonFeature]
    bbox: BoundingBox | None = None
