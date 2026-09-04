"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
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
    WGS84_ELLIPSOID = auto()

class GeometryTypes(IntEnum):
    POINT = 0
    MULTI_POINT = auto()
    LINE_STRING = auto()
    MULTI_LINE_STRING = auto()
    POLYGON = auto()
    MULTI_POLYGON = auto()
    GEOMETRY_COLLECTION = auto()

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

class Position(OCCIDModel):
    'Position in space, address or placement'
    __occid_model_id__: ClassVar[int] = 190
    __occid_semantic_role__: ClassVar[str] = 'type'

class SpatialStruct(OCCIDModel):
    'Spatial struct support models'
    __occid_model_id__: ClassVar[int] = 226
    __occid_semantic_role__: ClassVar[str] = 'representation'

class EulerAngles(OCCIDModel):
    'Euler attitude in radians; frame metadata is optional in the record but consumers performing transforms or control must require the frames they depend on'
    __occid_model_id__: ClassVar[int] = 68
    __occid_semantic_role__: ClassVar[str] = 'representation'
    roll_rad: builtins.float
    pitch_rad: builtins.float
    yaw_rad: builtins.float
    body_frame: BodyReferenceFrame | None = None
    reference_frame: InertialReferenceFrame | None = None

class LocalDirection(OCCIDModel):
    'Local bearing/azimuth/elevation angles in radians; slant_range is an optional distance in meters when range is known'
    __occid_model_id__: ClassVar[int] = 126
    __occid_semantic_role__: ClassVar[str] = 'representation'
    bearing: builtins.float
    azimuth: builtins.float
    elevation: builtins.float
    slant_range: builtins.float | None = None

class LocalVector(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 128
    __occid_semantic_role__: ClassVar[str] = 'representation'
    x: builtins.float
    y: builtins.float
    z: builtins.float
    frame: InertialReferenceFrame

class GlobalPosition(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 90
    __occid_semantic_role__: ClassVar[str] = 'representation'
    lat: builtins.float
    lon: builtins.float
    alt: builtins.float
    mgrs: builtins.str | None = None
    datum: Literal['WGS84'] = Field(default='WGS84', frozen=True)
    alt_frame: AltitudeDatum

class GeoPath(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 87
    __occid_semantic_role__: ClassVar[str] = 'representation'
    points: list[GlobalPosition]

class GeoArea(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 86
    __occid_semantic_role__: ClassVar[str] = 'representation'
    vertices: list[GlobalPosition]

class BoundingBox(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 24
    __occid_semantic_role__: ClassVar[str] = 'representation'
    x1: builtins.float
    y1: builtins.float
    z1: builtins.float
    x2: builtins.float
    y2: builtins.float
    z2: builtins.float

class VelocityVector(OCCIDModel):
    'Linear velocity with optional explicit inertial reference frame'
    __occid_model_id__: ClassVar[int] = 268
    __occid_semantic_role__: ClassVar[str] = 'representation'
    x: builtins.float
    y: builtins.float
    z: builtins.float
    frame: InertialReferenceFrame | None = None

class AngularVelocityVector(OCCIDModel):
    'Body angular velocity in radians per second with optional explicit body frame'
    __occid_model_id__: ClassVar[int] = 10
    __occid_semantic_role__: ClassVar[str] = 'representation'
    x_rad_s: builtins.float
    y_rad_s: builtins.float
    z_rad_s: builtins.float
    frame: BodyReferenceFrame | None = None

class AltitudeState(OCCIDModel):
    'Simultaneous altitude observations must carry their own vertical reference; absolute and relative values never share one ambiguous datum'
    __occid_model_id__: ClassVar[int] = 9
    __occid_semantic_role__: ClassVar[str] = 'representation'
    absolute_m: builtins.float | None = None
    absolute_datum: AltitudeDatum | None = None
    relative_m: builtins.float | None = None
    relative_datum: AltitudeDatum | None = None

class LocationUncertainty(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 131
    __occid_semantic_role__: ClassVar[str] = 'representation'
    horiz_err_m: builtins.float | None = None
    vert_err_m: builtins.float | None = None
    ellipse_major_m: builtins.float | None = None
    ellipse_minor_m: builtins.float | None = None
    ellipse_bearing_deg: builtins.float | None = None

class LocationState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 130
    __occid_semantic_role__: ClassVar[str] = 'representation'
    inertial_frame: InertialReferenceFrame | None = None
    body_frame: BodyReferenceFrame | None = None
    position: GlobalPosition | None = None
    local_position: LocalVector | None = None
    uncertainty: LocationUncertainty | None = None
    attitude: EulerAngles | None = None
    altitude: AltitudeState | None = None
    velocity: VelocityVector | None = None
    navigation_validity: NavigationValidity | None = None
    gnss: GnssSolution | None = None

class SpotterOrigin(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 228
    __occid_semantic_role__: ClassVar[str] = 'representation'
    position: GlobalPosition
    attitude: EulerAngles | None = None
    look_vector: LocalDirection | None = None
