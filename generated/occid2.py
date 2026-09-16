# GENERATED FILE - DO NOT EDIT
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from runtime import (
    AxisValue,
    RelationType,
    SemanticAxis,
    SemanticEnum,
    SemanticModel,
    SemanticRegistry,
    Store,
    product_names,
)

class Substrate(SemanticAxis):
    _axis_name = 'Substrate'
    _cardinality = 'one'
    _applies = None

Substrate.BIOLOGICAL = AxisValue('Substrate', 'BIOLOGICAL')
Substrate.MECHANICAL = AxisValue('Substrate', 'MECHANICAL')
Substrate.CYBER = AxisValue('Substrate', 'CYBER')

class PhysicalDomain(SemanticAxis):
    _axis_name = 'PhysicalDomain'
    _cardinality = 'one'
    _applies = None

PhysicalDomain.LAND = AxisValue('PhysicalDomain', 'LAND')
PhysicalDomain.AIR = AxisValue('PhysicalDomain', 'AIR')
PhysicalDomain.SEA = AxisValue('PhysicalDomain', 'SEA')
PhysicalDomain.UNDERSEA = AxisValue('PhysicalDomain', 'UNDERSEA')
PhysicalDomain.SPACE = AxisValue('PhysicalDomain', 'SPACE')

class Controller(SemanticAxis):
    _axis_name = 'Controller'
    _cardinality = 'one'
    _applies = {'all': ['Machine']}

Controller.MANNED = AxisValue('Controller', 'MANNED')
Controller.UNMANNED = AxisValue('Controller', 'UNMANNED')

class Locomotion(SemanticAxis):
    _axis_name = 'Locomotion'
    _cardinality = 'one'
    _applies = None

Locomotion.SELF_PROPELLED = AxisValue('Locomotion', 'SELF_PROPELLED')
Locomotion.EXTERNAL = AxisValue('Locomotion', 'EXTERNAL')
Locomotion.STATIC = AxisValue('Locomotion', 'STATIC')

class Airframe(SemanticAxis):
    _axis_name = 'Airframe'
    _cardinality = 'one'
    _applies = {'all': ['Machine', 'PhysicalDomain.AIR']}

Airframe.MULTIROTOR = AxisValue('Airframe', 'MULTIROTOR')
Airframe.FIXED_WING = AxisValue('Airframe', 'FIXED_WING')

class Frame(SemanticAxis):
    _axis_name = 'Frame'
    _cardinality = 'one'
    _applies = None

Frame.WGS84 = AxisValue('Frame', 'WGS84')
Frame.LOCAL = AxisValue('Frame', 'LOCAL')
Frame.BODY = AxisValue('Frame', 'BODY')

class BloodGroup(SemanticAxis):
    _axis_name = 'BloodGroup'
    _cardinality = 'one'
    _applies = {'all': ['Substrate.BIOLOGICAL']}

BloodGroup.A_POS = AxisValue('BloodGroup', 'A_POS')
BloodGroup.A_NEG = AxisValue('BloodGroup', 'A_NEG')
BloodGroup.B_POS = AxisValue('BloodGroup', 'B_POS')
BloodGroup.B_NEG = AxisValue('BloodGroup', 'B_NEG')
BloodGroup.AB_POS = AxisValue('BloodGroup', 'AB_POS')
BloodGroup.AB_NEG = AxisValue('BloodGroup', 'AB_NEG')
BloodGroup.O_POS = AxisValue('BloodGroup', 'O_POS')
BloodGroup.O_NEG = AxisValue('BloodGroup', 'O_NEG')

class Realm(SemanticAxis):
    _axis_name = 'Realm'
    _cardinality = 'one'
    _applies = None

Realm.WORLD = AxisValue('Realm', 'WORLD')
Realm.INFORMATION = AxisValue('Realm', 'INFORMATION')

class TemporalMode(SemanticAxis):
    _axis_name = 'TemporalMode'
    _cardinality = 'one'
    _applies = None

TemporalMode.ACHIEVE = AxisValue('TemporalMode', 'ACHIEVE')
TemporalMode.MAINTAIN = AxisValue('TemporalMode', 'MAINTAIN')

class TruthTarget(SemanticAxis):
    _axis_name = 'TruthTarget'
    _cardinality = 'one'
    _applies = {'any': ['Existence', 'Connectivity']}

TruthTarget.TRUE = AxisValue('TruthTarget', 'TRUE')
TruthTarget.FALSE = AxisValue('TruthTarget', 'FALSE')

class ManeuverIntent(SemanticEnum):
    MOVE = 0
    HOLD = 1

ManeuverIntent._semantic_map = {
    'MOVE': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position']),
    'HOLD': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position']),
}

class InformationIntent(SemanticEnum):
    LOCATE = 0
    TRACK = 1
    IDENTIFY = 2
    CLASSIFY = 3

InformationIntent._semantic_map = {
    'LOCATE': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position']),
    'TRACK': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position']),
    'IDENTIFY': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Identity']),
    'CLASSIFY': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Classification']),
}

class EffectIntent(SemanticEnum):
    CREATE = 0
    REMOVE = 1

EffectIntent._semantic_map = {
    'CREATE': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.TRUE']),
    'REMOVE': product_names(['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.FALSE']),
}

class TaskPriority(SemanticEnum):
    ROUTINE = 0
    HIGH = 1
    IMMEDIATE = 2

TaskPriority._semantic_map = {
}

class TaskStatus(SemanticEnum):
    NEW = 0
    ACTIVE = 1
    COMPLETE = 2
    FAILED = 3
    CANCELLED = 4

TaskStatus._semantic_map = {
}

AirMission = product_names(['Root', 'Control', 'Directive', 'Mission', 'PhysicalDomain.AIR'])

AirTask = product_names(['Root', 'Control', 'Directive', 'Task', 'PhysicalDomain.AIR'])

UGV = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'])

UAV = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'])

Drone = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'])

@dataclass(kw_only=True)
class Root(SemanticModel):
    _semantics: ClassVar = product_names(['Root'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Object(Root):
    _semantics: ClassVar = product_names(['Root', 'Object'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Locality(Object):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Locality'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    name: str | None = None

@dataclass(kw_only=True)
class Entity(Object):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    uid: str
    name: str | None = None

@dataclass(kw_only=True)
class Biological(Entity):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Person(Biological):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL', 'Person'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    name: str | None = None

@dataclass(kw_only=True)
class Actor(Person):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL', 'Person', 'Actor'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('role',)
    role: str | None = None

@dataclass(kw_only=True)
class Machine(Entity):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('serial_number',)
    serial_number: str | None = None

@dataclass(kw_only=True)
class Vehicle(Machine):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    model: str | None = None

@dataclass(kw_only=True)
class CrewedVehicle(Vehicle):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class UnmannedVehicle(Vehicle):
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Data(Root):
    _semantics: ClassVar = product_names(['Root', 'Data'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class State(Data):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Mark(Data):
    _semantics: ClassVar = product_names(['Root', 'Data', 'Mark', 'State', 'Position', 'GlobalPosition', 'Frame.WGS84'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    uid: str
    name: str | None = None

@dataclass(kw_only=True)
class Position(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Position'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Altitude(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Altitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('m',)
    m: float

@dataclass(kw_only=True)
class Existence(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Existence'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Connectivity(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Connectivity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Identity(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Identity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Classification(State):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Classification'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class GlobalPosition(Position):
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Position', 'GlobalPosition', 'Frame.WGS84'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('lat', 'lon', 'alt_m')
    lat: float
    lon: float
    alt_m: float

@dataclass(kw_only=True)
class Control(Root):
    _semantics: ClassVar = product_names(['Root', 'Control'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Directive(Control):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Task(Directive):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'instruction', 'objective_uid', 'priority', 'status')
    uid: str
    instruction: str
    objective_uid: str | None = None
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

@dataclass(kw_only=True)
class Mission(Directive):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Mission'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class TaskManeuver(Task):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task', 'TaskManeuver'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: ManeuverIntent

@dataclass(kw_only=True)
class TaskInformation(Task):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task', 'TaskInformation'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: InformationIntent

@dataclass(kw_only=True)
class TaskEffect(Task):
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task', 'TaskEffect'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: EffectIntent

Destination = RelationType('Destination', (Task, Position))
Target = RelationType('Target', (Task, Entity))
AssignedWork = RelationType('AssignedWork', (Entity, Task))

REGISTRY_SPEC = {'axes': {'Substrate': {'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL', 'CYBER']}, 'PhysicalDomain': {'description': 'Existing domain; a bounded thing operates in exactly one.', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE']}, 'Controller': {'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'description': 'Simplified airframe construction, independent of takeoff capability.', 'cardinality': 'one', 'applies': {'all': ['Machine', 'PhysicalDomain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING']}, 'Frame': {'cardinality': 'one', 'values': ['WGS84', 'LOCAL', 'BODY']}, 'BloodGroup': {'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'requires': ['Biological'], 'values': ['A_POS', 'A_NEG', 'B_POS', 'B_NEG', 'AB_POS', 'AB_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity']}, 'values': ['TRUE', 'FALSE']}}, 'models': {'Root': {'parent': None, 'semantics': ['Root'], 'fields': []}, 'Object': {'parent': 'Root', 'semantics': ['Root', 'Object'], 'fields': []}, 'Locality': {'parent': 'Object', 'semantics': ['Root', 'Object', 'Locality'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None}]}, 'Entity': {'parent': 'Object', 'semantics': ['Root', 'Object', 'Entity'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional string', 'default': None}]}, 'Biological': {'parent': 'Entity', 'semantics': ['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL'], 'fields': []}, 'Person': {'parent': 'Biological', 'semantics': ['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL', 'Person'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None}]}, 'Actor': {'parent': 'Person', 'semantics': ['Root', 'Object', 'Entity', 'Biological', 'Substrate.BIOLOGICAL', 'Person', 'Actor'], 'fields': [{'name': 'role', 'type': 'optional string', 'default': None}]}, 'Machine': {'parent': 'Entity', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL'], 'fields': [{'name': 'serial_number', 'type': 'optional string', 'default': None}]}, 'Vehicle': {'parent': 'Machine', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'], 'fields': [{'name': 'model', 'type': 'optional string', 'default': None}]}, 'CrewedVehicle': {'parent': 'Vehicle', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'], 'fields': []}, 'UnmannedVehicle': {'parent': 'Vehicle', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'], 'fields': []}, 'Data': {'parent': 'Root', 'semantics': ['Root', 'Data'], 'fields': []}, 'State': {'parent': 'Data', 'semantics': ['Root', 'Data', 'State'], 'fields': []}, 'Mark': {'parent': 'Data', 'semantics': ['Root', 'Data', 'Mark', 'State', 'Position', 'GlobalPosition', 'Frame.WGS84'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional string', 'default': None}]}, 'Position': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Position'], 'fields': []}, 'Altitude': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Altitude'], 'fields': [{'name': 'm', 'type': 'float', 'default': None}], 'applies': ['PhysicalDomain.AIR']}, 'Existence': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Existence'], 'fields': []}, 'Connectivity': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Connectivity'], 'fields': []}, 'Identity': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Identity'], 'fields': []}, 'Classification': {'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Classification'], 'fields': []}, 'GlobalPosition': {'parent': 'Position', 'semantics': ['Root', 'Data', 'State', 'Position', 'GlobalPosition', 'Frame.WGS84'], 'fields': [{'name': 'lat', 'type': 'float', 'default': None}, {'name': 'lon', 'type': 'float', 'default': None}, {'name': 'alt_m', 'type': 'float', 'default': None}]}, 'Control': {'parent': 'Root', 'semantics': ['Root', 'Control'], 'fields': []}, 'Directive': {'parent': 'Control', 'semantics': ['Root', 'Control', 'Directive'], 'fields': []}, 'Task': {'parent': 'Directive', 'semantics': ['Root', 'Control', 'Directive', 'Task'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'instruction', 'type': 'string', 'default': None}, {'name': 'objective_uid', 'type': 'optional UID', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE'}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW'}]}, 'Mission': {'parent': 'Directive', 'semantics': ['Root', 'Control', 'Directive', 'Mission'], 'fields': []}, 'TaskManeuver': {'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task', 'TaskManeuver'], 'fields': [{'name': 'intent', 'type': 'ManeuverIntent', 'default': None}]}, 'TaskInformation': {'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task', 'TaskInformation'], 'fields': [{'name': 'intent', 'type': 'InformationIntent', 'default': None}]}, 'TaskEffect': {'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task', 'TaskEffect'], 'fields': [{'name': 'intent', 'type': 'EffectIntent', 'default': None}]}}, 'codewords': {'ManeuverIntent.MOVE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position'], 'ManeuverIntent.HOLD': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position'], 'InformationIntent.LOCATE': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position'], 'InformationIntent.TRACK': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position'], 'InformationIntent.IDENTIFY': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Identity'], 'InformationIntent.CLASSIFY': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Classification'], 'EffectIntent.CREATE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.TRUE'], 'EffectIntent.REMOVE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.FALSE']}, 'codeword_relations': {'ManeuverIntent.MOVE': 'Destination', 'ManeuverIntent.HOLD': 'Destination', 'InformationIntent.LOCATE': 'Target', 'InformationIntent.TRACK': 'Target', 'InformationIntent.IDENTIFY': 'Target', 'InformationIntent.CLASSIFY': 'Target', 'EffectIntent.CREATE': 'Target', 'EffectIntent.REMOVE': 'Target'}, 'aliases': {'AirMission': ['Root', 'Control', 'Directive', 'Mission', 'PhysicalDomain.AIR'], 'AirTask': ['Root', 'Control', 'Directive', 'Task', 'PhysicalDomain.AIR'], 'UGV': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'], 'UAV': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'], 'Drone': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR']}, 'relations': {'Destination': {'signature': ['Task', 'Position'], 'operand_names': [], 'specializes': None}, 'Target': {'signature': ['Task', 'Entity'], 'operand_names': [], 'specializes': None}, 'AssignedWork': {'signature': ['Entity', 'Task'], 'operand_names': [], 'specializes': None}}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)

def new_store() -> Store:
    return Store(REGISTRY)
