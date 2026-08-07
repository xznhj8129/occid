#!/usr/bin/env python3
"""Deterministic OCCID-only closed-loop command and control demonstration.

The scenario models one complete Observe-Orient-Decide-Act-Assess cycle:

1. A planning/decision agent receives vehicle identity, capability, position, and
   flight telemetry as OCCID records.
2. A deterministic decision rule creates an Objective, ISR Task, approved Plan,
   Assignment, Execution, and command message.
3. A simulated autonomous executor accepts the assignment, reports execution
   and task progress, emits updated telemetry, and returns an ISR observation.
4. The decision agent assesses the result and closes the objective.

Every application boundary performs a real OCCID encode/decode round trip. No
Sigma, HiveLink, MPFC, flight controller, message broker, simulator, or network
software is required. The only non-standard-library dependency is OCCID itself.

Run from the repository root:
    python end_to_end_ooda.py
    python end_to_end_ooda.py --json
    python end_to_end_ooda.py --output /tmp/occid-ooda-trace.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

from schema import (
    Agent,
    AltitudeDatum,
    ApplyPlanCommand,
    Assignment,
    AssignmentStatus,
    CapabilityRole,
    CommandMessage,
    Entity,
    EntityOperationalState,
    EntityState,
    EntityType,
    Execution,
    ExecutionPhase,
    StandardFlightMode,
    FlightPhase,
    GeoArea,
    GeoPath,
    GlobalPosition,
    IdentifierType,
    IntelCategory,
    IsrObservation,
    IsrResult,
    IsrTask,
    LocationState,
    LocationUncertainty,
    MessagePriority,
    MessageTarget,
    Node,
    Objective,
    ObservationKind,
    ObservationMessage,
    OCCIDModel,
    OCCID_MODEL_ID_BY_CLASS,
    Plan,
    PlanApprovalState,
    PlanStep,
    RecordMeta,
    SpotterOrigin,
    StringID,
    SuccessCriterion,
    TaskDelta,
    TaskISR,
    TaskPhase,
    TaskStatus,
    TelemetryMessage,
    TelemetryState,
    Timestamp,
    TrackState,
    TrackUpdate,
    UAVTelemetryMessage,
    VelocityVector,
)

ModelT = TypeVar("ModelT", bound=OCCIDModel)

BASE_LAT = 36.530440
BASE_LON = -83.216383


def sid(value: str, id_type: IdentifierType = IdentifierType.DB_ID) -> StringID:
    return StringID(id_type=id_type, value=value)


def record(record_id: str, timestamp: float, revision: int = 0) -> RecordMeta:
    return RecordMeta(
        record_id=sid(record_id),
        revision=revision,
        created_ts=timestamp,
        updated_ts=timestamp,
        origin_system="occid.demo.ooda",
        provenance=["deterministic-occid-only-scenario"],
    )


def timestamp(second: int) -> Timestamp:
    return Timestamp(
        seconds=float(second),
        minutes=0,
        hours=12,
        day=6,
        month=8,
        year=2026,
        tz=-4,
    )


def target(target_id: StringID) -> MessageTarget:
    return MessageTarget(target_id=target_id)


@dataclass(frozen=True)
class TraceEntry:
    index: int
    phase: str
    source: str
    destination: str
    purpose: str
    model_name: str
    model_id: int
    wire_bytes: int
    payload: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "phase": self.phase,
            "source": self.source,
            "destination": self.destination,
            "purpose": self.purpose,
            "model_name": self.model_name,
            "model_id": self.model_id,
            "wire_bytes": self.wire_bytes,
            "payload": self.payload,
        }


@dataclass
class ScenarioResult:
    trace: list[TraceEntry]
    records: dict[str, OCCIDModel]
    assertions: dict[str, bool]

    def as_dict(self) -> dict[str, Any]:
        return {
            "scenario": "occid_closed_loop_ooda",
            "software_dependencies": ["python-standard-library", "occid"],
            "trace": [entry.as_dict() for entry in self.trace],
            "assertions": self.assertions,
            "summary": {
                "trace_entries": len(self.trace),
                "model_types": sorted({entry.model_name for entry in self.trace}),
                "total_wire_bytes": sum(entry.wire_bytes for entry in self.trace),
                "objective_status": self.records["objective_complete"].status.name,
                "assignment_status": self.records["assignment_complete"].status.name,
                "execution_phase": self.records["execution_complete"].phase.name,
                "task_phase": self.records["task_complete"].phase.name,
                "observations": len(self.records["isr_result"].observations),
                "track_updates": len(self.records["isr_result"].track_updates),
            },
        }


class SemanticBoundary:
    """Application boundary that transports only OCCID-encoded bytes.

    It deliberately contains no routing, retry, broker, or radio behavior. Its
    job is to prove that the typed operational record survives serialization
    and reconstruction at a process/system boundary.
    """

    def __init__(self) -> None:
        self.trace: list[TraceEntry] = []

    def transfer(
        self,
        model: ModelT,
        *,
        phase: str,
        source: str,
        destination: str,
        purpose: str,
    ) -> ModelT:
        encoded = model.encode()
        decoded = type(model).decode(encoded)
        if decoded != model:
            raise AssertionError(f"OCCID round trip changed {type(model).__name__}")

        self.trace.append(
            TraceEntry(
                index=len(self.trace) + 1,
                phase=phase,
                source=source,
                destination=destination,
                purpose=purpose,
                model_name=type(decoded).__name__,
                model_id=OCCID_MODEL_ID_BY_CLASS[type(decoded)],
                wire_bytes=len(encoded),
                payload=decoded.model_dump(mode="json"),
            )
        )
        return decoded


class DeterministicDecisionAgent:
    """Minimal AIC2/OODA stand-in that reasons only over OCCID records."""

    def select_executor(
        self,
        entity: Entity,
        node: Node,
        entity_state: EntityState,
        telemetry: TelemetryState,
    ) -> Entity:
        capable = (
            node.entity_id == entity.entity_id
            and CapabilityRole.SENSOR in node.roles
            and CapabilityRole.EFFECTOR in node.roles
        )
        ready = entity_state.operational_status == EntityOperationalState.READY
        sufficient_energy = telemetry.battery_pct is not None and telemetry.battery_pct >= 50.0
        valid_position = entity_state.position is not None and entity_state.position.position is not None
        if not (capable and ready and sufficient_energy and valid_position):
            raise RuntimeError("no suitable ISR executor")
        return entity

    def decide(
        self,
        controller: Agent,
        executor: Entity,
        area: GeoArea,
        route: GeoPath,
    ) -> dict[str, OCCIDModel]:
        objective_id = sid("objective.recon-sector-alpha")
        task_id = sid("task.survey-sector-alpha")
        plan_id = sid("plan.survey-sector-alpha")
        assignment_id = sid("assignment.survey-sector-alpha.scout-1")
        execution_id = sid("execution.survey-sector-alpha.scout-1.attempt-1")

        objective = Objective(
            record=record("record.objective.recon-sector-alpha.r0", 2.0),
            objective_id=objective_id,
            name="Establish current activity in Sector Alpha",
            intent=(
                "Search the designated area and return a geolocated observation "
                "sufficient to establish whether relevant activity is present."
            ),
            desired_state="At least one geolocated ISR observation is available for assessment.",
            success_criteria=[
                SuccessCriterion(
                    criterion_id=sid("criterion.geolocated-observation"),
                    statement="One or more geolocated ISR observations are returned.",
                    metric="geolocated_observation_count",
                )
            ],
            target_refs=[sid("region.sector-alpha")],
            constraints=[],
            owner_id=controller.entity_id,
            start_time=2.0,
            deadline=30.0,
        )

        task = IsrTask(
            record=record("record.task.survey-sector-alpha.r0", 2.0),
            task_id=task_id,
            isr_task=TaskISR.SURVEY,
            area=area,
            dwell_seconds=20.0,
            priority=objective.priority,
            start_time=3.0,
            deadline=25.0,
        )

        assignment = Assignment(
            record=record("record.assignment.survey-sector-alpha.r0", 2.0),
            assignment_id=assignment_id,
            task_id=task_id,
            assignee_id=executor.entity_id,
            plan_id=plan_id,
            authority="AIC2 delegated mission authority",
            assigned_by=controller.entity_id,
            assigned_at=2.0,
            status=AssignmentStatus.ASSIGNED,
            constraints=[],
        )

        plan = Plan(
            record=record("record.plan.survey-sector-alpha.r0", 2.0),
            plan_id=plan_id,
            name="Scout-1 Sector Alpha ISR plan",
            objective_ids=[objective_id],
            task_ids=[task_id],
            actor_ids=[executor.entity_id],
            resource_ids=[],
            assignments=[assignment_id],
            steps=[
                PlanStep(
                    step_id=sid("step.survey-sector-alpha"),
                    task_id=task_id,
                    actor_ids=[executor.entity_id],
                    depends_on=[],
                    sequence=1,
                )
            ],
            routes=[route],
            constraints=[],
            contingencies=[],
            approval_state=PlanApprovalState.APPROVED,
        )

        execution = Execution(
            record=record("record.execution.survey-sector-alpha.r0", 2.0),
            execution_id=execution_id,
            assignment_id=assignment_id,
            executor_id=executor.entity_id,
            attempt=1,
            phase=ExecutionPhase.CREATED,
            progress=0.0,
            external_job_refs=[],
        )

        command = CommandMessage(
            src=target(controller.entity_id),
            dst=target(executor.entity_id),
            ts=timestamp(3),
            priority=MessagePriority.IMMEDIATE,
            seq=100,
            command=ApplyPlanCommand(plan=plan),
        )

        return {
            "objective": objective,
            "task": task,
            "plan": plan,
            "assignment": assignment,
            "execution": execution,
            "command": command,
        }

    def assess(
        self,
        objective: Objective,
        assignment: Assignment,
        execution: Execution,
        task_delta: TaskDelta,
        result: IsrResult,
    ) -> Objective:
        successful = (
            assignment.status == AssignmentStatus.COMPLETE
            and execution.phase == ExecutionPhase.SUCCEEDED
            and task_delta.phase == TaskPhase.DONE_OK
            and len(result.observations) >= 1
            and all(obs.position is not None for obs in result.observations)
        )
        if not successful:
            raise RuntimeError("objective success criterion was not satisfied")

        return Objective(
            record=record("record.objective.recon-sector-alpha.r1", 15.0, revision=1),
            objective_id=objective.objective_id,
            name=objective.name,
            intent=objective.intent,
            desired_state=objective.desired_state,
            success_criteria=objective.success_criteria,
            target_refs=objective.target_refs,
            constraints=objective.constraints,
            priority=objective.priority,
            status=TaskStatus.COMPLETE,
            owner_id=objective.owner_id,
            start_time=objective.start_time,
            deadline=objective.deadline,
        )


class SimulatedAutonomousExecutor:
    """Deterministic autonomous node consuming and producing OCCID records."""

    def execute(
        self,
        entity: Entity,
        node: Node,
        task: IsrTask,
        plan: Plan,
        assignment: Assignment,
        execution: Execution,
        command: CommandMessage,
    ) -> dict[str, OCCIDModel]:
        if assignment.assignee_id != entity.entity_id:
            raise RuntimeError("assignment targets another executor")
        if assignment.task_id != task.task_id:
            raise RuntimeError("assignment and task identity differ")
        if assignment.assignment_id not in plan.assignments:
            raise RuntimeError("plan does not reference assignment")
        if task.task_id not in plan.task_ids or entity.entity_id not in plan.actor_ids:
            raise RuntimeError("plan does not bind task to executor")
        if plan.approval_state != PlanApprovalState.APPROVED:
            raise RuntimeError("executor will not apply an unapproved plan")
        if command.dst.target_id != entity.entity_id:
            raise RuntimeError("command targets another entity")
        if command.command.plan.plan_id != plan.plan_id:
            raise RuntimeError("command carries another plan")
        if CapabilityRole.SENSOR not in node.roles:
            raise RuntimeError("executor has no advertised sensor role")

        accepted_assignment = Assignment(
            record=record("record.assignment.survey-sector-alpha.r1", 4.0, revision=1),
            assignment_id=assignment.assignment_id,
            task_id=assignment.task_id,
            assignee_id=assignment.assignee_id,
            plan_id=assignment.plan_id,
            authority=assignment.authority,
            assigned_by=assignment.assigned_by,
            assigned_at=assignment.assigned_at,
            accepted_at=4.0,
            status=AssignmentStatus.ACCEPTED,
            constraints=assignment.constraints,
        )

        running_execution = Execution(
            record=record("record.execution.survey-sector-alpha.r1", 4.0, revision=1),
            execution_id=execution.execution_id,
            assignment_id=execution.assignment_id,
            executor_id=execution.executor_id,
            attempt=execution.attempt,
            phase=ExecutionPhase.RUNNING,
            progress=0.1,
            started_at=4.0,
            external_job_refs=[],
        )

        running_task = TaskDelta(
            record=record("record.task-delta.survey-sector-alpha.running", 5.0),
            task_id=task.task_id,
            task_rev=1,
            phase=TaskPhase.RUNNING,
            progress=0.1,
            owner_id=entity.entity_id,
            updated_ts=5.0,
        )

        search_position = GlobalPosition(
            lat=BASE_LAT + 0.0012,
            lon=BASE_LON + 0.0013,
            alt=120.0,
            alt_frame=AltitudeDatum.RELATIVE,
        )
        active_state = EntityState(
            record=record("record.entity-state.scout-1.active", 8.0),
            subject_id=entity.entity_id,
            timestamp=8.0,
            position=LocationState(
                position=search_position,
                velocity=VelocityVector(x=12.0, y=1.0, z=0.0),
            ),
            operational_status=EntityOperationalState.ACTIVE,
            links={},
        )
        active_flight_state = TelemetryState(
            standard_mode=StandardFlightMode.MISSION,
            native_mode_name="NAV_WP",
            flight_phase=FlightPhase.PLAN_OPERATION,
            battery_pct=82.0,
        )

        observed_position = GlobalPosition(
            lat=BASE_LAT + 0.00145,
            lon=BASE_LON + 0.00155,
            alt=0.0,
            alt_frame=AltitudeDatum.TERRAIN,
        )
        observation = IsrObservation(
            record=record("record.observation.sector-alpha.1", 10.0),
            obs_id=sid("observation.sector-alpha.1"),
            track_id=sid("track.sector-alpha.1", IdentifierType.TRACK_ID),
            sensor_id=sid("sensor.scout-1.eo"),
            obs_ts=10.0,
            observation_kind=ObservationKind.DETECTION,
            category=IntelCategory.IMINT,
            spotter_origin=SpotterOrigin(position=search_position),
            position=observed_position,
            uncertainty=LocationUncertainty(horiz_err_m=3.0, vert_err_m=5.0),
        )
        track = TrackUpdate(
            record=record("record.track-update.sector-alpha.1", 10.0),
            track_id=observation.track_id,
            track_state=TrackState.ACTIVE,
            updated_ts=10.0,
        )
        isr_result = IsrResult(
            detections=[observation],
            track_updates=[track],
            observations=[observation],
        )

        complete_task = TaskDelta(
            record=record("record.task-delta.survey-sector-alpha.complete", 12.0),
            task_id=task.task_id,
            task_rev=2,
            phase=TaskPhase.DONE_OK,
            progress=1.0,
            owner_id=entity.entity_id,
            updated_ts=12.0,
        )
        complete_execution = Execution(
            record=record("record.execution.survey-sector-alpha.r2", 12.0, revision=2),
            execution_id=execution.execution_id,
            assignment_id=execution.assignment_id,
            executor_id=execution.executor_id,
            attempt=execution.attempt,
            phase=ExecutionPhase.SUCCEEDED,
            progress=1.0,
            started_at=4.0,
            completed_at=12.0,
            external_job_refs=[],
        )
        complete_assignment = Assignment(
            record=record("record.assignment.survey-sector-alpha.r2", 12.0, revision=2),
            assignment_id=assignment.assignment_id,
            task_id=assignment.task_id,
            assignee_id=assignment.assignee_id,
            plan_id=assignment.plan_id,
            authority=assignment.authority,
            assigned_by=assignment.assigned_by,
            assigned_at=assignment.assigned_at,
            accepted_at=4.0,
            status=AssignmentStatus.COMPLETE,
            constraints=assignment.constraints,
        )
        final_state = EntityState(
            record=record("record.entity-state.scout-1.complete", 13.0),
            subject_id=entity.entity_id,
            timestamp=13.0,
            position=LocationState(
                position=search_position,
                velocity=VelocityVector(x=0.0, y=0.0, z=0.0),
            ),
            operational_status=EntityOperationalState.READY,
            links={},
        )

        return {
            "assignment_accepted": accepted_assignment,
            "execution_running": running_execution,
            "task_running": running_task,
            "active_state": active_state,
            "active_flight_state": active_flight_state,
            "observation": observation,
            "track": track,
            "isr_result": isr_result,
            "task_complete": complete_task,
            "execution_complete": complete_execution,
            "assignment_complete": complete_assignment,
            "final_state": final_state,
        }


def build_initial_operational_picture() -> dict[str, OCCIDModel]:
    controller = Agent(
        record=record("record.entity.aic2.r0", 0.0),
        entity_id=sid("entity.aic2"),
        node_ids=[sid("node.aic2")],
        name="AIC2 decision agent",
        alt_ids=[],
        tags=["controller", "reasoning", "c2"],
        metadata={},
        relations=[],
    )
    executor = Entity(
        record=record("record.entity.scout-1.r0", 0.0),
        entity_id=sid("entity.uav.scout-1"),
        node_ids=[sid("node.uav.scout-1")],
        name="SCOUT-1",
        entity_type=EntityType.MACHINE,
        alt_ids=[],
        tags=["uav", "autonomous", "isr"],
        metadata={},
        relations=[],
    )
    executor_node = Node(
        node_id=executor.node_ids[0],
        entity_id=executor.entity_id,
        roles=[CapabilityRole.SENSOR, CapabilityRole.EFFECTOR],
        addresses=[],
        links={},
        radios={},
        protocols={},
    )

    initial_position = GlobalPosition(
        lat=BASE_LAT,
        lon=BASE_LON,
        alt=80.0,
        alt_frame=AltitudeDatum.RELATIVE,
    )
    initial_state = EntityState(
        record=record("record.entity-state.scout-1.initial", 1.0),
        subject_id=executor.entity_id,
        timestamp=1.0,
        position=LocationState(
            position=initial_position,
            velocity=VelocityVector(x=0.0, y=0.0, z=0.0),
        ),
        operational_status=EntityOperationalState.READY,
        links={},
    )
    initial_flight_state = TelemetryState(
        standard_mode=StandardFlightMode.EXTERNAL_CONTROL,
        native_mode_name="GUIDED",
        flight_phase=FlightPhase.PREFLIGHT,
        battery_pct=94.0,
    )

    state_message = TelemetryMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(1),
        priority=MessagePriority.ROUTINE,
        seq=1,
        state=initial_state,
    )
    flight_message = UAVTelemetryMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(1),
        priority=MessagePriority.ROUTINE,
        seq=2,
        state=initial_flight_state,
    )

    area = GeoArea(
        vertices=[
            GlobalPosition(lat=BASE_LAT + 0.0008, lon=BASE_LON + 0.0008, alt=0.0, alt_frame=AltitudeDatum.TERRAIN),
            GlobalPosition(lat=BASE_LAT + 0.0008, lon=BASE_LON + 0.0020, alt=0.0, alt_frame=AltitudeDatum.TERRAIN),
            GlobalPosition(lat=BASE_LAT + 0.0020, lon=BASE_LON + 0.0020, alt=0.0, alt_frame=AltitudeDatum.TERRAIN),
            GlobalPosition(lat=BASE_LAT + 0.0020, lon=BASE_LON + 0.0008, alt=0.0, alt_frame=AltitudeDatum.TERRAIN),
        ]
    )
    route = GeoPath(
        points=[
            initial_position,
            GlobalPosition(
                lat=BASE_LAT + 0.0012,
                lon=BASE_LON + 0.0013,
                alt=120.0,
                alt_frame=AltitudeDatum.RELATIVE,
            ),
        ]
    )

    return {
        "controller": controller,
        "executor": executor,
        "executor_node": executor_node,
        "initial_state": initial_state,
        "initial_flight_state": initial_flight_state,
        "state_message": state_message,
        "flight_message": flight_message,
        "area": area,
        "route": route,
    }


def run_scenario() -> ScenarioResult:
    boundary = SemanticBoundary()
    decision_agent = DeterministicDecisionAgent()
    autonomous_executor = SimulatedAutonomousExecutor()
    records = build_initial_operational_picture()

    # OBSERVE: the decision system receives identity, capability, and telemetry.
    controller = boundary.transfer(
        records["controller"],
        phase="OBSERVE",
        source="registry",
        destination="decision-agent",
        purpose="Load controller identity.",
    )
    executor = boundary.transfer(
        records["executor"],
        phase="OBSERVE",
        source="registry",
        destination="decision-agent",
        purpose="Load candidate executor identity and stable specification.",
    )
    executor_node = boundary.transfer(
        records["executor_node"],
        phase="ORIENT",
        source="capability-registry",
        destination="decision-agent",
        purpose="Relate the candidate entity to its sensing and effecting capability.",
    )
    state_message = boundary.transfer(
        records["state_message"],
        phase="OBSERVE",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report mutable entity position and readiness state.",
    )
    flight_message = boundary.transfer(
        records["flight_message"],
        phase="OBSERVE",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report flight mode, phase, and energy state.",
    )

    # ORIENT: select an actor by identity, capability, readiness, position, and energy.
    selected_executor = decision_agent.select_executor(
        executor,
        executor_node,
        state_message.state,
        flight_message.state,
    )

    # DECIDE: produce a complete control chain, not merely a low-level command.
    decision = decision_agent.decide(
        controller,
        selected_executor,
        records["area"],
        records["route"],
    )
    objective = boundary.transfer(
        decision["objective"],
        phase="DECIDE",
        source="decision-agent",
        destination="operational-record-store",
        purpose="Define the intended operational end state.",
    )
    task = boundary.transfer(
        decision["task"],
        phase="DECIDE",
        source="decision-agent",
        destination="autonomous-executor",
        purpose="Define the work required to satisfy the objective.",
    )
    plan = boundary.transfer(
        decision["plan"],
        phase="DECIDE",
        source="decision-agent",
        destination="autonomous-executor",
        purpose="Define the approved method, actor, route, and sequence.",
    )
    assignment = boundary.transfer(
        decision["assignment"],
        phase="DECIDE",
        source="decision-agent",
        destination="autonomous-executor",
        purpose="Bind the task to SCOUT-1 under explicit authority.",
    )
    execution = boundary.transfer(
        decision["execution"],
        phase="DECIDE",
        source="decision-agent",
        destination="execution-monitor",
        purpose="Create the first independently tracked execution attempt.",
    )
    command = boundary.transfer(
        decision["command"],
        phase="ACT",
        source="decision-agent",
        destination="autonomous-executor",
        purpose="Direct the executor to apply the approved plan.",
    )

    # ACT: the autonomous node validates the semantic package and executes it.
    outcome = autonomous_executor.execute(
        selected_executor,
        executor_node,
        task,
        plan,
        assignment,
        execution,
        command,
    )
    assignment_accepted = boundary.transfer(
        outcome["assignment_accepted"],
        phase="ACT",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report semantic acceptance of the assignment.",
    )
    execution_running = boundary.transfer(
        outcome["execution_running"],
        phase="ACT",
        source="autonomous-executor",
        destination="execution-monitor",
        purpose="Report that the execution attempt has started.",
    )
    task_running = boundary.transfer(
        outcome["task_running"],
        phase="ACT",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report task lifecycle progress independently of the task definition.",
    )

    active_state_message = TelemetryMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(8),
        priority=MessagePriority.ROUTINE,
        seq=3,
        state=outcome["active_state"],
    )
    active_flight_message = UAVTelemetryMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(8),
        priority=MessagePriority.ROUTINE,
        seq=4,
        state=outcome["active_flight_state"],
    )
    boundary.transfer(
        active_state_message,
        phase="ACT",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report updated position and active operational state.",
    )
    boundary.transfer(
        active_flight_message,
        phase="ACT",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report flight execution mode and remaining energy.",
    )

    observation_message = ObservationMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(10),
        priority=MessagePriority.PRIORITY,
        seq=5,
        observation=outcome["observation"],
    )
    boundary.transfer(
        observation_message,
        phase="ACT",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Return a geolocated external observation from the assigned search.",
    )
    isr_result = boundary.transfer(
        outcome["isr_result"],
        phase="ASSESS",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Return the structured ISR result and track update.",
    )
    task_complete = boundary.transfer(
        outcome["task_complete"],
        phase="ASSESS",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report successful completion of the task lifecycle.",
    )
    execution_complete = boundary.transfer(
        outcome["execution_complete"],
        phase="ASSESS",
        source="autonomous-executor",
        destination="execution-monitor",
        purpose="Report successful completion of the execution attempt.",
    )
    assignment_complete = boundary.transfer(
        outcome["assignment_complete"],
        phase="ASSESS",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Close the assignee binding after execution completes.",
    )

    final_state_message = TelemetryMessage(
        src=target(executor.entity_id),
        dst=target(controller.entity_id),
        ts=timestamp(13),
        priority=MessagePriority.ROUTINE,
        seq=6,
        state=outcome["final_state"],
    )
    final_state_message = boundary.transfer(
        final_state_message,
        phase="ASSESS",
        source="autonomous-executor",
        destination="decision-agent",
        purpose="Report final vehicle condition without modifying its identity record.",
    )

    objective_complete = decision_agent.assess(
        objective,
        assignment_complete,
        execution_complete,
        task_complete,
        isr_result,
    )
    objective_complete = boundary.transfer(
        objective_complete,
        phase="ASSESS",
        source="decision-agent",
        destination="operational-record-store",
        purpose="Close the objective after evaluating execution and ISR evidence.",
    )

    records.update(
        {
            "objective": objective,
            "task": task,
            "plan": plan,
            "assignment": assignment,
            "execution": execution,
            "assignment_accepted": assignment_accepted,
            "execution_running": execution_running,
            "task_running": task_running,
            "isr_result": isr_result,
            "task_complete": task_complete,
            "execution_complete": execution_complete,
            "assignment_complete": assignment_complete,
            "final_state": final_state_message.state,
            "objective_complete": objective_complete,
        }
    )

    assertions = {
        "all_application_boundaries_round_trip_occid": True,
        "stable_entity_identity_across_mutable_state": (
            records["initial_state"].subject_id == records["final_state"].subject_id == executor.entity_id
            and records["initial_state"].record.record_id != records["final_state"].record.record_id
        ),
        "objective_task_plan_assignment_execution_are_distinct": len(
            {
                objective.objective_id.value,
                task.task_id.value,
                plan.plan_id.value,
                assignment.assignment_id.value,
                execution.execution_id.value,
            }
        ) == 5,
        "control_chain_is_correlated": (
            objective.objective_id in plan.objective_ids
            and task.task_id in plan.task_ids
            and assignment.assignment_id in plan.assignments
            and execution.assignment_id == assignment.assignment_id
            and execution.executor_id == executor.entity_id
        ),
        "runtime_state_did_not_mutate_definitions": (
            objective.record.revision == 0
            and task.record.revision == 0
            and plan.record.revision == 0
            and task.status == TaskStatus.NEW
            and task_complete.phase == TaskPhase.DONE_OK
        ),
        "semantic_acceptance_is_distinct_from_execution": (
            assignment_accepted.status == AssignmentStatus.ACCEPTED
            and execution_running.phase == ExecutionPhase.RUNNING
            and assignment_accepted.record.record_id != execution_running.record.record_id
        ),
        "telemetry_and_observation_closed_the_loop": (
            final_state_message.state.subject_id == executor.entity_id
            and len(isr_result.observations) >= 1
            and isr_result.observations[0].position is not None
        ),
        "objective_completed_from_operational_evidence": objective_complete.status == TaskStatus.COMPLETE,
    }
    if not all(assertions.values()):
        failed = [name for name, passed in assertions.items() if not passed]
        raise AssertionError(f"scenario invariants failed: {', '.join(failed)}")

    return ScenarioResult(trace=boundary.trace, records=records, assertions=assertions)


def print_human(result: ScenarioResult) -> None:
    print("OCCID closed-loop command, control, telemetry, and OODA demonstration")
    print("=" * 74)
    for entry in result.trace:
        print(
            f"{entry.index:02d} {entry.phase:<7} "
            f"{entry.source:<23} -> {entry.destination:<24} "
            f"{entry.model_name:<22} {entry.wire_bytes:>5} B"
        )
        print(f"   {entry.purpose}")
    print("\nAssertions")
    for name, passed in result.assertions.items():
        print(f"  {'PASS' if passed else 'FAIL'}  {name}")
    summary = result.as_dict()["summary"]
    print("\nResult")
    print(
        f"  objective={summary['objective_status']} "
        f"assignment={summary['assignment_status']} "
        f"execution={summary['execution_phase']} "
        f"task={summary['task_phase']}"
    )
    print(
        f"  observations={summary['observations']} "
        f"track_updates={summary['track_updates']} "
        f"trace_entries={summary['trace_entries']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the complete machine-readable trace")
    parser.add_argument("--output", type=Path, help="write the complete trace to a JSON file")
    args = parser.parse_args()

    result = run_scenario()
    document = result.as_dict()

    if args.output:
        args.output.write_text(json.dumps(document, indent=2) + "\n")
        print(f"wrote {args.output}")
    if args.json:
        print(json.dumps(document, indent=2))
    elif not args.output:
        print_human(result)


if __name__ == "__main__":
    main()
