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
    __occid_parent__: ClassVar[str | None] = 'AirMachine'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Drone',)
    capabilities: list[Semantic[Capability]] | None = None
    uid: Semantic[ID]
    node_uids: list[Semantic[ID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    side: Semantic[ID] | None = None
    identity: StandardIdentity
    symbology: Semantic[Symbology] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[Semantic[EntityComponentRef]]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[AirNavigation]
    controller: Semantic[RobotController]
    remote_control: Semantic[RemoteControl]
    telemetry_type: TelemetryType

class Drone(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 82
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AirRobot'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    uid: Semantic[ID]
    node_uids: list[Semantic[ID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    side: Semantic[ID] | None = None
    identity: StandardIdentity
    symbology: Semantic[Symbology] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType = MachineType.ROBOT
    components: list[Semantic[EntityComponentRef]]
    airframe: AirframeType = AirframeType.COPTER
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[AirNavigation]
    controller: Semantic[RobotController]
    remote_control: Semantic[RemoteControl]
    telemetry_type: TelemetryType
