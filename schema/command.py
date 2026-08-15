"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .directive import Directive

### Enums

class CommandResult(IntEnum):
    ACCEPTED = 0
    TEMPORARILY_REJECTED = auto()
    DENIED = auto()
    UNSUPPORTED = auto()
    FAILED = auto()
    IN_PROGRESS = auto()
    CANCELLED = auto()

class StateChangeOperation(IntEnum):
    SET = 0
    ENABLE = auto()
    DISABLE = auto()

class ProcessControlOperation(IntEnum):
    START = 0
    STOP = auto()
    PAUSE = auto()
    RESUME = auto()
    CANCEL = auto()

class ConfigurationOperation(IntEnum):
    SET_PARAMETER = 0
    LOAD_CONFIGURATION = auto()

class MotionOperation(IntEnum):
    MOVE_TO = 0
    FOLLOW_PATH = auto()
    MAINTAIN = auto()
    STOP = auto()

class ResourceOperation(IntEnum):
    ACQUIRE = 0
    RELEASE = auto()
    ALLOCATE = auto()
    TRANSFER = auto()

class ExecutionOperation(IntEnum):
    EXECUTE = 0
    ABORT = auto()
    RESET = auto()

### Models

class Command(Directive):
    'Immediate bounded imperative applied to a concrete target without redefining task lifecycle semantics'
    __occid_model_id__: ClassVar[int] = 45
    target_ref: StringID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]

class StateChangeCommand(Command):
    'Change, enable, or disable one declared state property on the target'
    __occid_model_id__: ClassVar[int] = 303
    operation: StateChangeOperation
    property_name: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None

class ProcessControlCommand(Command):
    'Start, stop, pause, resume, or cancel a named process on the target'
    __occid_model_id__: ClassVar[int] = 304
    operation: ProcessControlOperation
    process_name: builtins.str | None = None

class ConfigurationCommand(Command):
    'Set a configuration parameter or load a referenced configuration on the target'
    __occid_model_id__: ClassVar[int] = 305
    operation: ConfigurationOperation
    parameter_name: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    configuration_ref: StringID | None = None

class MotionCommand(Command):
    'Direct immediate target motion using a destination, path, or maintained spatial condition'
    __occid_model_id__: ClassVar[int] = 306
    operation: MotionOperation
    destination: GlobalPosition | None = None
    path: GeoPath | None = None
    radius_m: builtins.float | None = None
    speed_ms: builtins.float | None = None
    yaw_rad: builtins.float | None = None

class ResourceCommand(Command):
    'Acquire, release, allocate, or transfer a referenced resource'
    __occid_model_id__: ClassVar[int] = 307
    operation: ResourceOperation
    resource_ref: StringID | None = None
    quantity: builtins.float | None = None
    destination_ref: StringID | None = None

class ExecutionCommand(Command):
    'Execute, abort, or reset a referenced plan, execution, or executable object'
    __occid_model_id__: ClassVar[int] = 308
    operation: ExecutionOperation
    dispatch_id: StringID | None = None
