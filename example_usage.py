"""OCCID end-to-end field manual.

This is not a normal programming example or test fixture. It is the readable,
executable answer to "how is OCCID supposed to work?": architecture expressed
as code in one small operational scenario.

Identity rule:

    UID = UUIDv4, globally unique, immutable machine identity
    ID  = sequential integer scoped to the semantic OCCID class

Entity 38, Track 38, and Task 38 are unrelated class-local IDs. Their UIDs are
globally unambiguous. Durable cross-object references use UIDs, never IDs.

The scenario walks through identity provisioning, organizations, relationships,
communications, external protocol mapping, authority, tasking, execution,
MAVLink telemetry, OCCID reporting, observation, tracking, and compact wire.
"""

from __future__ import annotations

import struct
import time
import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone

from interop.cot import CotPointFields, cot_point_to_location_state
from interop.mavsdk import (
    MavsdkPositionFields,
    goto_command_to_fields,
    position_to_location_state,
)
from occid import (
    AddressKind,
    AltitudeDatum,
    Assignment,
    AssignmentStatus,
    CapabilityRole,
    CommandMessage,
    ConfidenceLevel,
    ControlLease,
    ControlLevel,
    DeliveryReceipt,
    DeliveryState,
    DirectedRelationship,
    Entity,
    EntityState,
    EntityType,
    Execution,
    ExecutionAcceptance,
    ExecutionCommand,
    ExecutionOperation,
    ExecutionPhase,
    ExecutionStatusReport,
    GlobalPosition,
    Group,
    IdentityBootstrap,
    InformationIntent,
    InertialReferenceFrame,
    IntelCategory,
    IsrObservation,
    Link,
    LinkDataType,
    LinkDirection,
    LinkType,
    MessagePriority,
    MessageTarget,
    MotionCommand,
    MotionOperation,
    NetworkAddress,
    Node,
    Objective,
    ObservationKind,
    ObservationMessage,
    ObservationTimeBasis,
    OrgTopology,
    OrgType,
    Plan,
    PlanApprovalState,
    PlanStep,
    RecordMeta,
    RelationshipKind,
    SpotterOrigin,
    TaskDelta,
    TaskInformation,
    TaskPhase,
    TaskPriority,
    TelemetryMessage,
    Timestamp,
    Track,
    TrackState,
    TrackUpdate,
    UID,
    UAVTelemetryMessage,
    Unit,
    VelocityVector,
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
# UID globally, ID inside a semantic class
# ---------------------------------------------------------------------------


def new_uid() -> UID:
    return UID(bytes=uuid.uuid4().bytes)


@dataclass
class ClassIDRegistry:
    """Small human IDs have one independent sequence per semantic class."""

    next_id: dict[str, int] = field(default_factory=dict)

    def allocate(self, object_class: str) -> int:
        value = self.next_id.get(object_class, 1)
        self.next_id[object_class] = value + 1
        return value


# ---------------------------------------------------------------------------
# Small mechanics used by the walkthrough
# ---------------------------------------------------------------------------


def record(registry: ClassIDRegistry, origin: str) -> RecordMeta:
    now = time.time()
    return RecordMeta(
        uid=new_uid(),
        id=registry.allocate("Record"),
        created_ts=now,
        updated_ts=now,
        origin_system=origin,
        provenance=[],
    )


def message_timestamp() -> Timestamp:
    now = datetime.fromtimestamp(time.time(), timezone.utc)
    return Timestamp(
        seconds=now.second + now.microsecond / 1_000_000.0,
        minutes=now.minute,
        hours=now.hour,
        day=now.day,
        month=now.month,
        year=now.year,
        tz=0,
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
    # Independent class-local ID spaces. The deliberate overlap makes the rule
    # impossible to miss: Entity 38, Track 38, and Task 38 are all valid.
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

    # -----------------------------------------------------------------------
    # 1. Identity provisioning
    # -----------------------------------------------------------------------
    # Organizations are real OCCID objects. A managed Node then receives one
    # real OCCID IdentityBootstrap binding its Node, Entity, and Organization.
    task_force = Group(
        record=record(registry, "provisioning"),
        uid=new_uid(),
        id=registry.allocate("Organization"),
        name="Task Force Frog",
        unit_code="TFF",
        callsign="FROG-HQ",
        org_type=OrgType.GOVT,
        topology=OrgTopology.HIERARCHICAL,
    )

    uas_unit = Unit(
        record=record(registry, "provisioning"),
        uid=new_uid(),
        id=registry.allocate("Organization"),
        name="UAS Section",
        unit_code="UAS",
        callsign="FROG-UAS",
        org_type=OrgType.GOVT,
        topology=OrgTopology.HIERARCHICAL,
    )

    hq_identity = IdentityBootstrap(
        node_uid=new_uid(),
        node_id=registry.allocate("Node"),
        entity_uid=new_uid(),
        entity_id=registry.allocate("Entity"),
        organization_uid=uas_unit.uid,
        organization_id=uas_unit.id,
    )

    uav_identity = IdentityBootstrap(
        node_uid=new_uid(),
        node_id=registry.allocate("Node"),
        entity_uid=new_uid(),
        entity_id=registry.allocate("Entity"),
        organization_uid=uas_unit.uid,
        organization_id=uas_unit.id,
    )

    operator = Entity(
        record=record(registry, "provisioning"),
        uid=hq_identity.entity_uid,
        id=hq_identity.entity_id,
        node_uids=[hq_identity.node_uid],
        name="Mission Operator",
        callsign="FROG-OPS",
        entity_type=EntityType.PERSON,
        tags=["OPERATOR"],
        metadata={},
        relations=[],
    )

    uav = Entity(
        record=record(registry, "provisioning"),
        uid=uav_identity.entity_uid,
        id=uav_identity.entity_id,
        node_uids=[uav_identity.node_uid],
        name="Frog UAV 38",
        callsign="FROG-38",
        entity_type=EntityType.MACHINE,
        tags=["UAV", "ISR"],
        metadata={},
        relations=[],
    )

    # -----------------------------------------------------------------------
    # 2. Nodes and communications
    # -----------------------------------------------------------------------
    hq_address = NetworkAddress(kind=AddressKind.IPV4, value="10.42.0.1", port=7447)
    uav_address = NetworkAddress(kind=AddressKind.IPV4, value="10.42.0.38", port=7447)

    hq_node = Node(
        uid=hq_identity.node_uid,
        id=hq_identity.node_id,
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
        uid=uav_identity.node_uid,
        id=uav_identity.node_id,
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
    # 3. Organization and chain of command
    # -----------------------------------------------------------------------
    # Structural relationships are typed ontology objects. They are not string
    # labels and they are not command authority. ControlLease below answers the
    # separate question "who may actually command this asset right now?"
    relationships = [
        DirectedRelationship(
            subject_uid=uas_unit.uid,
            object_uid=task_force.uid,
            relation=RelationshipKind.MEMBER_OF,
            since_ts=time.time(),
            source="provisioning",
        ),
        DirectedRelationship(
            subject_uid=task_force.uid,
            object_uid=uas_unit.uid,
            relation=RelationshipKind.COMMANDS,
            since_ts=time.time(),
            source="provisioning",
        ),
        DirectedRelationship(
            subject_uid=operator.uid,
            object_uid=uas_unit.uid,
            relation=RelationshipKind.MEMBER_OF,
            since_ts=time.time(),
            source="provisioning",
        ),
        DirectedRelationship(
            subject_uid=uav.uid,
            object_uid=uas_unit.uid,
            relation=RelationshipKind.MEMBER_OF,
            since_ts=time.time(),
            source="provisioning",
        ),
        DirectedRelationship(
            subject_uid=operator.uid,
            object_uid=uav.uid,
            relation=RelationshipKind.OPERATES,
            since_ts=time.time(),
            source="provisioning",
        ),
    ]

    # -----------------------------------------------------------------------
    # 4. External protocols become OCCID observations/state
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
        obs_ts=cot.event_ts,
        observation_kind=ObservationKind.TRACK,
        position=reported_position,
        uncertainty=cot_location.uncertainty,
        confidence=ConfidenceLevel.LOW,
    )

    initial_track_update = TrackUpdate(
        record=record(registry, "adapter.cot"),
        track_uid=track.uid,
        track_state=TrackState.NEW,
        updated_ts=time.time(),
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
        source_observation_ts=mavlink.time_boot_ms / 1000.0,
        source_time_basis=ObservationTimeBasis.BOOT,
        received_ts=time.time(),
    )

    external_identity_map = {
        f"cot.uid:{cot.uid}": track.uid,
        f"mavlink:{mavlink.system_id}:{mavlink.component_id}": uav.uid,
    }

    # -----------------------------------------------------------------------
    # 5. Authority
    # -----------------------------------------------------------------------
    control_lease = ControlLease(
        record=record(registry, "sigma.authority"),
        uid=new_uid(),
        id=registry.allocate("Authority"),
        holder_uid=operator.uid,
        granted_by_uid=task_force.uid,
        scope_uids=[uav.uid],
        constraints=[],
        asset_uid=uav.uid,
        control_level=ControlLevel.FULL,
        lease_start=time.time(),
        lease_end=time.time() + 900.0,
        lease_rev=1,
    )

    # -----------------------------------------------------------------------
    # 6. Objective -> Task -> Assignment -> Plan -> Execution
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
    )

    # Assignment refers to Plan, and Plan refers to Assignment, so allocate the
    # Plan identity before constructing either object. No wrapper object exists.
    plan_uid = new_uid()
    plan_id = registry.allocate("Plan")

    assignment = Assignment(
        record=record(registry, "sigma.control"),
        uid=new_uid(),
        id=registry.allocate("Assignment"),
        task_uid=task.uid,
        assignee_uid=uav.uid,
        plan_uid=plan_uid,
        authority_uid=control_lease.uid,
        assigned_by_uid=operator.uid,
        assigned_at=time.time(),
        status=AssignmentStatus.ASSIGNED,
        constraints=[],
    )

    plan = Plan(
        record=record(registry, "sigma.control"),
        uid=plan_uid,
        id=plan_id,
        name="Inspect Route 6 contact",
        objective_uids=[objective.uid],
        task_uids=[task.uid],
        actor_uids=[uav.uid],
        resource_uids=[],
        assignment_uids=[assignment.uid],
        steps=[
            PlanStep(
                id=1,
                task_uid=task.uid,
                actor_uids=[uav.uid],
                depends_on=[],
                sequence=1,
            )
        ],
        routes=[],
        constraints=[],
        contingencies=[],
        approval_state=PlanApprovalState.APPROVED,
    )

    execution = Execution(
        record=record(registry, "sigma.execution"),
        uid=new_uid(),
        id=registry.allocate("Execution"),
        assignment_uid=assignment.uid,
        executor_uid=uav_node.uid,
        attempt=1,
        phase=ExecutionPhase.QUEUED,
        external_job_refs=[],
    )

    # -----------------------------------------------------------------------
    # 7. Dispatch over communications, then executor acceptance
    # -----------------------------------------------------------------------
    dispatch_ref = f"task-{task.id}-attempt-{execution.attempt}"

    start_execution = ExecutionCommand(
        target_uid=execution.uid,
        constraints=[],
        operation=ExecutionOperation.EXECUTE,
        dispatch_ref=dispatch_ref,
    )

    start_message = CommandMessage(
        src=MessageTarget(target_uid=hq_node.uid),
        dst=MessageTarget(target_uid=uav_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.IMMEDIATE,
        seq=1,
        command=start_execution,
    )

    delivery_receipt = DeliveryReceipt(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.ROUTINE,
        seq=2,
        seq_reply=1,
        response_to=dispatch_ref,
        node_uid=uav_node.uid,
        delivery_state=DeliveryState.RECEIVED,
        seen_ts=time.time(),
    )

    acceptance = ExecutionAcceptance(
        execution_uid=execution.uid,
        dispatch_ref=dispatch_ref,
        executor_uid=uav_node.uid,
        accepted=True,
        reported_at=time.time(),
    )

    acceptance_report = TelemetryMessage(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.ROUTINE,
        seq=3,
        state=acceptance,
    )

    # -----------------------------------------------------------------------
    # 8. Concrete vehicle action, translated only at the edge to MAVSDK
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
    # 9. MAVLink telemetry -> OCCID telemetry
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
        source_observation_ts=mavlink_moving.time_boot_ms / 1000.0,
        source_time_basis=ObservationTimeBasis.BOOT,
        received_ts=time.time(),
    )

    uav_telemetry = UAVTelemetryMessage(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.ROUTINE,
        seq=4,
        state=uav_state,
    )

    # -----------------------------------------------------------------------
    # 10. OCCID-native task/execution reporting
    # -----------------------------------------------------------------------
    task_delta = TaskDelta(
        record=record(registry, "mpfc.execution"),
        task_uid=task.uid,
        task_rev=1,
        phase=TaskPhase.RUNNING,
        progress=0.40,
        owner_uid=uav.uid,
        updated_ts=time.time(),
    )

    status_report = ExecutionStatusReport(
        execution_uid=execution.uid,
        dispatch_ref=dispatch_ref,
        executor_uid=uav_node.uid,
        found=True,
        phase=ExecutionPhase.RUNNING,
        progress=0.40,
        task_delta=task_delta,
        entity_state=uav_state,
        reported_at=time.time(),
    )

    execution_report = TelemetryMessage(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.ROUTINE,
        seq=5,
        state=status_report,
    )

    # -----------------------------------------------------------------------
    # 11. Spotted: one new piece of evidence
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
        obs_ts=time.time(),
        observation_kind=ObservationKind.DETECTION,
        category=IntelCategory.IMINT,
        spotter_origin=spotter_origin,
        position=first_spot_position,
        confidence=ConfidenceLevel.MEDIUM,
    )

    spot_report = ObservationMessage(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.PRIORITY,
        seq=6,
        observation=first_spot,
    )

    # -----------------------------------------------------------------------
    # 12. Tracking: later evidence correlates to the same Track 38
    # -----------------------------------------------------------------------
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
        obs_ts=time.time(),
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
        updated_ts=time.time(),
        confidence=ConfidenceLevel.HIGH,
    )

    track_report = ObservationMessage(
        src=MessageTarget(target_uid=uav_node.uid),
        dst=MessageTarget(target_uid=hq_node.uid),
        ts=message_timestamp(),
        priority=MessagePriority.PRIORITY,
        seq=7,
        observation=track_update,
    )

    # The maintained contact picture is a projection over evidence and current
    # track state, not a second giant ontology record containing copies of both.
    track_observations = [source_observation, first_spot, tracking_observation]

    # -----------------------------------------------------------------------
    # 13. Compact OCCID wire
    # -----------------------------------------------------------------------
    wire_payloads = {
        "initial_track_update": initial_track_update.encode(),
        "start_execution": start_message.encode(),
        "delivery_receipt": delivery_receipt.encode(),
        "acceptance_report": acceptance_report.encode(),
        "motion_command": move.encode(),
        "uav_telemetry": uav_telemetry.encode(),
        "execution_report": execution_report.encode(),
        "spot_report": spot_report.encode(),
        "track_report": track_report.encode(),
    }

    # -----------------------------------------------------------------------
    # Human-readable walkthrough summary
    # -----------------------------------------------------------------------
    print("1. UID and class-local ID")
    print(f"   Entity {uav.id:>2}: UID {uav.uid}")
    print(f"   Track  {track.id:>2}: UID {track.uid}")
    print(f"   Task   {task.id:>2}: UID {task.uid}")
    print("   Same integer ID is valid across different classes; UIDs never collide.")

    print("\n2. Identity provisioning")
    print(f"   Organization {task_force.id}: {task_force.uid}  {task_force.name}")
    print(f"   Organization {uas_unit.id}: {uas_unit.uid}  {uas_unit.name}")
    print(
        f"   HQ bootstrap:  Node {hq_identity.node_id} -> "
        f"Entity {hq_identity.entity_id} -> Organization {hq_identity.organization_id}"
    )
    print(
        f"   UAV bootstrap: Node {uav_identity.node_id} -> "
        f"Entity {uav_identity.entity_id} -> Organization {uav_identity.organization_id}"
    )
    print(f"   Entity {operator.id}:       {operator.uid}  {operator.callsign}")
    print(f"   Entity {uav.id}:       {uav.uid}  {uav.callsign}")
    print(f"   Node {hq_node.id}:         {hq_node.uid}")
    print(f"   Node {uav_node.id}:         {uav_node.uid}")

    print("\n3. Organization and chain of command")
    for relationship in relationships:
        print(
            f"   {relationship.subject_uid} "
            f"--{relationship.relation.name.lower()}--> "
            f"{relationship.object_uid}"
        )

    print("\n4. Communications")
    print(f"   HQ Node {hq_node.id}:          {hq_node.uid} @ {hq_node.addresses[0].value}")
    print(f"   UAV Node {uav_node.id}:         {uav_node.uid} @ {uav_node.addresses[0].value}")
    print(
        "   Message route:        "
        f"{start_message.src.target_uid} -> {start_message.dst.target_uid}"
    )

    print("\n5. External identity mapping")
    print(
        f"   CoT uid {cot.uid} -> Track {track.id} / "
        f"{external_identity_map[f'cot.uid:{cot.uid}']}"
    )
    print(f"   Source callsign:       {cot.callsign}")
    print(
        f"   MAVLink {mavlink.system_id}:{mavlink.component_id} -> "
        f"Entity {uav.id} / "
        f"{external_identity_map[f'mavlink:{mavlink.system_id}:{mavlink.component_id}']}"
    )

    print("\n6. Initial operational picture")
    print(f"   Track {track.id}: state {initial_track_update.track_state.name}")
    print(
        "   Reported position:    "
        f"{source_observation.position.lat:.6f}, {source_observation.position.lon:.6f}"
    )
    print(f"   Initial UAV subject:   {initial_uav_state.subject_uid}")

    print("\n7. Authority")
    print(f"   Authority {control_lease.id}:         {control_lease.uid}")
    print(f"   Holder UID:           {control_lease.holder_uid}")
    print(f"   Granted-by UID:       {control_lease.granted_by_uid}")
    print(f"   Asset UID:            {control_lease.asset_uid}")
    print(f"   Control level:        {control_lease.control_level.name}")

    print("\n8. Mission control graph")
    print(f"   Objective {objective.id}:        {objective.uid}")
    print(f"   Task {task.id}:             {task.uid}")
    print(f"   Assignment {assignment.id}:       {assignment.uid}")
    print(f"   Plan {plan.id}:             {plan.uid}")
    print(f"   Assigned Entity UID:   {assignment.assignee_uid}")
    print(f"   Executor Node UID:     {execution.executor_uid}")
    print(f"   Execution {execution.id}:        {execution.uid}")

    print("\n9. Dispatch and executor acceptance")
    print(f"   Command target UID:    {start_message.command.target_uid}")
    print(f"   Dispatch ref:          {start_message.command.dispatch_ref}")
    print(f"   Delivery state:        {delivery_receipt.delivery_state.name}")
    print(f"   Executor accepted:     {acceptance.accepted}")

    print("\n10. Concrete vehicle action")
    print(f"   Motion target UID:     {move.target_uid}")
    print(
        "   MAVSDK goto:          "
        f"{outbound_goto.latitude_deg:.6f}, {outbound_goto.longitude_deg:.6f}, "
        f"{outbound_goto.absolute_altitude_m:.1f} m MSL"
    )

    print("\n11. MAVLink telemetry -> OCCID telemetry")
    print(
        "   MAVLink ownship:      "
        f"{mavlink_moving.latitude_deg:.6f}, {mavlink_moving.longitude_deg:.6f}"
    )
    print(f"   OCCID subject UID:     {uav_state.subject_uid}")
    print(f"   OCCID telemetry route: Node {uav_node.id} -> Node {hq_node.id}")

    print("\n12. OCCID execution/task report")
    print(f"   Task {task.id}:             {task_delta.phase.name} {task_delta.progress:.0%}")
    print(f"   Execution {execution.id}:        {status_report.phase.name} {status_report.progress:.0%}")

    print("\n13. Spotted")
    print(f"   Observation {first_spot.id}:     {first_spot.observation_kind.name}")
    print(f"   Correlates to Track:  {track.id} / {first_spot.track_uid}")
    print(f"   Confidence:           {first_spot.confidence.name}")

    print("\n14. Tracking")
    print(
        f"   Observation {tracking_observation.id}:     "
        f"{tracking_observation.observation_kind.name}"
    )
    print(f"   Same Track UID:       {tracking_observation.track_uid}")
    print(f"   Confidence:           {tracking_observation.confidence.name}")

    print("\n15. Maintained contact information")
    print(f"   Track {track.id}:             {track.uid}")
    print(f"   State:                {track_update.track_state.name}")
    print(f"   Confidence:           {track_update.confidence.name}")
    print(f"   Observations:         {len(track_observations)}")
    print(
        "   Current position:     "
        f"{tracking_observation.position.lat:.6f}, "
        f"{tracking_observation.position.lon:.6f}"
    )

    print("\n16. Compact OCCID wire")
    for name, payload in wire_payloads.items():
        print(f"   {name:20s} {len(payload):4d} bytes  {payload.hex()}")


if __name__ == "__main__":
    main()
