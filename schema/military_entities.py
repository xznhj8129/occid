"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain
from .entities import EntityType, PropulsionType

### Models

class MilitaryPerson(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 152
    __occid_semantic_role__: ClassVar[str] = 'representation'
    capabilities: list[Capability] | None = None
    record: Record
    uid: UID
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[UID]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.PERSON
    tags: list[builtins.str]
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    role: builtins.str
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    attack_modes: list[AttackMode]
    weapons: list[ItemCount]
    ammo: list[ItemCount]

class MilitaryMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 150
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
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 149
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
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType
    components: list[EntityComponentRef]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: GroundNavigation
    payload: SerializeAsAny[Payload | SensorPayload | ImageSensor | RFSensor | EffectsPayload]
    effects: GroundEffects

class MilitaryAirMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 147
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
    metadata: dict[builtins.str, SerializeAsAny[MetadataValue | MeasurementQuality]]
    relations: list[DirectedRelationship]
    symbology: Symbology | None = None
    display_meta: DisplayMeta | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[EntityComponentRef]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, SerializeAsAny[SensorPayload | ImageSensor | RFSensor]]
    navigation: SerializeAsAny[AirNavigation | MilitaryAirNavigation]
    payload: SerializeAsAny[Payload | SensorPayload | ImageSensor | RFSensor | EffectsPayload]
    effects: AirEffects
