"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain
from .entities import AirMachine, AirframeType, MachineType

### Models

class AirRobot(AirMachine):
    'Any type of flying drone'
    __occid_model_id__: ClassVar[int] = 252
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    machine_type: MachineType = MachineType.ROBOT
    controller: RobotController
    remote_control: RemoteControlSchema

class Drone(AirRobot):
    __occid_model_id__: ClassVar[int] = 253
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    airframe: AirframeType = AirframeType.COPTER
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    serial_uid: StringID
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: AirNavigationSchema
