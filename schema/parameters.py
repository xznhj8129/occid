"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .properties import Properties

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

class Parameters(Properties):
    pass

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
