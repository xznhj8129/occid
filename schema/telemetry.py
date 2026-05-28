"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .message import Message

### Models

class TelemetryMessage(Message):
    'Message whose payload reports sender or asset state'
    state: SerializeAsAny[State | Kinematic | Internal | Position | Guidance | PlanProgress | TelemetryState | NavigationValidity | GnssSolution | FlightControlState | Sensor | Input | Resources | Condition | Lifecycle | Assignment]

class CapabilityAdvert(TelemetryMessage):
    node_id: str
    roles: list[CapabilityRole]
    link_ids: list[str]
    sensor_ids: list[str]
    payload_ids: list[str]

class StateDelta(TelemetryMessage):
    entity_id: str
    changed_fields: dict[str, SerializeAsAny[State | Kinematic | Internal | Position | Guidance | PlanProgress | TelemetryState | NavigationValidity | GnssSolution | FlightControlState | Sensor | Input | Resources | Condition | Lifecycle | Assignment]]

class TransportCounters(TelemetryMessage):
    rx_count: int = 0
    tx_count: int = 0
    parse_error_count: int = 0
    dropped_count: int = 0

class TransportError(TelemetryMessage):
    error: NetworkError
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
