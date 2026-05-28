"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .entities import AirMachine, GroundMachine, Machine, MachineType
from .guidance import Guidance
from .interface import Interface
from .property import Property

### Enums

class VideoProtocol(IntEnum):
    RTSP = 0
    RTMP = auto()
    SRT = auto()
    HLS = auto()
    UDP = auto()
    TCP = auto()

class SerialTelemetryType(IntEnum):
    MSP = 0
    MAVLINK = auto()

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

class GroundRobot(GroundMachine):
    machine_type: MachineType = MachineType.ROBOT
    robot_control: RobotControlSchema | None = None
    remote_control: RemoteControlSchema

class AirRobot(AirMachine):
    machine_type: MachineType = MachineType.ROBOT
    robot_control: RobotControlSchema | None = None
    remote_control: RemoteControlSchema

class Parameters(Property):
    'Current operating configuration or control regime'

class VideoConfigSchema(Parameters):
    protocol: VideoProtocol | None = None
    port: int | None = None
    stream_url: str | None = None
    overlay_url: str | None = None
    webrtc_url: str | None = None
    overlay_webrtc_url: str | None = None
    hls_url: str | None = None

class ReceiverConfig(Parameters):
    rx_min_usec: int
    rx_max_usec: int
    rx_center_usec: int

class ChannelMapEntry(Parameters):
    axis: ControlAxis
    source_channel: int
    output_channel: int | None = None
    label: str | None = None

class ModeRange(Parameters):
    mode_id: int | None = None
    mode_name: str | None = None
    channel: int
    range: NumericRange

class RobotControlSchema(Parameters):
    control_modes: RobotControlMode | None = None
    autopilot: bool | None = None
    autopilot_controller_model: str = ''
    autopilot_type: AutopilotType | None = None
    autopilot_fw: FirmwareInfo | None = None

class RemoteControlSchema(Interface):
    links: dict[str, LinkSchema]
    rc_link: str = ''
    vid_link: str = ''
    ctrl_video_sep: bool | None = None
    telemetry: TelemetryState | None = None
    rc_telemetry: ControlAxisSet | None = None
    control_input: ControlAxisSet | None = None
    control_output: ControlAxisSet | None = None
    control_override: ControlOverride | None = None
    receiver_config: ReceiverConfig | None = None
    channel_map: list[ChannelMapEntry]
    mode_ranges: list[ModeRange]

class FlightControlState(Guidance):
    armed: bool | None = None
    in_air: bool | None = None
    override_active: bool | None = None
    failsafe: bool | None = None
    active_modes: list[int]
    active_mode_names: list[str]
    nav_state_code: int | None = None
    flight_mode: str | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None
    plan_progress: PlanProgress | None = None
    navigation_validity: NavigationValidity | None = None
    readiness: VehicleReadinessState | None = None
    controller_identity: FlightControllerIdentity | None = None
    runtime_load: RuntimeLoadState | None = None
