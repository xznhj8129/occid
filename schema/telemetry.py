"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .message import Message

### Models

class TelemetryMessage(Message):
    'Message whose payload reports sender or asset state'
    __occid_model_id__: ClassVar[int] = 208
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    state: SerializeAsAny[State | Kinematic | ImuSample | Internal | FirmwareInfo | RuntimeLoadState | Position | LocationState | SpotterOrigin | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | SensorState | TrackerState | FlightSensorConfiguration | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Resource | FuelState | SuppliesSchema | PowerSourceSchema | PowerStateSchema | ElectricalResourceState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | LinkState | MeshLink | Activation | Validation | Cue | Lifecycle | Execution | ExecutionAcceptance | ExecutionStatusReport | TaskDelta | EntityState]

class UAVTelemetryMessage(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 209
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    state: EntityState

class CapabilityAdvert(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 210
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    node_id: UID
    roles: list[CapabilityRole]
    link_ids: list[builtins.str]
    sensor_ids: list[builtins.str]
    payload_ids: list[builtins.str]

class StateDelta(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 211
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    entity_id: UID
    changed_fields: dict[builtins.str, SerializeAsAny[State | Kinematic | ImuSample | Internal | FirmwareInfo | RuntimeLoadState | Position | LocationState | SpotterOrigin | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | SensorState | TrackerState | FlightSensorConfiguration | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Resource | FuelState | SuppliesSchema | PowerSourceSchema | PowerStateSchema | ElectricalResourceState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | LinkState | MeshLink | Activation | Validation | Cue | Lifecycle | Execution | ExecutionAcceptance | ExecutionStatusReport | TaskDelta | EntityState]]

class TransportCounters(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 212
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    rx_count: builtins.int = 0
    tx_count: builtins.int = 0
    parse_error_count: builtins.int = 0
    dropped_count: builtins.int = 0

class TransportError(TelemetryMessage):
    __occid_model_id__: ClassVar[int] = 213
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    error: NetworkError
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
