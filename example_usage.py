"""OCCID end-to-end field manual.

This is not a normal programming example or test fixture. It is the readable,
executable answer to "how is OCCID supposed to work?": architecture expressed
as code in one small operational scenario.

Identity rule:

    UID = exact 16-byte OCCID identity value; this example allocates it with UUIDv4
    ID  = sequential integer scoped to its declared IntID namespace/family

Entity 38, Track 38, and Task 38 are unrelated local IDs because they belong to
different IntID namespaces. Their UIDs are globally unambiguous. Durable
cross-object references use UIDs, never IDs.

The scenario walks through identities, organizations, communications, external
protocol mapping, authority, tasking, dispatch, vehicle action, telemetry,
observation, execution, tracking, and compact wire.
"""

from __future__ import annotations

import struct
import time
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from interop.cot import CotPointFields, cot_point_to_location_state
from interop.mavsdk import (
    MavsdkPositionFields,
    goto_command_to_fields,
    position_to_location_state,
)
from occid import (
    AddressKind,
    AirNavigation,
    AirframeType,
    AltitudeDatum,
    AssignmentStatus,
    AutopilotType,
    CapabilityRole,
    CommandAuthority,
    CommandMessage,
    ConfidenceLevel,
    Drone,
    EntityState,
    Execution,
    ExecutionCommand,
    ExecutionOperation,
    ExecutionPhase,
    FirmwareInfo,
    GlobalPosition,
    Group,
    InformationIntent,
    InertialReferenceFrame,
    IntelCategory,
    IsrObservation,
    Link,
    LinkDataType,
    LinkDirection,
    LinkType,
    MessagePriority,
    MotionCommand,
    MotionOperation,
    NavAids,
    NavigationMode,
    NetworkAddress,
    Node,
    Objective,
    ObservationKind,
    ObservationMessage,
    ObservationTimeBasis,
    OrgLevel,
    OrgTopology,
    OrgType,
    Plan,
    PlanApprovalState,
    Person,
    PlanStep,
    PropulsionType,
    Record,
    RemoteControl,
    RobotController,
    Role,
    Roster,
    SpotterOrigin,
    TaskAssignment,
    TaskInformation,
    TaskPhase,
    TaskPriority,
    TaskStatus,
    Timestamp,
    Track,
    TrackState,
    TrackUpdate,
    UID,
    UAVTelemetryMessage,
    Unit,
    VelocityVector,
    Version,
    WeatherLimits,
)


# ---------------------------------------------------------------------------
# External protocol fixtures
# ---------------------------------------------------------------------------
# These remain protocol-native. CoT UID and MAVLink sysid/compid are not OCCID
# identity and are never substituted for OCCID UID or ID.

COT_XML = """\
<event version="2.0"
       uid="contact-route6-1"
       type="a-u-G"
       time="2026-08-25T17:00:00Z"
       start="2026-08-25T17:00:00Z"
       stale="2026-08-25T17:05:00Z"
       how="m-g">
    <point lat="45.5024"
           lon="-73.5665"
           hae="42.0"
           ce="6.0"
           le="10.0"/>
    <detail>
        <contact callsign="CONTACT-1"/>
    </detail>
</event>
"""

MAVLINK_GLOBAL_POSITION_INT = bytes.fromhex(
    "fd1c00002a0701210000"
    "40e2010028021f1b588526d4c0d40100409c0000f4010000ceff2823"
    "665f"
)

MAVLINK_GLOBAL_POSITION_INT_MOVING = bytes.fromhex(
    "fd1c00002b0701210000"
    "10ea0100c8111f1be09826d448e80100c8af00002c01c800ecffa00f"
    "5005"
)

MAVLINK_GLOBAL_POSITION_INT_ID = 33
MAVLINK_GLOBAL_POSITION_INT_CRC_EXTRA = 104


# ---------------------------------------------------------------------------
# UID globally, ID inside an IntID namespace/family
# ---------------------------------------------------------------------------


def new_uid() -> UID:
    return UID(uuid.uuid4().bytes)


def uid_str(uid: UID) -> str:
    return str(UUID(bytes=uid.root))


def local_id(value) -> int:
    return int(value.root)


@dataclass
class ClassIDRegistry:
    """Small human IDs have one independent sequence per IntID namespace."""

    next_id: dict[str, int] = field(default_factory=dict)

    def allocate(self, object_class: str) -> int:
        value = self.next_id.get(object_class, 1)
        self.next_id[object_class] = value + 1
        return value


# ---------------------------------------------------------------------------
# Small mechanics used by the walkthrough
# ---------------------------------------------------------------------------


def timestamp(value: float | None = None) -> Timestamp:
    return Timestamp(utime=time.time() if value is None else value, tz=0)


def record(registry: ClassIDRegistry, origin: str) -> Record:
    now = timestamp()
    return Record(
        uid=new_uid(),
        id=registry.allocate("Record"),
        created_ts=now,
        updated_ts=now,
        origin_system=origin,
        provenance=[],
    )


@dataclass(frozen=True)
class ParsedCotEvent:
    uid: str
    cot_type: str
    callsign: str | None
    event_ts: float
    point: CotPointFields


@dataclass(frozen=True)
class ParsedMavlinkPosition:
    system_id: int
    component_id: int
    time_boot_ms: int
    latitude_deg: float
    longitude_deg: float
    absolute_altitude_m: float
    relative_altitude_m: float
    velocity_north_m_s: float
    velocity_east_m_s: float
    velocity_down_m_s: float
    heading_deg: float | None


def parse_cot_xml(xml_text: str) -> ParsedCotEvent:
    event = ET.fromstring(xml_text)
    if event.tag != "event":
        raise ValueError("expected CoT <event> root")

    point = event.find("point")
    if point is None:
        raise ValueError("CoT event has no <point>")

    event_time = event.get("time")
    if event_time is None:
        raise ValueError("CoT event has no time")

    contact = event.find("./detail/contact")

    def required_float(name: str) -> float:
        value = point.get(name)
        if value is None:
            raise ValueError(f"CoT point has no {name}")
        return float(value)

    def optional_float(name: str) -> float | None:
        value = point.get(name)
        return None if value is None else float(value)

    return ParsedCotEvent(
        uid=event.attrib["uid"],
        cot_type=event.attrib["type"],
        callsign=None if contact is None else contact.get("callsign"),
        event_ts=datetime.fromisoformat(event_time.replace("Z", "+00:00")).timestamp(),
        point=CotPointFields(
            lat_deg=required_float("lat"),
            lon_deg=required_float("lon"),
            hae_m=required_float("hae"),
            ce_m=optional_float("ce"),
            le_m=optional_float("le"),
        ),
    )


def _x25_accumulate(byte: int, crc: int) -> int:
    tmp = byte ^ (crc & 0xFF)
    tmp = (tmp ^ (tmp << 4)) & 0xFF
    return ((crc >> 8) ^ (tmp << 8) ^ (tmp << 3) ^ (tmp >> 4)) & 0xFFFF


def _mavlink_crc(data: bytes, crc_extra: int) -> int:
    crc = 0xFFFF
    for byte in data:
        crc = _x25_accumulate(byte, crc)
    return _x25_accumulate(crc_extra, crc)


def parse_mavlink_global_position(frame: bytes) -> ParsedMavlinkPosition:
    if len(frame) < 12 or frame[0] != 0xFD:
        raise ValueError("expected MAVLink v2 frame")

    payload_len = frame[1]
    if frame[2] & 0x01:
        raise ValueError("signed MAVLink frames are outside this tiny parser")

    frame_len = 10 + payload_len + 2
    if len(frame) != frame_len:
        raise ValueError(f"unexpected MAVLink frame length {len(frame)} != {frame_len}")

    message_id = frame[7] | (frame[8] << 8) | (frame[9] << 16)
    if message_id != MAVLINK_GLOBAL_POSITION_INT_ID:
        raise ValueError(f"expected GLOBAL_POSITION_INT, got message {message_id}")
    if payload_len != 28:
        raise ValueError(f"unexpected GLOBAL_POSITION_INT payload length {payload_len}")

    payload = frame[10 : 10 + payload_len]
    expected_crc = struct.unpack_from("<H", frame, 10 + payload_len)[0]
    actual_crc = _mavlink_crc(
        frame[1 : 10 + payload_len],
        MAVLINK_GLOBAL_POSITION_INT_CRC_EXTRA,
    )
    if actual_crc != expected_crc:
        raise ValueError(
            f"MAVLink checksum mismatch 0x{actual_crc:04x} != 0x{expected_crc:04x}"
        )

    (
        time_boot_ms,
        lat,
        lon,
        alt_mm,
        relative_alt_mm,
        vx_cm_s,
        vy_cm_s,
        vz_cm_s,
        heading_cdeg,
    ) = struct.unpack("<IiiiihhhH", payload)

    return ParsedMavlinkPosition(
        system_id=frame[5],
        component_id=frame[6],
        time_boot_ms=time_boot_ms,
        latitude_deg=lat / 1e7,
        longitude_deg=lon / 1e7,
        absolute_altitude_m=alt_mm / 1000.0,
        relative_altitude_m=relative_alt_mm / 1000.0,
        velocity_north_m_s=vx_cm_s / 100.0,
        velocity_east_m_s=vy_cm_s / 100.0,
        velocity_down_m_s=vz_cm_s / 100.0,
        heading_deg=None if heading_cdeg == 0xFFFF else heading_cdeg / 100.0,
    )


# ---------------------------------------------------------------------------
# Complete OCCID walkthrough
# ---------------------------------------------------------------------------


def main() -> None:
    # ID allocation follows the namespace declared by IntID(...). Group and Unit
    # therefore share Organization IDs, Person and Drone share Entity IDs, while
    # Track and Task have independent sequences.
    registry = ClassIDRegistry(
        next_id={
            "Organization": 2,
            "Entity": 37,
            "Node": 5,
            "Track": 38,
            "Observation": 1,
            "Authority": 1,
            "Objective": 1,
            "Task": 38,
            "Assignment": 1,
            "Plan": 1,
            "Execution": 1,
            "Record": 1,
        }
    )

    # Allocate stable identities before constructing objects that refer to one
    # another. This is ordinary OCCID identity, not a separate bootstrap model.
    task_force_uid = new_uid()
    task_force_id = registry.allocate("Organization")
    uas_unit_uid = new_uid()
    uas_unit_id = registry.allocate("Organization")
    operator_uid = new_uid()
    operator_id = registry.allocate("Entity")
    uav_uid = new_uid()
    uav_id = registry.allocate("Entity")
    hq_node_uid = new_uid()
    hq_node_id = registry.allocate("Node")
    uav_node_uid = new_uid()
    uav_node_id = registry.allocate("Node")

    # -----------------------------------------------------------------------
    # 1. Entities and communications endpoints
    # -----------------------------------------------------------------------
    operator = Person(
        record=record(registry, "provisioning"),
        uid=operator_uid,
        id=operator_id,
        node_uids=[hq_node_uid],
        name="Mission Operator",
        callsign="FROG-OPS",
        tags=["OPERATOR"],
        metadata={},
        relations=[],
        role="operator",
        navigation=NavigationMode.MANUAL,
        navaids=[],
        sensors={},
    )

    uav = Drone(
        record=record(registry, "provisioning"),
        uid=uav_uid,
        id=uav_id,
        node_uids=[uav_node_uid],
        name="Frog UAV 38",
        callsign="FROG-38",
        tags=["UAV", "ISR"],
        metadata={},
        relations=[],
        propulsion=PropulsionType.ROTARY_WING,
        components=[],
        model="Frog UAV",
        sensors={},
        navigation=AirNavigation(
            flight_type=AirframeType.COPTER,
            control_modes=[],
            weather_limits=WeatherLimits(),
            propulsion=PropulsionType.ROTARY_WING,
            navigation=NavigationMode.GNSS,
            navaids=[NavAids.GNSS],
            max_range=0.0,
            max_flight_t=0.0,
            max_spd=0.0,
            cruise_spd=0.0,
            max_alt=0.0,
        ),
        controller=RobotController(
            autopilot_type=AutopilotType.PX4,
            autopilot_firmware=FirmwareInfo(
                name="PX4",
                version=Version(major=1, minor=0, patch=0),
            ),
        ),
        remote_control=RemoteControl(channel_map=[], mode_ranges=[]),
    )

    hq_address = NetworkAddress(kind=AddressKind.IPV4, value="10.42.0.1", port=7447)
    uav_address = NetworkAddress(kind=AddressKind.IPV4, value="10.42.0.38", port=7447)

    hq_node = Node(
        uid=hq_node_uid,
        id=hq_node_id,
        entity_uid=operator.uid,
        roles=[CapabilityRole.CONTROLLER, CapabilityRole.GATEWAY],
        addresses=[hq_address],
        links={
            "hivelink": Link(
                name="HiveLink bearer",
                interface_name="hivelink0",
                link_type=LinkType.MESH,
                data_type=LinkDataType.PACKET,
                direction=LinkDirection.FULL_DUPLEX,
            )
        },
        radios={},
        protocols={},
    )

    uav_node = Node(
        uid=uav_node_uid,
        id=uav_node_id,
        entity_uid=uav.uid,
        roles=[CapabilityRole.SENSOR, CapabilityRole.EFFECTOR, CapabilityRole.RELAY],
        addresses=[uav_address],
        links={
            "hivelink": Link(
                name="HiveLink bearer",
                interface_name="hivelink0",
                link_type=LinkType.MESH,
                data_type=LinkDataType.PACKET,
                direction=LinkDirection.FULL_DUPLEX,
            )
        },
        radios={},
        protocols={},
    )

    # -----------------------------------------------------------------------
    # 2. Organization
    # -----------------------------------------------------------------------
    # Organization.elements is the authoritative containment/membership edge.
    # The Group contains the Unit; the Unit contains its individual actors.
    uas_unit = Unit(
        record=record(registry, "provisioning"),
        uid=uas_unit_uid,
        id=uas_unit_id,
        name="UAS Section",
        unit_code="UAS",
        callsign="FROG-UAS",
        org_level=OrgLevel.UNIT,
        org_rank=1,
        org_type=OrgType.GOVT,
        topology=OrgTopology.HIERARCHICAL,
        elements=[operator.uid, uav.uid],
        roster=Roster(roster={}),
        leases=[],
    )

    task_force = Group(
        record=record(registry, "provisioning"),
        uid=task_force_uid,
        id=task_force_id,
        name="Task Force Frog",
        unit_code="TFF",
        callsign="FROG-HQ",
        org_level=OrgLevel.GROUP,
        org_rank=0,
        org_type=OrgType.GOVT,
        topology=OrgTopology.HIERARCHICAL,
        elements=[uas_unit.uid],
        roster=Roster(roster={}),
        leases=[],
    )

    # -----------------------------------------------------------------------
    # 3. External protocols become OCCID observations and state
    # -----------------------------------------------------------------------
    cot = parse_cot_xml(COT_XML)
    mavlink = parse_mavlink_global_position(MAVLINK_GLOBAL_POSITION_INT)

    cot_location = cot_point_to_location_state(cot.point)
    if cot_location.position is None:
        raise ValueError("CoT point conversion did not produce a global position")
    reported_position = cot_location.position

    track = Track(
        record=record(registry, "sigma.track"),
        uid=new_uid(),
        id=registry.allocate("Track"),
    )

    source_observation = IsrObservation(
        record=record(registry, "adapter.cot"),
        uid=new_uid(),
        id=registry.allocate("Observation"),
        track_uid=track.uid,
        obs_ts=timestamp(cot.event_ts),
        observation_kind=ObservationKind.TRACK,
        position=reported_position,
        uncertainty=cot_location.uncertainty,
        confidence=ConfidenceLevel.LOW,
    )

    initial_track_update = TrackUpdate(
        record=record(registry, "adapter.cot"),
        track_uid=track.uid,
        track_state=TrackState.NEW,
        updated_ts=timestamp(),
        confidence=ConfidenceLevel.LOW,
    )

    mavlink_location = position_to_location_state(
        MavsdkPositionFields(
            latitude_deg=mavlink.latitude_deg,
            longitude_deg=mavlink.longitude_deg,
            absolute_altitude_m=mavlink.absolute_altitude_m,
            relative_altitude_m=mavlink.relative_altitude_m,
        )
    )

    initial_uav_state = EntityState(
        record=record(registry, "adapter.mavlink"),
        subject_uid=uav.uid,
        timestamp=time.time(),
        position=mavlink_location,
        motion=VelocityVector(
            x=mavlink.velocity_north_m_s,
            y=mavlink.velocity_east_m_s,
            z=mavlink.velocity_down_m_s,
            frame=InertialReferenceFrame.NED,
        ),
        link_states={},
        source_observation_ts=timestamp(mavlink.time_boot_ms / 1000.0),
        source_time_basis=ObservationTimeBasis.BOOT,
        received_ts=timestamp(),
    )

    external_identity_map = {
        f"cot.uid:{cot.uid}": track.uid,
        f"mavlink:{mavlink.system_id}:{mavlink.component_id}": uav.uid,
    }

    # -----------------------------------------------------------------------
    # 4. Organizational authority
    # -----------------------------------------------------------------------
    command_authority = CommandAuthority(
        record=record(registry, "sigma.authority"),
        uid=new_uid(),
        id=registry.allocate("Authority"),
        holder_uid=operator.uid,
        granted_by_uid=task_force.uid,
        scope_uids=[uas_unit.uid, uav.uid],
        constraints=[],
        organization_uid=uas_unit.uid,
        role=Role(),
    )

    # -----------------------------------------------------------------------
    # 5. Objective -> Task -> Assignment -> Plan
    # -----------------------------------------------------------------------
    objective = Objective(
        record=record(registry, "sigma.control"),
        uid=new_uid(),
        id=registry.allocate("Objective"),
        name="Inspect reported contact",
        intent="Determine the current status of the reported Route 6 contact.",
        desired_state="The contact has been inspected and the track is updated.",
        success_criteria=[],
        target_uids=[track.uid],
        constraints=[],
        priority=TaskPriority.HIGH,
        owner_uid=operator.uid,
        start_time=time.time(),
    )

    task = TaskInformation(
        record=record(registry, "sigma.control"),
        uid=new_uid(),
        id=registry.allocate("Task"),
        instruction="Inspect the reported contact and update its status.",
        intent=InformationIntent.OBSERVE,
        target_uids=[track.uid],
        location_uids=[],
        objective_uid=objective.uid,
        constraints=[],
        start_time=time.time(),
        priority=TaskPriority.HIGH,
        status=TaskStatus.ACCEPTED,
        phase=TaskPhase.ASSIGNED,
    )

    assignment = TaskAssignment(
        record=record(registry, "sigma.control"),
        uid=new_uid(),
        id=registry.allocate("Assignment"),
        assignee_uid=uav.uid,
        authority_uid=command_authority.uid,
        assigned_by_uid=operator.uid,
        status=AssignmentStatus.ACTIVE,
        constraints=[],
        task_uid=task.uid,
    )

    plan = Plan(
        record=record(registry, "sigma.control"),
        uid=new_uid(),
        id=registry.allocate("Plan"),
        name="Inspect Route 6 contact",
        objective_uids=[objective.uid],
        task_uids=[task.uid],
        actor_uids=[uav.uid],
        resource_uids=[],
        assignment_uids=[assignment.uid],
        steps=[PlanStep(actor_uids=[uav.uid], depends_on=[], sequence=1)],
        routes=[],
        constraints=[],
        contingencies=[],
        approval_state=PlanApprovalState.APPROVED,
    )

    # -----------------------------------------------------------------------
    # 6. Dispatch
    # -----------------------------------------------------------------------
    start_execution = ExecutionCommand(
        target_uid=plan.uid,
        constraints=[],
        operation=ExecutionOperation.EXECUTE,
    )

    start_message = CommandMessage(
        src=hq_node.uid,
        dst=uav_node.uid,
        ts=timestamp(),
        priority=MessagePriority.IMMEDIATE,
        seq=1,
        command=start_execution,
    )

    execution_started = timestamp()

    # -----------------------------------------------------------------------
    # 7. Concrete vehicle action, translated only at the edge to MAVSDK
    # -----------------------------------------------------------------------
    move = MotionCommand(
        target_uid=uav.uid,
        constraints=[],
        operation=MotionOperation.MOVE_TO,
        destination=GlobalPosition(
            lat=reported_position.lat,
            lon=reported_position.lon,
            alt=60.0,
            alt_frame=AltitudeDatum.RELATIVE,
        ),
    )

    outbound_goto = goto_command_to_fields(
        move,
        current_absolute_altitude_m=mavlink.absolute_altitude_m,
        current_relative_altitude_m=mavlink.relative_altitude_m,
    )

    # -----------------------------------------------------------------------
    # 8. MAVLink telemetry -> OCCID telemetry
    # -----------------------------------------------------------------------
    mavlink_moving = parse_mavlink_global_position(MAVLINK_GLOBAL_POSITION_INT_MOVING)
    moving_location = position_to_location_state(
        MavsdkPositionFields(
            latitude_deg=mavlink_moving.latitude_deg,
            longitude_deg=mavlink_moving.longitude_deg,
            absolute_altitude_m=mavlink_moving.absolute_altitude_m,
            relative_altitude_m=mavlink_moving.relative_altitude_m,
        )
    )

    uav_state = EntityState(
        record=record(registry, "adapter.mavlink"),
        subject_uid=uav.uid,
        timestamp=time.time(),
        position=moving_location,
        motion=VelocityVector(
            x=mavlink_moving.velocity_north_m_s,
            y=mavlink_moving.velocity_east_m_s,
            z=mavlink_moving.velocity_down_m_s,
            frame=InertialReferenceFrame.NED,
        ),
        link_states={},
        source_observation_ts=timestamp(mavlink_moving.time_boot_ms / 1000.0),
        source_time_basis=ObservationTimeBasis.BOOT,
        received_ts=timestamp(),
    )

    uav_telemetry = UAVTelemetryMessage(
        src=uav_node.uid,
        dst=hq_node.uid,
        ts=timestamp(),
        priority=MessagePriority.ROUTINE,
        seq=2,
        state=uav_state,
    )

    # -----------------------------------------------------------------------
    # 9. New evidence and maintained Track
    # -----------------------------------------------------------------------
    if uav_state.position is None or uav_state.position.position is None:
        raise ValueError("ownship telemetry has no global position")

    spotter_origin = SpotterOrigin(position=uav_state.position.position)

    first_spot_position = GlobalPosition(
        lat=reported_position.lat + 0.00003,
        lon=reported_position.lon + 0.00002,
        alt=reported_position.alt,
        alt_frame=reported_position.alt_frame,
    )

    first_spot = IsrObservation(
        record=record(registry, "mpfc.observation"),
        uid=new_uid(),
        id=registry.allocate("Observation"),
        track_uid=track.uid,
        obs_ts=timestamp(),
        observation_kind=ObservationKind.DETECTION,
        category=IntelCategory.IMINT,
        spotter_origin=spotter_origin,
        position=first_spot_position,
        confidence=ConfidenceLevel.MEDIUM,
    )

    spot_report = ObservationMessage(
        src=uav_node.uid,
        dst=hq_node.uid,
        ts=timestamp(),
        priority=MessagePriority.PRIORITY,
        seq=3,
        observation=first_spot,
    )

    tracked_position = GlobalPosition(
        lat=first_spot_position.lat + 0.00005,
        lon=first_spot_position.lon + 0.00004,
        alt=first_spot_position.alt,
        alt_frame=first_spot_position.alt_frame,
    )

    tracking_observation = IsrObservation(
        record=record(registry, "mpfc.observation"),
        uid=new_uid(),
        id=registry.allocate("Observation"),
        track_uid=track.uid,
        obs_ts=timestamp(),
        observation_kind=ObservationKind.TRACK,
        category=IntelCategory.IMINT,
        spotter_origin=spotter_origin,
        position=tracked_position,
        confidence=ConfidenceLevel.HIGH,
    )

    track_update = TrackUpdate(
        record=record(registry, "mpfc.tracker"),
        track_uid=track.uid,
        track_state=TrackState.ACTIVE,
        updated_ts=timestamp(),
        confidence=ConfidenceLevel.HIGH,
    )

    track_report = ObservationMessage(
        src=uav_node.uid,
        dst=hq_node.uid,
        ts=timestamp(),
        priority=MessagePriority.PRIORITY,
        seq=4,
        observation=track_update,
    )

    track_observations = [source_observation, first_spot, tracking_observation]

    # -----------------------------------------------------------------------
    # 10. Execution is the occurrence itself
    # -----------------------------------------------------------------------
    execution = Execution(
        record=record(registry, "sigma.execution"),
        uid=new_uid(),
        id=registry.allocate("Execution"),
        assignment_uid=assignment.uid,
        executor_uid=uav_node.uid,
        attempt=1,
        phase=ExecutionPhase.SUCCEEDED,
        progress=1.0,
        started_at=execution_started,
        completed_at=timestamp(),
        external_job_refs=[],
    )

    # -----------------------------------------------------------------------
    # 11. Compact OCCID wire
    # -----------------------------------------------------------------------
    wire_payloads = {
        "initial_track_update": initial_track_update.encode(),
        "start_execution": start_message.encode(),
        "motion_command": move.encode(),
        "uav_telemetry": uav_telemetry.encode(),
        "spot_report": spot_report.encode(),
        "track_report": track_report.encode(),
        "execution": execution.encode(),
    }

    # -----------------------------------------------------------------------
    # Human-readable walkthrough summary
    # -----------------------------------------------------------------------
    print("1. UID and IntID namespaces")
    print(f"   Entity {local_id(uav.id):>2}: UID {uid_str(uav.uid)}")
    print(f"   Track  {local_id(track.id):>2}: UID {uid_str(track.uid)}")
    print(f"   Task   {local_id(task.id):>2}: UID {uid_str(task.uid)}")
    print("   Equal local IDs are valid across different IntID namespaces.")

    print("\n2. Organization")
    print(f"   {task_force.name}: Organization {local_id(task_force.id)} -> Unit {local_id(uas_unit.id)}")
    print(f"   {uas_unit.name}: Entity {local_id(operator.id)}, Entity {local_id(uav.id)}")

    print("\n3. Communications")
    print(f"   HQ Node {local_id(hq_node.id)}:  {uid_str(hq_node.uid)} @ {hq_node.addresses[0].value}")
    print(f"   UAV Node {local_id(uav_node.id)}: {uid_str(uav_node.uid)} @ {uav_node.addresses[0].value}")

    print("\n4. External identity mapping")
    print(
        f"   CoT uid {cot.uid} -> Track {local_id(track.id)} / "
        f"{uid_str(external_identity_map[f'cot.uid:{cot.uid}'])}"
    )
    print(
        f"   MAVLink {mavlink.system_id}:{mavlink.component_id} -> Entity {local_id(uav.id)} / "
        f"{uid_str(external_identity_map[f'mavlink:{mavlink.system_id}:{mavlink.component_id}'])}"
    )
    print(f"   Initial UAV subject: {uid_str(initial_uav_state.subject_uid)}")

    print("\n5. Organizational authority")
    print(f"   Authority {local_id(command_authority.id)}: {uid_str(command_authority.uid)}")
    print(f"   Organization UID: {uid_str(command_authority.organization_uid)}")
    print(f"   Holder UID:       {uid_str(command_authority.holder_uid)}")

    print("\n6. Control graph")
    print(f"   Objective {local_id(objective.id)}:  {uid_str(objective.uid)}")
    print(f"   Task {local_id(task.id)}:       {uid_str(task.uid)}")
    print(f"   Assignment {local_id(assignment.id)}: {uid_str(assignment.uid)}")
    print(f"   Plan {local_id(plan.id)}:       {uid_str(plan.uid)}")
    print(f"   Assigned Entity: {uid_str(assignment.assignee_uid)}")

    print("\n7. Dispatch")
    print(f"   {uid_str(start_message.src)} -> {uid_str(start_message.dst)}")
    print(f"   Execute target: {uid_str(start_message.command.target_uid)}")

    print("\n8. Concrete vehicle action")
    print(f"   Motion target: {uid_str(move.target_uid)}")
    print(
        "   MAVSDK goto:   "
        f"{outbound_goto.latitude_deg:.6f}, {outbound_goto.longitude_deg:.6f}, "
        f"{outbound_goto.absolute_altitude_m:.1f} m MSL"
    )

    print("\n9. MAVLink telemetry -> OCCID telemetry")
    print(
        "   MAVLink ownship: "
        f"{mavlink_moving.latitude_deg:.6f}, {mavlink_moving.longitude_deg:.6f}"
    )
    print(f"   OCCID subject:    {uid_str(uav_state.subject_uid)}")
    print(f"   Telemetry route:  Node {local_id(uav_node.id)} -> Node {local_id(hq_node.id)}")

    print("\n10. Observation and tracking")
    print(f"   Observation {local_id(first_spot.id)}: {first_spot.observation_kind.name}")
    print(f"   Observation {local_id(tracking_observation.id)}: {tracking_observation.observation_kind.name}")
    print(f"   Track {local_id(track.id)}: {track_update.track_state.name}, {track_update.confidence.name}")
    print(f"   Evidence count: {len(track_observations)}")

    print("\n11. Execution occurrence")
    print(f"   Execution {local_id(execution.id)}: {uid_str(execution.uid)}")
    print(f"   Assignment UID: {uid_str(execution.assignment_uid)}")
    print(f"   Phase: {execution.phase.name}, progress {execution.progress:.0%}")

    print("\n12. Compact OCCID wire")
    for name, payload in wire_payloads.items():
        print(f"   {name:20s} {len(payload):4d} bytes  {payload.hex()}")


if __name__ == "__main__":
    main()
