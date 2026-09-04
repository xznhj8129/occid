"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain
from .entities import AirframeType, EntityType, MachineType

### Models

class AirRobot(OCCIDModel):
    'Any type of flying drone'
    __occid_model_id__: ClassVar[int] = 7
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
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[EntityComponentRef]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, SensorPayload]
    navigation: AirNavigationSchema
    controller: RobotController
    remote_control: RemoteControlSchema

class Drone(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 56
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
    metadata: dict[builtins.str, MetadataValue]
    relations: list[DirectedRelationship]
    symbology: SymbologySchema | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[EntityComponentRef]
    airframe: AirframeType = AirframeType.COPTER
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, SensorPayload]
    navigation: AirNavigationSchema
    controller: RobotController
    remote_control: RemoteControlSchema
