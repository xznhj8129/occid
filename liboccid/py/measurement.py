"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class BearingReference(IntEnum):
    TRUE_NORTH = 0
    MAGNETIC_NORTH = auto()
    GRID_NORTH = auto()

### Models

class SpatialMeasurement(OCCIDModel):
    'Persisted spatial measurement whose measured quantity is distinct from any graphic used to display it'
    __occid_model_id__: ClassVar[int] = 297
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('DistanceMeasurement', 'AreaMeasurement', 'BearingMeasurement', 'RadiusMeasurement', 'RouteMeasurement')
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None

class DistanceMeasurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 79
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialMeasurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None
    origin_uid: Semantic[ID]
    target_uid: Semantic[ID]
    distance: Semantic[DistanceMeters]

class AreaMeasurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialMeasurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None
    location_uid: Semantic[ID]
    area: Semantic[AreaSquareMeters]

class BearingMeasurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 29
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialMeasurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None
    origin_uid: Semantic[ID]
    target_uid: Semantic[ID]
    bearing: Semantic[AngleDegrees]
    reference: BearingReference

class RadiusMeasurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialMeasurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None
    center_uid: Semantic[ID]
    radius: Semantic[DistanceMeters]

class RouteMeasurement(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 283
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpatialMeasurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[ID]
    name: builtins.str | None = None
    measured_ts: Semantic[Timestamp] | None = None
    path_uid: Semantic[ID]
    distance: Semantic[DistanceMeters]
