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

class Condition(OCCIDModel):
    'Reusable predicate logic evaluated against object, system, or process facts; it describes logic rather than the mutable state of evaluating that logic'
    __occid_model_id__: ClassVar[int] = 40
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Data'
    __occid_children__: ClassVar[tuple[str, ...]] = ('Predicate', 'BooleanLogic')

class Predicate(OCCIDModel):
    'Atomic condition leaf; concrete predicate schemas define operands and comparison semantics instead of embedding free-form expressions'
    __occid_model_id__: ClassVar[int] = 207
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Condition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    subject_ref: Semantic[UID] | None = None

class BooleanLogic(OCCIDModel):
    'Boolean composition of Conditions; NONE is identity and NOT is negation for a single term, while the remaining operators combine the term set'
    __occid_model_id__: ClassVar[int] = 22
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Condition'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    operator: BooleanOperator
    terms: list[Semantic[Condition]]
