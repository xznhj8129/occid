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

class TacticalGraphicStatus(IntEnum):
    PRESENT = 0
    PLANNED = auto()

### Models

class Representation(OCCIDModel):
    'An authored or shared depiction, presentation, organization, or view of operational information; representation changes do not alter the represented subject itself'
    __occid_model_id__: ClassVar[int] = 311
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('IdentifiedRepresentation',)

class IdentifiedRepresentation(OCCIDModel):
    'Persisted shared representation with durable OCCID identity, distinct from transient renderer or session state'
    __occid_model_id__: ClassVar[int] = 164
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Representation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Graphic', 'Layer', 'MapView')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class ColorComponent(OCCIDModel):
    'Component of a declared graphic color value'
    __occid_model_id__: ClassVar[int] = 54
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ColorChannel',)

class ColorChannel(OCCIDValue[builtins.int]):
    __occid_model_id__: ClassVar[int] = 53
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ColorComponent'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class Opacity(OCCIDValue[builtins.float]):
    'Graphic opacity ratio where zero is fully transparent and one is fully opaque'
    __occid_model_id__: ClassVar[int] = 259
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Ratio'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class ColorRGBA(OCCIDModel):
    'Device-independent sRGB color components used for authored graphic portrayal'
    __occid_model_id__: ClassVar[int] = 55
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    red: Semantic[ColorChannel]
    green: Semantic[ColorChannel]
    blue: Semantic[ColorChannel]
    alpha: Semantic[Opacity] | None = None

class GraphicLength(OCCIDModel):
    'Length used by a graphic portrayal, explicitly distinguishing screen-space and world-space values'
    __occid_model_id__: ClassVar[int] = 149
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Measurement'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    value: builtins.float
    unit: GraphicLengthUnit

class StrokeStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 353
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    width: Semantic[GraphicLength] | None = None
    pattern: StrokePattern | None = None

class FillStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 117
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    pattern: FillPattern | None = None

class TextStyle(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 383
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    color: Semantic[ColorRGBA] | None = None
    background: Semantic[ColorRGBA] | None = None
    size: Semantic[GraphicLength] | None = None
    alignment: TextAlignment | None = None

class GraphicStyle(OCCIDModel):
    'Renderer-independent authored portrayal of a graphic'
    __occid_model_id__: ClassVar[int] = 150
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
    __occid_model_id__: ClassVar[int] = 289
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    position: Semantic[GlobalPosition]

class SubjectAnchor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 356
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_uid: Semantic[UID]

class PathAnchor(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 273
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AnnotationAnchor'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    path_uid: Semantic[UID]
    distance_from_start: Semantic[DistanceMeters]

class RepresentationSource(OCCIDModel):
    'Source used to construct a reference or data representation'
    __occid_model_id__: ClassVar[int] = 312
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ExternalRepresentationSource', 'MediaRepresentationSource')

class ExternalRepresentationSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 116
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RepresentationSource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uri: builtins.str
    format: RepresentationFormat

class GeoRegistration(OCCIDModel):
    'Geographic footprint used to register media or an external representation to the operational map'
    __occid_model_id__: ClassVar[int] = 142
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    footprint: Semantic[GeoArea]

class MediaRepresentationSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 217
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'RepresentationSource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    media_uid: Semantic[UID]
    registration: Semantic[GeoRegistration] | None = None

class Graphic(OCCIDModel):
    'Persisted graphical representation of one or more operational subjects or spatial constructs'
    __occid_model_id__: ClassVar[int] = 148
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
    __occid_model_id__: ClassVar[int] = 144
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
    'Symbolic portrayal of an operational subject using a declared symbology'
    __occid_model_id__: ClassVar[int] = 363
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitarySymbolGraphic',)
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    subject_uid: Semantic[UID]
    symbology: Semantic[Symbology]

class AnnotationGraphic(OCCIDModel):
    'Human-authored annotation anchored to space or another operational object'
    __occid_model_id__: ClassVar[int] = 18
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Graphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LabelGraphic', 'NoteGraphic', 'CalloutGraphic', 'MediaGraphic')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    anchor: Semantic[AnnotationAnchor]

class LabelGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 181
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

class NoteGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 253
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
    text: Semantic[Text]

class CalloutGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 40
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
    text: Semantic[Text]

class MediaGraphic(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 214
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
    __occid_model_id__: ClassVar[int] = 145
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
    registration: Semantic[GeoRegistration]

class MeasurementGraphic(OCCIDModel):
    'Graphic portrayal of a semantic measurement object; the measurement result is not encoded in the graphic itself'
    __occid_model_id__: ClassVar[int] = 211
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
    __occid_model_id__: ClassVar[int] = 183
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
    __occid_model_id__: ClassVar[int] = 270
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
    __occid_model_id__: ClassVar[int] = 307
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
    __occid_model_id__: ClassVar[int] = 78
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
    __occid_model_id__: ClassVar[int] = 184
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    layer_uid: Semantic[UID]
    visible: builtins.bool
    opacity: Semantic[Opacity] | None = None

class MapGrid(OCCIDModel):
    'Coordinate-reference grid definition used by a saved map representation; renderer appearance is optional representation data'
    __occid_model_id__: ClassVar[int] = 206
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('UTMMapGrid', 'MGRSMapGrid', 'LatitudeLongitudeMapGrid', 'LocalMapGrid')
    style: Semantic[GraphicStyle] | None = None

class UTMZone(OCCIDValue[builtins.int]):
    'Universal Transverse Mercator longitudinal zone code'
    __occid_model_id__: ClassVar[int] = 397
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()

class UTMMapGrid(OCCIDModel):
    'Fixed Universal Transverse Mercator grid'
    __occid_model_id__: ClassVar[int] = 396
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    zone: Semantic[UTMZone]
    hemisphere: Hemisphere
    interval: Semantic[DistanceMeters]

class MGRSMapGrid(OCCIDModel):
    'Military Grid Reference System display grid'
    __occid_model_id__: ClassVar[int] = 203
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    interval: Semantic[DistanceMeters]

class LatitudeLongitudeMapGrid(OCCIDModel):
    'Geographic latitude/longitude grid with angular spacing'
    __occid_model_id__: ClassVar[int] = 182
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    interval: Semantic[AngleDegrees]

class LocalMapGrid(OCCIDModel):
    'Pinned local metric grid whose positive north axis is rotated clockwise from true north'
    __occid_model_id__: ClassVar[int] = 196
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MapGrid'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    style: Semantic[GraphicStyle] | None = None
    origin: Semantic[GlobalPosition]
    interval: Semantic[DistanceMeters]
    bearing: Semantic[AngleDegrees]

class MapView(OCCIDModel):
    'Named saved operational map view over shared layers; transient browser viewport state need not be persisted as a MapView'
    __occid_model_id__: ClassVar[int] = 207
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

class MilitarySymbolGraphic(OCCIDModel):
    'Military-standard symbolic portrayal of an identified operational subject'
    __occid_model_id__: ClassVar[int] = 238
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SymbolGraphic'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('Graphic')]
    style: Semantic[GraphicStyle] | None = None
    temporal_extent: Semantic[TimeRange] | None = None
    subject_uid: Semantic[UID]
    symbology: Semantic[MilitarySymbology]

class TacticalGraphic(OCCIDModel):
    'Doctrinal military tactical graphic or control measure; exact graphic meaning is carried by a standard-qualified SIDC rather than an application-local string kind'
    __occid_model_id__: ClassVar[int] = 365
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
    sidc: Semantic[SIDC]
    control_points: list[Semantic[GlobalPosition]]
    status: TacticalGraphicStatus = TacticalGraphicStatus.PRESENT
