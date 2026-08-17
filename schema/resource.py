"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .state import State

### Models

class Resource(State):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'
    __occid_model_id__: ClassVar[int] = 184
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class FuelState(Resource):
    __occid_model_id__: ClassVar[int] = 185
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    fuel_type: FuelType
    capacity: builtins.float | None = None
    remaining: builtins.float | None = None

class SuppliesSchema(Resource):
    __occid_model_id__: ClassVar[int] = 186
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    fuel: FuelState | None = None
    stores: list[ItemCount]

class PowerSourceSchema(Resource):
    __occid_model_id__: ClassVar[int] = 187
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    source_id: StringID
    power_type: PowerType
    status: PowerStatus
    remaining_pct: builtins.float | None = None

class PowerStateSchema(Resource):
    __occid_model_id__: ClassVar[int] = 188
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    status: PowerStatus
    sources: list[PowerSourceSchema]
    electrical_sources: list[ElectricalResourceState]

class ElectricalResourceState(Resource):
    __occid_model_id__: ClassVar[int] = 189
    __occid_semantic_role__: ClassVar[str] = 'specialization'
    source_id: StringID | None = None
    voltage_v: builtins.float | None = None
    current_a: builtins.float | None = None
    power_w: builtins.float | None = None
    consumed_mah: builtins.float | None = None
    consumed_mwh: builtins.float | None = None
    consumed_ah: builtins.float | None = None
    remaining_pct: builtins.float | None = None
    remaining_capacity: builtins.float | None = None
    temperature_deg_c: builtins.float | None = None
