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
    __occid_model_id__: ClassVar[int] = 226
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]
    robot_control: Semantic[RobotController] | None = None
    remote_control: Semantic[RemoteControl]

class GroundRobot(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 105
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'GroundMachine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[Semantic[EntityComponentRef]]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[GroundNavigation]

class VideoConfig(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 288
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Parameter'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    protocol: VideoProtocol | None = None
    port: builtins.int | None = None
    stream_url: builtins.str | None = None
    overlay_url: builtins.str | None = None
    webrtc_url: builtins.str | None = None
    overlay_webrtc_url: builtins.str | None = None
    hls_url: builtins.str | None = None

class ReceiverConfig(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 217
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Parameter'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    rx_min_usec: builtins.int
    rx_max_usec: builtins.int
    rx_center_usec: builtins.int

class ChannelMapEntry(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 29
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Parameter'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    axis: ControlAxis
    source_channel: builtins.int
    output_channel: builtins.int | None = None
    label: builtins.str | None = None

class ModeRange(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 170
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Parameter'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    mode_id: builtins.int
    mode_name: builtins.str | None = None
    channel: builtins.int
    range: Semantic[NumericRange]

class RobotController(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 227
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Parameter'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    key: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    control_modes: RobotControlMode | None = None
    autopilot_type: AutopilotType
    autopilot_firmware: Semantic[FirmwareInfo]

class RemoteControl(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 221
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Interface'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    rc_link: builtins.str = ''
    vid_link: builtins.str = ''
    ctrl_video_sep: builtins.bool | None = None
    rc_telemetry: Semantic[ControlAxisSet] | None = None
    control_input: Semantic[ControlAxisSet] | None = None
    control_output: Semantic[ControlAxisSet] | None = None
    control_override: Semantic[ControlOverride] | None = None
    receiver_config: Semantic[ReceiverConfig] | None = None
    channel_map: list[Semantic[ChannelMapEntry]]
    mode_ranges: list[Semantic[ModeRange]]

class ObserverSource(OCCIDModel):
    'Entity-owned imagery/video observation source with OCCID identity, local acquisition source, camera geometry, and telemetry links'
    __occid_model_id__: ClassVar[int] = 184
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Interface'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ObserverSource')]
    entity_uid: Semantic[UID]
    name: builtins.str
    local_source: builtins.str
    objtype: EntitySubtype = EntitySubtype.AIR_ROBOT
    active: builtins.bool = True
    pos: Semantic[GlobalPosition] | None = None
    attitude: Semantic[EulerAngles] | None = None
    gimbal_ang: Semantic[EulerAngles] | None = None
    gimbal_axes: list[GimbalAxis]
    field_of_view: Semantic[SensorFieldOfView] | None = None
    media_kind: SensorDataFormat = SensorDataFormat.VIDEO
    video: Semantic[VideoConfig] | None = None
    video_res: tuple[builtins.int, builtins.int] | None = None
    telemetry_type: TelemetryType | None = None
    telem_port: builtins.str | None = None
    telem_baud: builtins.int | None = None
    commands_allowed: builtins.bool = False
    can_zoom: builtins.bool = False

class FlightControlState(OCCIDModel):
    'Portable flight-controller operational state independent of endpoint-specific mode identifiers'
    __occid_model_id__: ClassVar[int] = 84
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'GNC'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    armed: builtins.bool | None = None
    in_air: builtins.bool | None = None
    override_active: builtins.bool | None = None
    failsafe: builtins.bool | None = None
    standard_mode: StandardFlightMode | None = None
    attitude_setpoint: Semantic[ControlAttitudeSetpoint] | None = None
    navigation_validity: Semantic[NavigationValidity] | None = None
    readiness: Semantic[NavReadinessState] | None = None
    runtime_load: Semantic[RuntimeLoadState] | None = None
