"""Reference SDK interoperability mappings for OCCID.

Interop modules provide deterministic type/structure conversion only. They do
not own endpoint I/O, operation selection, sequencing, retries, or autonomy.
"""

from .common import *
from .cot import *
from .mavsdk import *
from .msp import *
