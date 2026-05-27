from .common import *
from .communication import *
from .control import *
from .data import *
from .military import *
from .military_communication import *
from .military_definition import *
from .objects import *
from .constraint import *
from .effect import *
from .entities import *
from .event import *
from .feed import *
from .interface import *
from .media import *
from .message import *
from .network import *
from .node import *
from .objective import *
from .observation import *
from .organization import *
from .plan import *
from .property import *
from .reference import *
from .state import *
from .aerial import *
from .assignment import *
from .c3 import *
from .directive import *
from .health import *
from .input import *
from .internal import *
from .isr import *
from .kinematic import *
from .lifecycle import *
from .military_organization import *
from .protocol import *
from .radio import *
from .resources import *
from .response import *
from .sensors import *
from .spatial import *
from .telemetry import *
from .mesh import *
from .military_aerial import *
from .military_isr import *
from .military_radio import *
from .robot import *
from .military_effects import *
from .military_entities import *
from .military_tasks import *

for _model in [obj for obj in list(globals().values()) if OCCIDModel in getattr(obj, "__mro__", ()) and obj is not OCCIDModel]:
    _model.model_rebuild(_types_namespace=globals())

__all__ = [name for name in globals() if not name.startswith("_")]
