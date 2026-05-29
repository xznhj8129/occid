"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .entities import GroundMachine, Machine, MachineType
from .guidance import Guidance
from .interface import Interface
from .parameter import Parameter

### Enums

class VideoProtocol(IntEnum):
    RTSP = 0
    RTMP = auto()
    SRT = auto()
    HLS = auto()
    UDP = auto()
    TCP = auto()

class TelemetryType(IntEnum):
    MSP = 0
    MAVLINK = auto()
    CRSF = auto()

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

### Models

class Robot(Machine):
    'Robot entities and control surfaces'
    __occid_model_id__: ClassVar[int] = 238
    robot_control: RobotController | None = None
    remote_control: RemoteControlSchema

class GroundRobot(GroundMachine):
    __occid_model_id__: ClassVar[int] = 239
    machine_type: MachineType = MachineType.ROBOT

class VideoConfigSchema(Parameter):
    __occid_model_id__: ClassVar[int] = 240
    protocol: VideoProtocol | None = None
    port: builtins.int | None = None
    stream_url: builtins.str | None = None
    overlay_url: builtins.str | None = None
    webrtc_url: builtins.str | None = None
    overlay_webrtc_url: builtins.str | None = None
    hls_url: builtins.str | None = None

class ReceiverConfig(Parameter):
    __occid_model_id__: ClassVar[int] = 241
    rx_min_usec: builtins.int
    rx_max_usec: builtins.int
    rx_center_usec: builtins.int

class ChannelMapEntry(Parameter):
    __occid_model_id__: ClassVar[int] = 242
    axis: ControlAxis
    source_channel: builtins.int
    output_channel: builtins.int | None = None
    label: builtins.str | None = None

class ModeRange(Parameter):
    __occid_model_id__: ClassVar[int] = 243
    mode_id: builtins.int | None = None
    mode_name: builtins.str | None = None
    channel: builtins.int
    range: NumericRange

class RobotController(Parameter):
    __occid_model_id__: ClassVar[int] = 244
    control_modes: RobotControlMode | None = None
    autopilot_type: AutopilotType
    autopilot_firmware: FirmwareInfo

class RemoteControlSchema(Interface):
    __occid_model_id__: ClassVar[int] = 245
    rc_link: builtins.str = ''
    vid_link: builtins.str = ''
    ctrl_video_sep: builtins.bool | None = None
    telemetry: TelemetryState | None = None
    rc_telemetry: ControlAxisSet | None = None
    control_input: ControlAxisSet | None = None
    control_output: ControlAxisSet | None = None
    control_override: ControlOverride | None = None
    receiver_config: ReceiverConfig | None = None
    channel_map: list[ChannelMapEntry]
    mode_ranges: list[ModeRange]

class FlightControlState(Guidance):
    __occid_model_id__: ClassVar[int] = 246
    armed: builtins.bool | None = None
    in_air: builtins.bool | None = None
    override_active: builtins.bool | None = None
    failsafe: builtins.bool | None = None
    active_modes: list[builtins.int]
    active_mode_names: list[builtins.str]
    nav_state_code: builtins.int | None = None
    flight_mode: builtins.str | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None
    navigation_validity: NavigationValidity | None = None
    readiness: NavReadinessState | None = None
    runtime_load: RuntimeLoadState | None = None
