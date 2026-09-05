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

class Command(OCCIDModel):
    'Immediate bounded imperative applied to a concrete target without redefining task lifecycle semantics'
    __occid_model_id__: ClassVar[int] = 35
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Directive'
    __occid_children__: ClassVar[tuple[str, ...]] = ('StateChangeCommand', 'ProcessControlCommand', 'ConfigurationCommand', 'MotionCommand', 'ResourceCommand', 'ExecutionCommand')
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]

class StateChangeCommand(OCCIDModel):
    'Change, enable, or disable one declared state property on the target'
    __occid_model_id__: ClassVar[int] = 247
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: StateChangeOperation
    property_name: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None

class ProcessControlCommand(OCCIDModel):
    'Start, stop, pause, resume, or cancel a named process on the target'
    __occid_model_id__: ClassVar[int] = 208
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: ProcessControlOperation
    process_name: builtins.str | None = None

class ConfigurationCommand(OCCIDModel):
    'Set a configuration parameter or load a referenced configuration on the target'
    __occid_model_id__: ClassVar[int] = 41
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: ConfigurationOperation
    parameter_name: builtins.str | None = None
    value: Semantic[MetadataValue] | None = None
    configuration_uid: Semantic[UID] | None = None

class MotionCommand(OCCIDModel):
    'Direct immediate target motion using a destination, path, or maintained spatial condition'
    __occid_model_id__: ClassVar[int] = 171
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: MotionOperation
    destination: Semantic[GlobalPosition] | None = None
    path: Semantic[GeoPath] | None = None
    radius_m: builtins.float | None = None
    speed_ms: builtins.float | None = None
    yaw_rad: builtins.float | None = None

class ResourceCommand(OCCIDModel):
    'Acquire, release, allocate, or transfer a referenced resource'
    __occid_model_id__: ClassVar[int] = 223
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: ResourceOperation
    resource_uid: Semantic[UID] | None = None
    quantity: builtins.float | None = None

class ExecutionCommand(OCCIDModel):
    'Execute, abort, or reset a referenced plan, execution, or executable object'
    __occid_model_id__: ClassVar[int] = 80
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Command'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    target_uid: Semantic[UID]
    constraints: list[Semantic[Constraint]]
    operation: ExecutionOperation
