"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .communication import Communication

### Enums

class CapabilityRole(IntEnum):
    CONTROLLER = 0
    RELAY = auto()
    SENSOR = auto()
    EFFECTOR = auto()
    GATEWAY = auto()
    RECORDER = auto()

### Models

class Node(Communication):
    'Endpoint that sends, receives, relays, records, controls, or bridges messages'

class NodeRef(Node):
    node_id: str
