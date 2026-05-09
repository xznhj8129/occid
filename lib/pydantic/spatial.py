"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

class InertialReferenceFrame(IntEnum):
    NEU = 0
    NED = auto()
    ENU = auto()

class BodyReferenceFrame(IntEnum):
    FLU = 0
    FRD = auto()

class AltitudeDatum(IntEnum):
    RELATIVE = 0
    SEA_LEVEL = auto()
    TERRAIN = auto()
    POI_RELATIVE = auto()
    BAROMETRIC = auto()
    INVALID = auto()

class GeometryTypes(IntEnum):
    POINT = 0
    MULTI_POINT = auto()
    LINE_STRING = auto()
    MULTI_LINE_STRING = auto()
    POLYGON = auto()
    MULTI_POLYGON = auto()
    GEOMETRY_COLLECTION = auto()

class GeoJsonGeometryTypes(str, Enum):
    POINT = 'Point'
    MULTI_POINT = 'MultiPoint'
    LINE_STRING = 'LineString'
    MULTI_LINE_STRING = 'MultiLineString'
    POLYGON = 'Polygon'
    MULTI_POLYGON = 'MultiPolygon'
    GEOMETRY_COLLECTION = 'GeometryCollection'

class SurfaceFormationShapes(IntEnum):
    COLUMN = 0
    LINE = auto()
    SCREEN = auto()
    WEDGE = auto()
    LOZENGE = auto()
    CIRCLE = auto()
    SQUARE = auto()

class FormationForm(IntEnum):
    PERIMETER = 0
    FILL = auto()

class RouteLeg(IntEnum):
    UNDEFINED = 0
    OUTBOUND = auto()
    RETURN = auto()

class RouteMethod(IntEnum):
    WALKING = 0
    DRIVING = auto()
    FLYING = auto()
    SWIMMING = auto()
    WATERCRAFT = auto()

class RouteType(IntEnum):
    PRIMARY = 0
    SECONDARY = auto()

class WaypointType(IntEnum):
    GLOBAL = 0
    LOCAL = auto()
    OBJECT = auto()

class NavAids(IntEnum):
    NONE = 0
    GNSS = auto()
    INS = auto()
    TERRAIN_MATCH = auto()
    CELESTIAL = auto()
    VISUAL = auto()

### Models

class EulerAngles(SigmaModel):
    pitch: float | None = None
    heading: float | None = None
    roll: float | None = None
    frame: BodyReferenceFrame | None = None

class LocalDirection(SigmaModel):
    bearing: float | None = None
    azimuth: float | None = None
    elevation: float | None = None
    slant_range: float | None = None

class LocalVector(SigmaModel):
    x: float | None = None
    y: float | None = None
    z: float | None = None
    frame: InertialReferenceFrame | None = None

class GlobalPosition(SigmaModel):
    lat: float | None = None
    lon: float | None = None
    alt: float | None = None
    mgrs: str | None = None
    datum: Literal['"WGS84"'] = Field(default='"WGS84"', frozen=True)
    alt_frame: AltitudeDatum | None = None

class GeoPath(SigmaModel):
    points: list[GlobalPosition] = Field(default_factory=list)

class GeoArea(SigmaModel):
    vertices: list[GlobalPosition] = Field(default_factory=list)

class BoundingBox(SigmaModel):
    x1: float | None = None
    y1: float | None = None
    z1: float | None = None
    x2: float | None = None
    y2: float | None = None
    z2: float | None = None

class VelocityVector(SigmaModel):
    x: float | None = None
    y: float | None = None
    z: float | None = None

class FeaturePropertyValue(SigmaModel):
    text_value: str | None = None
    int_value: int | None = None
    float_value: float | None = None
    bool_value: bool | None = None

class FeatureProperty(SigmaModel):
    key: str
    value: FeaturePropertyValue

class GeoJsonGeometry(SigmaModel):
    type: GeoJsonGeometryTypes
    coordinates: Any | None = None
    geometries: list[GeoJsonGeometry] | None = None
    bbox: BoundingBox | None = None

class GeoJsonFeature(SigmaModel):
    type: Literal['"Feature"'] = Field(default='"Feature"', frozen=True)
    geometry: GeoJsonGeometry
    properties: list[FeatureProperty] = Field(default_factory=list)
    id: (str | int) | None = None
    bbox: BoundingBox | None = None

class GeoJsonFeatureCollection(SigmaModel):
    type: Literal['"FeatureCollection"'] = Field(default='"FeatureCollection"', frozen=True)
    features: list[GeoJsonFeature] = Field(default_factory=list)
    bbox: BoundingBox | None = None

class LocationUncertainty(SigmaModel):
    horiz_err_m: float | None = None
    vert_err_m: float | None = None
    ellipse_major_m: float | None = None
    ellipse_minor_m: float | None = None
    ellipse_bearing_deg: float | None = None

class LocationState(SigmaModel):
    inertial_frame: InertialReferenceFrame | None = None
    body_frame: BodyReferenceFrame | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    attitude: EulerAngles | None = None
