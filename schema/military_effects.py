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

class EffectsSchema_type(IntEnum):
    GROUND = 0
    AIR = auto()

### Models

class PayloadAllocation(OCCIDModel):
    payload_type: PayloadType
    qty: builtins.int = 0

class PayloadPlanSchema(OCCIDModel):
    requested: list[PayloadAllocation]
    approved: list[PayloadAllocation]
    loaded: list[PayloadAllocation]
    notes: builtins.str | None = None

class PayloadMountSchema(OCCIDModel):
    mount_id: StringID
    item_id: StringID
    qty: builtins.int = 0
    pylons: builtins.str = ''
    launcher: builtins.str = ''
    compat_tags: list[PayloadType]
    loaded: list[PayloadAllocation]

class PayloadSchema(OCCIDModel):
    item_type: PayloadType
    state: PayloadState | None = None
    weapons: list[ItemCount]
    ammo: list[ItemCount]
    ordnance: list[ItemCount]
    payload_mounts: dict[builtins.str, PayloadMountSchema]
    payload_plan: PayloadPlanSchema | None = None

class EffectsSchema(OCCIDModel):
    has_launchers: builtins.bool
    esad: EsadMunitionStatus | None = None
    payload_mounts: dict[builtins.str, PayloadMountSchema]
    effect_domain: OperationalDomain
    launch_domain: OperationalDomain
    guidance: GuidanceType
    warhead: WarheadType
    pylon_format: builtins.str = ''

class GroundEffectsSchema(EffectsSchema):
    attack_modes: list[AttackMode]

class AirEffectsSchema(EffectsSchema):
    reusable: builtins.bool | None = None
    attack_modes: list[AirAttackMode]

class TargetPrioritySchema(OCCIDModel):
    threat: ThreatLevel | None = None
    is_high_value: builtins.bool = False
    note: builtins.str | None = None

class TargetKinematics(OCCIDModel):
    location_state: LocationState
    velocity: VelocityVector | None = None
    velocity_covariance: VelocityVector | None = None

class TargetSetCoord(OCCIDModel):
    time_usec: builtins.int
    target_set_id: builtins.int
    target_set_name: builtins.str
    center: GlobalPosition
    radius_m: builtins.float
    time_start_usec: builtins.int
    time_end_usec: builtins.int

class TargetBoxCoord(OCCIDModel):
    time_usec: builtins.int
    target_set_id: builtins.int
    target_set_name: builtins.str
    corners: list[GlobalPosition]
    time_start_usec: builtins.int
    time_end_usec: builtins.int

class TargetCoord(OCCIDModel):
    time_usec: builtins.int
    target_set_id: builtins.int
    target_name: builtins.str
    kinematics: TargetKinematics
    cep_desired_m: builtins.float
    cep_max_m: builtins.float
    target_class: ObservedObjectType
    target_force: Faction

class Fires(OCCIDModel):
    time_usec: builtins.int
    time_impact_usec: builtins.int
    target_position: GlobalPosition
    effector_id: builtins.int
    sequence: builtins.int
    cep_expected_m: builtins.float

class SplashCorrection(OCCIDModel):
    time_usec: builtins.int
    splash_position: GlobalPosition
    sequence: builtins.int
    type_detected: builtins.int
    cep_expected_m: builtins.float

class TargetHandover(OCCIDModel):
    time_usec: builtins.int
    detected_first_usec: builtins.int
    valid_until_usec: builtins.int
    kinematics: TargetKinematics
    target_set_id: builtins.int
    target_name: builtins.str
    match_media_url: builtins.str
    confidence_score: builtins.float
    authorization: list[builtins.int]
    target_class: ObservedObjectType
    target_force: Faction
    match_media_type: SensorDataFormat

class BattleDamageAssessment(OCCIDModel):
    time_usec: builtins.int
    kinematics: TargetKinematics
    target_set_id: builtins.int
    target_name: builtins.str
    authorization: list[builtins.int]
    destruction_pct: builtins.int
    confidence_pct: builtins.int
    target_class: ObservedObjectType
    target_force: Faction

class EsadState(OCCIDModel):
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
    time_usec: builtins.int
    arming_challenge_hash: builtins.int
    arming_request: EsadArmingRequest

class RwsPose(OCCIDModel):
    time_usec: builtins.int
    kinematics: TargetKinematics
    offset_x_m: builtins.float
    offset_y_m: builtins.float
    offset_z_m: builtins.float
    orientation_quaternion: tuple[builtins.float, builtins.float, builtins.float, builtins.float]
    accuracy_roll_rad: builtins.float
    accuracy_pitch_rad: builtins.float
    accuracy_yaw_rad: builtins.float
    coordinate_frame: builtins.int

class RwsState(OCCIDModel):
    time_usec: builtins.int
    weapon_string: builtins.str
    arming_state: RwsArmingState
    weapon_type: builtins.int
