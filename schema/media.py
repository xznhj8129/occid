"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Media(OCCIDModel):
    'Recorded, streamed, sampled, or otherwise encoded information used as an operational representation'
    __occid_model_id__: ClassVar[int] = 214
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'IdentifiedRepresentation'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MediaItem',)
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class MediaItem(OCCIDModel):
    'Identified media resource with address, provenance, and common storage metadata; concrete media semantics are expressed by children'
    __occid_model_id__: ClassVar[int] = 216
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Media'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ImageMedia', 'VideoMedia', 'AudioMedia', 'SpectrumMedia', 'PointCloudMedia', 'DocumentMedia', 'BinaryMedia')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class ImageMedia(OCCIDModel):
    'Two-dimensional visual media'
    __occid_model_id__: ClassVar[int] = 167
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('StillImage',)
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class StillImage(OCCIDModel):
    'Time-static image media independent of how the image was produced'
    __occid_model_id__: ClassVar[int] = 353
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ImageMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Photograph', 'VideoFrame')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class Photograph(OCCIDModel):
    'Still image produced by an imaging sensor or camera'
    __occid_model_id__: ClassVar[int] = 282
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'StillImage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class VideoFrame(OCCIDModel):
    'Still image identified as a frame originating from video media'
    __occid_model_id__: ClassVar[int] = 410
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'StillImage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    video_uid: Semantic[UID] | None = None

class VideoMedia(OCCIDModel):
    'Time-varying visual media'
    __occid_model_id__: ClassVar[int] = 411
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('VideoRecording', 'LiveVideoStream')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class VideoRecording(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 412
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'VideoMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    duration: Semantic[Duration] | None = None

class LiveVideoStream(OCCIDModel):
    'Live or near-live video stream endpoint'
    __occid_model_id__: ClassVar[int] = 194
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'VideoMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class AudioMedia(OCCIDModel):
    'Acoustic or other audio-band media'
    __occid_model_id__: ClassVar[int] = 27
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('AudioRecording', 'LiveAudioStream')
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class AudioRecording(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 28
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AudioMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    duration: Semantic[Duration] | None = None

class LiveAudioStream(OCCIDModel):
    'Live or near-live audio stream endpoint'
    __occid_model_id__: ClassVar[int] = 193
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AudioMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class SpectrumMedia(OCCIDModel):
    'Frequency-domain sampled or recorded media'
    __occid_model_id__: ClassVar[int] = 347
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ('SpectrumRecording',)
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class SpectrumRecording(OCCIDModel):
    'Recorded radio-frequency or other spectrum data over a declared frequency span'
    __occid_model_id__: ClassVar[int] = 348
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SpectrumMedia'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
    frequency_range: Semantic[FrequencyRange] | None = None
    duration: Semantic[Duration] | None = None

class PointCloudMedia(OCCIDModel):
    'Spatial point-cloud media'
    __occid_model_id__: ClassVar[int] = 289
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class DocumentMedia(OCCIDModel):
    'Human- or machine-readable document media'
    __occid_model_id__: ClassVar[int] = 92
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None

class BinaryMedia(OCCIDModel):
    'Binary media whose deeper semantics are not yet known or not represented by another MediaItem child'
    __occid_model_id__: ClassVar[int] = 36
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'MediaItem'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    id: Annotated[IntID, IDNamespace('MediaItem')]
    uri: builtins.str
    size: Semantic[ByteCount] | None = None
    content_type: builtins.str | None = None
    source_uid: Semantic[UID] | None = None
    captured_ts: Semantic[Timestamp] | None = None
