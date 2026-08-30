"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .entities import EntitySubtype, GroundMachine, Machine, MachineType
from .gnc import GNC
from .interface import Interface
from .parameter import Parameter
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

class Robot(Machine):
    'Robot entities and control surfaces'
    __occid_model_id__: ClassVar[int] = 242
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    robot_control: RobotController | None = None
    remote_control: RemoteControlSchema

class GroundRobot(GroundMachine):
    __occid_model_id__: ClassVar[int] = 243
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    machine_type: MachineType = MachineType.ROBOT

class VideoConfigSchema(Parameter):
    __occid_model_id__: ClassVar[int] = 244
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    protocol: VideoProtocol | None = None
    port: builtins.int | None = None
    stream_url: builtins.str | None = None
    overlay_url: builtins.str | None = None
    webrtc_url: builtins.str | None = None
    overlay_webrtc_url: builtins.str | None = None
    hls_url: builtins.str | None = None

class ReceiverConfig(Parameter):
    __occid_model_id__: ClassVar[int] = 245
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    rx_min_usec: builtins.int
    rx_max_usec: builtins.int
    rx_center_usec: builtins.int

class ChannelMapEntry(Parameter):
    __occid_model_id__: ClassVar[int] = 246
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    axis: ControlAxis
    source_channel: builtins.int
    output_channel: builtins.int | None = None
    label: builtins.str | None = None

class ModeRange(Parameter):
    __occid_model_id__: ClassVar[int] = 247
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    mode_id: builtins.int | None = None
    mode_name: builtins.str | None = None
    channel: builtins.int
    range: NumericRange

class RobotController(Parameter):
    __occid_model_id__: ClassVar[int] = 248
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    control_modes: RobotControlMode | None = None
    autopilot_type: AutopilotType
    autopilot_firmware: FirmwareInfo

class RemoteControlSchema(Interface):
    __occid_model_id__: ClassVar[int] = 249
    __occid_semantic_role__: ClassVar[str] = 'specialization'
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

class ObserverSource(Interface):
    'Entity-owned imagery/video observation source with stable source identity, local acquisition source, camera geometry, and telemetry links'
    __occid_model_id__: ClassVar[int] = 250
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    record: RecordMeta
    source_id: UID
    entity_id: UID
    name: builtins.str
    local_source: builtins.str
    objtype: EntitySubtype = EntitySubtype.AIR_ROBOT
    active: builtins.bool = True
    pos: GlobalPosition | None = None
    attitude: EulerAngles | None = None
    gimbal_ang: EulerAngles | None = None
    gimbal_axes: list[GimbalAxis]
    fov_h_deg: builtins.float | None = None
    fov_v_deg: builtins.float | None = None
    media_kind: SensorDataFormat = SensorDataFormat.VIDEO
    video: VideoConfigSchema | None = None
    video_res: tuple[builtins.int, builtins.int] | None = None
    telemetry_type: TelemetryType | None = None
    telem_port: builtins.str | None = None
    telem_baud: builtins.int | None = None
    commands_allowed: builtins.bool = False
    can_zoom: builtins.bool = False

class FlightControlState(GNC):
    'Portable flight-controller operational state independent of endpoint-specific mode identifiers'
    __occid_model_id__: ClassVar[int] = 251
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    armed: builtins.bool | None = None
    in_air: builtins.bool | None = None
    override_active: builtins.bool | None = None
    failsafe: builtins.bool | None = None
    standard_mode: StandardFlightMode | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None
    navigation_validity: NavigationValidity | None = None
    readiness: NavReadinessState | None = None
    runtime_load: RuntimeLoadState | None = None
