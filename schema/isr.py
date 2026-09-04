"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class ObservationMessage(OCCIDModel):
    'Message whose payload reports external objects, events, environment, or intelligence'
    __occid_model_id__: ClassVar[int] = 169
    __occid_semantic_role__: ClassVar[str] = 'type'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    observation: Classification | Track | Assessment | IsrResult | Detection | VisionBox | VisionDetection | VisionDetectionFrame | IsrObservation | TrackUpdate

class ProtocolEventMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 196
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    observation: Classification | Track | Assessment | IsrResult | Detection | VisionBox | VisionDetection | VisionDetectionFrame | IsrObservation | TrackUpdate
    event_ref: builtins.str
    event_type: builtins.str
    event_method: builtins.str | None = None
    callsign: builtins.str | None = None
    time_text: builtins.str | None = None
    start_text: builtins.str | None = None
    stale_text: builtins.str | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    detail: ProtocolPayload | None = None
    source_address: NetworkAddress | None = None
    targets: list[UID]
