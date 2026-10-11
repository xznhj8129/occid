# GENERATED FILE - DO NOT EDIT
from __future__ import annotations

from typing import Annotated, Any, ClassVar
from pydantic import Field

from ..runtime import (
    AxisValue,
    Equation,
    ExpressionType,
    RelationType,
    SemanticAxis,
    SemanticEnum,
    SemanticModel,
    SemanticReference,
    SemanticRegistry,
    Store,
    UID,
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

class Root(SemanticModel):
    _model_id: ClassVar[int] = 51
    _semantics: ClassVar = product_names(['Root'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Object(Root):
    _model_id: ClassVar[int] = 38
    _semantics: ClassVar = product_names(['Object'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Locality(Object):
    _model_id: ClassVar[int] = 33
    _semantics: ClassVar = product_names(['Locality'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

class Entity(Object):
    _model_id: ClassVar[int] = 23
    _semantics: ClassVar = product_names(['Entity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    name: str | None = None

class Biological(Entity):
    _model_id: ClassVar[int] = 7
    _semantics: ClassVar = product_names(['Biological', 'Substrate.BIOLOGICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Person(Biological):
    _model_id: ClassVar[int] = 42
    _semantics: ClassVar = product_names(['Substrate.BIOLOGICAL', 'Person'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

class Actor(Person):
    _model_id: ClassVar[int] = 2
    _semantics: ClassVar = product_names(['Substrate.BIOLOGICAL', 'Actor'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('role',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    role: Annotated[Role, SemanticReference('Role')] | None = None

class Machine(Entity):
    _model_id: ClassVar[int] = 34
    _semantics: ClassVar = product_names(['Machine', 'Substrate.MECHANICAL'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('serial_number',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    serial_number: str | None = None

class Vehicle(Machine):
    _model_id: ClassVar[int] = 60
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('model',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    model: str | None = None

class CrewedVehicle(Vehicle):
    _model_id: ClassVar[int] = 17
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class UnmannedVehicle(Vehicle):
    _model_id: ClassVar[int] = 59
    _semantics: ClassVar = product_names(['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Data(Root):
    _model_id: ClassVar[int] = 18
    _semantics: ClassVar = product_names(['Data'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class State(Data):
    _model_id: ClassVar[int] = 54
    _semantics: ClassVar = product_names(['State'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Position(State):
    _model_id: ClassVar[int] = 45
    _semantics: ClassVar = product_names(['Position'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Velocity(State):
    _model_id: ClassVar[int] = 61
    _semantics: ClassVar = product_names(['Velocity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Attitude(State):
    _model_id: ClassVar[int] = 5
    _semantics: ClassVar = product_names(['Attitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Identity(State):
    _model_id: ClassVar[int] = 28
    _semantics: ClassVar = product_names(['Identity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Classification(State):
    _model_id: ClassVar[int] = 9
    _semantics: ClassVar = product_names(['Classification'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Existence(State):
    _model_id: ClassVar[int] = 24
    _semantics: ClassVar = product_names(['Existence'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Connectivity(State):
    _model_id: ClassVar[int] = 13
    _semantics: ClassVar = product_names(['Connectivity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Engagement(State):
    _model_id: ClassVar[int] = 22
    _semantics: ClassVar = product_names(['Engagement'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Activity(State):
    _model_id: ClassVar[int] = 1
    _semantics: ClassVar = product_names(['Activity'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Paused(State):
    _model_id: ClassVar[int] = 41
    _semantics: ClassVar = product_names(['Paused'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Hold(State):
    _model_id: ClassVar[int] = 27
    _semantics: ClassVar = product_names(['Hold'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Text(State):
    _model_id: ClassVar[int] = 57
    _semantics: ClassVar = product_names(['Text'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Duration(State):
    _model_id: ClassVar[int] = 21
    _semantics: ClassVar = product_names(['Duration'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Angle(State):
    _model_id: ClassVar[int] = 4
    _semantics: ClassVar = product_names(['Angle'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Distance(State):
    _model_id: ClassVar[int] = 20
    _semantics: ClassVar = product_names(['Distance'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Speed(State):
    _model_id: ClassVar[int] = 53
    _semantics: ClassVar = product_names(['Speed'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Count(State):
    _model_id: ClassVar[int] = 16
    _semantics: ClassVar = product_names(['Count'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Ordinal(State):
    _model_id: ClassVar[int] = 40
    _semantics: ClassVar = product_names(['Ordinal'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Code(State):
    _model_id: ClassVar[int] = 10
    _semantics: ClassVar = product_names(['Code'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Scalar(State):
    _model_id: ClassVar[int] = 52
    _semantics: ClassVar = product_names(['Scalar'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Altitude(State):
    _model_id: ClassVar[int] = 3
    _semantics: ClassVar = product_names(['Altitude'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class GlobalPosition(SemanticModel):
    _model_id: ClassVar[int] = 26
    _semantics: ClassVar = product_names(['GlobalPosition', 'Position', 'Representation.Geodetic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('lat', 'lon', 'h')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic',)
    lat: float
    lon: float
    h: float

class LocalPosition(SemanticModel):
    _model_id: ClassVar[int] = 31
    _semantics: ClassVar = product_names(['LocalPosition', 'Position', 'Representation.LocalCartesian'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('x', 'y', 'z')
    _units: ClassVar[dict[str, str]] = {'x': 'm', 'y': 'm', 'z': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.LocalCartesian',)
    x: float
    y: float
    z: float

class LocalVelocity(SemanticModel):
    _model_id: ClassVar[int] = 32
    _semantics: ClassVar = product_names(['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('vx', 'vy', 'vz')
    _units: ClassVar[dict[str, str]] = {'vx': 'm/s', 'vy': 'm/s', 'vz': 'm/s'}
    _charts: ClassVar[tuple[str, ...]] = ('Velocity * Representation.LocalCartesian',)
    vx: float
    vy: float
    vz: float

class LocalAttitude(SemanticModel):
    _model_id: ClassVar[int] = 30
    _semantics: ClassVar = product_names(['LocalAttitude', 'Attitude', 'Representation.LocalEuler'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('roll', 'pitch', 'yaw')
    _units: ClassVar[dict[str, str]] = {'roll': 'rad', 'pitch': 'rad', 'yaw': 'rad'}
    _charts: ClassVar[tuple[str, ...]] = ('Attitude * Representation.LocalEuler',)
    roll: float
    pitch: float
    yaw: float

class QuaternionAttitude(SemanticModel):
    _model_id: ClassVar[int] = 47
    _semantics: ClassVar = product_names(['QuaternionAttitude', 'Attitude', 'Representation.Quaternion'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('qw', 'qx', 'qy', 'qz')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ('Attitude * Representation.Quaternion',)
    qw: float
    qx: float
    qy: float
    qz: float

class Mark(Data):
    _model_id: ClassVar[int] = 35
    _semantics: ClassVar = product_names(['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name', 'lat', 'lon', 'h')
    _units: ClassVar[dict[str, str]] = {'lat': 'deg', 'lon': 'deg', 'h': 'm'}
    _charts: ClassVar[tuple[str, ...]] = ('Position * Representation.Geodetic',)
    uid: UID
    name: str | None = None
    lat: float
    lon: float
    h: float

class Control(Root):
    _model_id: ClassVar[int] = 15
    _semantics: ClassVar = product_names(['Control'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Directive(Control):
    _model_id: ClassVar[int] = 19
    _semantics: ClassVar = product_names(['Directive'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Task(Directive):
    _model_id: ClassVar[int] = 55
    _semantics: ClassVar = product_names(['Task'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'instruction', 'intent', 'priority', 'status')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    instruction: str
    intent: TaskIntent
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW

class Mission(Directive):
    _model_id: ClassVar[int] = 36
    _semantics: ClassVar = product_names(['Mission'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Time(State):
    _model_id: ClassVar[int] = 58
    _semantics: ClassVar = product_names(['Time'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Range(Data):
    _model_id: ClassVar[int] = 48
    _semantics: ClassVar = product_names(['Range'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class NumericRange(Range):
    _model_id: ClassVar[int] = 37
    _semantics: ClassVar = product_names(['NumericRange'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('min_value', 'max_value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    min_value: float | None = None
    max_value: float | None = None

class Condition(Data):
    _model_id: ClassVar[int] = 12
    _semantics: ClassVar = product_names(['Condition'])
    _declared_fields: ClassVar[tuple[str, ...]] = ()
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()

class Predicate(Condition):
    _model_id: ClassVar[int] = 46
    _semantics: ClassVar = product_names(['Predicate'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('subject_uid', 'quantity', 'value')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    subject_uid: UID | None = None
    quantity: str | None = None
    value: float | None = None

class BooleanLogic(Condition):
    _model_id: ClassVar[int] = 8
    _semantics: ClassVar = product_names(['BooleanLogic'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('operator', 'terms')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    operator: BooleanOperator
    terms: list[Annotated[Condition, SemanticReference('Condition')]] = Field(default_factory=list)

class GeoPath(Data):
    _model_id: ClassVar[int] = 25
    _semantics: ClassVar = product_names(['GeoPath'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('points',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    points: list[Annotated[GlobalPosition, SemanticReference('GlobalPosition')]] = Field(default_factory=list)

class Role(Data):
    _model_id: ClassVar[int] = 50
    _semantics: ClassVar = product_names(['Role'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('name',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    name: str | None = None

class Resource(Object):
    _model_id: ClassVar[int] = 49
    _semantics: ClassVar = product_names(['Resource'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID | None = None
    name: str | None = None

class Constraint(Control):
    _model_id: ClassVar[int] = 14
    _semantics: ClassVar = product_names(['Constraint'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('condition',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    condition: Annotated[Condition, SemanticReference('Condition')] | None = None

class TaskTimeWindow(Constraint):
    _model_id: ClassVar[int] = 56
    _semantics: ClassVar = product_names(['TaskTimeWindow'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('earliest_start', 'latest_finish')
    _units: ClassVar[dict[str, str]] = {'earliest_start': 's', 'latest_finish': 's'}
    _charts: ClassVar[tuple[str, ...]] = ()
    earliest_start: float | None = None
    latest_finish: float | None = None

class WeatherLimits(Constraint):
    _model_id: ClassVar[int] = 62
    _semantics: ClassVar = product_names(['WeatherLimits'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('ifr', 'night', 'rain', 'snow', 'temp', 'wind', 'vis', 'icing')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    ifr: bool | None = None
    night: bool | None = None
    rain: Annotated[NumericRange, SemanticReference('NumericRange')] | None = None
    snow: Annotated[NumericRange, SemanticReference('NumericRange')] | None = None
    temp: Annotated[NumericRange, SemanticReference('NumericRange')] | None = None
    wind: Annotated[NumericRange, SemanticReference('NumericRange')] | None = None
    vis: Annotated[NumericRange, SemanticReference('NumericRange')] | None = None
    icing: bool | None = None

class Objective(Control):
    _model_id: ClassVar[int] = 39
    _semantics: ClassVar = product_names(['Objective'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name', 'condition', 'criteria', 'priority', 'status', 'start_time', 'deadline')
    _units: ClassVar[dict[str, str]] = {'start_time': 's', 'deadline': 's'}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    name: str
    condition: Annotated[Condition, SemanticReference('Condition')] | None = None
    criteria: list[Annotated[Condition, SemanticReference('Condition')]] = Field(default_factory=list)
    priority: TaskPriority = TaskPriority.ROUTINE
    status: TaskStatus = TaskStatus.NEW
    start_time: float | None = None
    deadline: float | None = None

class Command(Directive):
    _model_id: ClassVar[int] = 11
    _semantics: ClassVar = product_names(['Command'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'operation')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    operation: CommandOperation

class Authority(Control):
    _model_id: ClassVar[int] = 6
    _semantics: ClassVar = product_names(['Authority'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'role')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    role: Annotated[Role, SemanticReference('Role')] | None = None

class Lease(Authority):
    _model_id: ClassVar[int] = 29
    _semantics: ClassVar = product_names(['Lease'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('bound', 'control_level')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    bound: Annotated[Condition, SemanticReference('Condition')] | None = None
    control_level: ControlLevel | None = None

class Plan(Control):
    _model_id: ClassVar[int] = 43
    _semantics: ClassVar = product_names(['Plan'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('uid', 'name', 'approval_state')
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    uid: UID
    name: str | None = None
    approval_state: PlanApprovalState = PlanApprovalState.DRAFT

class PlanContingency(Data):
    _model_id: ClassVar[int] = 44
    _semantics: ClassVar = product_names(['PlanContingency'])
    _declared_fields: ClassVar[tuple[str, ...]] = ('condition',)
    _units: ClassVar[dict[str, str]] = {}
    _charts: ClassVar[tuple[str, ...]] = ()
    condition: Annotated[Condition, SemanticReference('Condition')]

Directed = RelationType('Directed', (Root, Root), operand_names=('source', 'target'))
AssignedWork = RelationType('AssignedWork', (Entity, Task), operand_names=('assignee', 'work'), specializes=Directed)
ConstrainedBy = RelationType('ConstrainedBy', (Control, Constraint), operand_names=('subject', 'constraint'), specializes=Directed)
OwnedBy = RelationType('OwnedBy', (Objective, Entity), operand_names=('objective', 'owner'), specializes=Directed)
Holds = RelationType('Holds', (Authority, Entity), operand_names=('authority', 'holder'), specializes=Directed)
GrantedBy = RelationType('GrantedBy', (Authority, Entity), operand_names=('authority', 'grantor'), specializes=Directed)
Controls = RelationType('Controls', (Lease, Object), operand_names=('lease', 'asset'), specializes=Directed)
Contains = RelationType('Contains', (Plan, Root), operand_names=('plan', 'item'), specializes=Directed)

REGISTRY_SPEC = {'axes': {'Substrate': {'cardinality': 'one', 'values': ['BIOLOGICAL', 'MECHANICAL', 'CYBER']}, 'PhysicalDomain': {'description': 'A bounded thing operates in exactly one domain.', 'cardinality': 'one', 'values': ['LAND', 'AIR', 'SEA', 'UNDERSEA', 'SPACE']}, 'Controller': {'cardinality': 'one', 'applies': {'all': ['Machine']}, 'values': ['MANNED', 'UNMANNED']}, 'Locomotion': {'cardinality': 'one', 'values': ['SELF_PROPELLED', 'EXTERNAL', 'STATIC']}, 'Airframe': {'description': 'Airframe construction, independent of takeoff capability.', 'cardinality': 'one', 'applies': {'all': ['Machine', 'PhysicalDomain.AIR']}, 'values': ['MULTIROTOR', 'FIXED_WING']}, 'Representation': {'description': 'The coordinate scheme through which a structured quantity becomes data variables.', 'cardinality': 'many', 'values': ['Geodetic', 'LocalCartesian', 'LocalEuler', 'Quaternion']}, 'BloodGroup': {'cardinality': 'one', 'applies': {'all': ['Substrate.BIOLOGICAL']}, 'requires': ['Biological'], 'values': ['A_POS', 'A_NEG', 'B_POS', 'B_NEG', 'AB_POS', 'AB_NEG', 'O_POS', 'O_NEG']}, 'Realm': {'cardinality': 'one', 'values': ['WORLD', 'INFORMATION']}, 'TemporalMode': {'cardinality': 'one', 'values': ['ACHIEVE', 'MAINTAIN']}, 'TruthTarget': {'cardinality': 'one', 'applies': {'any': ['Existence', 'Connectivity', 'Engagement', 'Activity', 'Paused', 'Hold']}, 'values': ['TRUE', 'FALSE']}}, 'enums': {'TaskPriority': {'ROUTINE': 0, 'HIGH': 1, 'IMMEDIATE': 2}, 'TaskStatus': {'NEW': 0, 'ACTIVE': 1, 'COMPLETE': 2, 'FAILED': 3, 'CANCELLED': 4, 'ACCEPTED': 5}, 'ControlLevel': {'NONE': 0, 'MONITOR': 1, 'GUIDE': 2, 'FULL': 3}, 'PlanApprovalState': {'DRAFT': 0, 'PROPOSED': 1, 'APPROVED': 2, 'REJECTED': 3, 'SUPERSEDED': 4}, 'BooleanOperator': {'NONE': 0, 'NOT': 1, 'AND': 2, 'OR': 3, 'XOR': 4, 'NAND': 5, 'NOR': 6, 'XNOR': 7}, 'TaskIntent': {'MOVE': 0, 'HOLD': 1, 'LOCATE': 2, 'TRACK': 3, 'CREATE': 4, 'REMOVE': 5, 'MODIFY': 6, 'PROTECT': 7, 'IDENTIFY': 8, 'CLASSIFY': 9, 'FOLLOW': 10, 'MEASURE': 11, 'RESTORE': 12, 'DENY': 13, 'TRANSPORT': 14}, 'CommandOperation': {'ENGAGE': 0, 'DISENGAGE': 1, 'PAUSE': 2, 'RESUME': 3, 'SET': 4, 'MOVE': 5, 'ALLOCATE': 6, 'TRANSFER': 7, 'LOAD_CONFIGURATION': 8, 'RESET': 9}}, 'models': {'Root': {'model_id': 51, 'parent': None, 'semantics': ['Root'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Object': {'model_id': 38, 'parent': 'Root', 'semantics': ['Object'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Locality': {'model_id': 33, 'parent': 'Object', 'semantics': ['Locality'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Entity': {'model_id': 23, 'parent': 'Object', 'semantics': ['Entity'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Biological': {'model_id': 7, 'parent': 'Entity', 'semantics': ['Biological', 'Substrate.BIOLOGICAL'], 'fields': [], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Person': {'model_id': 42, 'parent': 'Biological', 'semantics': ['Substrate.BIOLOGICAL', 'Person'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Actor': {'model_id': 2, 'parent': 'Person', 'semantics': ['Substrate.BIOLOGICAL', 'Actor'], 'fields': [{'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}]}, 'Machine': {'model_id': 34, 'parent': 'Entity', 'semantics': ['Machine', 'Substrate.MECHANICAL'], 'fields': [{'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Vehicle': {'model_id': 60, 'parent': 'Machine', 'semantics': ['Substrate.MECHANICAL', 'Vehicle', 'Locomotion.SELF_PROPELLED'], 'fields': [{'name': 'model', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'model', 'type': 'optional string', 'default': None, 'unit': None}]}, 'CrewedVehicle': {'model_id': 17, 'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'CrewedVehicle', 'Controller.MANNED'], 'fields': [], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'model', 'type': 'optional string', 'default': None, 'unit': None}]}, 'UnmannedVehicle': {'model_id': 59, 'parent': 'Vehicle', 'semantics': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED'], 'fields': [], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'serial_number', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'model', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Data': {'model_id': 18, 'parent': 'Root', 'semantics': ['Data'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'State': {'model_id': 54, 'parent': 'Data', 'semantics': ['State'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Position': {'model_id': 45, 'parent': 'State', 'semantics': ['Position'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Velocity': {'model_id': 61, 'parent': 'State', 'semantics': ['Velocity'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Attitude': {'model_id': 5, 'parent': 'State', 'semantics': ['Attitude'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Identity': {'model_id': 28, 'parent': 'State', 'semantics': ['Identity'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Classification': {'model_id': 9, 'parent': 'State', 'semantics': ['Classification'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Existence': {'model_id': 24, 'parent': 'State', 'semantics': ['Existence'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Connectivity': {'model_id': 13, 'parent': 'State', 'semantics': ['Connectivity'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Engagement': {'model_id': 22, 'parent': 'State', 'semantics': ['Engagement'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Activity': {'model_id': 1, 'parent': 'State', 'semantics': ['Activity'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Paused': {'model_id': 41, 'parent': 'State', 'semantics': ['Paused'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Hold': {'model_id': 27, 'parent': 'State', 'semantics': ['Hold'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Text': {'model_id': 57, 'parent': 'State', 'semantics': ['Text'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Duration': {'model_id': 21, 'parent': 'State', 'semantics': ['Duration'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Angle': {'model_id': 4, 'parent': 'State', 'semantics': ['Angle'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Distance': {'model_id': 20, 'parent': 'State', 'semantics': ['Distance'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Speed': {'model_id': 53, 'parent': 'State', 'semantics': ['Speed'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Count': {'model_id': 16, 'parent': 'State', 'semantics': ['Count'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Ordinal': {'model_id': 40, 'parent': 'State', 'semantics': ['Ordinal'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Code': {'model_id': 10, 'parent': 'State', 'semantics': ['Code'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Scalar': {'model_id': 52, 'parent': 'State', 'semantics': ['Scalar'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Altitude': {'model_id': 3, 'parent': 'State', 'semantics': ['Altitude'], 'fields': [], 'chart_fields': [], 'applies': ['PhysicalDomain.AIR'], 'effective_fields': []}, 'GlobalPosition': {'model_id': 26, 'parent': None, 'semantics': ['GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}], 'effective_fields': [{'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}]}, 'LocalPosition': {'model_id': 31, 'parent': None, 'semantics': ['LocalPosition', 'Position', 'Representation.LocalCartesian'], 'fields': [{'name': 'x', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'y', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'z', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Position * Representation.LocalCartesian', 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}], 'effective_fields': [{'name': 'x', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'y', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}, {'name': 'z', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.LocalCartesian'}]}, 'LocalVelocity': {'model_id': 32, 'parent': None, 'semantics': ['LocalVelocity', 'Velocity', 'Representation.LocalCartesian'], 'fields': [{'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}], 'chart_fields': [{'chart': 'Velocity * Representation.LocalCartesian', 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}], 'effective_fields': [{'name': 'vx', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vy', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}, {'name': 'vz', 'type': 'float', 'default': None, 'unit': 'm/s', 'chart': 'Velocity * Representation.LocalCartesian'}]}, 'LocalAttitude': {'model_id': 30, 'parent': None, 'semantics': ['LocalAttitude', 'Attitude', 'Representation.LocalEuler'], 'fields': [{'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}], 'chart_fields': [{'chart': 'Attitude * Representation.LocalEuler', 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}], 'effective_fields': [{'name': 'roll', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'pitch', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}, {'name': 'yaw', 'type': 'float', 'default': None, 'unit': 'rad', 'chart': 'Attitude * Representation.LocalEuler'}]}, 'QuaternionAttitude': {'model_id': 47, 'parent': None, 'semantics': ['QuaternionAttitude', 'Attitude', 'Representation.Quaternion'], 'fields': [{'name': 'qw', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qx', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qy', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qz', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}], 'chart_fields': [{'chart': 'Attitude * Representation.Quaternion', 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}], 'effective_fields': [{'name': 'qw', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qx', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qy', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}, {'name': 'qz', 'type': 'float', 'default': None, 'unit': None, 'chart': 'Attitude * Representation.Quaternion'}]}, 'Mark': {'model_id': 35, 'parent': 'Data', 'semantics': ['Mark', 'GlobalPosition', 'Position', 'Representation.Geodetic'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}], 'chart_fields': [{'chart': 'Position * Representation.Geodetic', 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'lat', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'lon', 'type': 'float', 'default': None, 'unit': 'deg', 'chart': 'Position * Representation.Geodetic'}, {'name': 'h', 'type': 'float', 'default': None, 'unit': 'm', 'chart': 'Position * Representation.Geodetic'}]}, 'Control': {'model_id': 15, 'parent': 'Root', 'semantics': ['Control'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Directive': {'model_id': 19, 'parent': 'Control', 'semantics': ['Directive'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Task': {'model_id': 55, 'parent': 'Directive', 'semantics': ['Task'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'instruction', 'type': 'string', 'default': None, 'unit': None}, {'name': 'intent', 'type': 'TaskIntent', 'default': None, 'unit': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'instruction', 'type': 'string', 'default': None, 'unit': None}, {'name': 'intent', 'type': 'TaskIntent', 'default': None, 'unit': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}]}, 'Mission': {'model_id': 36, 'parent': 'Directive', 'semantics': ['Mission'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Time': {'model_id': 58, 'parent': 'State', 'semantics': ['Time'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Range': {'model_id': 48, 'parent': 'Data', 'semantics': ['Range'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'NumericRange': {'model_id': 37, 'parent': 'Range', 'semantics': ['NumericRange'], 'fields': [{'name': 'min_value', 'type': 'optional float', 'default': None, 'unit': None}, {'name': 'max_value', 'type': 'optional float', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'min_value', 'type': 'optional float', 'default': None, 'unit': None}, {'name': 'max_value', 'type': 'optional float', 'default': None, 'unit': None}]}, 'Condition': {'model_id': 12, 'parent': 'Data', 'semantics': ['Condition'], 'fields': [], 'chart_fields': [], 'effective_fields': []}, 'Predicate': {'model_id': 46, 'parent': 'Condition', 'semantics': ['Predicate'], 'fields': [{'name': 'subject_uid', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'quantity', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'value', 'type': 'optional float', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'subject_uid', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'quantity', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'value', 'type': 'optional float', 'default': None, 'unit': None}]}, 'BooleanLogic': {'model_id': 8, 'parent': 'Condition', 'semantics': ['BooleanLogic'], 'fields': [{'name': 'operator', 'type': 'BooleanOperator', 'default': None, 'unit': None}, {'name': 'terms', 'type': 'list[Condition]', 'default': None}], 'chart_fields': [], 'effective_fields': [{'name': 'operator', 'type': 'BooleanOperator', 'default': None, 'unit': None}, {'name': 'terms', 'type': 'list[Condition]', 'default': None}]}, 'GeoPath': {'model_id': 25, 'parent': 'Data', 'semantics': ['GeoPath'], 'fields': [{'name': 'points', 'type': 'list[GlobalPosition]', 'default': None}], 'chart_fields': [], 'effective_fields': [{'name': 'points', 'type': 'list[GlobalPosition]', 'default': None}]}, 'Role': {'model_id': 50, 'parent': 'Data', 'semantics': ['Role'], 'fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Resource': {'model_id': 49, 'parent': 'Object', 'semantics': ['Resource'], 'fields': [{'name': 'uid', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'optional UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}]}, 'Constraint': {'model_id': 14, 'parent': 'Control', 'semantics': ['Constraint'], 'fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}]}, 'TaskTimeWindow': {'model_id': 56, 'parent': 'Constraint', 'semantics': ['TaskTimeWindow'], 'fields': [{'name': 'earliest_start', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'latest_finish', 'type': 'optional float', 'default': None, 'unit': 's'}], 'chart_fields': [], 'effective_fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'earliest_start', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'latest_finish', 'type': 'optional float', 'default': None, 'unit': 's'}]}, 'WeatherLimits': {'model_id': 62, 'parent': 'Constraint', 'semantics': ['WeatherLimits'], 'fields': [{'name': 'ifr', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'night', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'rain', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'snow', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'temp', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'wind', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'vis', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'icing', 'type': 'optional bool', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'ifr', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'night', 'type': 'optional bool', 'default': None, 'unit': None}, {'name': 'rain', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'snow', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'temp', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'wind', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'vis', 'type': 'optional NumericRange', 'default': None, 'unit': None}, {'name': 'icing', 'type': 'optional bool', 'default': None, 'unit': None}]}, 'Objective': {'model_id': 39, 'parent': 'Control', 'semantics': ['Objective'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'string', 'default': None, 'unit': None}, {'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'criteria', 'type': 'list[Condition]', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}, {'name': 'start_time', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'deadline', 'type': 'optional float', 'default': None, 'unit': 's'}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'string', 'default': None, 'unit': None}, {'name': 'condition', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'criteria', 'type': 'list[Condition]', 'default': None}, {'name': 'priority', 'type': 'TaskPriority', 'default': 'ROUTINE', 'unit': None}, {'name': 'status', 'type': 'TaskStatus', 'default': 'NEW', 'unit': None}, {'name': 'start_time', 'type': 'optional float', 'default': None, 'unit': 's'}, {'name': 'deadline', 'type': 'optional float', 'default': None, 'unit': 's'}]}, 'Command': {'model_id': 11, 'parent': 'Directive', 'semantics': ['Command'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'operation', 'type': 'CommandOperation', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'operation', 'type': 'CommandOperation', 'default': None, 'unit': None}]}, 'Authority': {'model_id': 6, 'parent': 'Control', 'semantics': ['Authority'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}]}, 'Lease': {'model_id': 29, 'parent': 'Authority', 'semantics': ['Lease'], 'fields': [{'name': 'bound', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'control_level', 'type': 'optional ControlLevel', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'role', 'type': 'optional Role', 'default': None, 'unit': None}, {'name': 'bound', 'type': 'optional Condition', 'default': None, 'unit': None}, {'name': 'control_level', 'type': 'optional ControlLevel', 'default': None, 'unit': None}]}, 'Plan': {'model_id': 43, 'parent': 'Control', 'semantics': ['Plan'], 'fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'approval_state', 'type': 'PlanApprovalState', 'default': 'DRAFT', 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'uid', 'type': 'UID', 'default': None, 'unit': None}, {'name': 'name', 'type': 'optional string', 'default': None, 'unit': None}, {'name': 'approval_state', 'type': 'PlanApprovalState', 'default': 'DRAFT', 'unit': None}]}, 'PlanContingency': {'model_id': 44, 'parent': 'Data', 'semantics': ['PlanContingency'], 'fields': [{'name': 'condition', 'type': 'Condition', 'default': None, 'unit': None}], 'chart_fields': [], 'effective_fields': [{'name': 'condition', 'type': 'Condition', 'default': None, 'unit': None}]}}, 'charts': [{'display': 'Position * Representation.Geodetic', 'factors': ['Position', 'Representation.Geodetic'], 'coords': [{'name': 'lat', 'type': 'float', 'unit': 'deg'}, {'name': 'lon', 'type': 'float', 'unit': 'deg'}, {'name': 'h', 'type': 'float', 'unit': 'm'}]}, {'display': 'Position * Representation.LocalCartesian', 'factors': ['Position', 'Representation.LocalCartesian'], 'coords': [{'name': 'x', 'type': 'float', 'unit': 'm'}, {'name': 'y', 'type': 'float', 'unit': 'm'}, {'name': 'z', 'type': 'float', 'unit': 'm'}]}, {'display': 'Velocity * Representation.LocalCartesian', 'factors': ['Velocity', 'Representation.LocalCartesian'], 'coords': [{'name': 'vx', 'type': 'float', 'unit': 'm/s'}, {'name': 'vy', 'type': 'float', 'unit': 'm/s'}, {'name': 'vz', 'type': 'float', 'unit': 'm/s'}]}, {'display': 'Attitude * Representation.LocalEuler', 'factors': ['Attitude', 'Representation.LocalEuler'], 'coords': [{'name': 'roll', 'type': 'float', 'unit': 'rad'}, {'name': 'pitch', 'type': 'float', 'unit': 'rad'}, {'name': 'yaw', 'type': 'float', 'unit': 'rad'}]}, {'display': 'Attitude * Representation.Quaternion', 'factors': ['Attitude', 'Representation.Quaternion'], 'coords': [{'name': 'qw', 'type': 'float', 'unit': None}, {'name': 'qx', 'type': 'float', 'unit': None}, {'name': 'qy', 'type': 'float', 'unit': None}, {'name': 'qz', 'type': 'float', 'unit': None}]}], 'expressions': {'POSITION_GOAL': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': []}, 'POSITION_QUERY': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': []}, 'EXISTENCE_GOAL': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'OBJECT_STATE_GOAL': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'ENGAGEMENT_COMMAND': {'description': "The target's engagement state is asserted.", 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': []}, 'PROCESS_COMMAND': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': []}, 'MOVE': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.MOVE']}, 'HOLD': {'description': "An actor's position is the destination.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'destination': ['Position']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'actor', 'equals': 'destination'}], 'words': ['TaskIntent.HOLD']}, 'LOCATE': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.LOCATE']}, 'TRACK': {'description': "An entity's position is the answer.", 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.MAINTAIN'], 'given': {'target': ['Entity']}, 'sought': {'position': ['Position']}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'position'}], 'words': ['TaskIntent.TRACK']}, 'CREATE': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.TRUE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.CREATE']}, 'REMOVE': {'description': "An object's existence is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE', 'Existence', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.REMOVE']}, 'MODIFY': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.MODIFY']}, 'PROTECT': {'description': "An object's state is asserted.", 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.PROTECT']}, 'ENGAGE': {'description': "The target's engagement state is asserted.", 'factors': ['Command', 'TruthTarget.TRUE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ENGAGE']}, 'DISENGAGE': {'description': "The target's engagement state is asserted.", 'factors': ['Command', 'TruthTarget.FALSE'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.DISENGAGE']}, 'PAUSE': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused', 'TruthTarget.TRUE'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.PAUSE']}, 'RESUME': {'description': 'A running process is asserted paused or released.', 'factors': ['Command', 'Paused', 'TruthTarget.FALSE'], 'given': {'target': ['Object'], 'process': ['Text']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESUME']}, 'IDENTIFY': {'description': 'Solve for the identity of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'identity': ['Identity']}, 'equations': [{'quantity': 'Identity', 'of': 'target', 'equals': 'identity'}], 'words': ['TaskIntent.IDENTIFY']}, 'CLASSIFY': {'description': 'Solve for the classification of an entity.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'classification': ['Classification']}, 'equations': [{'quantity': 'Classification', 'of': 'target', 'equals': 'classification'}], 'words': ['TaskIntent.CLASSIFY']}, 'FOLLOW': {'description': 'Follow a path.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN'], 'given': {'actor': ['Entity'], 'path': ['GeoPath']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.FOLLOW']}, 'MEASURE': {'description': 'Measure a state of a target.', 'factors': ['Task', 'Realm.INFORMATION', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Entity']}, 'sought': {'measurement': ['State']}, 'equations': [], 'words': ['TaskIntent.MEASURE']}, 'RESTORE': {'description': 'Return an object to a prior state.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.RESTORE']}, 'DENY': {'description': 'Prevent connectivity to an object.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.MAINTAIN', 'Connectivity', 'TruthTarget.FALSE'], 'given': {'object': ['Object']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.DENY']}, 'TRANSPORT': {'description': 'Move a thing between places; which end and what moves are bindings.', 'factors': ['Task', 'Realm.WORLD', 'TemporalMode.ACHIEVE'], 'given': {'cargo': ['Object'], 'origin': ['Position'], 'destination': ['Position']}, 'sought': {}, 'equations': [], 'words': ['TaskIntent.TRANSPORT']}, 'SET': {'description': 'Set a declared state property on the target.', 'factors': ['Command'], 'given': {'target': ['Object'], 'property': ['Text'], 'value': ['Scalar']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.SET']}, 'DIRECT': {'description': 'Direct the target to a destination or along a path.', 'factors': ['Command', 'TemporalMode.ACHIEVE'], 'given': {'target': ['Object'], 'destination': ['Position'], 'path': ['GeoPath'], 'radius': ['Distance'], 'speed': ['Speed'], 'yaw': ['Angle']}, 'sought': {}, 'equations': [{'quantity': 'Position', 'of': 'target', 'equals': 'destination'}], 'words': ['CommandOperation.MOVE']}, 'ALLOCATE': {'description': 'Allocate a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource'], 'quantity': ['Count']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.ALLOCATE']}, 'TRANSFER': {'description': 'Transfer a referenced resource.', 'factors': ['Command'], 'given': {'target': ['Object'], 'resource': ['Resource'], 'quantity': ['Count']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.TRANSFER']}, 'LOAD_CONFIGURATION': {'description': 'Load a referenced configuration on the target.', 'factors': ['Command'], 'given': {'target': ['Object'], 'parameter': ['Text'], 'value': ['Scalar']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.LOAD_CONFIGURATION']}, 'RESET': {'description': 'Reset the target to its initial state.', 'factors': ['Command'], 'given': {'target': ['Object']}, 'sought': {}, 'equations': [], 'words': ['CommandOperation.RESET']}}, 'word_expressions': {'TaskIntent.MOVE': 'MOVE', 'TaskIntent.HOLD': 'HOLD', 'TaskIntent.LOCATE': 'LOCATE', 'TaskIntent.TRACK': 'TRACK', 'TaskIntent.CREATE': 'CREATE', 'TaskIntent.REMOVE': 'REMOVE', 'TaskIntent.MODIFY': 'MODIFY', 'TaskIntent.PROTECT': 'PROTECT', 'CommandOperation.ENGAGE': 'ENGAGE', 'CommandOperation.DISENGAGE': 'DISENGAGE', 'CommandOperation.PAUSE': 'PAUSE', 'CommandOperation.RESUME': 'RESUME', 'TaskIntent.IDENTIFY': 'IDENTIFY', 'TaskIntent.CLASSIFY': 'CLASSIFY', 'TaskIntent.FOLLOW': 'FOLLOW', 'TaskIntent.MEASURE': 'MEASURE', 'TaskIntent.RESTORE': 'RESTORE', 'TaskIntent.DENY': 'DENY', 'TaskIntent.TRANSPORT': 'TRANSPORT', 'CommandOperation.SET': 'SET', 'CommandOperation.MOVE': 'DIRECT', 'CommandOperation.ALLOCATE': 'ALLOCATE', 'CommandOperation.TRANSFER': 'TRANSFER', 'CommandOperation.LOAD_CONFIGURATION': 'LOAD_CONFIGURATION', 'CommandOperation.RESET': 'RESET'}, 'aliases': {'AirMission': ['Mission', 'PhysicalDomain.AIR'], 'AirTask': ['Task', 'PhysicalDomain.AIR'], 'UGV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.LAND'], 'UAV': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR'], 'Drone': ['Substrate.MECHANICAL', 'Locomotion.SELF_PROPELLED', 'UnmannedVehicle', 'Controller.UNMANNED', 'PhysicalDomain.AIR', 'Airframe.MULTIROTOR'], 'Geodetic': ['Representation.Geodetic'], 'LocalCartesian': ['Representation.LocalCartesian'], 'LocalEuler': ['Representation.LocalEuler'], 'Quaternion': ['Representation.Quaternion']}, 'relations': {'Directed': {'signature': ['Root', 'Root'], 'operand_names': ['source', 'target'], 'specializes': None}, 'AssignedWork': {'signature': ['Entity', 'Task'], 'operand_names': ['assignee', 'work'], 'specializes': 'Directed'}, 'ConstrainedBy': {'signature': ['Control', 'Constraint'], 'operand_names': ['subject', 'constraint'], 'specializes': 'Directed'}, 'OwnedBy': {'signature': ['Objective', 'Entity'], 'operand_names': ['objective', 'owner'], 'specializes': 'Directed'}, 'Holds': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'holder'], 'specializes': 'Directed'}, 'GrantedBy': {'signature': ['Authority', 'Entity'], 'operand_names': ['authority', 'grantor'], 'specializes': 'Directed'}, 'Controls': {'signature': ['Lease', 'Object'], 'operand_names': ['lease', 'asset'], 'specializes': 'Directed'}, 'Contains': {'signature': ['Plan', 'Root'], 'operand_names': ['plan', 'item'], 'specializes': 'Directed'}}}
REGISTRY = SemanticRegistry(REGISTRY_SPEC)
MODEL_BY_ID = {1: Activity, 2: Actor, 3: Altitude, 4: Angle, 5: Attitude, 6: Authority, 7: Biological, 8: BooleanLogic, 9: Classification, 10: Code, 11: Command, 12: Condition, 13: Connectivity, 14: Constraint, 15: Control, 16: Count, 17: CrewedVehicle, 18: Data, 19: Directive, 20: Distance, 21: Duration, 22: Engagement, 23: Entity, 24: Existence, 25: GeoPath, 26: GlobalPosition, 27: Hold, 28: Identity, 29: Lease, 30: LocalAttitude, 31: LocalPosition, 32: LocalVelocity, 33: Locality, 34: Machine, 35: Mark, 36: Mission, 37: NumericRange, 38: Object, 39: Objective, 40: Ordinal, 41: Paused, 42: Person, 43: Plan, 44: PlanContingency, 45: Position, 46: Predicate, 47: QuaternionAttitude, 48: Range, 49: Resource, 50: Role, 51: Root, 52: Scalar, 53: Speed, 54: State, 55: Task, 56: TaskTimeWindow, 57: Text, 58: Time, 59: UnmannedVehicle, 60: Vehicle, 61: Velocity, 62: WeatherLimits}
REGISTRY.model_types = MODEL_BY_ID
for model in MODEL_BY_ID.values():
    model._registry = REGISTRY
    model.model_rebuild()

def new_store() -> Store:
    return Store(REGISTRY)

def decode(payload: bytes) -> SemanticModel:
    from ..wire import decode as decode_wire
    return decode_wire(payload, REGISTRY)

__all__ = ['ALLOCATE', 'Activity', 'Actor', 'AirMission', 'AirTask', 'Airframe', 'Altitude', 'Angle', 'AssignedWork', 'Attitude', 'Authority', 'Biological', 'BloodGroup', 'BooleanLogic', 'BooleanOperator', 'CLASSIFY', 'CREATE', 'Classification', 'Code', 'Command', 'CommandOperation', 'Condition', 'Connectivity', 'ConstrainedBy', 'Constraint', 'Contains', 'Control', 'ControlLevel', 'Controller', 'Controls', 'Count', 'CrewedVehicle', 'DENY', 'DIRECT', 'DISENGAGE', 'Data', 'Directed', 'Directive', 'Distance', 'Drone', 'Duration', 'ENGAGE', 'ENGAGEMENT_COMMAND', 'EXISTENCE_GOAL', 'Engagement', 'Entity', 'Existence', 'FOLLOW', 'GeoPath', 'Geodetic', 'GlobalPosition', 'GrantedBy', 'HOLD', 'Hold', 'Holds', 'IDENTIFY', 'Identity', 'LOAD_CONFIGURATION', 'LOCATE', 'Lease', 'LocalAttitude', 'LocalCartesian', 'LocalEuler', 'LocalPosition', 'LocalVelocity', 'Locality', 'Locomotion', 'MEASURE', 'MODEL_BY_ID', 'MODIFY', 'MOVE', 'Machine', 'Mark', 'Mission', 'NumericRange', 'OBJECT_STATE_GOAL', 'Object', 'Objective', 'Ordinal', 'OwnedBy', 'PAUSE', 'POSITION_GOAL', 'POSITION_QUERY', 'PROCESS_COMMAND', 'PROTECT', 'Paused', 'Person', 'PhysicalDomain', 'Plan', 'PlanApprovalState', 'PlanContingency', 'Position', 'Predicate', 'Quaternion', 'QuaternionAttitude', 'REGISTRY', 'REGISTRY_SPEC', 'REMOVE', 'RESET', 'RESTORE', 'RESUME', 'Range', 'Realm', 'Representation', 'Resource', 'Role', 'Root', 'SET', 'Scalar', 'Speed', 'State', 'Substrate', 'TRACK', 'TRANSFER', 'TRANSPORT', 'Task', 'TaskIntent', 'TaskPriority', 'TaskStatus', 'TaskTimeWindow', 'TemporalMode', 'Text', 'Time', 'TruthTarget', 'UAV', 'UGV', 'UID', 'UnmannedVehicle', 'Vehicle', 'Velocity', 'WeatherLimits', 'decode', 'new_store']