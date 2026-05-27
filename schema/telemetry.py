"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class Telemetry(Message):
    'Message whose payload reports sender or asset state'

class CapabilityAdvert(Telemetry):
    node_id: str
    roles: list[CapabilityRole]
    link_ids: list[str]
    sensor_ids: list[str]
    payload_ids: list[str]

class StateDelta(Telemetry):
    entity_id: str
    changed_fields: list[str]
    source: str | None = None

class TransportCounters(Telemetry):
    rx_count: int = 0
    tx_count: int = 0
    parse_error_count: int = 0
    dropped_count: int = 0

class TransportError(Telemetry):
    error: str
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
