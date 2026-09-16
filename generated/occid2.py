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

class Domain(SemanticAxis):
    _axis_name = 'Domain'
    _cardinality = 'one'
    _applies = None

Domain.LAND = AxisValue('Domain', 'LAND')
Domain.AIR = AxisValue('Domain', 'AIR')
Domain.SEA = AxisValue('Domain', 'SEA')
Domain.UNDERSEA = AxisValue('Domain', 'UNDERSEA')
Domain.SPACE = AxisValue('Domain', 'SPACE')
Domain.CYBER = AxisValue('Domain', 'CYBER')

class MachineKind(SemanticAxis):
    _axis_name = 'MachineKind'
    _cardinality = 'one'
    _applies = {'all': ['Machine']}

MachineKind.VEHICLE = AxisValue('MachineKind', 'VEHICLE')
MachineKind.ROBOT = AxisValue('MachineKind', 'ROBOT')

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
    _applies = {'all': ['Machine', 'Domain.AIR']}

Airframe.MULTIROTOR = AxisValue('Airframe', 'MULTIROTOR')
Airframe.FIXED_WING = AxisValue('Airframe', 'FIXED_WING')
Airframe.VTOL = AxisValue('Airframe', 'VTOL')

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

@dataclass(kw_only=True)
class Root(SemanticModel):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Object(Root):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Entity(Object):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    uid: str
    name: str | None = None

@dataclass(kw_only=True)
class Actor(Entity):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Actor'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Person(Actor):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Actor', 'Substrate.BIOLOGICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('role',)
    role: str | None = None

@dataclass(kw_only=True)
class Machine(Entity):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('serial_number',)
    serial_number: str | None = None

@dataclass(kw_only=True)
class Robot(Machine):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class GroundRobot(Robot):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT', 'Domain.LAND', 'Controller.UNMANNED', 'Locomotion.SELF_PROPELLED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    model: str | None = None

@dataclass(kw_only=True)
class Drone(Robot):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT', 'Domain.AIR', 'Controller.UNMANNED', 'Locomotion.SELF_PROPELLED', 'Airframe.MULTIROTOR'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    model: str | None = None

@dataclass(kw_only=True)
class Location(Object):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Location'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Mark(Location):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Object', 'Location'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    uid: str
    name: str | None = None

@dataclass(kw_only=True)
class Data(Root):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class State(Data):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Position(State):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Position'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Existence(State):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Existence'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Connectivity(State):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Connectivity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Identity(State):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Identity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Classification(State):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Classification'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class GlobalPosition(Position):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Data', 'State', 'Position', 'Frame.WGS84'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('lat', 'lon', 'alt_m')
    lat: float
    lon: float
    alt_m: float

@dataclass(kw_only=True)
class Control(Root):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Control'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Directive(Control):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Task(Directive):
    _semantic_role: ClassVar[str] = 'concept'
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'instruction', 'objective_uid', 'constraints', 'preconditions', 'priority', 'status')
    uid: str
    instruction: str
    objective_uid: str | None = None
    constraints: list[str] = field(default_factory=list)
    preconditions: list[str] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

@dataclass(kw_only=True)
class TaskManeuver(Task):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: ManeuverIntent

@dataclass(kw_only=True)
class TaskInformation(Task):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: InformationIntent

@dataclass(kw_only=True)
class TaskEffect(Task):
    _semantic_role: ClassVar[str] = 'representation'
    _semantics: ClassVar = product_names(['Root', 'Control', 'Directive', 'Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    intent: EffectIntent

Destination = RelationType('Destination', (Task, Location))

REGISTRY_SPEC = {'axes': {'Substrate': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL']}, 'Domain': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE', 'CYBER']}, 'MachineKind': {'semantic_role': 'axis', 'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['VEHICLE', 'ROBOT']}, 'Controller': {'semantic_role': 'axis', 'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'semantic_role': 'axis', 'cardinality': 'one', 'applies': {'all': ['Machine', 'Domain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING', 'VTOL']}, 'Frame': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['WGS84', 'LOCAL', 'BODY']}, 'BloodGroup': {'semantic_role': 'axis', 'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'values': ['A_POS', 'A_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'semantic_role': 'axis', 'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'semantic_role': 'axis', 'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity']}, 'values': ['TRUE', 'FALSE']}}, 'models': {'Root': {'semantic_role': 'concept', 'parent': None, 'semantics': ['Root'], 'fields': []}, 'Object': {'semantic_role': 'concept', 'parent': 'Root', 'semantics': ['Root', 'Object'], 'fields': []}, 'Entity': {'semantic_role': 'concept', 'parent': 'Object', 'semantics': ['Root', 'Object', 'Entity'], 'fields': ['uid', 'name']}, 'Actor': {'semantic_role': 'concept', 'parent': 'Entity', 'semantics': ['Root', 'Object', 'Entity', 'Actor'], 'fields': []}, 'Person': {'semantic_role': 'representation', 'parent': 'Actor', 'semantics': ['Root', 'Object', 'Entity', 'Actor', 'Substrate.BIOLOGICAL'], 'fields': ['role']}, 'Machine': {'semantic_role': 'concept', 'parent': 'Entity', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL'], 'fields': ['serial_number']}, 'Robot': {'semantic_role': 'concept', 'parent': 'Machine', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT'], 'fields': []}, 'GroundRobot': {'semantic_role': 'representation', 'parent': 'Robot', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT', 'Domain.LAND', 'Controller.UNMANNED', 'Locomotion.SELF_PROPELLED'], 'fields': ['model']}, 'Drone': {'semantic_role': 'representation', 'parent': 'Robot', 'semantics': ['Root', 'Object', 'Entity', 'Machine', 'Substrate.MECHANICAL', 'Robot', 'MachineKind.ROBOT', 'Domain.AIR', 'Controller.UNMANNED', 'Locomotion.SELF_PROPELLED', 'Airframe.MULTIROTOR'], 'fields': ['model']}, 'Location': {'semantic_role': 'concept', 'parent': 'Object', 'semantics': ['Root', 'Object', 'Location'], 'fields': []}, 'Mark': {'semantic_role': 'representation', 'parent': 'Location', 'semantics': ['Root', 'Object', 'Location'], 'fields': ['uid', 'name']}, 'Data': {'semantic_role': 'concept', 'parent': 'Root', 'semantics': ['Root', 'Data'], 'fields': []}, 'State': {'semantic_role': 'concept', 'parent': 'Data', 'semantics': ['Root', 'Data', 'State'], 'fields': []}, 'Position': {'semantic_role': 'concept', 'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Position'], 'fields': []}, 'Existence': {'semantic_role': 'concept', 'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Existence'], 'fields': []}, 'Connectivity': {'semantic_role': 'concept', 'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Connectivity'], 'fields': []}, 'Identity': {'semantic_role': 'concept', 'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Identity'], 'fields': []}, 'Classification': {'semantic_role': 'concept', 'parent': 'State', 'semantics': ['Root', 'Data', 'State', 'Classification'], 'fields': []}, 'GlobalPosition': {'semantic_role': 'representation', 'parent': 'Position', 'semantics': ['Root', 'Data', 'State', 'Position', 'Frame.WGS84'], 'fields': ['lat', 'lon', 'alt_m']}, 'Control': {'semantic_role': 'concept', 'parent': 'Root', 'semantics': ['Root', 'Control'], 'fields': []}, 'Directive': {'semantic_role': 'concept', 'parent': 'Control', 'semantics': ['Root', 'Control', 'Directive'], 'fields': []}, 'Task': {'semantic_role': 'concept', 'parent': 'Directive', 'semantics': ['Root', 'Control', 'Directive', 'Task'], 'fields': ['uid', 'instruction', 'objective_uid', 'constraints', 'preconditions', 'priority', 'status']}, 'TaskManeuver': {'semantic_role': 'representation', 'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task'], 'fields': ['intent']}, 'TaskInformation': {'semantic_role': 'representation', 'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task'], 'fields': ['intent']}, 'TaskEffect': {'semantic_role': 'representation', 'parent': 'Task', 'semantics': ['Root', 'Control', 'Directive', 'Task'], 'fields': ['intent']}}, 'codewords': {'ManeuverIntent.MOVE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position'], 'ManeuverIntent.HOLD': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position'], 'InformationIntent.LOCATE': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Position'], 'InformationIntent.TRACK': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN', 'Data', 'State', 'Position'], 'InformationIntent.IDENTIFY': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Identity'], 'InformationIntent.CLASSIFY': ['Root', 'Control', 'Directive', 'Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Classification'], 'EffectIntent.CREATE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.TRUE'], 'EffectIntent.REMOVE': ['Root', 'Control', 'Directive', 'Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Data', 'State', 'Existence', 'TruthTarget.FALSE']}, 'relations': {'Destination': ['Task', 'Location']}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)

def new_store() -> Store:
    return Store(REGISTRY)
