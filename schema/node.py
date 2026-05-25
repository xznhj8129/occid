"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import Communication

### Models

class Node(Communication):
    pass

class NodeRef(Node):
    node_id: str
