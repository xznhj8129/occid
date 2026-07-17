"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class ObservationMessage(Message):
    'Message whose payload reports external objects, events, environment, or intelligence'
    __occid_model_id__: ClassVar[int] = 160
    observation: SerializeAsAny[Observation | Detection | VisionBox | VisionDetection | VisionDetectionFrame | Classification | Track | TrackUpdate | IntelTrackSchema | Assessment | IsrResult | IsrObservation]

class ProtocolEventMessage(ObservationMessage):
    __occid_model_id__: ClassVar[int] = 161
    uid: StringID
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
    targets: list[MessageTarget]
