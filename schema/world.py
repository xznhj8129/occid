"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .objects import Collection, Feature

### Models

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
