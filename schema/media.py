"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class MediaSpectrum(IntEnum):
    VISUAL = 0
    AUDIO = auto()
    RADIO = auto()
    IR = auto()
    UV = auto()
    MOTION = auto()
    MATTER = auto()

class MediaTimeOrigin(IntEnum):
    RECORDED = 0
    STREAMED = auto()

class MediaLiveness(IntEnum):
    FINISHED = 0
    LIVE = auto()

class ImageOrigin(IntEnum):
    PHOTO = 0
    VIDEO_CAPTURE = auto()
    SCREEN_CAPTURE = auto()
    GENERATED = auto()
    SCAN = auto()

class MediaDomain(IntEnum):
    SPATIAL = 0
    TEMPORAL = auto()
    FREQUENCY = auto()
    TIME_FREQUENCY = auto()

### Models

class Media(OCCIDModel):
    'Recorded, streamed, sampled, or otherwise encoded non-text information used as an operational representation'
    __occid_model_id__: ClassVar[int] = 213
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MediaItem',)

class MediaItem(OCCIDModel):
    'Identified media resource with typed content, address, acquisition provenance, and common storage metadata; concrete media semantics are expressed by children'
    __occid_model_id__: ClassVar[int] = 215
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Media'
    __occid_children__: ClassVar[tuple[str, ...]] = ('StillMedia', 'DurationalMedia')
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]

class CaptureSize2D(OCCIDModel):
    '2D media size'
    __occid_model_id__: ClassVar[int] = 43
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    width: builtins.int
    height: builtins.int

class CaptureSize3D(OCCIDModel):
    '2D media size'
    __occid_model_id__: ClassVar[int] = 44
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Property'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    length: builtins.int
    width: builtins.int
    height: builtins.int

class StillMedia(OCCIDModel):
    'Spatial-domain fixed media'
    __occid_model_id__: ClassVar[int] = 351
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('PointCloudMedia', 'StillImage')
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]

class PointCloudMedia(OCCIDModel):
    'Spatial point-cloud media'
    __occid_model_id__: ClassVar[int] = 286
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'StillMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.MATTER
    size: Semantic[CaptureSize3D]
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]

class StillImage(OCCIDModel):
    'Time-static image frame'
    __occid_model_id__: ClassVar[int] = 350
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'StillMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VideoFrame',)
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.VISUAL
    size: Semantic[CaptureSize2D]
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    origin_type: ImageOrigin

class VideoFrame(OCCIDModel):
    'Still image identified as a frame originating from video media'
    __occid_model_id__: ClassVar[int] = 408
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'StillImage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.VISUAL
    size: Semantic[CaptureSize2D]
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    origin_type: ImageOrigin = ImageOrigin.VIDEO_CAPTURE
    video_uid: Semantic[UID] | None = None
    frame_n: builtins.int

class DurationalMedia(OCCIDModel):
    'Media with a time dimension'
    __occid_model_id__: ClassVar[int] = 95
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VideoMedia', 'AudioMedia', 'SpectrumMedia')
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin

class VideoMedia(OCCIDModel):
    'Time-varying visual media'
    __occid_model_id__: ClassVar[int] = 409
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'DurationalMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ('LiveVideoStream',)
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.VISUAL
    size: Semantic[CaptureSize2D]
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin
    has_audio: builtins.bool

class LiveVideoStream(OCCIDModel):
    'Live or near-live video stream endpoint'
    __occid_model_id__: ClassVar[int] = 193
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'VideoMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.VISUAL
    size: Semantic[CaptureSize2D]
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin = MediaTimeOrigin.STREAMED
    has_audio: builtins.bool
    path: Semantic[NetworkAddress]

class AudioMedia(OCCIDModel):
    'Acoustic or other audio-band media'
    __occid_model_id__: ClassVar[int] = 27
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'DurationalMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum = MediaSpectrum.AUDIO
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin

class SpectrumMedia(OCCIDModel):
    'Frequency-domain sampled or recorded media'
    __occid_model_id__: ClassVar[int] = 344
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'DurationalMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SpectrumRecording',)
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin

class SpectrumRecording(OCCIDModel):
    'Recorded radio-frequency or other spectrum data over a declared frequency span'
    __occid_model_id__: ClassVar[int] = 345
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpectrumMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('MediaItem')]
    content_type: MediaSpectrum
    size: Semantic[ByteCount] | None = None
    producer_uid: Semantic[UID] | None = None
    sensor_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    duration: Semantic[Duration]
    start_time: Semantic[Timestamp] | None = None
    end_time: Semantic[Timestamp] | None = None
    is_live: MediaLiveness
    time_origin: MediaTimeOrigin
    frequency_range: Semantic[FrequencyRange] | None = None
