from .common import *
from .communication import *
from .data import *
from .effects import *
from .health import *
from .mesh import *
from .network import *
from .objects import *
from .radio import *
from .robot import *
from .spatial import *
from .aerial import *
from .organization import *
from .tasks import *
from .entities import *
from .isr import *
from .sensors import *

for _model in [obj for obj in list(globals().values()) if OCCIDModel in getattr(obj, "__mro__", ()) and obj is not OCCIDModel]:
    _model.model_rebuild(_types_namespace=globals())

__all__ = [name for name in globals() if not name.startswith("_")]
