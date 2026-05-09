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

### Models

class RobotControlSchema(SigmaModel):
    control_modes: RobotControlMode | None = None
    autopilot: bool | None = None
    autopilot_controller_model: str = '""'
    autopilot_type: AutopilotType | None = None
    autopilot_fw: FirmwareInfo | None = None

class RemoteControlSchema(SigmaModel):
    links: dict[str, LinkSchema] = Field(default_factory=dict)
    rc_link: str = '""'
    vid_link: str = '""'
    ctrl_video_sep: bool | None = None
    telemetry: TelemetryState | None = None

class ControlLease(SigmaModel):
    asset_id: str
    holder_id: str
    control_level: ControlLevel
    lease_start: float
    lease_end: float
    lease_rev: int = '0'
