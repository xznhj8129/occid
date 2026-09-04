"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

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

class StateChangeCommand(OCCIDModel):
    'Change, enable, or disable one declared state property on the target'
    __occid_model_id__: ClassVar[int] = 230
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: StateChangeOperation
    property_name: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None

class ProcessControlCommand(OCCIDModel):
    'Start, stop, pause, resume, or cancel a named process on the target'
    __occid_model_id__: ClassVar[int] = 194
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: ProcessControlOperation
    process_name: builtins.str | None = None

class ConfigurationCommand(OCCIDModel):
    'Set a configuration parameter or load a referenced configuration on the target'
    __occid_model_id__: ClassVar[int] = 37
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: ConfigurationOperation
    parameter_name: builtins.str | None = None
    value: SerializeAsAny[MetadataValue | MeasurementQuality] | None = None
    configuration_uid: UID | None = None

class MotionCommand(OCCIDModel):
    'Direct immediate target motion using a destination, path, or maintained spatial condition'
    __occid_model_id__: ClassVar[int] = 159
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: MotionOperation
    destination: GlobalPosition | None = None
    path: GeoPath | None = None
    radius_m: builtins.float | None = None
    speed_ms: builtins.float | None = None
    yaw_rad: builtins.float | None = None

class ResourceCommand(OCCIDModel):
    'Acquire, release, allocate, or transfer a referenced resource'
    __occid_model_id__: ClassVar[int] = 208
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: ResourceOperation
    resource_uid: UID | None = None
    quantity: builtins.float | None = None

class ExecutionCommand(OCCIDModel):
    'Execute, abort, or reset a referenced plan, execution, or executable object'
    __occid_model_id__: ClassVar[int] = 71
    __occid_semantic_role__: ClassVar[str] = 'type'
    target_uid: UID
    constraints: list[SerializeAsAny[Constraint | Restriction | Limitation | TaskTimeWindow | WeatherLimits]]
    operation: ExecutionOperation
