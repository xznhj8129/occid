"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class Resource(OCCIDModel):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'
    __occid_model_id__: ClassVar[int] = 207
    __occid_semantic_role__: ClassVar[str] = 'type'

class FuelState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 83
    __occid_semantic_role__: ClassVar[str] = 'representation'
    fuel_type: FuelType
    capacity: builtins.float | None = None
    remaining: builtins.float | None = None

class Supplies(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 235
    __occid_semantic_role__: ClassVar[str] = 'representation'
    fuel: FuelState | None = None
    stores: list[ItemCount]

class PowerSource(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 191
    __occid_semantic_role__: ClassVar[str] = 'representation'
    source_ref: builtins.str
    power_type: PowerType
    status: PowerStatus
    remaining_pct: builtins.float | None = None

class PowerState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 192
    __occid_semantic_role__: ClassVar[str] = 'representation'
    status: PowerStatus
    sources: list[PowerSource]
    electrical_sources: list[ElectricalResourceState]

class ElectricalResourceState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 61
    __occid_semantic_role__: ClassVar[str] = 'representation'
    source_uid: UID | None = None
    voltage_v: builtins.float | None = None
    current_a: builtins.float | None = None
    power_w: builtins.float | None = None
    consumed_mah: builtins.float | None = None
    consumed_mwh: builtins.float | None = None
    consumed_ah: builtins.float | None = None
    remaining_pct: builtins.float | None = None
    remaining_capacity: builtins.float | None = None
    temperature_deg_c: builtins.float | None = None
