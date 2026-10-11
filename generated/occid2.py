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
    _applies = {'any': ['Existence', 'Connectivity', 'Engagement', 'Activity', 'Paused', 'Hold']}

TruthTarget.TRUE = AxisValue('TruthTarget', 'TRUE')
TruthTarget.FALSE = AxisValue('TruthTarget', 'FALSE')

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
    ACCEPTED = 5

TaskStatus._semantic_map = {
}

class ControlLevel(SemanticEnum):
    NONE = 0
    MONITOR = 1
    GUIDE = 2
    FULL = 3

ControlLevel._semantic_map = {
}

class PlanApprovalState(SemanticEnum):
    DRAFT = 0
    PROPOSED = 1
    APPROVED = 2
    REJECTED = 3
    SUPERSEDED = 4

PlanApprovalState._semantic_map = {
}

class BooleanOperator(SemanticEnum):
    NONE = 0
    NOT = 1
    AND = 2
    OR = 3
    XOR = 4
    NAND = 5
    NOR = 6
    XNOR = 7

BooleanOperator._semantic_map = {
}

class TaskIntent(SemanticEnum):
    MOVE = 0
    HOLD = 1
    LOCATE = 2
    TRACK = 3
    CREATE = 4
    REMOVE = 5
    MODIFY = 6
    PROTECT = 7
    IDENTIFY = 8
    CLASSIFY = 9
    FOLLOW = 10
    MEASURE = 11
    RESTORE = 12
    DENY = 13
    TRANSPORT = 14

TaskIntent._semantic_map = {
    'MOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'HOLD': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'LOCATE': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'TRACK': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN']),
    'CREATE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE']),
    'REMOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE']),
    'MODIFY': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'PROTECT': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'IDENTIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'CLASSIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'FOLLOW': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'MEASURE': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'RESTORE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'DENY': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE']),
    'TRANSPORT': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
}

class CommandOperation(SemanticEnum):
    ENGAGE = 0
    DISENGAGE = 1
    PAUSE = 2
    RESUME = 3
    SET = 4
    MOVE = 5
    ALLOCATE = 6
    TRANSFER = 7
    LOAD_CONFIGURATION = 8
    RESET = 9

CommandOperation._semantic_map = {
    'ENGAGE': product_names(['Command', 'TruthTarget.TRUE']),
    'DISENGAGE': product_names(['Command', 'TruthTarget.FALSE']),
    'PAUSE': product_names(['Command', 'Paused', 'TruthTarget.TRUE']),
    'RESUME': product_names(['Command', 'Paused', 'TruthTarget.FALSE']),
    'SET': product_names(['Command']),
    'MOVE': product_names(['Command', 'TemporalMode.ACHIEVE']),
    'ALLOCATE': product_names(['Command']),
    'TRANSFER': product_names(['Command']),
    'LOAD_CONFIGURATION': product_names(['Command']),
    'RESET': product_names(['Command']),
}

POSITION_GOAL = ExpressionType(
    'POSITION_GOAL',
    product_names(['Task', 'Realm.WORLD']),
    given={'actor': product_names(['Entity']), 'destination': product_names(['Position'])},
    sought={},
    equations=(Equation('Position', 'actor', 'destination'),),
    words=(),
)

POSITION_QUERY = ExpressionType(
    'POSITION_QUERY',
    product_names(['Task', 'Realm.INFORMATION']),
    given={'target': product_names(['Entity'])},
    sought={'position': product_names(['Position'])},
    equations=(Equation('Position', 'target', 'position'),),
    words=(),
)

EXISTENCE_GOAL = ExpressionType(
    'EXISTENCE_GOAL',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=(),
)

OBJECT_STATE_GOAL = ExpressionType(
    'OBJECT_STATE_GOAL',
    product_names(['Task', 'Realm.WORLD']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=(),
)

ENGAGEMENT_COMMAND = ExpressionType(
    'ENGAGEMENT_COMMAND',
    product_names(['Command']),
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=(),
)

PROCESS_COMMAND = ExpressionType(
    'PROCESS_COMMAND',
    product_names(['Command', 'Paused']),
    given={'target': product_names(['Object']), 'process': product_names(['Text'])},
    sought={},
    equations=(),
    words=(),
)

MOVE = ExpressionType(
    'MOVE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    given={'actor': product_names(['Entity']), 'destination': product_names(['Position'])},
    sought={},
    equations=(Equation('Position', 'actor', 'destination'),),
    words=('TaskIntent.MOVE',),
)

HOLD = ExpressionType(
    'HOLD',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    given={'actor': product_names(['Entity']), 'destination': product_names(['Position'])},
    sought={},
    equations=(Equation('Position', 'actor', 'destination'),),
    words=('TaskIntent.HOLD',),
)

LOCATE = ExpressionType(
    'LOCATE',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    given={'target': product_names(['Entity'])},
    sought={'position': product_names(['Position'])},
    equations=(Equation('Position', 'target', 'position'),),
    words=('TaskIntent.LOCATE',),
)

TRACK = ExpressionType(
    'TRACK',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN']),
    given={'target': product_names(['Entity'])},
    sought={'position': product_names(['Position'])},
    equations=(Equation('Position', 'target', 'position'),),
    words=('TaskIntent.TRACK',),
)

CREATE = ExpressionType(
    'CREATE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.CREATE',),
)

REMOVE = ExpressionType(
    'REMOVE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.REMOVE',),
)

MODIFY = ExpressionType(
    'MODIFY',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.MODIFY',),
)

PROTECT = ExpressionType(
    'PROTECT',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.PROTECT',),
)

ENGAGE = ExpressionType(
    'ENGAGE',
    product_names(['Command', 'TruthTarget.TRUE']),
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.ENGAGE',),
)

DISENGAGE = ExpressionType(
    'DISENGAGE',
    product_names(['Command', 'TruthTarget.FALSE']),
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.DISENGAGE',),
)

PAUSE = ExpressionType(
    'PAUSE',
    product_names(['Command', 'Paused', 'TruthTarget.TRUE']),
    given={'target': product_names(['Object']), 'process': product_names(['Text'])},
    sought={},
    equations=(),
    words=('CommandOperation.PAUSE',),
)

RESUME = ExpressionType(
    'RESUME',
    product_names(['Command', 'Paused', 'TruthTarget.FALSE']),
    given={'target': product_names(['Object']), 'process': product_names(['Text'])},
    sought={},
    equations=(),
    words=('CommandOperation.RESUME',),
)

IDENTIFY = ExpressionType(
    'IDENTIFY',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    given={'target': product_names(['Entity'])},
    sought={'identity': product_names(['Identity'])},
    equations=(Equation('Identity', 'target', 'identity'),),
    words=('TaskIntent.IDENTIFY',),
)

CLASSIFY = ExpressionType(
    'CLASSIFY',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    given={'target': product_names(['Entity'])},
    sought={'classification': product_names(['Classification'])},
    equations=(Equation('Classification', 'target', 'classification'),),
    words=('TaskIntent.CLASSIFY',),
)

FOLLOW = ExpressionType(
    'FOLLOW',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    given={'actor': product_names(['Entity']), 'path': product_names(['GeoPath'])},
    sought={},
    equations=(),
    words=('TaskIntent.FOLLOW',),
)

MEASURE = ExpressionType(
    'MEASURE',
    product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    given={'target': product_names(['Entity'])},
    sought={'measurement': product_names(['State'])},
    equations=(),
    words=('TaskIntent.MEASURE',),
)

RESTORE = ExpressionType(
    'RESTORE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.RESTORE',),
)

DENY = ExpressionType(
    'DENY',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE']),
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.DENY',),
)

TRANSPORT = ExpressionType(
    'TRANSPORT',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    given={'cargo': product_names(['Object']), 'origin': product_names(['Position']), 'destination': product_names(['Position'])},
    sought={},
    equations=(),
    words=('TaskIntent.TRANSPORT',),
)

SET = ExpressionType(
    'SET',
    product_names(['Command']),
    given={'target': product_names(['Object']), 'property': product_names(['Text']), 'value': product_names(['Scalar'])},
    sought={},
    equations=(),
    words=('CommandOperation.SET',),
)

DIRECT = ExpressionType(
    'DIRECT',
    product_names(['Command', 'TemporalMode.ACHIEVE']),
    given={'target': product_names(['Object']), 'destination': product_names(['Position']), 'path': product_names(['GeoPath']), 'radius': product_names(['Distance']), 'speed': product_names(['Speed']), 'yaw': product_names(['Angle'])},
    sought={},
    equations=(Equation('Position', 'target', 'destination'),),
    words=('CommandOperation.MOVE',),
)

ALLOCATE = ExpressionType(
    'ALLOCATE',
    product_names(['Command']),
    given={'target': product_names(['Object']), 'resource': product_names(['Resource']), 'quantity': product_names(['Count'])},
    sought={},
    equations=(),
    words=('CommandOperation.ALLOCATE',),
)

TRANSFER = ExpressionType(
    'TRANSFER',
    product_names(['Command']),
    given={'target': product_names(['Object']), 'resource': product_names(['Resource']), 'quantity': product_names(['Count'])},
    sought={},
    equations=(),
    words=('CommandOperation.TRANSFER',),
)

LOAD_CONFIGURATION = ExpressionType(
    'LOAD_CONFIGURATION',
    product_names(['Command']),
    given={'target': product_names(['Object']), 'parameter': product_names(['Text']), 'value': product_names(['Scalar'])},
    sought={},
    equations=(),
    words=('CommandOperation.LOAD_CONFIGURATION',),
)

RESET = ExpressionType(
    'RESET',
    product_names(['Command']),
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.RESET',),
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

Epoch = product_names(['Representation.Epoch'])

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
    role: Role | None = None

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
class Engagement(State):
    _semantics: ClassVar = product_names(['Engagement'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Activity(State):
    _semantics: ClassVar = product_names(['Activity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Paused(State):
    _semantics: ClassVar = product_names(['Paused'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Hold(State):
    _semantics: ClassVar = product_names(['Hold'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Text(State):
    _semantics: ClassVar = product_names(['Text'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Duration(State):
    _semantics: ClassVar = product_names(['Duration'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Angle(State):
    _semantics: ClassVar = product_names(['Angle'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Distance(State):
    _semantics: ClassVar = product_names(['Distance'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Speed(State):
    _semantics: ClassVar = product_names(['Speed'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Count(State):
    _semantics: ClassVar = product_names(['Count'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Ordinal(State):
    _semantics: ClassVar = product_names(['Ordinal'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Code(State):
    _semantics: ClassVar = product_names(['Code'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Scalar(State):
    _semantics: ClassVar = product_names(['Scalar'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Altitude(State):
    _semantics: ClassVar = product_names(['Altitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

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
class QuaternionAttitude(SemanticModel):
    _semantics: ClassVar = product_names(['QuaternionAttitude', 'Attitude', 'Representation.Quaternion'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('qw', 'qx', 'qy', 'qz')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Attitude * Representation.Quaternion',)
    qw: float
    qx: float
    qy: float
    qz: float

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
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'instruction', 'intent', 'priority', 'status')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str
    instruction: str
    intent: TaskIntent
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

@dataclass(kw_only=True)
class Mission(Directive):
    _semantics: ClassVar = product_names(['Mission'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Record(Data):
    _semantics: ClassVar = product_names(['Record'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'id', 'revision', 'created_ts', 'updated_ts', 'origin_system', 'provenance')
    _units: ClassVar[dict[str, str]] = {'created_ts': 's', 'updated_ts': 's'}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str
    id: int | None = None
    revision: int | None = None
    created_ts: float
    updated_ts: float
    origin_system: str
    provenance: list[str] = field(default_factory=list)

@dataclass(kw_only=True)
class Time(State):
    _semantics: ClassVar = product_names(['Time'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Range(Data):
    _semantics: ClassVar = product_names(['Range'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class NumericRange(Range):
    _semantics: ClassVar = product_names(['NumericRange'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('min_value', 'max_value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    min_value: float | None = None
    max_value: float | None = None

@dataclass(kw_only=True)
class Condition(Data):
    _semantics: ClassVar = product_names(['Condition'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Predicate(Condition):
    _semantics: ClassVar = product_names(['Predicate'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('subject', 'quantity', 'value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    subject: str | None = None
    quantity: str | None = None
    value: float | None = None

@dataclass(kw_only=True)
class BooleanLogic(Condition):
    _semantics: ClassVar = product_names(['BooleanLogic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operator', 'terms')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operator: BooleanOperator
    terms: list[Condition] = field(default_factory=list)

@dataclass(kw_only=True)
class GeoPath(Data):
    _semantics: ClassVar = product_names(['GeoPath'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('points',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    points: list[GlobalPosition] = field(default_factory=list)

@dataclass(kw_only=True)
class Role(Data):
    _semantics: ClassVar = product_names(['Role'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

@dataclass(kw_only=True)
class Resource(Object):
    _semantics: ClassVar = product_names(['Resource'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str | None = None
    name: str | None = None

@dataclass(kw_only=True)
class Constraint(Control):
    _semantics: ClassVar = product_names(['Constraint'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('condition',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    condition: Condition | None = None

@dataclass(kw_only=True)
class TaskTimeWindow(Constraint):
    _semantics: ClassVar = product_names(['TaskTimeWindow'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('earliest_start', 'latest_finish')
    _units: ClassVar[dict[str, str]] = {'earliest_start': 's', 'latest_finish': 's'}
    _charts: ClassVar[tuple[str, ...]] = ()
    earliest_start: float | None = None
    latest_finish: float | None = None

@dataclass(kw_only=True)
class WeatherLimits(Constraint):
    _semantics: ClassVar = product_names(['WeatherLimits'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('ifr', 'night', 'rain', 'snow', 'temp', 'wind', 'vis', 'icing')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    ifr: bool | None = None
    night: bool | None = None
    rain: NumericRange | None = None
    snow: NumericRange | None = None
    temp: NumericRange | None = None
    wind: NumericRange | None = None
    vis: NumericRange | None = None
    icing: bool | None = None

@dataclass(kw_only=True)
class Objective(Control):
    _semantics: ClassVar = product_names(['Objective'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('record', 'uid', 'id', 'name', 'condition', 'criteria', 'priority', 'status', 'start_time', 'deadline')
    _units: ClassVar[dict[str, str]] = {'start_time': 's', 'deadline': 's'}
    _charts: ClassVar[tuple[str, ...]] = ()
    record: Record | None = None
    uid: str
    id: int | None = None
    name: str
    condition: Condition | None = None
    criteria: list[Condition] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    start_time: float | None = None
    deadline: float | None = None

@dataclass(kw_only=True)
class Command(Directive):
    _semantics: ClassVar = product_names(['Command'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'operation')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: str
    operation: CommandOperation

@dataclass(kw_only=True)
class Authority(Control):
    _semantics: ClassVar = product_names(['Authority'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('record', 'uid', 'id', 'role')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    record: Record | None = None
    uid: str
    id: int | None = None
    role: Role | None = None

@dataclass(kw_only=True)
class Lease(Authority):
    _semantics: ClassVar = product_names(['Lease'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('bound', 'control_level')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    bound: Condition | None = None
    control_level: ControlLevel | None = None

@dataclass(kw_only=True)
class Plan(Control):
    _semantics: ClassVar = product_names(['Plan'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('record', 'uid', 'id', 'name', 'approval_state')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    record: Record | None = None
    uid: str
    id: int | None = None
    name: str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

@dataclass(kw_only=True)
class PlanContingency(Data):
    _semantics: ClassVar = product_names(['PlanContingency'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('condition',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    condition: Condition

Directed = RelationType('Directed', (Root, Root), operand_names=('source', 'target'))
AssignedWork = RelationType('AssignedWork', (Entity, Task), operand_names=('assignee', 'work'))
ConstrainedBy = RelationType('ConstrainedBy', (Control, Constraint), operand_names=('subject', 'constraint'))
OwnedBy = RelationType('OwnedBy', (Objective, Entity), operand_names=('objective', 'owner'))
Holds = RelationType('Holds', (Authority, Entity), operand_names=('authority', 'holder'))
GrantedBy = RelationType('GrantedBy', (Authority, Entity), operand_names=('authority', 'grantor'))
Controls = RelationType('Controls', (Lease, Object), operand_names=('lease', 'asset'))
Contains = RelationType('Contains', (Plan, Root), operand_names=('plan', 'item'))

REGISTRY_SPEC = {'axes': {'Substrate': {'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL', 'CYBER']}, 'PhysicalDomain': {'description': 'A bounded thing operates in exactly one domain.', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE']}, 'Controller': {'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'description': 'Airframe construction, independent of takeoff capability.', 'cardinality': 'one', 'applies': {'all': ['Machine', 'PhysicalDomain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING']}, 'Representation': {'description': 'The coordinate scheme through which a structured quantity becomes data variables.', 'cardinality': 'many', 'values': ['Geodetic', 'LocalCartesian', 'LocalEuler', 'Quaternion']}, 'BloodGroup': {'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'requires': ['Biological'], 'values': ['A_POS', 'A_NEG', 'B_POS', 'B_NEG', 'AB_POS', 'AB_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity', 'Engagement', 'Activity', 'Paused', 'Hold']}, 'values': ['TRUE', 'FALSE']}}, 'models': {'Root': {'parent': None, 'semantics': ['Root'], 'fields': [], 'chart_fields': []}, 'Object': {'parent': 'Root', 'semantics': ['Object'], 'fields': [], 'chart_fields': []}, 'Locality': {'parent': 'Object', 'semantics': ['Locality'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Entity': {'parent': 'Object', 'semantics': ['Entity'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Biological': {'parent': 'Entity', 'semantics': ['Biological', 'Substrate.BIOLOGICAL'], 'fields': [], 'chart_fields': []}, 'Person': {'parent': 'Biological', 'semantics': ['Substrate.BIOLOGICAL', 'Person'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Actor': {'parent': 'Person', 'semantics': ['Substrate.BIOLOGICAL', 'Actor'], 'fields': [{'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}], 'chart_fields': []}, 'Machine': {'parent': 'Entity', 'semantics': ['Machine', 'Substrate.MECHANICAL'], 'fields': [{'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Vehicle': {'parent': 'Machine', 'semantics': ['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'], 'fields': [{'name': 'model', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'CrewedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'], 'fields': [], 'chart_fields': []}, 'UnmannedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'], 'fields': [], 'chart_fields': []}, 'Data': {'parent': 'Root', 'semantics': ['Data'], 'fields': [], 'chart_fields': []}, 'State': {'parent': 'Data', 'semantics': ['State'], 'fields': [], 'chart_fields': []}, 'Position': {'parent': 'State', 'semantics': ['Position'], 'fields': [], 'chart_fields': []}, 'Velocity': {'parent': 'State', 'semantics': ['Velocity'], 'fields': [], 'chart_fields': []}, 'Attitude': {'parent': 'State', 'semantics': ['Attitude'], 'fields': [], 'chart_fields': []}, 'Identity': {'parent': 'State', 'semantics': ['Identity'], 'fields': [], 'chart_fields': []}, 'Classification': {'parent': 'State', 'semantics': ['Classification'], 'fields': [], 'chart_fields': []}, 'Existence': {'parent': 'State', 'semantics': ['Existence'], 'fields': [], 'chart_fields': []}, 'Connectivity': {'parent': 'State', 'semantics': ['Connectivity'], 'fields': [], 'chart_fields': []}, 'Engagement': {'parent': 'State', 'semantics': ['Engagement'], 'fields': [], 'chart_fields': []}, 'Activity': {'parent': 'State', 'semantics': ['Activity'], 'fields': [], 'chart_fields': []}, 'Paused': {'parent': 'State', 'semantics': ['Paused'], 'fields': [], 'chart_fields': []}, 'Hold': {'parent': 'State', 'semantics': ['Hold'], 'fields': [], 'chart_fields': []}, 'Text': {'parent': 'State', 'semantics': ['Text'], 'fields': [], 'chart_fields': []}, 'Duration': {'parent': 'State', 'semantics': ['Duration'], 'fields': [], 'chart_fields': []}, 'Angle': {'parent': 'State', 'semantics': ['Angle'], 'fields': [], 'chart_fields': []}, 'Distance': {'parent': 'State', 'semantics': ['Distance'], 'fields': [], 'chart_fields': []}, 'Speed': {'parent': 'State', 'semantics': ['Speed'], 'fields': [], 'chart_fields': []}, 'Count': {'parent': 'State', 'semantics': ['Count'], 'fields': [], 'chart_fields': []}, 'Ordinal': {'parent': 'State', 'semantics': ['Ordinal'], 'fields': [], 'chart_fields': []}, 'Code': {'parent': 'State', 'semantics': ['Code'], 'fields': [], 'chart_fields': []}, 'Scalar': {'parent': 'State', 'semantics': ['Scalar'], 'fields': [], 'chart_fields': []}, 'Altitude': {'parent': 'State', 'semantics': ['Altitude'], 'fields': [], 'chart_fields': [], 'applies': ['PhysicalDomain.AIR']}, 'GlobalPosition': {'parent': None, 'semantics': ['GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'LocalPosition': {'parent': None, 'semantics': ['LocalPosition', 'Position', 'Representation.LocalCartesian'], 'fields': [{'name': 'x', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'y', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'z', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Position * Representation.LocalCartesian', 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}]}, 'LocalVelocity': {'parent': None, 'semantics': ['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'], 'fields': [{'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Velocity * Representation.LocalCartesian', 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}]}, 'LocalAttitude': {'parent': None, 'semantics': ['LocalAttitude', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}], 'chart_fields': [{'chart': 'Attitude * Representation.LocalEuler', 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}]}, 'QuaternionAttitude': {'parent': None, 'semantics': ['QuaternionAttitude', 'Attitude', 'Representation.Quaternion'], 'fields': [{'name': 'qw', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qx', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qy', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qz', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}], 'chart_fields': [{'chart': 'Attitude * Representation.Quaternion', 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}]}, 'Mark': {'parent': 'Data', 'semantics': ['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'Control': {'parent': 'Root', 'semantics': ['Control'], 'fields': [], 'chart_fields': []}, 'Directive': {'parent': 'Control', 'semantics': ['Directive'], 'fields': [], 'chart_fields': []}, 'Task': {'parent': 'Directive', 'semantics': ['Task'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'instruction', 'type': 'string', 'default': None, 'unit': None}, {'name': 'intent', 'type': 'TaskIntent', 'default': None, 'unit': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}], 'chart_fields': []}, 'Mission': {'parent': 'Directive', 'semantics': ['Mission'], 'fields': [], 'chart_fields': []}, 'Record': {'parent': 'Data', 'semantics': ['Record'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'id', 'type': 'optional int', 'default': None, 'unit': None}, {'name': 'revision', 'type': 'optional int', 'default': None, 'unit': None}, {'name': 'created_ts', 'type': 'float', 'default': None, 'unit': 's'}, {'name': 'updated_ts', 'type': 'float', 'default': None, 'unit': 's'}, {'name': 'origin_system', 'type': 'string', 'default': None, 'unit': None}, {'name': 'provenance', 'type': 'list[string]', 'default': None}], 'chart_fields': []}, 'Time': {'parent': 'State', 'semantics': ['Time'], 'fields': [], 'chart_fields': []}, 'Range': {'parent': 'Data', 'semantics': ['Range'], 'fields': [], 'chart_fields': []}, 'NumericRange': {'parent': 'Range', 'semantics': ['NumericRange'], 'fields': [{'name': 'min_value', 'type': 'optional float', 'default': None, 'unit': None}, {'name': 'max_value', 'type': 'optional float', 'default': None, 'unit': None}], 'chart_fields': []}, 'Condition': {'parent': 'Data', 'semantics': ['Condition'], 'fields': [], 'chart_fields': []}, 'Predicate': {'parent': 'Condition', 'semantics': ['Predicate'], 'fields': [{'name': 'subject', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'quantity', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'value', 'type': 'optional float', 'default': None, 'unit': None}], 'chart_fields': []}, 'BooleanLogic': {'parent': 'Condition', 'semantics': ['BooleanLogic'], 'fields': [{'name': 'operator', 'type': 'BooleanOperator', 'default': None, 'unit': None}, {'name': 'terms', 'type': 'list[Condition]', 'default': None}], 'chart_fields': []}, 'GeoPath': {'parent': 'Data', 'semantics': ['GeoPath'], 'fields': [{'name': 'points', 'type': 'list[GlobalPosition]', 'default': None}], 'chart_fields': []}, 'Role': {'parent': 'Data', 'semantics': ['Role'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Resource': {'parent': 'Object', 'semantics': ['Resource'], 'fields': [{'name': 'uid', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': []}, 'Constraint': {'parent': 'Control', 'semantics': ['Constraint'], 'fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}], 'chart_fields': []}, 'TaskTimeWindow': {'parent': 'Constraint', 'semantics': ['TaskTimeWindow'], 'fields': [{'name': 'earliest_start', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'latest_finish', 'type': 'optional float', 'default': None, 'unit': 's'}], 'chart_fields': []}, 'WeatherLimits': {'parent': 'Constraint', 'semantics': ['WeatherLimits'], 'fields': [{'name': 'ifr', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'night', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'rain', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'snow', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'temp', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'wind', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'vis', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'icing', 'type': 'optional bool', 'default': None, 'unit': None}], 'chart_fields': []}, 'Objective': {'parent': 'Control', 'semantics': ['Objective'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None, 'unit': None}, {'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'id', 'type': 'optional int', 'default': None, 'unit': None}, {'name': 'name', 'type': 'string', 'default': None, 'unit': None}, {'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'criteria', 'type': 'list[Condition]', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}, {'name': 'start_time', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'deadline', 'type': 'optional float', 'default': None, 'unit': 's'}], 'chart_fields': []}, 'Command': {'parent': 'Directive', 'semantics': ['Command'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'operation', 'type': 'CommandOperation', 'default': None, 'unit': None}], 'chart_fields': []}, 'Authority': {'parent': 'Control', 'semantics': ['Authority'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None, 'unit': None}, {'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'id', 'type': 'optional int', 'default': None, 'unit': None}, {'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}], 'chart_fields': []}, 'Lease': {'parent': 'Authority', 'semantics': ['Lease'], 'fields': [{'name': 'bound', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'control_level', 'type': 'optional ControlLevel', 'default': None, 'unit': None}], 'chart_fields': []}, 'Plan': {'parent': 'Control', 'semantics': ['Plan'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None, 'unit': None}, {'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'id', 'type': 'optional int', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'approval_state', 'type': 'PlanApprovalState', 'default': 'DRAFT', 'unit': None}], 'chart_fields': []}, 'PlanContingency': {'parent': 'Data', 'semantics': ['PlanContingency'], 'fields': [{'name': 'condition', 'type': 'Condition', 'default': None, 'unit': None}], 'chart_fields': []}}, 'charts': [{'display': 'Position * Representation.Geodetic', 'factors': ['Position', 'Representation.Geodetic'], 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}, {'display': 'Position * Representation.LocalCartesian', 'factors': ['Position', 'Representation.LocalCartesian'], 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}, {'display': 'Velocity * Representation.LocalCartesian', 'factors': ['Velocity', 'Representation.LocalCartesian'], 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}, {'display': 'Attitude * Representation.LocalEuler', 'factors': ['Attitude', 'Representation.LocalEuler'], 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}, {'display': 'Attitude * Representation.Quaternion', 'factors': ['Attitude', 'Representation.Quaternion'], 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}], 'expressions': {'POSITION_GOAL': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': []}, 'POSITION_QUERY': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': []}, 'EXISTENCE_GOAL': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'OBJECT_STATE_GOAL': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'ENGAGEMENT_COMMAND': {'description': "The target's engagement state is asserted.", 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'PROCESS_COMMAND': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': []}, 'MOVE': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.MOVE']}, 'HOLD': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.HOLD']}, 'LOCATE': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.LOCATE']}, 'TRACK': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.TRACK']}, 'CREATE': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.CREATE']}, 'REMOVE': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.REMOVE']}, 'MODIFY': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.MODIFY']}, 'PROTECT': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.PROTECT']}, 'ENGAGE': {'description': "The target's engagement state is asserted.", 'factors': ['Command', 'TruthTarget.TRUE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ENGAGE']}, 'DISENGAGE': {'description': "The target's engagement state is asserted.", 'factors': ['Command', 'TruthTarget.FALSE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.DISENGAGE']}, 'PAUSE': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused', 'TruthTarget.TRUE'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.PAUSE']}, 'RESUME': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused', 'TruthTarget.FALSE'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESUME']}, 'IDENTIFY': {'description': 'Solve for the identity of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'identity': ['Identity']}, 'equations': [{'quantity': 'Identity', 'of': 'target', 'equals': 'identity'}], 'words': ['TaskIntent.IDENTIFY']}, 'CLASSIFY': {'description': 'Solve for the classification of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'classification': ['Classification']}, 'equations': [{'quantity': 'Classification', 'of': 'target', 'equals': 'classification'}], 'words': ['TaskIntent.CLASSIFY']}, 'FOLLOW': {'description': 'Follow a path.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'path': ['GeoPath']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.FOLLOW']}, 'MEASURE': {'description': 'Measure a state of a target.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'measurement': ['State']}, 'equations': [], 'words': ['TaskIntent.MEASURE']}, 'RESTORE': {'description': 'Return an object to a prior state.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.RESTORE']}, 'DENY': {'description': 'Prevent connectivity to an object.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.DENY']}, 'TRANSPORT': {'description': 'Move a thing between places; which end and what moves are bindings.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'cargo': ['Object'], 'origin': ['Position'], 'destination': ['Position']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.TRANSPORT']}, 'SET': {'description': 'Set a declared state property on the target.', 'factors': ['Command'], 'given': {'target': ['Object'], 'property': ['Text'], 'value': ['Scalar']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.SET']}, 'DIRECT': {'description': 'Direct the target to a destination or along a path.', 'factors': ['Command', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Object'], 'destination': ['Position'], 'path': ['GeoPath'], 'radius': ['Distance'], 'speed': ['Speed'], 'yaw': ['Angle']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'destination'}], 'words': ['CommandOperation.MOVE']}, 'ALLOCATE': {'description': 'Allocate a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource'], 'quantity': ['Count']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ALLOCATE']}, 'TRANSFER': {'description': 'Transfer a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource'], 'quantity': ['Count']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.TRANSFER']}, 'LOAD_CONFIGURATION': {'description': 'Load a referenced configuration on the target.', 'factors': ['Command'], 'given': {'target': ['Object'], 'parameter': ['Text'], 'value': ['Scalar']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.LOAD_CONFIGURATION']}, 'RESET': {'description': 'Reset the target to its initial state.', 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESET']}}, 'word_expressions': {'TaskIntent.MOVE': 'MOVE', 'TaskIntent.HOLD': 'HOLD', 'TaskIntent.LOCATE': 'LOCATE', 'TaskIntent.TRACK': 'TRACK', 'TaskIntent.CREATE': 'CREATE', 'TaskIntent.REMOVE': 'REMOVE', 'TaskIntent.MODIFY': 'MODIFY', 'TaskIntent.PROTECT': 'PROTECT', 'CommandOperation.ENGAGE': 'ENGAGE', 'CommandOperation.DISENGAGE': 'DISENGAGE', 'CommandOperation.PAUSE': 'PAUSE', 'CommandOperation.RESUME': 'RESUME', 'TaskIntent.IDENTIFY': 'IDENTIFY', 'TaskIntent.CLASSIFY': 'CLASSIFY', 'TaskIntent.FOLLOW': 'FOLLOW', 'TaskIntent.MEASURE': 'MEASURE', 'TaskIntent.RESTORE': 'RESTORE', 'TaskIntent.DENY': 'DENY', 'TaskIntent.TRANSPORT': 'TRANSPORT', 'CommandOperation.SET': 'SET', 'CommandOperation.MOVE': 'DIRECT', 'CommandOperation.ALLOCATE': 'ALLOCATE', 'CommandOperation.TRANSFER': 'TRANSFER', 'CommandOperation.LOAD_CONFIGURATION': 'LOAD_CONFIGURATION', 'CommandOperation.RESET': 'RESET'}, 'aliases': {'AirMission': ['Mission', 'PhysicalDomain.AIR'], 'AirTask': ['Task', 'PhysicalDomain.AIR'], 'UGV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'], 'UAV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'], 'Drone': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'], 'Geodetic': ['Representation.Geodetic'], 'LocalCartesian': ['Representation.LocalCartesian'], 'LocalEuler': ['Representation.LocalEuler'], 'Quaternion': ['Representation.Quaternion'], 'Epoch': ['Representation.Epoch']}, 'relations': {'Directed': {'signature': ['Root', 'Root'], 'operand_names': ['source', 'target']}, 'AssignedWork': {'signature': ['Entity', 'Task'], 'operand_names': ['assignee', 'work']}, 'ConstrainedBy': {'signature': ['Control', 'Constraint'], 'operand_names': ['subject', 'constraint']}, 'OwnedBy': {'signature': ['Objective', 'Entity'], 'operand_names': ['objective', 'owner']}, 'Holds': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'holder']}, 'GrantedBy': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'grantor']}, 'Controls': {'signature': ['Lease', 'Object'], 'operand_names': ['lease', 'asset']}, 'Contains': {'signature': ['Plan', 'Root'], 'operand_names': ['plan', 'item']}}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)

def new_store() -> Store:
    return Store(REGISTRY)
