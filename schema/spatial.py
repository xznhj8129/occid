"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State
from .struct import Bearing, Bounding, GeoPos, Measurement, Pose, Shape, Struct, StructPath, Uncertainty, Vector

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

### Models

class SpatialStruct(Struct):
    'Spatial struct support models'

class EulerAngles(Pose):
    pitch: builtins.float
    heading: builtins.float
    roll: builtins.float
    frame: BodyReferenceFrame

class LocalDirection(Bearing):
    bearing: builtins.float
    azimuth: builtins.float
    elevation: builtins.float
    slant_range: builtins.float

class LocalVector(Vector):
    x: builtins.float
    y: builtins.float
    z: builtins.float
    frame: InertialReferenceFrame

class GlobalPosition(GeoPos):
    lat: builtins.float
    lon: builtins.float
    alt: builtins.float
    mgrs: builtins.str | None = None
    datum: Literal['WGS84'] = Field(default='WGS84', frozen=True)
    alt_frame: AltitudeDatum

class GeoPath(StructPath):
    points: list[GlobalPosition]

class GeoArea(Shape):
    vertices: list[GlobalPosition]

class BoundingBox(Bounding):
    x1: builtins.float
    y1: builtins.float
    z1: builtins.float
    x2: builtins.float
    y2: builtins.float
    z2: builtins.float

class VelocityVector(Vector):
    x: builtins.float
    y: builtins.float
    z: builtins.float

class AngularVelocityVector(Vector):
    x_rad_s: builtins.float
    y_rad_s: builtins.float
    z_rad_s: builtins.float
    frame: BodyReferenceFrame

class AltitudeState(Measurement):
    absolute_m: builtins.float | None = None
    relative_m: builtins.float | None = None
    datum: AltitudeDatum

class LocationUncertainty(Uncertainty):
    horiz_err_m: builtins.float | None = None
    vert_err_m: builtins.float | None = None
    ellipse_major_m: builtins.float | None = None
    ellipse_minor_m: builtins.float | None = None
    ellipse_bearing_deg: builtins.float | None = None

class GeoJsonGeometry(Shape):
    type: GeoJsonGeometryTypes
    coordinates: Any | None = None
    geometries: list[GeoJsonGeometry] | None = None
    bbox: BoundingBox | None = None

class Position(State):
    'Position in space, address or placement'

class LocationState(Position):
    inertial_frame: InertialReferenceFrame | None = None
    body_frame: BodyReferenceFrame | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    attitude: EulerAngles | None = None
    altitude: AltitudeState | None = None
    velocity: VelocityVector | None = None
    navigation_validity: NavigationValidity | None = None
    gnss: GnssSolution | None = None

class SpotterOrigin(Position):
    position: GlobalPosition
    attitude: EulerAngles | None = None
    look_vector: LocalDirection | None = None
