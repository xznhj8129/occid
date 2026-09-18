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
Representation.Epoch = AxisValue('Representation', 'Epoch')
Representation.UID = AxisValue('Representation', 'UID')
Representation.IntID = AxisValue('Representation', 'IntID')
Representation.PlainText = AxisValue('Representation', 'PlainText')
Representation.Seconds = AxisValue('Representation', 'Seconds')
Representation.Radians = AxisValue('Representation', 'Radians')
Representation.Meters = AxisValue('Representation', 'Meters')
Representation.MetersPerSecond = AxisValue('Representation', 'MetersPerSecond')
Representation.MSL = AxisValue('Representation', 'MSL')
Representation.FlightLevel = AxisValue('Representation', 'FlightLevel')
Representation.Count = AxisValue('Representation', 'Count')
Representation.Ordinal = AxisValue('Representation', 'Ordinal')
Representation.Protocol = AxisValue('Representation', 'Protocol')
Representation.Decimal = AxisValue('Representation', 'Decimal')
Representation.Integer = AxisValue('Representation', 'Integer')

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

class TaskIntent(SemanticEnum):
    MOVE = 0
    HOLD = 1
    FOLLOW = 2
    LOCATE = 3
    TRACK = 4
    IDENTIFY = 5
    CLASSIFY = 6
    MEASURE = 7
    CREATE = 8
    REMOVE = 9
    MODIFY = 10
    RESTORE = 11
    PROTECT = 12
    DENY = 13
    TRANSPORT = 14

TaskIntent._semantic_map = {
    'MOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'HOLD': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'FOLLOW': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'LOCATE': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'TRACK': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN']),
    'IDENTIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'CLASSIFY': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'MEASURE': product_names(['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE']),
    'CREATE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE']),
    'REMOVE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE']),
    'MODIFY': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'RESTORE': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
    'PROTECT': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']),
    'DENY': product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE']),
    'TRANSPORT': product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']),
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
    ACCEPTED = 5

TaskStatus._semantic_map = {
}

class TaskPhase(SemanticEnum):
    CREATED = 0
    DISPATCHED = 1
    ASSIGNED = 2
    RUNNING = 3
    DONE_OK = 4
    DONE_FAIL = 5
    CANCELLED = 6

TaskPhase._semantic_map = {
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

MODIFY = ExpressionType(
    'MODIFY',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']), 
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.MODIFY',),
)

RESTORE = ExpressionType(
    'RESTORE',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE']), 
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.RESTORE',),
)

PROTECT = ExpressionType(
    'PROTECT',
    product_names(['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN']), 
    given={'object': product_names(['Object'])},
    sought={},
    equations=(),
    words=('TaskIntent.PROTECT',),
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
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.PAUSE',),
)

RESUME = ExpressionType(
    'RESUME',
    product_names(['Command', 'Paused', 'TruthTarget.FALSE']), 
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.RESUME',),
)

SET = ExpressionType(
    'SET',
    product_names(['Command']), 
    given={'target': product_names(['Object'])},
    sought={},
    equations=(),
    words=('CommandOperation.SET',),
)

DIRECT = ExpressionType(
    'DIRECT',
    product_names(['Command', 'TemporalMode.ACHIEVE']), 
    given={'target': product_names(['Object']), 'destination': product_names(['Position']), 'path': product_names(['GeoPath'])},
    sought={},
    equations=(Equation('Position', 'target', 'destination'),),
    words=('CommandOperation.MOVE',),
)

ALLOCATE = ExpressionType(
    'ALLOCATE',
    product_names(['Command']), 
    given={'target': product_names(['Object']), 'resource': product_names(['Resource'])},
    sought={},
    equations=(),
    words=('CommandOperation.ALLOCATE',),
)

TRANSFER = ExpressionType(
    'TRANSFER',
    product_names(['Command']), 
    given={'target': product_names(['Object']), 'resource': product_names(['Resource'])},
    sought={},
    equations=(),
    words=('CommandOperation.TRANSFER',),
)

LOAD_CONFIGURATION = ExpressionType(
    'LOAD_CONFIGURATION',
    product_names(['Command']), 
    given={'target': product_names(['Object'])},
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
    name: PlainText | None = None

@dataclass(kw_only=True)
class Entity(Object):
    _semantics: ClassVar = product_names(['Entity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    name: PlainText | None = None

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
    name: PlainText | None = None

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
    serial_number: PlainText | None = None

@dataclass(kw_only=True)
class Vehicle(Machine):
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    model: PlainText | None = None

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
class UID(SemanticModel):
    _semantics: ClassVar = product_names(['UID', 'Identity', 'Representation.UID'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Identity * Representation.UID',)
    uid: str

@dataclass(kw_only=True)
class IntID(SemanticModel):
    _semantics: ClassVar = product_names(['IntID', 'Identity', 'Representation.IntID'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('id',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Identity * Representation.IntID',)
    id: int

@dataclass(kw_only=True)
class PlainText(SemanticModel):
    _semantics: ClassVar = product_names(['PlainText', 'Text', 'Representation.PlainText'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('value',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Text * Representation.PlainText',)
    value: str

@dataclass(kw_only=True)
class DurationSeconds(SemanticModel):
    _semantics: ClassVar = product_names(['DurationSeconds', 'Duration', 'Representation.Seconds'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('seconds',)
    _units: ClassVar[dict[str, str]] = {'seconds': 's'}
    _charts: ClassVar[tuple[str, ...]] = ('Duration * Representation.Seconds',)
    seconds: float

@dataclass(kw_only=True)
class AngleRadians(SemanticModel):
    _semantics: ClassVar = product_names(['AngleRadians', 'Angle', 'Representation.Radians'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('rad',)
    _units: ClassVar[dict[str, str]] = {'rad': 'rad'}
    _charts: ClassVar[tuple[str, ...]] = ('Angle * Representation.Radians',)
    rad: float

@dataclass(kw_only=True)
class DistanceMeters(SemanticModel):
    _semantics: ClassVar = product_names(['DistanceMeters', 'Distance', 'Representation.Meters'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('m',)
    _units: ClassVar[dict[str, str]] = {'m': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Distance * Representation.Meters',)
    m: float

@dataclass(kw_only=True)
class SpeedMetersPerSecond(SemanticModel):
    _semantics: ClassVar = product_names(['SpeedMetersPerSecond', 'Speed', 'Representation.MetersPerSecond'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('mps',)
    _units: ClassVar[dict[str, str]] = {'mps': 'm/s'}
    _charts: ClassVar[tuple[str, ...]] = ('Speed * Representation.MetersPerSecond',)
    mps: float

@dataclass(kw_only=True)
class AltitudeMSL(SemanticModel):
    _semantics: ClassVar = product_names(['AltitudeMSL', 'Altitude', 'Representation.MSL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('m',)
    _units: ClassVar[dict[str, str]] = {'m': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Altitude * Representation.MSL',)
    m: float

@dataclass(kw_only=True)
class AltitudeFlightLevel(SemanticModel):
    _semantics: ClassVar = product_names(['AltitudeFlightLevel', 'Altitude', 'Representation.FlightLevel'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('fl',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Altitude * Representation.FlightLevel',)
    fl: float

@dataclass(kw_only=True)
class ItemCount(SemanticModel):
    _semantics: ClassVar = product_names(['ItemCount', 'Count', 'Representation.Count'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('count',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Count * Representation.Count',)
    count: int

@dataclass(kw_only=True)
class OrdinalValue(SemanticModel):
    _semantics: ClassVar = product_names(['OrdinalValue', 'Ordinal', 'Representation.Ordinal'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('n',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Ordinal * Representation.Ordinal',)
    n: int

@dataclass(kw_only=True)
class ProtocolCode(SemanticModel):
    _semantics: ClassVar = product_names(['ProtocolCode', 'Code', 'Representation.Protocol'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('code',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Code * Representation.Protocol',)
    code: int

@dataclass(kw_only=True)
class ScalarDecimal(SemanticModel):
    _semantics: ClassVar = product_names(['ScalarDecimal', 'Scalar', 'Representation.Decimal'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('value',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Scalar * Representation.Decimal',)
    value: float

@dataclass(kw_only=True)
class ScalarInteger(SemanticModel):
    _semantics: ClassVar = product_names(['ScalarInteger', 'Scalar', 'Representation.Integer'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('value',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Scalar * Representation.Integer',)
    value: int

@dataclass(kw_only=True)
class Mark(Data):
    _semantics: ClassVar = product_names(['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name', 'lat', 'lon', 'h')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic',)
    uid: UID
    name: PlainText | None = None
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
    uid: UID
    instruction: PlainText
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

@dataclass(kw_only=True)
class TaskManeuver(Task):
    _semantics: ClassVar = product_names(['TaskManeuver'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: TaskIntent

@dataclass(kw_only=True)
class TaskInformation(Task):
    _semantics: ClassVar = product_names(['TaskInformation'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: TaskIntent

@dataclass(kw_only=True)
class TaskEffect(Task):
    _semantics: ClassVar = product_names(['TaskEffect'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: TaskIntent

@dataclass(kw_only=True)
class TaskTransport(Task):
    _semantics: ClassVar = product_names(['TaskTransport'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('intent',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    intent: TaskIntent

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
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    id: IntID | None = None
    revision: ItemCount | None = None
    created_ts: Timestamp
    updated_ts: Timestamp
    origin_system: PlainText
    provenance: list[PlainText] = field(default_factory=list)

@dataclass(kw_only=True)
class Time(State):
    _semantics: ClassVar = product_names(['Time'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Timestamp(SemanticModel):
    _semantics: ClassVar = product_names(['Timestamp', 'Time', 'Representation.Epoch'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('utime', 'tz')
    _units: ClassVar[dict[str, str]] = {'utime': 's'}
    _charts: ClassVar[tuple[str, ...]] = ('Time * Representation.Epoch',)
    utime: float
    tz: int

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
    min_value: ScalarDecimal | None = None
    max_value: ScalarDecimal | None = None

@dataclass(kw_only=True)
class MetadataValue(Data):
    _semantics: ClassVar = product_names(['MetadataValue'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('str', 'int', 'float', 'bool')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    str: PlainText | None = None
    int: ScalarInteger | None = None
    float: ScalarDecimal | None = None
    bool: bool | None = None

@dataclass(kw_only=True)
class Condition(Data):
    _semantics: ClassVar = product_names(['Condition'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

@dataclass(kw_only=True)
class Predicate(Condition):
    _semantics: ClassVar = product_names(['Predicate'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('subject_ref',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    subject_ref: UID | None = None

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
class SuccessCriterion(Data):
    _semantics: ClassVar = product_names(['SuccessCriterion'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('statement', 'metric', 'target_value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    statement: PlainText
    metric: PlainText | None = None
    target_value: MetadataValue | None = None

@dataclass(kw_only=True)
class Role(Data):
    _semantics: ClassVar = product_names(['Role'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: PlainText | None = None

@dataclass(kw_only=True)
class Resource(Object):
    _semantics: ClassVar = product_names(['Resource'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID | None = None
    name: PlainText | None = None

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
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    earliest_start: Timestamp | None = None
    latest_finish: Timestamp | None = None

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
    _declared_fields: ClassVar[tuple[str, ...]] = ('record', 'uid', 'id', 'name', 'intent', 'desired_state', 'success_criteria', 'priority', 'status', 'start_time', 'deadline')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    record: Record | None = None
    uid: UID
    id: IntID | None = None
    name: PlainText
    intent: PlainText
    desired_state: PlainText
    success_criteria: list[SuccessCriterion] = field(default_factory=list)
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    start_time: Timestamp | None = None
    deadline: Timestamp | None = None

@dataclass(kw_only=True)
class Command(Directive):
    _semantics: ClassVar = product_names(['Command'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID

@dataclass(kw_only=True)
class StateChangeCommand(Command):
    _semantics: ClassVar = product_names(['StateChangeCommand', 'Engagement'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operation', 'property_name', 'value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operation: CommandOperation
    property_name: PlainText | None = None
    value: MetadataValue | None = None

@dataclass(kw_only=True)
class ProcessControlCommand(Command):
    _semantics: ClassVar = product_names(['ProcessControlCommand', 'Activity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operation', 'process_name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operation: CommandOperation
    process_name: PlainText | None = None

@dataclass(kw_only=True)
class ConfigurationCommand(Command):
    _semantics: ClassVar = product_names(['ConfigurationCommand'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operation', 'parameter_name', 'value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operation: CommandOperation
    parameter_name: PlainText | None = None
    value: MetadataValue | None = None

@dataclass(kw_only=True)
class MotionCommand(Command):
    _semantics: ClassVar = product_names(['MotionCommand', 'Position'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operation', 'destination', 'path', 'radius_m', 'speed_ms', 'yaw_rad')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operation: CommandOperation
    destination: GlobalPosition | None = None
    path: GeoPath | None = None
    radius_m: DistanceMeters | None = None
    speed_ms: SpeedMetersPerSecond | None = None
    yaw_rad: AngleRadians | None = None

@dataclass(kw_only=True)
class ResourceCommand(Command):
    _semantics: ClassVar = product_names(['ResourceCommand', 'Hold'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operation', 'quantity')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operation: CommandOperation
    quantity: ItemCount | None = None

@dataclass(kw_only=True)
class Authority(Control):
    _semantics: ClassVar = product_names(['Authority'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('record', 'uid', 'id', 'role')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    record: Record | None = None
    uid: UID
    id: IntID | None = None
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
    uid: UID
    id: IntID | None = None
    name: PlainText | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

@dataclass(kw_only=True)
class PlanContingency(Data):
    _semantics: ClassVar = product_names(['PlanContingency'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('condition',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    condition: Condition

@dataclass(kw_only=True)
class VehicleState(SemanticModel):
    _semantics: ClassVar = product_names(['Position', 'Representation.Geodetic', 'Velocity', 'Representation.LocalCartesian', 'Attitude', 'Representation.LocalEuler'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'lat', 'lon', 'h', 'vx', 'vy', 'vz', 'roll', 'pitch', 'yaw')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm', 'vx': 'm/s', 'vy': 'm/s', 'vz': 'm/s', 'roll': 'rad', 'pitch': 'rad', 'yaw': 'rad'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic', 'Velocity * Representation.LocalCartesian', 'Attitude * Representation.LocalEuler')
    _projection: ClassVar[bool] = True
    uid: UID
    lat: float | None = None
    lon: float | None = None
    h: float | None = None
    vx: float | None = None
    vy: float | None = None
    vz: float | None = None
    roll: float | None = None
    pitch: float | None = None
    yaw: float | None = None

AssignedWork = RelationType('AssignedWork', (Entity, Task), operand_names=('assignee', 'work'))
ConstrainedBy = RelationType('ConstrainedBy', (Control, Constraint), operand_names=('subject', 'constraint'))
OwnedBy = RelationType('OwnedBy', (Objective, Entity), operand_names=('objective', 'owner'))
Holds = RelationType('Holds', (Authority, Entity), operand_names=('authority', 'holder'))
GrantedBy = RelationType('GrantedBy', (Authority, Entity), operand_names=('authority', 'grantor'))
Controls = RelationType('Controls', (Lease, Object), operand_names=('lease', 'asset'))
Contains = RelationType('Contains', (Plan, Root), operand_names=('plan', 'item'))

REGISTRY_SPEC = {'axes': {'Substrate': {'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL', 'CYBER']}, 'PhysicalDomain': {'description': 'A bounded thing operates in exactly one domain.', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE']}, 'Controller': {'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'description': 'Airframe construction, independent of takeoff capability.', 'cardinality': 'one', 'applies': {'all': ['Machine', 'PhysicalDomain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING']}, 'Representation': {'description': 'How a semantic quantity becomes irreducible data variables.', 'cardinality': 'many', 'values': ['Geodetic', 'LocalCartesian', 'LocalEuler', 'Quaternion', 'Epoch', 'UID', 'IntID', 'PlainText', 'Seconds', 'Radians', 'Meters', 'MetersPerSecond', 'MSL', 'FlightLevel', 'Count', 'Ordinal', 'Protocol', 'Decimal', 'Integer']}, 'BloodGroup': {'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'requires': ['Biological'], 'values': ['A_POS', 'A_NEG', 'B_POS', 'B_NEG', 'AB_POS', 'AB_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity', 'Engagement', 'Activity', 'Paused', 'Hold']}, 'values': ['TRUE', 'FALSE']}}, 'models': {'Root': {'parent': None, 'semantics': ['Root'], 'fields': [], 'chart_fields': []}, 'Object': {'parent': 'Root', 'semantics': ['Object'], 'fields': [], 'chart_fields': []}, 'Locality': {'parent': 'Object', 'semantics': ['Locality'], 'fields': [{'name': 'name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Entity': {'parent': 'Object', 'semantics': ['Entity'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Biological': {'parent': 'Entity', 'semantics': ['Biological', 'Substrate.BIOLOGICAL'], 'fields': [], 'chart_fields': []}, 'Person': {'parent': 'Biological', 'semantics': ['Substrate.BIOLOGICAL', 'Person'], 'fields': [{'name': 'name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Actor': {'parent': 'Person', 'semantics': ['Substrate.BIOLOGICAL', 'Actor'], 'fields': [{'name': 'role', 'type': 'optional Role', 'default': None}], 'chart_fields': []}, 'Machine': {'parent': 'Entity', 'semantics': ['Machine', 'Substrate.MECHANICAL'], 'fields': [{'name': 'serial_number', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Vehicle': {'parent': 'Machine', 'semantics': ['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'], 'fields': [{'name': 'model', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'CrewedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'], 'fields': [], 'chart_fields': []}, 'UnmannedVehicle': {'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'], 'fields': [], 'chart_fields': []}, 'Data': {'parent': 'Root', 'semantics': ['Data'], 'fields': [], 'chart_fields': []}, 'State': {'parent': 'Data', 'semantics': ['State'], 'fields': [], 'chart_fields': []}, 'Position': {'parent': 'State', 'semantics': ['Position'], 'fields': [], 'chart_fields': []}, 'Velocity': {'parent': 'State', 'semantics': ['Velocity'], 'fields': [], 'chart_fields': []}, 'Attitude': {'parent': 'State', 'semantics': ['Attitude'], 'fields': [], 'chart_fields': []}, 'Identity': {'parent': 'State', 'semantics': ['Identity'], 'fields': [], 'chart_fields': []}, 'Classification': {'parent': 'State', 'semantics': ['Classification'], 'fields': [], 'chart_fields': []}, 'Existence': {'parent': 'State', 'semantics': ['Existence'], 'fields': [], 'chart_fields': []}, 'Connectivity': {'parent': 'State', 'semantics': ['Connectivity'], 'fields': [], 'chart_fields': []}, 'Engagement': {'parent': 'State', 'semantics': ['Engagement'], 'fields': [], 'chart_fields': []}, 'Activity': {'parent': 'State', 'semantics': ['Activity'], 'fields': [], 'chart_fields': []}, 'Paused': {'parent': 'State', 'semantics': ['Paused'], 'fields': [], 'chart_fields': []}, 'Hold': {'parent': 'State', 'semantics': ['Hold'], 'fields': [], 'chart_fields': []}, 'Text': {'parent': 'State', 'semantics': ['Text'], 'fields': [], 'chart_fields': []}, 'Duration': {'parent': 'State', 'semantics': ['Duration'], 'fields': [], 'chart_fields': []}, 'Angle': {'parent': 'State', 'semantics': ['Angle'], 'fields': [], 'chart_fields': []}, 'Distance': {'parent': 'State', 'semantics': ['Distance'], 'fields': [], 'chart_fields': []}, 'Speed': {'parent': 'State', 'semantics': ['Speed'], 'fields': [], 'chart_fields': []}, 'Count': {'parent': 'State', 'semantics': ['Count'], 'fields': [], 'chart_fields': []}, 'Ordinal': {'parent': 'State', 'semantics': ['Ordinal'], 'fields': [], 'chart_fields': []}, 'Code': {'parent': 'State', 'semantics': ['Code'], 'fields': [], 'chart_fields': []}, 'Scalar': {'parent': 'State', 'semantics': ['Scalar'], 'fields': [], 'chart_fields': []}, 'Altitude': {'parent': 'State', 'semantics': ['Altitude'], 'fields': [], 'chart_fields': [], 'applies': ['PhysicalDomain.AIR']}, 'GlobalPosition': {'parent': None, 'semantics': ['GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'LocalPosition': {'parent': None, 'semantics': ['LocalPosition', 'Position', 'Representation.LocalCartesian'], 'fields': [{'name': 'x', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'y', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'z', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Position * Representation.LocalCartesian', 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}]}, 'LocalVelocity': {'parent': None, 'semantics': ['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'], 'fields': [{'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Velocity * Representation.LocalCartesian', 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}]}, 'LocalAttitude': {'parent': None, 'semantics': ['LocalAttitude', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}], 'chart_fields': [{'chart': 'Attitude * Representation.LocalEuler', 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}]}, 'UID': {'parent': None, 'semantics': ['UID', 'Identity', 'Representation.UID'], 'fields': [{'name': 'uid', 'type': 'string', 'default': None, 'unit': None, 'chart': 'Identity * Representation.UID'}], 'chart_fields': [{'chart': 'Identity * Representation.UID', 'coords': [{'name': 'uid', 'type': 'string', 'unit': None}]}]}, 'IntID': {'parent': None, 'semantics': ['IntID', 'Identity', 'Representation.IntID'], 'fields': [{'name': 'id', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Identity * Representation.IntID'}], 'chart_fields': [{'chart': 'Identity * Representation.IntID', 'coords': [{'name': 'id', 'type': 'int', 'unit': None}]}]}, 'PlainText': {'parent': None, 'semantics': ['PlainText', 'Text', 'Representation.PlainText'], 'fields': [{'name': 'value', 'type': 'string', 'default': None, 'unit': None, 'chart': 'Text * Representation.PlainText'}], 'chart_fields': [{'chart': 'Text * Representation.PlainText', 'coords': [{'name': 'value', 'type': 'string', 'unit': None}]}]}, 'DurationSeconds': {'parent': None, 'semantics': ['DurationSeconds', 'Duration', 'Representation.Seconds'], 'fields': [{'name': 'seconds', 'type': 'float', 'default': None, 'unit': 's', 'chart': 'Duration * Representation.Seconds'}], 'chart_fields': [{'chart': 'Duration * Representation.Seconds', 'coords': [{'name': 'seconds', 'type': 'float', 'unit': 's'}]}]}, 'AngleRadians': {'parent': None, 'semantics': ['AngleRadians', 'Angle', 'Representation.Radians'], 'fields': [{'name': 'rad', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Angle * Representation.Radians'}], 'chart_fields': [{'chart': 'Angle * Representation.Radians', 'coords': [{'name': 'rad', 'type': 'float', 'unit': 'rad'}]}]}, 'DistanceMeters': {'parent': None, 'semantics': ['DistanceMeters', 'Distance', 'Representation.Meters'], 'fields': [{'name': 'm', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Distance * Representation.Meters'}], 'chart_fields': [{'chart': 'Distance * Representation.Meters', 'coords': [{'name': 'm', 'type': 'float', 'unit': 'm'}]}]}, 'SpeedMetersPerSecond': {'parent': None, 'semantics': ['SpeedMetersPerSecond', 'Speed', 'Representation.MetersPerSecond'], 'fields': [{'name': 'mps', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Speed * Representation.MetersPerSecond'}], 'chart_fields': [{'chart': 'Speed * Representation.MetersPerSecond', 'coords': [{'name': 'mps', 'type': 'float', 'unit': 'm/s'}]}]}, 'AltitudeMSL': {'parent': None, 'semantics': ['AltitudeMSL', 'Altitude', 'Representation.MSL'], 'fields': [{'name': 'm', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Altitude * Representation.MSL'}], 'chart_fields': [{'chart': 'Altitude * Representation.MSL', 'coords': [{'name': 'm', 'type': 'float', 'unit': 'm'}]}]}, 'AltitudeFlightLevel': {'parent': None, 'semantics': ['AltitudeFlightLevel', 'Altitude', 'Representation.FlightLevel'], 'fields': [{'name': 'fl', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Altitude * Representation.FlightLevel'}], 'chart_fields': [{'chart': 'Altitude * Representation.FlightLevel', 'coords': [{'name': 'fl', 'type': 'float', 'unit': None}]}]}, 'ItemCount': {'parent': None, 'semantics': ['ItemCount', 'Count', 'Representation.Count'], 'fields': [{'name': 'count', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Count * Representation.Count'}], 'chart_fields': [{'chart': 'Count * Representation.Count', 'coords': [{'name': 'count', 'type': 'int', 'unit': None}]}]}, 'OrdinalValue': {'parent': None, 'semantics': ['OrdinalValue', 'Ordinal', 'Representation.Ordinal'], 'fields': [{'name': 'n', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Ordinal * Representation.Ordinal'}], 'chart_fields': [{'chart': 'Ordinal * Representation.Ordinal', 'coords': [{'name': 'n', 'type': 'int', 'unit': None}]}]}, 'ProtocolCode': {'parent': None, 'semantics': ['ProtocolCode', 'Code', 'Representation.Protocol'], 'fields': [{'name': 'code', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Code * Representation.Protocol'}], 'chart_fields': [{'chart': 'Code * Representation.Protocol', 'coords': [{'name': 'code', 'type': 'int', 'unit': None}]}]}, 'ScalarDecimal': {'parent': None, 'semantics': ['ScalarDecimal', 'Scalar', 'Representation.Decimal'], 'fields': [{'name': 'value', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Scalar * Representation.Decimal'}], 'chart_fields': [{'chart': 'Scalar * Representation.Decimal', 'coords': [{'name': 'value', 'type': 'float', 'unit': None}]}]}, 'ScalarInteger': {'parent': None, 'semantics': ['ScalarInteger', 'Scalar', 'Representation.Integer'], 'fields': [{'name': 'value', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Scalar * Representation.Integer'}], 'chart_fields': [{'chart': 'Scalar * Representation.Integer', 'coords': [{'name': 'value', 'type': 'int', 'unit': None}]}]}, 'Mark': {'parent': 'Data', 'semantics': ['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'name', 'type': 'optional PlainText', 'default': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}]}, 'Control': {'parent': 'Root', 'semantics': ['Control'], 'fields': [], 'chart_fields': []}, 'Directive': {'parent': 'Control', 'semantics': ['Directive'], 'fields': [], 'chart_fields': []}, 'Task': {'parent': 'Directive', 'semantics': ['Task'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'instruction', 'type': 'PlainText', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE'}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW'}], 'chart_fields': []}, 'TaskManeuver': {'parent': 'Task', 'semantics': ['TaskManeuver'], 'fields': [{'name': 'intent', 'type': 'TaskIntent', 'default': None}], 'chart_fields': []}, 'TaskInformation': {'parent': 'Task', 'semantics': ['TaskInformation'], 'fields': [{'name': 'intent', 'type': 'TaskIntent', 'default': None}], 'chart_fields': []}, 'TaskEffect': {'parent': 'Task', 'semantics': ['TaskEffect'], 'fields': [{'name': 'intent', 'type': 'TaskIntent', 'default': None}], 'chart_fields': []}, 'TaskTransport': {'parent': 'Task', 'semantics': ['TaskTransport'], 'fields': [{'name': 'intent', 'type': 'TaskIntent', 'default': None}], 'chart_fields': []}, 'Mission': {'parent': 'Directive', 'semantics': ['Mission'], 'fields': [], 'chart_fields': []}, 'Record': {'parent': 'Data', 'semantics': ['Record'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'id', 'type': 'optional IntID', 'default': None}, {'name': 'revision', 'type': 'optional ItemCount', 'default': None}, {'name': 'created_ts', 'type': 'Timestamp', 'default': None}, {'name': 'updated_ts', 'type': 'Timestamp', 'default': None}, {'name': 'origin_system', 'type': 'PlainText', 'default': None}, {'name': 'provenance', 'type': 'list[PlainText]', 'default': None}], 'chart_fields': []}, 'Time': {'parent': 'State', 'semantics': ['Time'], 'fields': [], 'chart_fields': []}, 'Timestamp': {'parent': None, 'semantics': ['Timestamp', 'Time', 'Representation.Epoch'], 'fields': [{'name': 'utime', 'type': 'float', 'default': None, 'unit': 's', 'chart': 'Time * Representation.Epoch'}, {'name': 'tz', 'type': 'int', 'default': None, 'unit': None, 'chart': 'Time * Representation.Epoch'}], 'chart_fields': [{'chart': 'Time * Representation.Epoch', 'coords': [{'name': 'utime', 'type': 'float', 'unit': 's'}, {'name': 'tz', 'type': 'int', 'unit': None}]}]}, 'Range': {'parent': 'Data', 'semantics': ['Range'], 'fields': [], 'chart_fields': []}, 'NumericRange': {'parent': 'Range', 'semantics': ['NumericRange'], 'fields': [{'name': 'min_value', 'type': 'optional ScalarDecimal', 'default': None}, {'name': 'max_value', 'type': 'optional ScalarDecimal', 'default': None}], 'chart_fields': []}, 'MetadataValue': {'parent': 'Data', 'semantics': ['MetadataValue'], 'fields': [{'name': 'str', 'type': 'optional PlainText', 'default': None}, {'name': 'int', 'type': 'optional ScalarInteger', 'default': None}, {'name': 'float', 'type': 'optional ScalarDecimal', 'default': None}, {'name': 'bool', 'type': 'optional bool', 'default': None}], 'chart_fields': []}, 'Condition': {'parent': 'Data', 'semantics': ['Condition'], 'fields': [], 'chart_fields': []}, 'Predicate': {'parent': 'Condition', 'semantics': ['Predicate'], 'fields': [{'name': 'subject_ref', 'type': 'optional UID', 'default': None}], 'chart_fields': []}, 'BooleanLogic': {'parent': 'Condition', 'semantics': ['BooleanLogic'], 'fields': [{'name': 'operator', 'type': 'BooleanOperator', 'default': None}, {'name': 'terms', 'type': 'list[Condition]', 'default': None}], 'chart_fields': []}, 'GeoPath': {'parent': 'Data', 'semantics': ['GeoPath'], 'fields': [{'name': 'points', 'type': 'list[GlobalPosition]', 'default': None}], 'chart_fields': []}, 'SuccessCriterion': {'parent': 'Data', 'semantics': ['SuccessCriterion'], 'fields': [{'name': 'statement', 'type': 'PlainText', 'default': None}, {'name': 'metric', 'type': 'optional PlainText', 'default': None}, {'name': 'target_value', 'type': 'optional MetadataValue', 'default': None}], 'chart_fields': []}, 'Role': {'parent': 'Data', 'semantics': ['Role'], 'fields': [{'name': 'name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Resource': {'parent': 'Object', 'semantics': ['Resource'], 'fields': [{'name': 'uid', 'type': 'optional UID', 'default': None}, {'name': 'name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'Constraint': {'parent': 'Control', 'semantics': ['Constraint'], 'fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None}], 'chart_fields': []}, 'TaskTimeWindow': {'parent': 'Constraint', 'semantics': ['TaskTimeWindow'], 'fields': [{'name': 'earliest_start', 'type': 'optional Timestamp', 'default': None}, {'name': 'latest_finish', 'type': 'optional Timestamp', 'default': None}], 'chart_fields': []}, 'WeatherLimits': {'parent': 'Constraint', 'semantics': ['WeatherLimits'], 'fields': [{'name': 'ifr', 'type': 'optional bool', 'default': None}, {'name': 'night', 'type': 'optional bool', 'default': None}, {'name': 'rain', 'type': 'optional NumericRange', 'default': None}, {'name': 'snow', 'type': 'optional NumericRange', 'default': None}, {'name': 'temp', 'type': 'optional NumericRange', 'default': None}, {'name': 'wind', 'type': 'optional NumericRange', 'default': None}, {'name': 'vis', 'type': 'optional NumericRange', 'default': None}, {'name': 'icing', 'type': 'optional bool', 'default': None}], 'chart_fields': []}, 'Objective': {'parent': 'Control', 'semantics': ['Objective'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None}, {'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'id', 'type': 'optional IntID', 'default': None}, {'name': 'name', 'type': 'PlainText', 'default': None}, {'name': 'intent', 'type': 'PlainText', 'default': None}, {'name': 'desired_state', 'type': 'PlainText', 'default': None}, {'name': 'success_criteria', 'type': 'list[SuccessCriterion]', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE'}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW'}, {'name': 'start_time', 'type': 'optional Timestamp', 'default': None}, {'name': 'deadline', 'type': 'optional Timestamp', 'default': None}], 'chart_fields': []}, 'Command': {'parent': 'Directive', 'semantics': ['Command'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}], 'chart_fields': []}, 'StateChangeCommand': {'parent': 'Command', 'semantics': ['StateChangeCommand', 'Engagement'], 'fields': [{'name': 'operation', 'type': 'CommandOperation', 'default': None}, {'name': 'property_name', 'type': 'optional PlainText', 'default': None}, {'name': 'value', 'type': 'optional MetadataValue', 'default': None}], 'chart_fields': []}, 'ProcessControlCommand': {'parent': 'Command', 'semantics': ['ProcessControlCommand', 'Activity'], 'fields': [{'name': 'operation', 'type': 'CommandOperation', 'default': None}, {'name': 'process_name', 'type': 'optional PlainText', 'default': None}], 'chart_fields': []}, 'ConfigurationCommand': {'parent': 'Command', 'semantics': ['ConfigurationCommand'], 'fields': [{'name': 'operation', 'type': 'CommandOperation', 'default': None}, {'name': 'parameter_name', 'type': 'optional PlainText', 'default': None}, {'name': 'value', 'type': 'optional MetadataValue', 'default': None}], 'chart_fields': []}, 'MotionCommand': {'parent': 'Command', 'semantics': ['MotionCommand', 'Position'], 'fields': [{'name': 'operation', 'type': 'CommandOperation', 'default': None}, {'name': 'destination', 'type': 'optional GlobalPosition', 'default': None}, {'name': 'path', 'type': 'optional GeoPath', 'default': None}, {'name': 'radius_m', 'type': 'optional DistanceMeters', 'default': None}, {'name': 'speed_ms', 'type': 'optional SpeedMetersPerSecond', 'default': None}, {'name': 'yaw_rad', 'type': 'optional AngleRadians', 'default': None}], 'chart_fields': []}, 'ResourceCommand': {'parent': 'Command', 'semantics': ['ResourceCommand', 'Hold'], 'fields': [{'name': 'operation', 'type': 'CommandOperation', 'default': None}, {'name': 'quantity', 'type': 'optional ItemCount', 'default': None}], 'chart_fields': []}, 'Authority': {'parent': 'Control', 'semantics': ['Authority'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None}, {'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'id', 'type': 'optional IntID', 'default': None}, {'name': 'role', 'type': 'optional Role', 'default': None}], 'chart_fields': []}, 'Lease': {'parent': 'Authority', 'semantics': ['Lease'], 'fields': [{'name': 'bound', 'type': 'optional Condition', 'default': None}, {'name': 'control_level', 'type': 'optional ControlLevel', 'default': None}], 'chart_fields': []}, 'Plan': {'parent': 'Control', 'semantics': ['Plan'], 'fields': [{'name': 'record', 'type': 'optional Record', 'default': None}, {'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'id', 'type': 'optional IntID', 'default': None}, {'name': 'name', 'type': 'optional PlainText', 'default': None}, {'name': 'approval_state', 'type': 'PlanApprovalState', 'default': 'DRAFT'}], 'chart_fields': []}, 'PlanContingency': {'parent': 'Data', 'semantics': ['PlanContingency'], 'fields': [{'name': 'condition', 'type': 'Condition', 'default': None}], 'chart_fields': []}}, 'charts': [{'display': 'Position * Representation.Geodetic', 'factors': ['Position', 'Representation.Geodetic'], 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}, {'display': 'Position * Representation.LocalCartesian', 'factors': ['Position', 'Representation.LocalCartesian'], 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}, {'display': 'Velocity * Representation.LocalCartesian', 'factors': ['Velocity', 'Representation.LocalCartesian'], 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}, {'display': 'Attitude * Representation.LocalEuler', 'factors': ['Attitude', 'Representation.LocalEuler'], 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}, {'display': 'Attitude * Representation.Quaternion', 'factors': ['Attitude', 'Representation.Quaternion'], 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}, {'display': 'Time * Representation.Epoch', 'factors': ['Time', 'Representation.Epoch'], 'coords': [{'name': 'utime', 'type': 'float', 'unit': 's'}, {'name': 'tz', 'type': 'int', 'unit': None}]}, {'display': 'Identity * Representation.UID', 'factors': ['Identity', 'Representation.UID'], 'coords': [{'name': 'uid', 'type': 'string', 'unit': None}]}, {'display': 'Identity * Representation.IntID', 'factors': ['Identity', 'Representation.IntID'], 'coords': [{'name': 'id', 'type': 'int', 'unit': None}]}, {'display': 'Text * Representation.PlainText', 'factors': ['Text', 'Representation.PlainText'], 'coords': [{'name': 'value', 'type': 'string', 'unit': None}]}, {'display': 'Duration * Representation.Seconds', 'factors': ['Duration', 'Representation.Seconds'], 'coords': [{'name': 'seconds', 'type': 'float', 'unit': 's'}]}, {'display': 'Angle * Representation.Radians', 'factors': ['Angle', 'Representation.Radians'], 'coords': [{'name': 'rad', 'type': 'float', 'unit': 'rad'}]}, {'display': 'Distance * Representation.Meters', 'factors': ['Distance', 'Representation.Meters'], 'coords': [{'name': 'm', 'type': 'float', 'unit': 'm'}]}, {'display': 'Speed * Representation.MetersPerSecond', 'factors': ['Speed', 'Representation.MetersPerSecond'], 'coords': [{'name': 'mps', 'type': 'float', 'unit': 'm/s'}]}, {'display': 'Altitude * Representation.MSL', 'factors': ['Altitude', 'Representation.MSL'], 'coords': [{'name': 'm', 'type': 'float', 'unit': 'm'}]}, {'display': 'Altitude * Representation.FlightLevel', 'factors': ['Altitude', 'Representation.FlightLevel'], 'coords': [{'name': 'fl', 'type': 'float', 'unit': None}]}, {'display': 'Count * Representation.Count', 'factors': ['Count', 'Representation.Count'], 'coords': [{'name': 'count', 'type': 'int', 'unit': None}]}, {'display': 'Ordinal * Representation.Ordinal', 'factors': ['Ordinal', 'Representation.Ordinal'], 'coords': [{'name': 'n', 'type': 'int', 'unit': None}]}, {'display': 'Code * Representation.Protocol', 'factors': ['Code', 'Representation.Protocol'], 'coords': [{'name': 'code', 'type': 'int', 'unit': None}]}, {'display': 'Scalar * Representation.Decimal', 'factors': ['Scalar', 'Representation.Decimal'], 'coords': [{'name': 'value', 'type': 'float', 'unit': None}]}, {'display': 'Scalar * Representation.Integer', 'factors': ['Scalar', 'Representation.Integer'], 'coords': [{'name': 'value', 'type': 'int', 'unit': None}]}], 'expressions': {'MOVE': {'description': 'Move an actor until its position is the destination.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.MOVE']}, 'HOLD': {'description': "Maintain an actor's position at the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.HOLD']}, 'LOCATE': {'description': 'Solve for the position of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.LOCATE']}, 'TRACK': {'description': "Maintain awareness of an entity's position.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.TRACK']}, 'IDENTIFY': {'description': 'Solve for the identity of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'identity': ['Identity']}, 'equations': [{'quantity': 'Identity', 'of': 'target', 'equals': 'identity'}], 'words': ['TaskIntent.IDENTIFY']}, 'CLASSIFY': {'description': 'Solve for the classification of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'classification': ['Classification']}, 'equations': [{'quantity': 'Classification', 'of': 'target', 'equals': 'classification'}], 'words': ['TaskIntent.CLASSIFY']}, 'CREATE': {'description': 'Make an object exist.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.CREATE']}, 'REMOVE': {'description': 'Make an object cease to exist.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.REMOVE']}, 'FOLLOW': {'description': 'Follow a path.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'path': ['GeoPath']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.FOLLOW']}, 'MEASURE': {'description': 'Measure a state of a target.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'measurement': ['State']}, 'equations': [], 'words': ['TaskIntent.MEASURE']}, 'MODIFY': {'description': "Change an object's state.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.MODIFY']}, 'RESTORE': {'description': 'Return an object to a prior state.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.RESTORE']}, 'PROTECT': {'description': 'Keep an object in its current state.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.PROTECT']}, 'DENY': {'description': 'Prevent connectivity to an object.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.DENY']}, 'TRANSPORT': {'description': 'Move a thing between places; which end and what moves are bindings.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'cargo': ['Object'], 'origin': ['Position'], 'destination': ['Position']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.TRANSPORT']}, 'ENGAGE': {'description': 'Assert the target state true.', 'factors': ['Command', 'TruthTarget.TRUE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ENGAGE']}, 'DISENGAGE': {'description': 'Assert the target state false.', 'factors': ['Command', 'TruthTarget.FALSE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.DISENGAGE']}, 'PAUSE': {'description': 'Hold a running process paused.', 'factors': ['Command', 'Paused', 'TruthTarget.TRUE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.PAUSE']}, 'RESUME': {'description': 'Release a process from paused.', 'factors': ['Command', 'Paused', 'TruthTarget.FALSE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESUME']}, 'SET': {'description': 'Set a declared state property on the target.', 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.SET']}, 'DIRECT': {'description': 'Direct the target to a destination or along a path.', 'factors': ['Command', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Object'], 'destination': ['Position'], 'path': ['GeoPath']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'destination'}], 'words': ['CommandOperation.MOVE']}, 'ALLOCATE': {'description': 'Allocate a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ALLOCATE']}, 'TRANSFER': {'description': 'Transfer a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.TRANSFER']}, 'LOAD_CONFIGURATION': {'description': 'Load a referenced configuration on the target.', 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.LOAD_CONFIGURATION']}, 'RESET': {'description': 'Reset the target to its initial state.', 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESET']}}, 'word_expressions': {'TaskIntent.MOVE': 'MOVE', 'TaskIntent.HOLD': 'HOLD', 'TaskIntent.LOCATE': 'LOCATE', 'TaskIntent.TRACK': 'TRACK', 'TaskIntent.IDENTIFY': 'IDENTIFY', 'TaskIntent.CLASSIFY': 'CLASSIFY', 'TaskIntent.CREATE': 'CREATE', 'TaskIntent.REMOVE': 'REMOVE', 'TaskIntent.FOLLOW': 'FOLLOW', 'TaskIntent.MEASURE': 'MEASURE', 'TaskIntent.MODIFY': 'MODIFY', 'TaskIntent.RESTORE': 'RESTORE', 'TaskIntent.PROTECT': 'PROTECT', 'TaskIntent.DENY': 'DENY', 'TaskIntent.TRANSPORT': 'TRANSPORT', 'CommandOperation.ENGAGE': 'ENGAGE', 'CommandOperation.DISENGAGE': 'DISENGAGE', 'CommandOperation.PAUSE': 'PAUSE', 'CommandOperation.RESUME': 'RESUME', 'CommandOperation.SET': 'SET', 'CommandOperation.MOVE': 'DIRECT', 'CommandOperation.ALLOCATE': 'ALLOCATE', 'CommandOperation.TRANSFER': 'TRANSFER', 'CommandOperation.LOAD_CONFIGURATION': 'LOAD_CONFIGURATION', 'CommandOperation.RESET': 'RESET'}, 'aliases': {'AirMission': ['Mission', 'PhysicalDomain.AIR'], 'AirTask': ['Task', 'PhysicalDomain.AIR'], 'UGV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'], 'UAV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'], 'Drone': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'], 'Geodetic': ['Representation.Geodetic'], 'LocalCartesian': ['Representation.LocalCartesian'], 'LocalEuler': ['Representation.LocalEuler'], 'Quaternion': ['Representation.Quaternion'], 'Epoch': ['Representation.Epoch']}, 'relations': {'AssignedWork': {'signature': ['Entity', 'Task'], 'operand_names': ['assignee', 'work']}, 'ConstrainedBy': {'signature': ['Control', 'Constraint'], 'operand_names': ['subject', 'constraint']}, 'OwnedBy': {'signature': ['Objective', 'Entity'], 'operand_names': ['objective', 'owner']}, 'Holds': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'holder']}, 'GrantedBy': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'grantor']}, 'Controls': {'signature': ['Lease', 'Object'], 'operand_names': ['lease', 'asset']}, 'Contains': {'signature': ['Plan', 'Root'], 'operand_names': ['plan', 'item']}}, 'projections': {'VehicleState': {'semantics': ['Position', 'Representation.Geodetic', 'Velocity', 'Representation.LocalCartesian', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic', 'optional': True}, {'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian', 'optional': True}, {'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler', 'optional': True}], 'charts': ['Position * Representation.Geodetic', 'Velocity * Representation.LocalCartesian', 'Attitude * Representation.LocalEuler']}}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)

def new_store() -> Store:
    return Store(REGISTRY)
