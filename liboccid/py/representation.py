"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class GraphicLengthUnit(IntEnum):
    PIXEL = 0
    METER = auto()

class StrokePattern(IntEnum):
    SOLID = 0
    DASHED = auto()
    DOTTED = auto()
    DASH_DOT = auto()

class FillPattern(IntEnum):
    NONE = 0
    SOLID = auto()
    DIAGONAL = auto()
    CROSSHATCH = auto()
    DOTS = auto()

class TextAlignment(IntEnum):
    LEFT = 0
    CENTER = auto()
    RIGHT = auto()

class RepresentationFormat(IntEnum):
    GEOJSON = 0
    KML = auto()
    KMZ = auto()
    GPX = auto()
    MILX = auto()
    PMTILES = auto()
    MAPBUNDLE = auto()
    TILEJSON = auto()
    XYZ_TILES = auto()
    VECTOR_TILES = auto()
    RASTER_IMAGE = auto()

class Hemisphere(IntEnum):
    NORTH = 0
    SOUTH = auto()

### Models

class Representation(OCCIDModel):
    'An authored or shared depiction, presentation, organization, or view of operational information; representation changes do not alter the represented subject itself'
    __occid_model_id__: ClassVar[int] = 304
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IdentifiedRepresentation',)

class IdentifiedRepresentation(OCCIDModel):
    'Persisted shared representation with durable OCCID identity, distinct from transient renderer or session state'
    __occid_model_id__: ClassVar[int] = 162
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Representation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Graphic', 'Layer', 'MapView')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class ColorComponent(OCCIDModel):
    'Component of a declared graphic color value'
    __occid_model_id__: ClassVar[int] = 52
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ColorChannel',)

class ColorChannel(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 51
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ColorComponent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Opacity(OCCIDValue[builtins.float]):
    'Graphic opacity ratio where zero is fully transparent and one is fully opaque'
    __occid_model_id__: ClassVar[int] = 252
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Ratio'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ColorRGBA(OCCIDModel):
    'Device-independent sRGB color components used for authored graphic portrayal'
    __occid_model_id__: ClassVar[int] = 53
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    red: Semantic[ColorChannel]
    green: Semantic[ColorChannel]
    blue: Semantic[ColorChannel]
    alpha: Semantic[Opacity] | None = None

class GraphicLength(OCCIDModel):
    'Length used by a graphic portrayal, explicitly distinguishing screen-space and world-space values'
    __occid_model_id__: ClassVar[int] = 147
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    value: builtins.float
    unit: GraphicLengthUnit

class StrokeStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 345
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    width: Semantic[GraphicLength] | None = None
    pattern: StrokePattern | None = None

class FillStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    pattern: FillPattern | None = None

class TextStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 376
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    background: Semantic[ColorRGBA] | None = None
    size: Semantic[GraphicLength] | None = None
    alignment: TextAlignment | None = None

class GraphicStyle(OCCIDModel):
    'Renderer-independent authored portrayal of a graphic'
    __occid_model_id__: ClassVar[int] = 148
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    stroke: Semantic[StrokeStyle] | None = None
    fill: Semantic[FillStyle] | None = None
    text: Semantic[TextStyle] | None = None

class AnnotationAnchor(OCCIDModel):
    'Semantic anchor for an annotation graphic'
    __occid_model_id__: ClassVar[int] = 17
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('PositionAnchor', 'SubjectAnchor', 'PathAnchor')

class PositionAnchor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 282
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    position: Semantic[GlobalPosition]

class SubjectAnchor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 348
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[UID]

class PathAnchor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 266
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    path_uid: Semantic[UID]
    distance_from_start: Semantic[DistanceMeters]

class RepresentationSource(OCCIDModel):
    'Source used to construct a reference or data representation'
    __occid_model_id__: ClassVar[int] = 305
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ExternalRepresentationSource', 'MediaRepresentationSource')

class ExternalRepresentationSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 115
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RepresentationSource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uri: builtins.str
    format: RepresentationFormat

class MediaRepresentationSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 214
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RepresentationSource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    media_uid: Semantic[UID]
    registration: Semantic[GeoArea] | None = None

class Graphic(OCCIDModel):
    'Persisted graphical representation of one or more operational subjects or spatial constructs'
    __occid_model_id__: ClassVar[int] = 146
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'IdentifiedRepresentation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GeometryGraphic', 'SymbolGraphic', 'AnnotationGraphic', 'GeoreferencedMediaGraphic', 'MeasurementGraphic', 'TacticalGraphic')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None

class GeometryGraphic(OCCIDModel):
    'Graphic portrayal of an identified Location; the underlying geometry remains on the Location rather than on the graphic style object'
    __occid_model_id__: ClassVar[int] = 142
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    location_uid: Semantic[UID]

class SymbolGraphic(OCCIDModel):
    'Symbolic portrayal of an identified operational subject at a geographic position using a declared symbology'
    __occid_model_id__: ClassVar[int] = 355
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    subject_uid: Semantic[UID]
    position: Semantic[GlobalPosition]
    symbology: Semantic[Symbology]

class AnnotationGraphic(OCCIDModel):
    'Human-authored annotation anchored to space or another operational object'
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TextGraphic', 'MediaGraphic')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    anchor: Semantic[AnnotationAnchor]

class TextGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 375
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationGraphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    anchor: Semantic[AnnotationAnchor]
    text: Semantic[PlainText]

class MediaGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 211
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationGraphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    anchor: Semantic[AnnotationAnchor]
    media_uid: Semantic[UID]

class GeoreferencedMediaGraphic(OCCIDModel):
    'Graphic portrayal of media registered directly to geographic space'
    __occid_model_id__: ClassVar[int] = 143
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    media_uid: Semantic[UID]
    registration: Semantic[GeoArea]

class MeasurementGraphic(OCCIDModel):
    'Graphic portrayal of a semantic measurement object; the measurement result is not encoded in the graphic itself'
    __occid_model_id__: ClassVar[int] = 208
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    measurement_uid: Semantic[UID]

class Layer(OCCIDModel):
    'Shared organization of representations; visibility choices for a particular operator or saved map view are modeled separately'
    __occid_model_id__: ClassVar[int] = 180
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'IdentifiedRepresentation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('OverlayLayer', 'ReferenceLayer', 'DataLayer')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Layer')]
    temporal_extent: Semantic[TimeRange] | None = None

class OverlayLayer(OCCIDModel):
    'Layer whose membership consists of authored graphics'
    __occid_model_id__: ClassVar[int] = 263
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Layer'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Layer')]
    temporal_extent: Semantic[TimeRange] | None = None
    graphic_uids: list[Semantic[UID]]

class ReferenceLayer(OCCIDModel):
    'Layer backed by an external or media-derived geospatial representation source'
    __occid_model_id__: ClassVar[int] = 300
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Layer'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Layer')]
    temporal_extent: Semantic[TimeRange] | None = None
    source: Semantic[RepresentationSource]

class DataLayer(OCCIDModel):
    'Layer backed by a structured external representation source'
    __occid_model_id__: ClassVar[int] = 76
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Layer'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Layer')]
    temporal_extent: Semantic[TimeRange] | None = None
    source: Semantic[RepresentationSource]

class LayerView(OCCIDModel):
    'Presentation of one shared layer inside one saved view'
    __occid_model_id__: ClassVar[int] = 181
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    layer_uid: Semantic[UID]
    visible: builtins.bool
    opacity: Semantic[Opacity] | None = None

class MapGrid(OCCIDModel):
    'Coordinate-reference grid definition used by a saved map representation; renderer appearance is optional representation data'
    __occid_model_id__: ClassVar[int] = 203
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('UTMMapGrid', 'MGRSMapGrid', 'LatitudeLongitudeMapGrid', 'LocalMapGrid')
    style: Semantic[GraphicStyle] | None = None

class UTMZone(OCCIDValue[builtins.int]):
    'Universal Transverse Mercator longitudinal zone code'
    __occid_model_id__: ClassVar[int] = 390
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UTMMapGrid(OCCIDModel):
    'Fixed Universal Transverse Mercator grid'
    __occid_model_id__: ClassVar[int] = 389
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    zone: Semantic[UTMZone]
    hemisphere: Hemisphere
    interval: Semantic[DistanceMeters]

class MGRSMapGrid(OCCIDModel):
    'Military Grid Reference System display grid'
    __occid_model_id__: ClassVar[int] = 200
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    interval: Semantic[DistanceMeters]

class LatitudeLongitudeMapGrid(OCCIDModel):
    'Geographic latitude/longitude grid with angular spacing'
    __occid_model_id__: ClassVar[int] = 179
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    interval: Semantic[AngleDegrees]

class LocalMapGrid(OCCIDModel):
    'Pinned local metric grid whose positive north axis is rotated clockwise from true north'
    __occid_model_id__: ClassVar[int] = 193
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    origin: Semantic[GlobalPosition]
    interval: Semantic[DistanceMeters]
    bearing: Semantic[AngleDegrees]

class MapView(OCCIDModel):
    'Named saved operational map view over shared layers; transient browser viewport state need not be persisted as a MapView'
    __occid_model_id__: ClassVar[int] = 204
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'IdentifiedRepresentation'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MapView')]
    focus: Semantic[GlobalPosition] | None = None
    extent: Semantic[GeoArea] | None = None
    layers: list[Semantic[LayerView]]
    grid: Semantic[MapGrid] | None = None
    bearing: Semantic[AngleDegrees] | None = None

class TacticalGraphic(OCCIDModel):
    'Doctrinal military tactical graphic or control measure; exact graphic meaning is carried by a standard-qualified symbology code rather than an application-local string kind'
    __occid_model_id__: ClassVar[int] = 357
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    symbology: Semantic[Symbology]
    control_points: list[Semantic[GlobalPosition]]
