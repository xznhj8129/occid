"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class TelemetryMessage(Message):
    'Message whose payload reports sender or asset state'
    __occid_model_id__: ClassVar[int] = 208
    state: SerializeAsAny[State | Kinematic | ImuSample | Internal | FirmwareInfo | RuntimeLoadState | Position | LocationState | SpotterOrigin | Guidance | TelemetryState | NavigationValidity | GnssSolution | FlightControlState | SensorState | TrackerState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Resource | FuelState | SuppliesSchema | PowerSourceSchema | PowerStateSchema | ElectricalResourceState | Condition | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Lifecycle | TaskAssignment | Assignment | TaskDelta | FlightAssignment]

class UAVTelemetryMessage(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 209
    state: TelemetryState

class CapabilityAdvert(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 210
    node_id: StringID
    roles: list[CapabilityRole]
    link_ids: list[builtins.str]
    sensor_ids: list[builtins.str]
    payload_ids: list[builtins.str]

class StateDelta(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 211
    entity_id: StringID
    changed_fields: dict[builtins.str, SerializeAsAny[State | Kinematic | ImuSample | Internal | FirmwareInfo | RuntimeLoadState | Position | LocationState | SpotterOrigin | Guidance | TelemetryState | NavigationValidity | GnssSolution | FlightControlState | SensorState | TrackerState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Resource | FuelState | SuppliesSchema | PowerSourceSchema | PowerStateSchema | ElectricalResourceState | Condition | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Lifecycle | TaskAssignment | Assignment | TaskDelta | FlightAssignment]]

class TransportCounters(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 212
    rx_count: builtins.int = 0
    tx_count: builtins.int = 0
    parse_error_count: builtins.int = 0
    dropped_count: builtins.int = 0

class TransportError(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 213
    error: NetworkError
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
