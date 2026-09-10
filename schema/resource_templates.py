"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class NATOSupplyClass(IntEnum):
    CLASS_I = 0
    CLASS_II = auto()
    CLASS_III = auto()
    CLASS_IV = auto()
    CLASS_V = auto()
    CLASS_VI = auto()
    CLASS_VII = auto()
    CLASS_VIII = auto()
    CLASS_IX = auto()
    CLASS_X = auto()

### Models

class ResourceTemplate(OCCIDModel):
    'Identified definition of a resource kind that can be required, authorized, held, consumed, or assigned'
    __occid_model_id__: ClassVar[int] = 320
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('EquipmentTemplate', 'PersonnelTemplate', 'SupplyTemplate')
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class EquipmentTemplate(OCCIDModel):
    'Template of equipment counted or allocated as a resource; individual physical equipment may additionally exist as Equipment objects'
    __occid_model_id__: ClassVar[int] = 109
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class PersonnelTemplate(OCCIDModel):
    'Template of a personnel category used for strength, staffing, or resource planning'
    __occid_model_id__: ClassVar[int] = 281
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None

class SupplyTemplate(OCCIDModel):
    'Template of a consumable or stock resource with a customary quantity unit'
    __occid_model_id__: ClassVar[int] = 364
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'ResourceTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitarySupplyTemplate',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    quantity_unit: QuantityUnit | None = None

class ResourceRequirement(OCCIDModel):
    'Required or authorized quantity of one resource definition'
    __occid_model_id__: ClassVar[int] = 319
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    resource_definition_uid: Semantic[UID]
    quantity: Semantic[Quantity]

class MilitarySupplyTemplate(OCCIDModel):
    'Military supply definition classified by NATO-style supply class while retaining the generic resource identity and quantity unit'
    __occid_model_id__: ClassVar[int] = 238
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'SupplyTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('ResourceTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    quantity_unit: QuantityUnit | None = None
    supply_class: NATOSupplyClass
