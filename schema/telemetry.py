"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class TelemetryMessage(OCCIDModel):
    'Message whose payload reports sender or asset state'
    __occid_model_id__: ClassVar[int] = 250
    __occid_semantic_role__: ClassVar[str] = 'type'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LinkState | MeshLink | Lifecycle | Activation | Cue | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Internal | FirmwareInfo | RuntimeLoadState | Kinematic | ImuSample | Resource | FuelState | Supplies | PowerSource | PowerState | ElectricalResourceState | SensorState | TrackerState | FlightSensorConfiguration | EntityState | Validation | Position | LocationState | SpotterOrigin

class UAVTelemetryMessage(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 259
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: EntityState

class CapabilityAdvert(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 26
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LinkState | MeshLink | Lifecycle | Activation | Cue | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Internal | FirmwareInfo | RuntimeLoadState | Kinematic | ImuSample | Resource | FuelState | Supplies | PowerSource | PowerState | ElectricalResourceState | SensorState | TrackerState | FlightSensorConfiguration | EntityState | Validation | Position | LocationState | SpotterOrigin
    node_uid: UID
    roles: list[CapabilityRole]
    link_refs: list[builtins.str]
    sensor_refs: list[builtins.str]
    payload_refs: list[builtins.str]

class TransportCounters(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 257
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LinkState | MeshLink | Lifecycle | Activation | Cue | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Internal | FirmwareInfo | RuntimeLoadState | Kinematic | ImuSample | Resource | FuelState | Supplies | PowerSource | PowerState | ElectricalResourceState | SensorState | TrackerState | FlightSensorConfiguration | EntityState | Validation | Position | LocationState | SpotterOrigin
    rx_count: builtins.int = 0
    tx_count: builtins.int = 0
    parse_error_count: builtins.int = 0
    dropped_count: builtins.int = 0

class TransportError(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 258
    __occid_semantic_role__: ClassVar[str] = 'representation'
    src: UID
    dst: UID
    ts: Timestamp
    priority: MessagePriority
    seq: builtins.int
    state: LinkState | MeshLink | Lifecycle | Activation | Cue | GNC | NavigationValidity | GnssSolution | AutopilotMissionState | FlightControlState | Health | HealthAlert | SubsystemHealth | HealthSnapshot | MaintenanceStatus | NavReadinessState | Input | ControlAxisSet | ControlChannelValue | ControlOverride | ControlAttitudeSetpoint | Internal | FirmwareInfo | RuntimeLoadState | Kinematic | ImuSample | Resource | FuelState | Supplies | PowerSource | PowerState | ElectricalResourceState | SensorState | TrackerState | FlightSensorConfiguration | EntityState | Validation | Position | LocationState | SpotterOrigin
    error: NetworkError
    source_address: NetworkAddress | None = None
    payload: ProtocolPayload | None = None
