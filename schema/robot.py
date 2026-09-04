"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain
from .entities import EntitySubtype, EntityType, MachineType
from .payload import SensorDataFormat

### Enums

class VideoProtocol(IntEnum):
    RTSP = 0
    RTMP = auto()
    SRT = auto()
    HLS = auto()
    UDP = auto()
    TCP = auto()
    WEBRTC = auto()

class TelemetryType(IntEnum):
    MSP = 0
    MAVLINK = auto()
    CRSF = auto()
    MANUAL_ENTRY = auto()

class RCType(IntEnum):
    PWM = 0
    CRSF = auto()
    MAVLINK = auto()
    MSP = auto()

class UAVRadioType(IntEnum):
    ELRS = 0
    MLRS = auto()
    SIK = auto()
    WIFI_DUALBAND = auto()
    MESHTASTIC = auto()
    WIFI_915 = auto()

class AutopilotType(IntEnum):
    BETAFLIGHT = 0
    INAV = auto()
    ARDUPILOT = auto()
    PX4 = auto()
    CUSTOM = auto()

class RobotControlMode(IntEnum):
    MANUAL = 0
    REMOTE = auto()
    ASSISTED = auto()
    PROGRAMMED = auto()
    AUTONOMOUS = auto()
    ROGUE = auto()

class ControlAxis(IntEnum):
    ROLL = 0
    PITCH = auto()
    YAW = auto()
    THROTTLE = auto()
    AUX = auto()

class GimbalAxis(IntEnum):
    ROLL = 0
    PITCH = auto()
    YAW = auto()

### Models

class Robot(OCCIDModel):
    'Robot entities and control surfaces'
    __occid_model_id__: ClassVar[int] = 211
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]
    robot_control: RobotController | None = None
    remote_control: RemoteControl

class GroundRobot(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 96
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[EntityComponentRef]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: GroundNavigation

class VideoConfig(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 270
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    protocol: VideoProtocol | None = None
    port: builtins.int | None = None
    stream_url: builtins.str | None = None
    overlay_url: builtins.str | None = None
    webrtc_url: builtins.str | None = None
    overlay_webrtc_url: builtins.str | None = None
    hls_url: builtins.str | None = None

class ReceiverConfig(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 202
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    rx_min_usec: builtins.int
    rx_max_usec: builtins.int
    rx_center_usec: builtins.int

class ChannelMapEntry(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 28
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    axis: ControlAxis
    source_channel: builtins.int
    output_channel: builtins.int | None = None
    label: builtins.str | None = None

class ModeRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 158
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    mode_id: builtins.int
    mode_name: builtins.str | None = None
    channel: builtins.int
    range: NumericRange

class RobotController(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 212
    __occid_semantic_role__: ClassVar[str] = 'representation'
    key: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    control_modes: RobotControlMode | None = None
    autopilot_type: AutopilotType
    autopilot_firmware: FirmwareInfo

class RemoteControl(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 206
    __occid_semantic_role__: ClassVar[str] = 'representation'
    rc_link: builtins.str = ''
    vid_link: builtins.str = ''
    ctrl_video_sep: builtins.bool | None = None
    rc_telemetry: ControlAxisSet | None = None
    control_input: ControlAxisSet | None = None
    control_output: ControlAxisSet | None = None
    control_override: ControlOverride | None = None
    receiver_config: ReceiverConfig | None = None
    channel_map: list[ChannelMapEntry]
    mode_ranges: list[ModeRange]

class ObserverSource(OCCIDModel):
    'Entity-owned imagery/video observation source with OCCID identity, local acquisition source, camera geometry, and telemetry links'
    __occid_model_id__: ClassVar[int] = 170
    __occid_semantic_role__: ClassVar[str] = 'representation'
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('ObserverSource')]
    entity_uid: UID
    name: builtins.str
    local_source: builtins.str
    objtype: EntitySubtype = EntitySubtype.AIR_ROBOT
    active: builtins.bool = True
    pos: GlobalPosition | None = None
    attitude: EulerAngles | None = None
    gimbal_ang: EulerAngles | None = None
    gimbal_axes: list[GimbalAxis]
    field_of_view: SensorFieldOfView | None = None
    media_kind: SensorDataFormat = SensorDataFormat.VIDEO
    video: VideoConfig | None = None
    video_res: tuple[builtins.int, builtins.int] | None = None
    telemetry_type: TelemetryType | None = None
    telem_port: builtins.str | None = None
    telem_baud: builtins.int | None = None
    commands_allowed: builtins.bool = False
    can_zoom: builtins.bool = False

class FlightControlState(OCCIDModel):
    'Portable flight-controller operational state independent of endpoint-specific mode identifiers'
    __occid_model_id__: ClassVar[int] = 75
    __occid_semantic_role__: ClassVar[str] = 'representation'
    armed: builtins.bool | None = None
    in_air: builtins.bool | None = None
    override_active: builtins.bool | None = None
    failsafe: builtins.bool | None = None
    standard_mode: StandardFlightMode | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None
    navigation_validity: NavigationValidity | None = None
    readiness: NavReadinessState | None = None
    runtime_load: RuntimeLoadState | None = None
