"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class NATOSupplyClass(IntEnum):
    CLASS_I = 0
    CLASS_II = auto()
    CLASS_III = auto()
    CLASS_IV = auto()
    CLASS_V = auto()
    CLASS_VI = auto()
    CLASS_VII = auto()
    CLASS_VIII = auto()
    CLASS_IX = auto()
    CLASS_X = auto()

### Models

class Resource(OCCIDModel):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'
    __occid_model_id__: ClassVar[int] = 313
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ResourceHolding', 'InventoryState', 'FuelState', 'PowerSource', 'PowerState', 'ElectricalResourceState')

class ResourceHolding(OCCIDModel):
    'Current quantity of an identified resource definition held by a subject, separated from authorized or required quantity'
    __occid_model_id__: ClassVar[int] = 315
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    resource_definition_uid: Semantic[UID]
    on_hand: Semantic[Quantity]
    available: Semantic[Quantity] | None = None
    committed: Semantic[Quantity] | None = None

class InventoryState(OCCIDModel):
    'Current holdings of independently defined resources'
    __occid_model_id__: ClassVar[int] = 174
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Supplies',)
    holdings: list[Semantic[ResourceHolding]]

class FuelState(OCCIDModel):
    'Current amount and capacity of a consumable fuel resource in an explicitly declared quantity representation'
    __occid_model_id__: ClassVar[int] = 131
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    fuel_type: FuelType
    capacity: Semantic[Quantity] | None = None
    remaining: Semantic[Quantity] | None = None

class Supplies(OCCIDModel):
    'Supply-oriented inventory state retained as a specialization of generic inventory'
    __occid_model_id__: ClassVar[int] = 361
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'InventoryState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    holdings: list[Semantic[ResourceHolding]]
    fuel: Semantic[FuelState] | None = None

class PowerSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 290
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_uid: Semantic[UID] | None = None
    power_type: PowerType
    status: PowerStatus
    remaining_ratio: Semantic[NormalizedRatio] | None = None

class PowerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 291
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    status: PowerStatus
    sources: list[Semantic[PowerSource]]
    electrical_sources: list[Semantic[ElectricalResourceState]]

class ElectricalResourceState(OCCIDModel):
    'Electrical measurements and remaining storage state for one identified electrical resource'
    __occid_model_id__: ClassVar[int] = 102
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_uid: Semantic[UID] | None = None
    potential: Semantic[Volts] | None = None
    current: Semantic[Amperes] | None = None
    power: Semantic[Watts] | None = None
    consumed_charge: Semantic[AmpereHours] | None = None
    consumed_energy: Semantic[WattHours] | None = None
    remaining_ratio: Semantic[NormalizedRatio] | None = None
    remaining_charge: Semantic[AmpereHours] | None = None
    remaining_energy: Semantic[WattHours] | None = None
    temperature: Semantic[DegreesCelsius] | None = None

class ResourceTemplate(OCCIDModel):
    'Identified definition of a resource kind that can be required, authorized, held, consumed, or assigned'
    __occid_model_id__: ClassVar[int] = 317
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EquipmentTemplate', 'PersonnelTemplate', 'SupplyTemplate')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class EquipmentTemplate(OCCIDModel):
    'Template of equipment counted or allocated as a resource; individual physical equipment may additionally exist as Equipment objects'
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class PersonnelTemplate(OCCIDModel):
    'Template of a personnel category used for strength, staffing, or resource planning'
    __occid_model_id__: ClassVar[int] = 279
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class SupplyTemplate(OCCIDModel):
    'Template of a consumable or stock resource with a customary quantity unit'
    __occid_model_id__: ClassVar[int] = 362
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitarySupplyTemplate',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    quantity_unit: QuantityUnit | None = None

class ResourceRequirement(OCCIDModel):
    'Required or authorized quantity of one resource definition'
    __occid_model_id__: ClassVar[int] = 316
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    resource_definition_uid: Semantic[UID]
    quantity: Semantic[Quantity]

class MilitarySupplyTemplate(OCCIDModel):
    'Military supply definition classified by NATO-style supply class while retaining the generic resource identity and quantity unit'
    __occid_model_id__: ClassVar[int] = 237
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SupplyTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    quantity_unit: QuantityUnit | None = None
    supply_class: NATOSupplyClass
