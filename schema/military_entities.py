"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .definition import OperationalDomain
from .entities import EntityType, PropulsionType

### Models

class MilitaryPerson(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 164
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Person'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.PERSON
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    role: builtins.str
    op_domain: OperationalDomain = OperationalDomain.LAND
    propulsion: PropulsionType = PropulsionType.FOOT
    navigation: NavigationMode
    navaids: list[NavAids]
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    attack_modes: list[AttackMode]
    weapons: list[Semantic[ItemCount]]
    ammo: list[Semantic[ItemCount]]

class MilitaryMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 162
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Machine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]
    category: NATOUnitCategory | None = None

class MilitaryGroundMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 161
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'GroundMachine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType
    components: list[Semantic[EntityComponentRef]]
    op_domain: OperationalDomain = OperationalDomain.LAND
    model: builtins.str
    role: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[GroundNavigation]
    payload: Semantic[Payload]
    effects: Semantic[GroundEffects]

class MilitaryAirMachine(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 159
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'AirMachine'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('Entity')]
    node_uids: list[Semantic[UID]]
    name: builtins.str | None = None
    callsign: builtins.str | None = None
    entity_type: EntityType = EntityType.MACHINE
    tags: list[builtins.str]
    metadata: dict[builtins.str, Semantic[MetadataValue]]
    relations: list[Semantic[DirectedRelationship]]
    symbology: Semantic[Symbology] | None = None
    display_meta: Semantic[DisplayMeta] | None = None
    serial_number: builtins.str | None = None
    propulsion: PropulsionType
    machine_type: MachineType | None = None
    components: list[Semantic[EntityComponentRef]]
    airframe: AirframeType
    op_domain: OperationalDomain = OperationalDomain.AIR
    model: builtins.str
    sensors: dict[builtins.str, Semantic[SensorPayload]]
    navigation: Semantic[AirNavigation]
    payload: Semantic[Payload]
    effects: Semantic[AirEffects]
