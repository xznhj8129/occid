"""OCCID interoperability example.

This example starts at real protocol boundaries:

- a hardcoded Cursor-on-Target XML event;
- a hardcoded MAVLink v2 GLOBAL_POSITION_INT frame.

Tiny example parsers decode those protocol representations. Existing OCCID
interop helpers then normalize the useful protocol-independent meaning. The
normalized data is used in a small control flow and converted back toward a
vehicle-facing operation.

The parsers in this file are deliberately small teaching examples. They are not
complete CoT or MAVLink implementations.
"""

from __future__ import annotations

import struct
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from interop.cot import CotPointFields, cot_point_to_location_state
from interop.mavsdk import (
    MavsdkGotoFields,
    MavsdkPositionFields,
    goto_command_to_fields,
    position_to_location_state,
)
from occid import (
    AltitudeDatum,
    Assignment,
    AssignmentStatus,
    Authority,
    Entity,
    EntityState,
    EntityType,
    Execution,
    GlobalPosition,
    IdentifierType,
    InformationIntent,
    InertialReferenceFrame,
    IsrObservation,
    MotionCommand,
    MotionOperation,
    Objective,
    ObservationKind,
    ObservationTimeBasis,
    Plan,
    PlanApprovalState,
    RecordMeta,
    StringID,
    TaskInformation,
    VelocityVector,
    decode_model,
)


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

# MAVLink v2 GLOBAL_POSITION_INT.
# sysid=7, compid=1, boot=123.456 s
# lat=45.5017 deg, lon=-73.5673 deg
# altitude=120 m MSL, relative altitude=40 m
# velocity=(5.0, 0.0, -0.5) m/s NED, heading=90 deg
MAVLINK_GLOBAL_POSITION_INT = bytes.fromhex(
    "fd1c00002a0701210000"
    "40e2010028021f1b588526d4c0d40100409c0000f4010000ceff2823"
    "665f"
)

MAVLINK_GLOBAL_POSITION_INT_ID = 33
MAVLINK_GLOBAL_POSITION_INT_CRC_EXTRA = 104
EXAMPLE_RECEIVED_TS = 1787677205.0


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


@dataclass(frozen=True)
class TraceEntry:
    label: str
    model: str
    wire_bytes: int


@dataclass
class ExampleResult:
    cot: ParsedCotEvent
    mavlink: ParsedMavlinkPosition
    records: dict[str, Any] = field(default_factory=dict)
    trace: list[TraceEntry] = field(default_factory=list)
    outbound_goto: MavsdkGotoFields | None = None
    assertions: dict[str, bool] = field(default_factory=dict)


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


def record_meta(record_id: str, ts: float, origin: str) -> RecordMeta:
    return RecordMeta(
        record_id=sid(record_id),
        created_ts=ts,
        updated_ts=ts,
        origin_system=origin,
        provenance=[],
    )


def parse_cot_xml(xml_text: str) -> ParsedCotEvent:
    """Parse only the small CoT subset used by this example."""
    event = ET.fromstring(xml_text)
    if event.tag != "event":
        raise ValueError("expected CoT <event> root")

    point = event.find("point")
    if point is None:
        raise ValueError("CoT event has no <point>")

    contact = event.find("./detail/contact")
    callsign = None if contact is None else contact.get("callsign")
    event_time = event.get("time")
    if event_time is None:
        raise ValueError("CoT event has no time")

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
        callsign=callsign,
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
    return (
        (crc >> 8)
        ^ (tmp << 8)
        ^ (tmp << 3)
        ^ (tmp >> 4)
    ) & 0xFFFF


def _mavlink_crc(data: bytes, crc_extra: int) -> int:
    crc = 0xFFFF
    for byte in data:
        crc = _x25_accumulate(byte, crc)
    return _x25_accumulate(crc_extra, crc)


def parse_mavlink_global_position(frame: bytes) -> ParsedMavlinkPosition:
    """Parse one MAVLink v2 GLOBAL_POSITION_INT frame for the example."""
    if len(frame) < 12 or frame[0] != 0xFD:
        raise ValueError("expected MAVLink v2 frame")

    payload_len = frame[1]
    incompat_flags = frame[2]
    if incompat_flags & 0x01:
        raise ValueError("signed MAVLink frames are outside this tiny example parser")

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


def run_example() -> ExampleResult:
    cot = parse_cot_xml(COT_XML)
    mavlink = parse_mavlink_global_position(MAVLINK_GLOBAL_POSITION_INT)
    result = ExampleResult(cot=cot, mavlink=mavlink)

    def cross(label: str, value):
        payload = value.encode()
        decoded = decode_model(payload)
        if type(decoded) is not type(value) or decoded != value:
            raise AssertionError(f"{label}: OCCID encode/decode round trip changed value")
        result.trace.append(
            TraceEntry(
                label=label,
                model=type(value).__name__,
                wire_bytes=len(payload),
            )
        )
        return decoded

    operator_id = sid("entity.operator.1")
    uav_id = sid("entity.uav.7")
    contact_track_id = sid(f"track.cot.{cot.uid}")

    # CoT is parsed as CoT first, then normalized into OCCID observation semantics.
    cot_location = cot_point_to_location_state(cot.point)
    if cot_location.position is None:
        raise AssertionError("CoT point conversion did not produce a global position")

    contact_observation = cross(
        "cot.contact.observation",
        IsrObservation(
            record=record_meta(
                "record.observation.contact-route6-1",
                cot.event_ts,
                "example.cot",
            ),
            obs_id=sid("observation.contact-route6-1"),
            track_id=contact_track_id,
            obs_ts=cot.event_ts,
            observation_kind=ObservationKind.TRACK,
            position=cot_location.position,
            uncertainty=cot_location.uncertainty,
        ),
    )

    # The vehicle definition is stable identity. MAVLink supplies changing state.
    uav = cross(
        "uav.definition",
        Entity(
            record=record_meta("record.entity.uav.7", EXAMPLE_RECEIVED_TS, "example"),
            entity_id=uav_id,
            node_ids=[],
            name="FROG-7",
            entity_type=EntityType.MACHINE,
            alt_ids=[],
            tags=["UAV"],
            metadata={},
            relations=[],
        ),
    )

    mavlink_location = position_to_location_state(
        MavsdkPositionFields(
            latitude_deg=mavlink.latitude_deg,
            longitude_deg=mavlink.longitude_deg,
            absolute_altitude_m=mavlink.absolute_altitude_m,
            relative_altitude_m=mavlink.relative_altitude_m,
        )
    )
    uav_state = cross(
        "mavlink.uav.state",
        EntityState(
            record=record_meta(
                "record.state.uav.7.1",
                EXAMPLE_RECEIVED_TS,
                "example.mavlink",
            ),
            subject_id=uav.entity_id,
            timestamp=EXAMPLE_RECEIVED_TS,
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
            received_ts=EXAMPLE_RECEIVED_TS,
        ),
    )

    # The operational layer can now refer to the contact and the vehicle without
    # carrying CoT XML fields or MAVLink packet fields through the control model.
    objective = cross(
        "objective.created",
        Objective(
            record=record_meta("record.objective.inspect.1", EXAMPLE_RECEIVED_TS, "example"),
            objective_id=sid("objective.inspect.contact-route6-1"),
            name="Inspect reported contact",
            intent="Determine the current status of the reported Route 6 contact.",
            desired_state="The reported contact has been inspected and updated.",
            success_criteria=[],
            target_refs=[contact_track_id],
            constraints=[],
            owner_id=operator_id,
        ),
    )

    task = cross(
        "task.created",
        TaskInformation(
            record=record_meta("record.task.inspect.1", EXAMPLE_RECEIVED_TS, "example"),
            task_id=sid("task.inspect.contact-route6-1"),
            instruction="Inspect the reported contact and update its status.",
            intent=InformationIntent.OBSERVE,
            target_refs=[contact_track_id],
            location_refs=[],
            objective_id=objective.objective_id,
            constraints=[],
        ),
    )

    authority = cross(
        "authority.created",
        Authority(
            record=record_meta("record.authority.uav7.1", EXAMPLE_RECEIVED_TS, "example"),
            authority_id=sid("authority.operator.uav7"),
            holder_id=operator_id,
            granted_by=operator_id,
            scope_refs=[uav.entity_id, task.task_id],
            constraints=[],
        ),
    )

    assignment = cross(
        "assignment.created",
        Assignment(
            record=record_meta("record.assignment.inspect.1", EXAMPLE_RECEIVED_TS, "example"),
            assignment_id=sid("assignment.inspect.contact-route6-1.uav7"),
            task_id=task.task_id,
            assignee_id=uav.entity_id,
            authority_id=authority.authority_id,
            assigned_by=operator_id,
            assigned_at=EXAMPLE_RECEIVED_TS,
            status=AssignmentStatus.ASSIGNED,
            constraints=[],
        ),
    )

    plan = cross(
        "plan.created",
        Plan(
            record=record_meta("record.plan.inspect.1", EXAMPLE_RECEIVED_TS, "example"),
            plan_id=sid("plan.inspect.contact-route6-1"),
            name="Inspect Route 6 contact",
            objective_ids=[objective.objective_id],
            task_ids=[task.task_id],
            actor_ids=[uav.entity_id],
            resource_ids=[],
            assignments=[assignment.assignment_id],
            steps=[],
            routes=[],
            constraints=[],
            contingencies=[],
            approval_state=PlanApprovalState.APPROVED,
        ),
    )

    execution = cross(
        "execution.created",
        Execution(
            record=record_meta("record.execution.inspect.1", EXAMPLE_RECEIVED_TS, "example"),
            execution_id=sid("execution.inspect.contact-route6-1.1"),
            assignment_id=assignment.assignment_id,
            executor_id=uav.entity_id,
            external_job_refs=[],
        ),
    )

    # The CoT HAE altitude is not copied into a vehicle command. The planner
    # selects a 60 m relative flight altitude for the inspection operation.
    move = cross(
        "executor.motion.command",
        MotionCommand(
            target_ref=uav.entity_id,
            constraints=[],
            operation=MotionOperation.MOVE_TO,
            destination=GlobalPosition(
                lat=contact_observation.position.lat,
                lon=contact_observation.position.lon,
                alt=60.0,
                alt_frame=AltitudeDatum.RELATIVE,
            ),
        ),
    )

    result.outbound_goto = goto_command_to_fields(
        move,
        current_absolute_altitude_m=mavlink.absolute_altitude_m,
        current_relative_altitude_m=mavlink.relative_altitude_m,
    )

    result.records.update(
        contact_observation=contact_observation,
        uav=uav,
        uav_state=uav_state,
        objective=objective,
        task=task,
        authority=authority,
        assignment=assignment,
        plan=plan,
        execution=execution,
        move=move,
    )

    result.assertions.update(
        cot_became_observation=(
            contact_observation.observation_kind == ObservationKind.TRACK
            and contact_observation.position.lat == cot.point.lat_deg
            and contact_observation.position.alt_frame == AltitudeDatum.WGS84_ELLIPSOID
        ),
        mavlink_became_entity_state=(
            uav_state.subject_id == uav.entity_id
            and uav_state.position is not None
            and uav_state.position.position is not None
            and uav_state.position.position.alt_frame == AltitudeDatum.SEA_LEVEL
        ),
        task_targets_cot_track=contact_track_id in task.target_refs,
        assignment_targets_uav=assignment.assignee_id == uav.entity_id,
        execution_references_assignment=execution.assignment_id == assignment.assignment_id,
        plan_correlates_control=(
            objective.objective_id in plan.objective_ids
            and task.task_id in plan.task_ids
            and assignment.assignment_id in plan.assignments
        ),
        outbound_uses_contact_horizontal_position=(
            result.outbound_goto.latitude_deg == contact_observation.position.lat
            and result.outbound_goto.longitude_deg == contact_observation.position.lon
        ),
        outbound_uses_planned_relative_altitude=(
            move.destination.alt_frame == AltitudeDatum.RELATIVE
            and move.destination.alt == 60.0
            and result.outbound_goto.absolute_altitude_m == 140.0
        ),
    )
    return result


def main() -> None:
    result = run_example()

    print("1. Raw inputs")
    print(f"   CoT: {result.cot.uid} / {result.cot.callsign}")
    print(
        "   MAVLink: "
        f"sys={result.mavlink.system_id} comp={result.mavlink.component_id} "
        f"position=({result.mavlink.latitude_deg:.6f}, "
        f"{result.mavlink.longitude_deg:.6f})"
    )

    observation = result.records["contact_observation"]
    uav_state = result.records["uav_state"]
    print("\n2. OCCID semantic model")
    print(
        "   CoT -> IsrObservation: "
        f"track={observation.track_id.value} "
        f"position=({observation.position.lat:.6f}, {observation.position.lon:.6f})"
    )
    print(
        "   MAVLink -> EntityState: "
        f"subject={uav_state.subject_id.value} "
        f"position=({uav_state.position.position.lat:.6f}, "
        f"{uav_state.position.position.lon:.6f})"
    )

    task = result.records["task"]
    assignment = result.records["assignment"]
    execution = result.records["execution"]
    print("\n3. Shared operational flow")
    print(f"   Task: {task.task_id.value}")
    print(f"   Assignment: {assignment.assignment_id.value} -> {assignment.assignee_id.value}")
    print(f"   Execution: {execution.execution_id.value}")

    goto = result.outbound_goto
    print("\n4. Vehicle-facing operation")
    print(
        "   OCCID MotionCommand -> MAVSDK goto_location: "
        f"lat={goto.latitude_deg:.6f} lon={goto.longitude_deg:.6f} "
        f"absolute_altitude_m={goto.absolute_altitude_m:.1f}"
    )

    print("\n5. Checks")
    for name, passed in result.assertions.items():
        print(f"   {name}: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
