"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class BooleanOperator(IntEnum):
    NONE = 0
    NOT = auto()
    AND = auto()
    OR = auto()
    XOR = auto()
    NAND = auto()
    NOR = auto()
    XNOR = auto()

### Models

class Predicate(OCCIDModel):
    'Atomic condition leaf; concrete predicate schemas define operands and comparison semantics instead of embedding free-form expressions'
    __occid_model_id__: ClassVar[int] = 195
    __occid_semantic_role__: ClassVar[str] = 'type'
    subject_ref: UID | None = None

class BooleanLogic(OCCIDModel):
    'Boolean composition of Conditions; NONE is identity and NOT is negation for a single term, while the remaining operators combine the term set'
    __occid_model_id__: ClassVar[int] = 21
    __occid_semantic_role__: ClassVar[str] = 'type'
    operator: BooleanOperator
    terms: list[Predicate | BooleanLogic]
