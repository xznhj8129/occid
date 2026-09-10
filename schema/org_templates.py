"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Models

class OrgTemplate(OCCIDModel):
    'Reusable definition or template for an organization, distinct from a concrete Organization and its changing state'
    __occid_model_id__: ClassVar[int] = 269
    __occid_semantic_role__: ClassVar[str] = 'concept'
    __occid_parent__: ClassVar[str | None] = 'Definition'
    __occid_children__: ClassVar[tuple[str, ...]] = ('MilitaryOrgTemplate',)
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OrgTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    topology: OrgTopology | None = None
    resource_requirements: list[Semantic[ResourceRequirement]]

class OrgComposition(OCCIDModel):
    'Required or doctrinal quantity of subordinate organizations defined by reusable organization definitions'
    __occid_model_id__: ClassVar[int] = 267
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    org_template_uid: Semantic[UID]
    quantity: Semantic[Count]

class MilitaryOrgTemplate(OCCIDModel):
    'Reusable military organizational definition or template, including doctrinal structure and authorized resources'
    __occid_model_id__: ClassVar[int] = 233
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'OrgTemplate'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    record: Semantic[Record]
    uid: Semantic[UID]
    id: Annotated[IntID, IDNamespace('OrgTemplate')]
    name: builtins.str | None = None
    description: Semantic[PlainText] | None = None
    topology: OrgTopology | None = None
    resource_requirements: list[Semantic[ResourceRequirement]]
    category: NATOUnitCategory
    size: OOBSize
    op_domain: OperationalDomain
    tactical_elements: list[Semantic[OrgComposition]]
    support_elements: list[Semantic[OrgComposition]]
