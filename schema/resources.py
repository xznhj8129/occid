"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

### Models

class Resources(State):
    'Power, fuel, supply, inventory, payload loadout, capacity, and consumption state.'

class FuelState(Resources):
    fuel_type: FuelType
    capacity: float | None = None
    remaining: float | None = None

class SuppliesSchema(Resources):
    fuel: FuelState | None = None
    stores: list[ItemCount]

class PowerSourceSchema(Resources):
    source_id: str
    power_type: PowerType
    status: PowerStatus
    remaining_pct: float | None = None

class PowerStateSchema(Resources):
    status: PowerStatus
    sources: list[PowerSourceSchema]
    electrical_sources: list[ElectricalResourceState]

class ElectricalResourceState(Resources):
    source_id: str | None = None
    battery_id: int | None = None
    voltage_v: float | None = None
    current_a: float | None = None
    power_w: float | None = None
    consumed_mah: float | None = None
    consumed_mwh: float | None = None
    consumed_ah: float | None = None
    remaining_pct: float | None = None
    remaining_capacity: float | None = None
    temperature_deg_c: float | None = None
    rssi: float | None = None
