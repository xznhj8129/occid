"""Generated from core/schemav2."""
from __future__ import annotations
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
    payload_type: PayloadType
    qty: int = 0

class PayloadPlanSchema(OCCIDModel):
    requested: list[PayloadAllocation]
    approved: list[PayloadAllocation]
    loaded: list[PayloadAllocation]
    notes: str | None = None

class PayloadMountSchema(OCCIDModel):
    mount_id: str
    item_id: str
    qty: int = 0
    pylons: str = ''
    launcher: str = ''
    compat_tags: list[PayloadType]
    loaded: list[PayloadAllocation]

class PayloadSchema(OCCIDModel):
    item_type: PayloadType
    state: PayloadState | None = None
    weapons: list[ItemCount]
    ammo: list[ItemCount]
    ordnance: list[ItemCount]
    payload_mounts: dict[str, PayloadMountSchema]
    payload_plan: PayloadPlanSchema | None = None

class EffectsSchema(OCCIDModel):
    has_launchers: bool
    esad: EsadMunitionStatus | None = None
    payload_mounts: dict[str, PayloadMountSchema]
    effect_domain: OperationalDomain
    launch_domain: OperationalDomain
    guidance: GuidanceType
    warhead: WarheadType
    pylon_format: str = ''

class GroundEffectsSchema(EffectsSchema):
    attack_modes: list[AttackMode]

class AirEffectsSchema(EffectsSchema):
    reusable: bool | None = None
    attack_modes: list[AirAttackMode]

class TargetPrioritySchema(OCCIDModel):
    threat: ThreatLevel | None = None
    is_high_value: bool = False
    note: str | None = None

class TargetKinematics(OCCIDModel):
    location_state: LocationState
    velocity: VelocityVector | None = None
    velocity_covariance: VelocityVector | None = None

class TargetSetCoord(OCCIDModel):
    time_usec: int
    target_set_id: int
    target_set_name: str
    center: GlobalPosition
    radius_m: float
    time_start_usec: int
    time_end_usec: int

class TargetBoxCoord(OCCIDModel):
    time_usec: int
    target_set_id: int
    target_set_name: str
    corners: list[GlobalPosition]
    time_start_usec: int
    time_end_usec: int

class TargetCoord(OCCIDModel):
    time_usec: int
    target_set_id: int
    target_name: str
    kinematics: TargetKinematics
    cep_desired_m: float
    cep_max_m: float
    target_class: ObservedObjectType
    target_force: Faction

class Fires(OCCIDModel):
    time_usec: int
    time_impact_usec: int
    target_position: GlobalPosition
    effector_id: int
    sequence: int
    cep_expected_m: float

class SplashCorrection(OCCIDModel):
    time_usec: int
    splash_position: GlobalPosition
    sequence: int
    type_detected: int
    cep_expected_m: float

class TargetHandover(OCCIDModel):
    time_usec: int
    detected_first_usec: int
    valid_until_usec: int
    kinematics: TargetKinematics
    target_set_id: int
    target_name: str
    match_media_url: str
    confidence_score: float
    authorization: list[int]
    target_class: ObservedObjectType
    target_force: Faction
    match_media_type: SensorDataFormat

class BattleDamageAssessment(OCCIDModel):
    time_usec: int
    kinematics: TargetKinematics
    target_set_id: int
    target_name: str
    authorization: list[int]
    destruction_pct: int
    confidence_pct: int
    target_class: ObservedObjectType
    target_force: Faction

class EsadState(OCCIDModel):
    time_usec: int
    arming_challenge_hash: int
    fault_flags: EsadFaultFlag
    input_1: float
    input_2: float
    sw_version_hash: list[int]
    arming_status: ArmingStatus
    munition_status: EsadMunitionStatus
    ignition_status: EsadIgnitionStatus
    munition_type: int

class EsadArming(OCCIDModel):
    time_usec: int
    arming_challenge_hash: int
    arming_request: EsadArmingRequest

class RwsPose(OCCIDModel):
    time_usec: int
    kinematics: TargetKinematics
    offset_x_m: float
    offset_y_m: float
    offset_z_m: float
    orientation_quaternion: tuple[float, float, float, float]
    accuracy_roll_rad: float
    accuracy_pitch_rad: float
    accuracy_yaw_rad: float
    coordinate_frame: int

class RwsState(OCCIDModel):
    time_usec: int
    weapon_string: str
    arming_state: RwsArmingState
    weapon_type: int
