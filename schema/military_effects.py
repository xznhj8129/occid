"""Generated from core/schemav2."""
from __future__ import annotations
import builtins
from .common import *

### Enums

class GuidanceType(IntEnum):
    UNGUIDED = 0
    INERTIAL = auto()
    FPV = auto()
    MCLOS = auto()
    SACLOS = auto()
    OPTICAL = auto()
    IR = auto()
    RADAR = auto()
    LASER = auto()
    RF = auto()

class AttackMode(IntEnum):
    DIRECT_FIRE = 0
    INDIRECT_FIRE = auto()
    STANDOFF = auto()

class ThreatLevel(IntEnum):
    NONE = 0
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class ArmingStatus(IntEnum):
    DISARMED = 0
    ARMED = auto()
    FAULT = auto()

class EsadMunitionStatus(IntEnum):
    NOT_PRESENT = 0
    PRESENT = auto()
    READY = auto()
    FAULT = auto()

class EsadIgnitionStatus(IntEnum):
    OPEN = 0
    CLOSED = auto()
    FIRED = auto()
    FAULT = auto()

class EsadFaultFlag(IntEnum):
    NONE = 0
    WIRING = 1
    POWER_GLITCH = 2
    SIGNAL_INTEGRITY = 4
    SENSOR_ACC = 8
    SENSOR_LIDAR = 16

class EsadArmingRequest(IntEnum):
    DISARM = 0
    ARM = auto()

class RwsArmingState(IntEnum):
    SAFE = 0
    ARMED = auto()
    FAULT = auto()

class PayloadType(IntEnum):
    EO = 0
    EO_IR = auto()
    RADAR = auto()
    ELINT = auto()
    RELAY = auto()
    WEAPON = auto()
    CARGO = auto()
    JAMMER = auto()

class PayloadState(IntEnum):
    OFF = 0
    READY = auto()
    ACTIVE = auto()
    DEGRADED = auto()
    FAILED = auto()

class WarheadType(IntEnum):
    INERT = 0
    HE = auto()
    HEAT = auto()
    FRAG = auto()
    INC = auto()
    SMOKE = auto()
    AP = auto()
    EFP = auto()
    CRW = auto()

class TargetCategory(IntEnum):
    OBJECT = 0
    LOCATION = auto()
    AREA = auto()

### Models

class PayloadAllocation(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 193
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    payload_type: PayloadType
    qty: builtins.int = 0

class PayloadPlan(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 195
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    requested: list[Semantic[PayloadAllocation]]
    approved: list[Semantic[PayloadAllocation]]
    loaded: list[Semantic[PayloadAllocation]]
    notes: builtins.str | None = None

class PayloadMount(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 194
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    mount_ref: builtins.str
    item_ref: builtins.str
    qty: builtins.int = 0
    pylons: builtins.str = ''
    launcher: builtins.str = ''
    compat_tags: list[PayloadType]
    loaded: list[Semantic[PayloadAllocation]]

class EffectsPayload(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 68
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Payload'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    capabilities: list[Semantic[Capability]] | None = None
    item_type: PayloadType
    state: PayloadState | None = None
    weapons: list[Semantic[ItemCount]]
    ammo: list[Semantic[ItemCount]]
    ordnance: list[Semantic[ItemCount]]
    payload_mounts: dict[builtins.str, Semantic[PayloadMount]]
    payload_plan: Semantic[PayloadPlan] | None = None

class Effects(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 67
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('GroundEffects', 'AirEffects')
    has_launchers: builtins.bool
    esad: EsadMunitionStatus | None = None
    payload_mounts: dict[builtins.str, Semantic[PayloadMount]]
    effect_domain: OperationalDomain
    launch_domain: OperationalDomain
    guidance: GuidanceType
    warhead: WarheadType
    pylon_format: builtins.str = ''

class GroundEffects(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 101
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Effects'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    has_launchers: builtins.bool
    esad: EsadMunitionStatus | None = None
    payload_mounts: dict[builtins.str, Semantic[PayloadMount]]
    effect_domain: OperationalDomain
    launch_domain: OperationalDomain
    guidance: GuidanceType
    warhead: WarheadType
    pylon_format: builtins.str = ''
    attack_modes: list[AttackMode]

class AirEffects(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 4
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Effects'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    has_launchers: builtins.bool
    esad: EsadMunitionStatus | None = None
    payload_mounts: dict[builtins.str, Semantic[PayloadMount]]
    effect_domain: OperationalDomain
    launch_domain: OperationalDomain
    guidance: GuidanceType
    warhead: WarheadType
    pylon_format: builtins.str = ''
    reusable: builtins.bool | None = None
    attack_modes: list[AirAttackMode]

class TargetPriority(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 259
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    threat: ThreatLevel | None = None
    is_high_value: builtins.bool = False
    note: builtins.str | None = None

class TargetKinematics(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 258
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    location_state: Semantic[LocationState]
    velocity: Semantic[VelocityVector] | None = None
    velocity_covariance: Semantic[VelocityVector] | None = None

class TargetSet(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 260
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ('TargetSetCoord', 'TargetBoxCoord', 'TargetCoord')
    time_usec: builtins.int
    id: Annotated[IntID, IDNamespace('TargetSet')]
    name: builtins.str

class TargetSetCoord(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 261
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TargetSet'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    id: Annotated[IntID, IDNamespace('TargetSet')]
    name: builtins.str
    center: Semantic[GlobalPosition]
    radius_m: builtins.float
    time_start_usec: builtins.int
    time_end_usec: builtins.int

class TargetBoxCoord(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 255
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TargetSet'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    id: Annotated[IntID, IDNamespace('TargetSet')]
    name: builtins.str
    corners: list[Semantic[GlobalPosition]]
    time_start_usec: builtins.int
    time_end_usec: builtins.int

class TargetCoord(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 256
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'TargetSet'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    id: Annotated[IntID, IDNamespace('TargetSet')]
    name: builtins.str
    kinematics: Semantic[TargetKinematics]
    cep_desired_m: builtins.float
    cep_max_m: builtins.float
    target_class: ObservedObjectType
    target_force: Faction

class Fires(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 81
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    time_impact_usec: builtins.int
    target_position: Semantic[GlobalPosition]
    effector_id: Annotated[IntID, IDNamespace('Entity')]
    sequence: builtins.int
    cep_expected_m: builtins.float

class SplashCorrection(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 244
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    splash_position: Semantic[GlobalPosition]
    sequence: builtins.int
    type_detected: builtins.int
    cep_expected_m: builtins.float

class TargetHandover(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 257
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    detected_first_usec: builtins.int
    valid_until_usec: builtins.int
    kinematics: Semantic[TargetKinematics]
    target_set_id: Annotated[IntID, IDNamespace('TargetSet')]
    target_name: builtins.str
    match_media_url: builtins.str
    confidence_score: builtins.float
    authorization: list[builtins.int]
    target_class: ObservedObjectType
    target_force: Faction
    match_media_type: SensorDataFormat

class BattleDamageAssessment(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 20
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    kinematics: Semantic[TargetKinematics]
    target_set_id: Annotated[IntID, IDNamespace('TargetSet')]
    target_name: builtins.str
    authorization: list[builtins.int]
    destruction_pct: builtins.int
    confidence_pct: builtins.int
    target_class: ObservedObjectType
    target_force: Faction

class EsadState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 76
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    arming_challenge_hash: builtins.int
    fault_flags: EsadFaultFlag
    input_1: builtins.float
    input_2: builtins.float
    sw_version_hash: list[builtins.int]
    arming_status: ArmingStatus
    munition_status: EsadMunitionStatus
    ignition_status: EsadIgnitionStatus
    munition_type: builtins.int

class EsadArming(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 75
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    arming_challenge_hash: builtins.int
    arming_request: EsadArmingRequest

class RwsPose(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 233
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    kinematics: Semantic[TargetKinematics]
    offset_x_m: builtins.float
    offset_y_m: builtins.float
    offset_z_m: builtins.float
    orientation_quaternion: tuple[builtins.float, builtins.float, builtins.float, builtins.float]
    accuracy_roll_rad: builtins.float
    accuracy_pitch_rad: builtins.float
    accuracy_yaw_rad: builtins.float
    coordinate_frame: builtins.int

class RwsState(OCCIDModel):
    __occid_model_id__: ClassVar[int] = 234
    __occid_semantic_role__: ClassVar[str] = 'representation'
    __occid_parent__: ClassVar[str | None] = 'Struct'
    __occid_children__: ClassVar[tuple[str, ...]] = ()
    time_usec: builtins.int
    weapon_string: builtins.str
    arming_state: RwsArmingState
