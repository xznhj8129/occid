"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class ObservationMessage(OCCIDModel):
    'Message whose payload reports external objects, events, environment, or intelligence'
    __occid_model_id__: ClassVar[int] = 183
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Message'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ProtocolEventMessage',)
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    observation: Semantic[Observation]

class ProtocolEventMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 211
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ObservationMessage'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    src: Semantic[UID]
    dst: Semantic[UID]
    ts: Semantic[Timestamp]
    priority: MessagePriority
    seq: builtins.int
    observation: Semantic[Observation]
    event_ref: builtins.str
    event_type: builtins.str
    event_method: builtins.str | None = None
    callsign: builtins.str | None = None
    time_text: builtins.str | None = None
    start_text: builtins.str | None = None
    stale_text: builtins.str | None = None
    position: Semantic[GlobalPosition] | None = None
    uncertainty: Semantic[LocationUncertainty] | None = None
    detail: Semantic[ProtocolPayload] | None = None
    source_address: Semantic[NetworkAddress] | None = None
    targets: list[Semantic[UID]]
