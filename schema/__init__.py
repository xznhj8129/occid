from .common import *
from .root import *
from .communication import *
from .control import *
from .data import *
from .definition import *
from .object import *
from .struct import *
from .command import *
from .constraint import *
from .event import *
from .interface import *
from .link import *
from .media import *
from .message import *
from .network import *
from .node import *
from .observation import *
from .organization import *
from .property import *
from .protocol import *
from .record import *
from .reference import *
from .state import *
from .task import *
from .assignment import *
from .attribute import *
from .c3 import *
from .guidance import *
from .health import *
from .identity import *
from .input import *
from .internal import *
from .isr import *
from .kinematic import *
from .lifecycle import *
from .objective import *
from .parameter import *
from .plan import *
from .radio import *
from .relationship import *
from .resource import *
from .sensorstate import *
from .spatial import *
from .telemetry import *
from .entities import *
from .mesh import *
from .payload import *
from .robot import *
from .uav import *

for _model in [obj for obj in list(globals().values()) if OCCIDModel in getattr(obj, "__mro__", ()) and obj is not OCCIDModel]:
    _model.model_rebuild(_types_namespace=globals())

__all__ = [name for name in globals() if not name.startswith("_")]
