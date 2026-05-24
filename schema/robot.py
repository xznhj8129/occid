"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

### Enums

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

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GUIDE = auto()
    FULL = auto()

class ControlAxis(IntEnum):
    ROLL = 0
    PITCH = auto()
    YAW = auto()
    THROTTLE = auto()
    AUX = auto()

class FlightCommandType(IntEnum):
    ARM = 0
    DISARM = auto()
    TAKEOFF = auto()
    LAND = auto()
    RETURN_TO_LAUNCH = auto()
    SET_MODE = auto()
    GOTO = auto()
    SET_TAKEOFF_ALTITUDE = auto()
    SELECT_MISSION = auto()
    START_OFFBOARD = auto()
    STOP_OFFBOARD = auto()

### Models

class SoftwareBuildInfo(OCCIDModel):
    major: int | None = None
    minor: int | None = None
    patch: int | None = None
    git_hash: str | None = None
    version: str | None = None

class HardwareIdentity(OCCIDModel):
    hardware_uid: str | None = None
    legacy_uid: str | None = None
    vendor_id: int | None = None
    vendor_name: str | None = None
    product_id: int | None = None
    product_name: str | None = None
    board_info: str | None = None

class FlightControllerIdentity(OCCIDModel):
    api_version: str | None = None
    controller_variant: str | None = None
    hardware: HardwareIdentity | None = None
    flight_software: SoftwareBuildInfo | None = None
    os_software: SoftwareBuildInfo | None = None

class ControlAxisSet(OCCIDModel):
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None
    throttle: float | None = None
    aux: list[float]

class ControlChannelValue(OCCIDModel):
    channel_index: int
    value: float | None = None

class ControlOverride(OCCIDModel):
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None
    throttle: float | None = None
    aux: list[ControlChannelValue]

class ControlAttitudeSetpoint(OCCIDModel):
    roll_deg: float
    pitch_deg: float
    yaw_deg: float
    thrust_value: float

class ReceiverConfig(OCCIDModel):
    rx_min_usec: int | None = None
    rx_max_usec: int | None = None
    rx_center_usec: int | None = None

class ChannelMapEntry(OCCIDModel):
    axis: ControlAxis
    source_channel: int
    output_channel: int | None = None
    label: str | None = None

class ModeRange(OCCIDModel):
    mode_id: int | None = None
    mode_name: str | None = None
    channel: int
    range: NumericRange

class FlightControlState(OCCIDModel):
    armed: bool | None = None
    in_air: bool | None = None
    override_active: bool | None = None
    failsafe: bool | None = None
    active_modes: list[int]
    active_mode_names: list[str]
    nav_state_code: int | None = None
    flight_mode: str | None = None
    attitude_setpoint: ControlAttitudeSetpoint | None = None
    mission_progress: MissionProgress | None = None
    navigation_validity: NavigationValidity | None = None
    readiness: VehicleReadinessState | None = None
    controller_identity: FlightControllerIdentity | None = None
    runtime_load: RuntimeLoadState | None = None

class RobotControlSchema(OCCIDModel):
    control_modes: RobotControlMode | None = None
    autopilot: bool | None = None
    autopilot_controller_model: str = ''
    autopilot_type: AutopilotType | None = None
    autopilot_fw: FirmwareInfo | None = None

class RemoteControlSchema(OCCIDModel):
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

class ControlLease(OCCIDModel):
    asset_id: str
    holder_id: str
    control_level: ControlLevel
    lease_start: float
    lease_end: float
    lease_rev: int = 0
