"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

from .data import Data

### Models

class Condition(Data):
    'Reusable predicate logic evaluated against object, system, or process facts; it describes logic rather than the mutable state of evaluating that logic'
    __occid_model_id__: ClassVar[int] = 315

class Predicate(Condition):
    'Atomic condition leaf; concrete predicate schemas define operands and comparison semantics instead of embedding free-form expressions'
    __occid_model_id__: ClassVar[int] = 316
    subject_ref: StringID | None = None

class Conjunction(Condition):
    'Condition that is true when every term is true'
    __occid_model_id__: ClassVar[int] = 317
    terms: list[SerializeAsAny[Condition | Predicate | Conjunction | Disjunction | Negation]]

class Disjunction(Condition):
    'Condition that is true when any term is true'
    __occid_model_id__: ClassVar[int] = 318
    terms: list[SerializeAsAny[Condition | Predicate | Conjunction | Disjunction | Negation]]

class Negation(Condition):
    'Condition that is true when its term is false'
    __occid_model_id__: ClassVar[int] = 319
    term: SerializeAsAny[Condition | Predicate | Conjunction | Disjunction | Negation]
