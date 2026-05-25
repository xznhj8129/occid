"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .control import Control

### Enums

class ControlLevel(IntEnum):
    NONE = 0
    MONITOR = auto()
    GUIDE = auto()
    FULL = auto()

### Models

class Interface(Control):
    pass

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

class ControlLease(Interface):
    asset_id: str
    holder_id: str
    control_level: ControlLevel
    lease_start: float
    lease_end: float
    lease_rev: int = 0
