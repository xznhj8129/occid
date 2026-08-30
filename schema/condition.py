"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

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

class Condition(Data):
    'Reusable predicate logic evaluated against object, system, or process facts; it describes logic rather than the mutable state of evaluating that logic'
    __occid_model_id__: ClassVar[int] = 315
    __occid_semantic_role__: ClassVar[str] = 'ontology'

class Predicate(Condition):
    'Atomic condition leaf; concrete predicate schemas define operands and comparison semantics instead of embedding free-form expressions'
    __occid_model_id__: ClassVar[int] = 316
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    subject_ref: UID | None = None

class BooleanLogic(Condition):
    'Boolean composition of Conditions; NONE is identity and NOT is negation for a single term, while the remaining operators combine the term set'
    __occid_model_id__: ClassVar[int] = 317
    __occid_semantic_role__: ClassVar[str] = 'ontology'
    operator: BooleanOperator
    terms: list[SerializeAsAny[Condition | Predicate | BooleanLogic]]
