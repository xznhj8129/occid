"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class ObservationMessage(Message):
    'Message whose payload reports external objects, events, environment, or intelligence'
    observation: SerializeAsAny[Observation | Detection | Classification | Track | TrackUpdate | IntelTrackSchema | Assessment | IsrResult | IsrObservation]

class ProtocolEventMessage(ObservationMessage):
    uid: str
    event_type: str
    event_method: str | None = None
    callsign: str | None = None
    time_text: str | None = None
    start_text: str | None = None
    stale_text: str | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    detail: ProtocolPayload | None = None
    source_address: NetworkAddress | None = None
    targets: list[MessageTarget]
