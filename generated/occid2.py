# GENERATED FILE - DO NOT EDIT
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, ClassVar

from runtime import (
    AxisValue,
    Equation,
    ExpressionType,
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

class Representation(SemanticAxis):
    _axis_name = 'Representation'
    _cardinality = 'many'
    _applies = None

Representation.Geodetic = AxisValue('Representation', 'Geodetic')
Representation.LocalCartesian = AxisValue('Representation', 'LocalCartesian')
Representation.LocalEuler = AxisValue('Representation', 'LocalEuler')
Representation.Quaternion = AxisValue('Representation', 'Quaternion')

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
    'MOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'HOLD': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
}

class InformationIntent(SemanticEnum):
    LOCATE = 0
    TRACK = 1
    IDENTIFY = 2
    CLASSIFY = 3

InformationIntent._semantic_map = {
    'LOCATE': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'TRACK': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN']),
    'IDENTIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'CLASSIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
}

class EffectIntent(SemanticEnum):
    CREATE = 0
    REMOVE = 1

EffectIntent._semantic_map = {
    'CREATE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE']),
    'REMOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE']),
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

MOVE = ExpressionType(
    'MOVE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']), 
    given={'actor': product_names(['Entity']), 'destination': product_names(['Position'])},
    sought={},
    equations=(Equation('Position', 'actor', 'destination'),),
    words=('ManeuverIntent.MOVE',),
)

HOLD = ExpressionType(
    'HOLD',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']), 
    given={'actor': product_names(['Entity']), 'destination': product_names(['Position'])},
    sought={},
    equations=(Equation('Position', 'actor', 'destination'),),
    words=('ManeuverIntent.HOLD',),
)

LOCATE = ExpressionType(
    'LOCATE',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']), 
    given={'target': product_names(['Entity'])},
    sought={'position': product_names(['Position'])},
    equations=(Equation('Position', 'target', 'position'),),
    words=('InformationIntent.LOCATE',),
)

TRACK = ExpressionType(
    'TRACK',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN']), 
    given={'target': product_names(['Entity'])},
    sought={'position': product_names(['Position'])},
    equations=(Equation('Position', 'target', 'position'),),
    words=('InformationIntent.TRACK',),
)

IDENTIFY = ExpressionType(
    'IDENTIFY',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']), 
    given={'target': product_names(['Entity'])},
    sought={'identity': product_names(['Identity'])},
    equations=(Equation('Identity', 'target', 'identity'),),
    words=('InformationIntent.IDENTIFY',),
)

CLASSIFY = ExpressionType(
    'CLASSIFY',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']), 
    given={'target': product_names(['Entity'])},
    sought={'classification': product_names(['Classification'])},
    equations=(Equation('Classification', 'target', 'classification'),),
    words=('InformationIntent.CLASSIFY',),
)

CREATE = ExpressionType(
    'CREATE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE']), 
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('EffectIntent.CREATE',),
)

REMOVE = ExpressionType(
    'REMOVE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE']), 
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('EffectIntent.REMOVE',),
)

AirMission = product_names(['Mission', 'PhysicalDomain.AIR'])

AirTask = product_names(['Task', 'PhysicalDomain.AIR'])

UGV = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'])

UAV = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'])

Drone = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'])

Geodetic = product_names(['Representation.Geodetic'])

LocalCartesian = product_names(['Representation.LocalCartesian'])

LocalEuler = product_names(['Representation.LocalEuler'])

Quaternion = product_names(['Representation.Quaternion'])

@dataclass(kw_only=True)
class Root(SemanticModel):
    _semantics: ClassVar = product_names(['Root'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Object(Root):
    _semantics: ClassVar = product_names(['Object'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Locality(Object):
    _semantics: ClassVar = product_names(['Locality'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

@dataclass(kw_only=True)
class Entity(Object):
    _semantics: ClassVar = product_names(['Entity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str
    name: str | None = None

@dataclass(kw_only=True)
class Biological(Entity):
    _semantics: ClassVar = product_names(['Biological', 'Substrate.BIOLOGICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Person(Biological):
    _semantics: ClassVar = product_names(['Substrate.BIOLOGICAL', 'Person'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

@dataclass(kw_only=True)
class Actor(Person):
    _semantics: ClassVar = product_names(['Substrate.BIOLOGICAL', 'Actor'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('role',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    role: str | None = None

@dataclass(kw_only=True)
class Machine(Entity):
    _semantics: ClassVar = product_names(['Machine', 'Substrate.MECHANICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('serial_number',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    serial_number: str | None = None

@dataclass(kw_only=True)
class Vehicle(Machine):
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    model: str | None = None

@dataclass(kw_only=True)
class CrewedVehicle(Vehicle):
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class UnmannedVehicle(Vehicle):
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Data(Root):
    _semantics: ClassVar = product_names(['Data'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class State(Data):
    _semantics: ClassVar = product_names(['State'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Position(State):
    _semantics: ClassVar = product_names(['Position'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Velocity(State):
    _semantics: ClassVar = product_names(['Velocity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Attitude(State):
    _semantics: ClassVar = product_names(['Attitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Identity(State):
    _semantics: ClassVar = product_names(['Identity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Classification(State):
    _semantics: ClassVar = product_names(['Classification'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Existence(State):
    _semantics: ClassVar = product_names(['Existence'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Connectivity(State):
    _semantics: ClassVar = product_names(['Connectivity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Altitude(State):
    _semantics: ClassVar = product_names(['Altitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('m',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    m: float

@dataclass(kw_only=True)
class GlobalPosition(SemanticModel):
    _semantics: ClassVar = product_names(['GlobalPosition', 'Position', 'Representation.Geodetic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('lat', 'lon', 'h')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic',)
    lat: float
    lon: float
    h: float

@dataclass(kw_only=True)
class LocalPosition(SemanticModel):
    _semantics: ClassVar = product_names(['LocalPosition', 'Position', 'Representation.LocalCartesian'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('x', 'y', 'z')
    _units: ClassVar[dict[str, str]] = {'x': 'm', 'y': 'm', 'z': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.LocalCartesian',)
    x: float
    y: float
    z: float

@dataclass(kw_only=True)
class LocalVelocity(SemanticModel):
    _semantics: ClassVar = product_names(['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('vx', 'vy', 'vz')
    _units: ClassVar[dict[str, str]] = {'vx': 'm/s', 'vy': 'm/s', 'vz': 'm/s'}
    _charts: ClassVar[tuple[str, ...]] = ('Velocity * Representation.LocalCartesian',)
    vx: float
    vy: float
    vz: float

@dataclass(kw_only=True)
class LocalAttitude(SemanticModel):
    _semantics: ClassVar = product_names(['LocalAttitude', 'Attitude', 'Representation.LocalEuler'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('roll', 'pitch', 'yaw')
    _units: ClassVar[dict[str, str]] = {'roll': 'rad', 'pitch': 'rad', 'yaw': 'rad'}
    _charts: ClassVar[tuple[str, ...]] = ('Attitude * Representation.LocalEuler',)
    roll: float
    pitch: float
    yaw: float

@dataclass(kw_only=True)
class Mark(Data):
    _semantics: ClassVar = product_names(['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name', 'lat', 'lon', 'h')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic',)
    uid: str
    name: str | None = None
    lat: float
    lon: float
    h: float

@dataclass(kw_only=True)
class Control(Root):
    _semantics: ClassVar = product_names(['Control'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Directive(Control):
    _semantics: ClassVar = product_names(['Directive'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Task(Directive):
    _semantics: ClassVar = product_names(['Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'instruction', 'priority', 'status')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str
    instruction: str
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

@dataclass(kw_only=True)
class Mission(Directive):
    _semantics: ClassVar = product_names(['Mission'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class TaskManeuver(Task):
    _semantics: ClassVar = product_names(['TaskManeuver'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: ManeuverIntent

@dataclass(kw_only=True)
class TaskInformation(Task):
    _semantics: ClassVar = product_names(['TaskInformation'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: InformationIntent

@dataclass(kw_only=True)
class TaskEffect(Task):
    _semantics: ClassVar = product_names(['TaskEffect'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: EffectIntent

@dataclass(kw_only=True)
class VehicleState(SemanticModel):
    _semantics: ClassVar = product_names(['Position', 'Representation.Geodetic', 'Velocity', 'Representation.LocalCartesian', 'Attitude', 'Representation.LocalEuler'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'lat', 'lon', 'h', 'vx', 'vy', 'vz', 'roll', 'pitch', 'yaw')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm', 'vx': 'm/s', 'vy': 'm/s', 'vz': 'm/s', 'roll': 'rad', 'pitch': 'rad', 'yaw': 'rad'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic', 'Velocity * Representation.LocalCartesian', 'Attitude * Representation.LocalEuler')
    _projection: ClassVar[bool] = True
    uid: str
    lat: float | None = None
    lon: float | None = None
    h: float | None = None
    vx: float | None = None
    vy: float | None = None
    vz: float | None = None
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None

Directed = RelationType('Directed', (Root, Root), operand_names=('source', 'target'))
Affects = RelationType('Affects', (Object, Root), operand_names=('source', 'target'), base=Directed)
AssignedWork = RelationType('AssignedWork', (Entity, Task), operand_names=('assignee', 'work'), base=Directed)

REGISTRY_SPEC = {'axes': {'Substrate': {'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL', 'CYBER']}, 'PhysicalDomain': {'description': 'A bounded thing operates in exactly one domain.', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE']}, 'Controller': {'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'description': 'Airframe construction, independent of takeoff capability.', 'cardinality': 'one', 'applies': {'all': ['Machine', 'PhysicalDomain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING']}, 'Representation': {'description': 'How a semantic quantity becomes irreducible data variables.', 'cardinality': 'many', 'values': ['Geodetic', 'LocalCartesian', 'LocalEuler', 'Quaternion']}, 'BloodGroup': {'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'requires': ['Biological'], 'values': ['A_POS', 'A_NEG', 'B_POS', 'B_NEG', 'AB_POS', 'AB_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity']}, 'values': ['TRUE', 'FALSE']}}, 'models': {'Root': {'parent': None, 'semantics': ['Root'], 'fields': [], 'chart_fields': []}, 'Object': {'parent': 'Root', 'semantics': ['Object'], 'fields': [], 'chart_fields': []}, 'Locality': {'parent': 'Object', 'semantics': ['Locality'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'Entity': {'parent': 'Object', 'semantics': ['Entity'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'Biological': {'parent': 'Entity', 'semantics': ['Biological', 'Substrate.BIOLOGICAL'], 'fields': [], 'chart_fields': []}, 'Person': {'parent': 'Biological', 'semantics': ['Substrate.BIOLOGICAL', 'Person'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'Actor': {'parent': 'Person', 'semantics': ['Substrate.BIOLOGICAL', 'Actor'], 'fields': [{'name': 'role', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'Machine': {'parent': 'Entity', 'semantics': ['Machine', 'Substrate.MECHANICAL'], 'fields': [{'name': 'serial_number', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'Vehicle': {'parent': 'Machine', 'semantics': ['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'], 'fields': [{'name': 'model', 'type': 'optional string', 'default': None}], 'chart_fields': []}, 'CrewedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'], 'fields': [], 'chart_fields': []}, 'UnmannedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'], 'fields': [], 'chart_fields': []}, 'Data': {'parent': 'Root', 'semantics': ['Data'], 'fields': [], 'chart_fields': []}, 'State': {'parent': 'Data', 'semantics': ['State'], 'fields': [], 'chart_fields': []}, 'Position': {'parent': 'State', 'semantics': ['Position'], 'fields': [], 'chart_fields': []}, 'Velocity': {'parent': 'State', 'semantics': ['Velocity'], 'fields': [], 'chart_fields': []}, 'Attitude': {'parent': 'State', 'semantics': ['Attitude'], 'fields': [], 'chart_fields': []}, 'Identity': {'parent': 'State', 'semantics': ['Identity'], 'fields': [], 'chart_fields': []}, 'Classification': {'parent': 'State', 'semantics': ['Classification'], 'fields': [], 'chart_fields': []}, 'Existence': {'parent': 'State', 'semantics': ['Existence'], 'fields': [], 'chart_fields': []}, 'Connectivity': {'parent': 'State', 'semantics': ['Connectivity'], 'fields': [], 'chart_fields': []}, 'Altitude': {'parent': 'State', 'semantics': ['Altitude'], 'fields': [{'name': 'm', 'type': 'float', 'default': None}], 'chart_fields': [], 'applies': ['PhysicalDomain.AIR']}, 'GlobalPosition': {'parent': None, 'semantics': ['GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'LocalPosition': {'parent': None, 'semantics': ['LocalPosition', 'Position', 'Representation.LocalCartesian'], 'fields': [{'name': 'x', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'y', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'z', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Position * Representation.LocalCartesian', 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}]}, 'LocalVelocity': {'parent': None, 'semantics': ['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'], 'fields': [{'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Velocity * Representation.LocalCartesian', 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}]}, 'LocalAttitude': {'parent': None, 'semantics': ['LocalAttitude', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}], 'chart_fields': [{'chart': 'Attitude * Representation.LocalEuler', 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}]}, 'Mark': {'parent': 'Data', 'semantics': ['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional string', 'default': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'Control': {'parent': 'Root', 'semantics': ['Control'], 'fields': [], 'chart_fields': []}, 'Directive': {'parent': 'Control', 'semantics': ['Directive'], 'fields': [], 'chart_fields': []}, 'Task': {'parent': 'Directive', 'semantics': ['Task'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'instruction', 'type': 'string', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE'}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW'}], 'chart_fields': []}, 'Mission': {'parent': 'Directive', 'semantics': ['Mission'], 'fields': [], 'chart_fields': []}, 'TaskManeuver': {'parent': 'Task', 'semantics': ['TaskManeuver'], 'fields': [{'name': 'intent', 'type': 'ManeuverIntent', 'default': None}], 'chart_fields': []}, 'TaskInformation': {'parent': 'Task', 'semantics': ['TaskInformation'], 'fields': [{'name': 'intent', 'type': 'InformationIntent', 'default': None}], 'chart_fields': []}, 'TaskEffect': {'parent': 'Task', 'semantics': ['TaskEffect'], 'fields': [{'name': 'intent', 'type': 'EffectIntent', 'default': None}], 'chart_fields': []}}, 'charts': [{'display': 'Position * Representation.Geodetic', 'factors': ['Position', 'Representation.Geodetic'], 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}, {'display': 'Position * Representation.LocalCartesian', 'factors': ['Position', 'Representation.LocalCartesian'], 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}, {'display': 'Velocity * Representation.LocalCartesian', 'factors': ['Velocity', 'Representation.LocalCartesian'], 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}, {'display': 'Attitude * Representation.LocalEuler', 'factors': ['Attitude', 'Representation.LocalEuler'], 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}, {'display': 'Attitude * Representation.Quaternion', 'factors': ['Attitude', 'Representation.Quaternion'], 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}], 'expressions': {'MOVE': {'description': 'Move an actor until its position is the destination.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['ManeuverIntent.MOVE']}, 'HOLD': {'description': "Maintain an actor's position at the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['ManeuverIntent.HOLD']}, 'LOCATE': {'description': 'Solve for the position of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['InformationIntent.LOCATE']}, 'TRACK': {'description': "Maintain awareness of an entity's position.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['InformationIntent.TRACK']}, 'IDENTIFY': {'description': 'Solve for the identity of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'identity': ['Identity']}, 'equations': [{'quantity': 'Identity', 'of': 'target', 'equals': 'identity'}], 'words': ['InformationIntent.IDENTIFY']}, 'CLASSIFY': {'description': 'Solve for the classification of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'classification': ['Classification']}, 'equations': [{'quantity': 'Classification', 'of': 'target', 'equals': 'classification'}], 'words': ['InformationIntent.CLASSIFY']}, 'CREATE': {'description': 'Make an object exist.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['EffectIntent.CREATE']}, 'REMOVE': {'description': 'Make an object cease to exist.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['EffectIntent.REMOVE']}}, 'word_expressions': {'ManeuverIntent.MOVE': 'MOVE', 'ManeuverIntent.HOLD': 'HOLD', 'InformationIntent.LOCATE': 'LOCATE', 'InformationIntent.TRACK': 'TRACK', 'InformationIntent.IDENTIFY': 'IDENTIFY', 'InformationIntent.CLASSIFY': 'CLASSIFY', 'EffectIntent.CREATE': 'CREATE', 'EffectIntent.REMOVE': 'REMOVE'}, 'aliases': {'AirMission': ['Mission', 'PhysicalDomain.AIR'], 'AirTask': ['Task', 'PhysicalDomain.AIR'], 'UGV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'], 'UAV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'], 'Drone': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'], 'Geodetic': ['Representation.Geodetic'], 'LocalCartesian': ['Representation.LocalCartesian'], 'LocalEuler': ['Representation.LocalEuler'], 'Quaternion': ['Representation.Quaternion']}, 'relations': {'Directed': {'signature': ['Root', 'Root'], 'operand_names': ['source', 'target'], 'specializes': None}, 'Affects': {'signature': ['Object', 'Root'], 'operand_names': ['source', 'target'], 'specializes': 'Directed'}, 'AssignedWork': {'signature': ['Entity', 'Task'], 'operand_names': ['assignee', 'work'], 'specializes': 'Directed'}}, 'projections': {'VehicleState': {'semantics': ['Position', 'Representation.Geodetic', 'Velocity', 'Representation.LocalCartesian', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}], 'charts': ['Position * Representation.Geodetic', 'Velocity * Representation.LocalCartesian', 'Attitude * Representation.LocalEuler']}}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)

def new_store() -> Store:
    return Store(REGISTRY)
