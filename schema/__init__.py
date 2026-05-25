from .common import *
from .aerial import *
from .communication import *
from .control import *
from .core import *
from .data import *
from .definition import *
from .health import *
from .mesh import *
from .objects import *
from .radio import *
from .robot import *
from .sensors import *
from .spatial import *
from .struct import *
from .entities import *
from .network import *
from .organization import *
from .tasks import *

for _model in [obj for obj in list(globals().values()) if OCCIDModel in getattr(obj, "__mro__", ()) and obj is not OCCIDModel]:
    _model.model_rebuild(_types_namespace=globals())

__all__ = [name for name in globals() if not name.startswith("_")]
