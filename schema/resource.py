"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Resource(OCCIDModel):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'
    __occid_model_id__: ClassVar[int] = 222
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'State'
    __occid_children__: ClassVar[tuple[str, ...]] = ('FuelState', 'Supplies', 'PowerSource', 'PowerState', 'ElectricalResourceState')

class FuelState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 92
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    fuel_type: FuelType
    capacity: builtins.float | None = None
    remaining: builtins.float | None = None

class Supplies(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 253
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    fuel: Semantic[FuelState] | None = None
    stores: list[Semantic[ItemCount]]

class PowerSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 205
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_ref: builtins.str
    power_type: PowerType
    status: PowerStatus
    remaining_pct: builtins.float | None = None

class PowerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 206
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    status: PowerStatus
    sources: list[Semantic[PowerSource]]
    electrical_sources: list[Semantic[ElectricalResourceState]]

class ElectricalResourceState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 69
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Resource'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    source_uid: Semantic[UID] | None = None
    voltage_v: builtins.float | None = None
    current_a: builtins.float | None = None
    power_w: builtins.float | None = None
    consumed_mah: builtins.float | None = None
    consumed_mwh: builtins.float | None = None
    consumed_ah: builtins.float | None = None
    remaining_pct: builtins.float | None = None
    remaining_capacity: builtins.float | None = None
    temperature_deg_c: builtins.float | None = None
