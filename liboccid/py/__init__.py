from .common import *
from .common import _validate_semantic_registry
from .activation import *
from .assignment import *
from .attribute import *
from .authority import *
from .c3 import *
from .capability import *
from .command import *
from .communication import *
from .condition import *
from .constraint import *
from .context import *
from .control import *
from .cue import *
from .data import *
from .definition import *
from .directive import *
from .event import *
from .execution import *
from .gnc import *
from .health import *
from .identity import *
from .input import *
from .internal import *
from .isr import *
from .kinematic import *
from .lifecycle import *
from .link import *
from .measurement import *
from .media import *
from .mesh import *
from .message import *
from .military_effects import *
from .military_tasks import *
from .network import *
from .node import *
from .object import *
from .observation import *
from .parameter import *
from .payload import *
from .plan import *
from .property import *
from .protocol import *
from .radio import *
from .record import *
from .relationship import *
from .representation import *
from .resource import *
from .root import *
from .sensorstate import *
from .spatial import *
from .state import *
from .struct import *
from .task import *
from .telemetry import *
from .validation import *
from .aerial import *
from .entities import *
from .objective import *
from .organization import *
from .military_entities import *
from .robot import *
from .uav import *

for _model in [obj for obj in list(globals().values()) if (OCCIDModel in getattr(obj, "__mro__", ()) or OCCIDValue in getattr(obj, "__mro__", ())) and obj not in {OCCIDModel, OCCIDValue}]:
    _model.model_rebuild(_types_namespace=globals())

_validate_semantic_registry()

__all__ = [name for name in globals() if not name.startswith("_")]
