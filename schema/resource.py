"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Resource(OCCIDModel):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'
    __occid_model_id__: ClassVar[int] = 316
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('ResourceHolding', 'InventoryState', 'FuelState', 'PowerSource', 'PowerState', 'ElectricalResourceState')

class ResourceHolding(OCCIDModel):
    'Current quantity of an identified resource definition held by a subject, separated from authorized or required quantity'
    __occid_model_id__: ClassVar[int] = 318
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
    __occid_model_id__: ClassVar[int] = 363
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'InventoryState'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    holdings: list[Semantic[ResourceHolding]]
    fuel: Semantic[FuelState] | None = None

class PowerSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 293
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_uid: Semantic[UID] | None = None
    power_type: PowerType
    status: PowerStatus
    remaining_ratio: Semantic[NormalizedRatio] | None = None

class PowerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 294
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
