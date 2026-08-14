"""Deterministic OCCID-only control loop demonstration.

The scenario crosses real OCCID encode/decode boundaries while keeping the
stable logical Task, its Assignment, and one Execution attempt distinct.
No Sigma, HiveLink, MPFC, broker, flight controller, or network service is
required.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any

from occid import (
    Assignment,
    AssignmentStatus,
    Authority,
    CommandMessage,
    Execution,
    ExecutionAcceptance,
    ExecutionCommand,
    ExecutionOperation,
    ExecutionPhase,
    ExecutionStatusReport,
    IdentifierType,
    MessagePriority,
    MessageTarget,
    OCCID_MODEL_ID_BY_CLASS,
    Objective,
    Plan,
    PlanApprovalState,
    RecordMeta,
    StringID,
    Task,
    TaskDelta,
    TaskIntent,
    TaskPhase,
    TaskStatus,
    TaskType,
    Timestamp,
    decode_model,
)


@dataclass(frozen=True)
class TraceEntry:
    label: str
    model: str
    model_id: int
    wire_bytes: int


@dataclass
class ScenarioResult:
    records: dict[str, Any] = field(default_factory=dict)
    trace: list[TraceEntry] = field(default_factory=list)
    assertions: dict[str, bool] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "assertions": self.assertions,
            "trace": [entry.__dict__ for entry in self.trace],
            "records": {
                name: value.model_dump(mode="json")
                for name, value in self.records.items()
                if hasattr(value, "model_dump")
            },
        }


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


def record_meta(record_id: str, ts: float) -> RecordMeta:
    return RecordMeta(
        record_id=sid(record_id),
        created_ts=ts,
        updated_ts=ts,
        origin_system="occid.demo",
        provenance=[],
    )


def timestamp(second: float) -> Timestamp:
    return Timestamp(
        seconds=second,
        minutes=0.0,
        hours=12.0,
        day=14.0,
        month=8.0,
        year=2026.0,
        tz=-4.0,
    )


def run_scenario() -> ScenarioResult:
    result = ScenarioResult()

    def cross(label: str, value):
        payload = value.encode()
        decoded = decode_model(payload)
        if type(decoded) is not type(value):
            raise AssertionError(f"{label}: decoded {type(decoded).__name__}, expected {type(value).__name__}")
        if decoded != value:
            raise AssertionError(f"{label}: round trip changed value")
        result.trace.append(
            TraceEntry(
                label=label,
                model=type(value).__name__,
                model_id=OCCID_MODEL_ID_BY_CLASS[type(value)],
                wire_bytes=len(payload),
            )
        )
        return decoded

    operator_id = sid("entity.operator.1")
    executor_id = sid("entity.scout.1")
    location_id = sid("location.route6.corridor")
    dispatch_id = sid("dispatch.route6.search.1")

    objective = cross(
        "objective.created",
        Objective(
            record=record_meta("record.objective.route6.1", 1.0),
            objective_id=sid("objective.route6.awareness"),
            name="Establish Route 6 traffic picture",
            intent="Establish what vehicle traffic is using Route 6.",
            desired_state="Current Route 6 vehicle traffic is identified and reported.",
            success_criteria=[],
            target_refs=[location_id],
            constraints=[],
            owner_id=operator_id,
        ),
    )

    task = cross(
        "task.created",
        Task(
            record=record_meta("record.task.route6.1", 2.0),
            task_id=sid("task.route6.search"),
            instruction="Search Route 6 and establish what vehicle traffic is using it.",
            task_type=TaskType.INFORMATION,
            task_intent=TaskIntent.SEARCH,
            target_refs=[],
            location_refs=[location_id],
            objective_id=objective.objective_id,
            constraints=[],
        ),
    )

    authority = cross(
        "authority.issued",
        Authority(
            record=record_meta("record.authority.scout1.1", 3.0),
            authority_id=sid("authority.scout1.route6"),
            holder_id=operator_id,
            granted_by=operator_id,
            scope_refs=[executor_id, task.task_id],
            constraints=[],
        ),
    )

    assignment = cross(
        "assignment.created",
        Assignment(
            record=record_meta("record.assignment.route6.1", 4.0),
            assignment_id=sid("assignment.route6.search.scout1"),
            task_id=task.task_id,
            assignee_id=executor_id,
            authority_id=authority.authority_id,
            assigned_by=operator_id,
            assigned_at=4.0,
            status=AssignmentStatus.ASSIGNED,
            constraints=[],
        ),
    )

    plan = cross(
        "plan.approved",
        Plan(
            record=record_meta("record.plan.route6.1", 5.0),
            plan_id=sid("plan.route6.search"),
            name="Route 6 search",
            objective_ids=[objective.objective_id],
            task_ids=[task.task_id],
            actor_ids=[executor_id],
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
            record=record_meta("record.execution.route6.1", 6.0),
            execution_id=sid("execution.route6.search.1"),
            assignment_id=assignment.assignment_id,
            executor_id=executor_id,
            external_job_refs=[],
        ),
    )

    command = ExecutionCommand(
        target_ref=plan.plan_id,
        constraints=[],
        operation=ExecutionOperation.EXECUTE,
        dispatch_id=dispatch_id,
    )
    command_message = cross(
        "dispatch.command",
        CommandMessage(
            src=MessageTarget(target_id=operator_id),
            dst=MessageTarget(target_id=executor_id),
            ts=timestamp(7.0),
            priority=MessagePriority.ROUTINE,
            seq=1,
            command=command,
        ),
    )

    acceptance = cross(
        "execution.accepted",
        ExecutionAcceptance(
            execution_id=execution.execution_id,
            dispatch_id=dispatch_id,
            executor_id=executor_id,
            accepted=True,
            reported_at=8.0,
        ),
    )

    assignment_active = cross(
        "assignment.active",
        Assignment(
            record=record_meta("record.assignment.route6.2", 9.0),
            assignment_id=assignment.assignment_id,
            task_id=task.task_id,
            assignee_id=executor_id,
            plan_id=plan.plan_id,
            authority_id=authority.authority_id,
            assigned_by=operator_id,
            assigned_at=4.0,
            accepted_at=8.0,
            status=AssignmentStatus.ACTIVE,
            constraints=[],
        ),
    )

    execution_running = cross(
        "execution.running",
        Execution(
            record=record_meta("record.execution.route6.2", 10.0),
            execution_id=execution.execution_id,
            assignment_id=assignment.assignment_id,
            executor_id=executor_id,
            phase=ExecutionPhase.RUNNING,
            progress=0.4,
            started_at=9.0,
            external_job_refs=[],
        ),
    )

    task_running = cross(
        "task.running",
        TaskDelta(
            record=record_meta("record.taskdelta.route6.1", 10.0),
            task_id=task.task_id,
            task_rev=1,
            phase=TaskPhase.RUNNING,
            progress=0.4,
            owner_id=executor_id,
            updated_ts=10.0,
        ),
    )

    status_running = cross(
        "execution.status.running",
        ExecutionStatusReport(
            execution_id=execution.execution_id,
            dispatch_id=dispatch_id,
            executor_id=executor_id,
            phase=ExecutionPhase.RUNNING,
            progress=0.4,
            task_delta=task_running,
            reported_at=10.0,
        ),
    )

    execution_complete = cross(
        "execution.succeeded",
        Execution(
            record=record_meta("record.execution.route6.3", 20.0),
            execution_id=execution.execution_id,
            assignment_id=assignment.assignment_id,
            executor_id=executor_id,
            phase=ExecutionPhase.SUCCEEDED,
            progress=1.0,
            started_at=9.0,
            completed_at=20.0,
            external_job_refs=[],
        ),
    )

    task_complete = cross(
        "task.complete",
        TaskDelta(
            record=record_meta("record.taskdelta.route6.2", 20.0),
            task_id=task.task_id,
            task_rev=2,
            phase=TaskPhase.DONE_OK,
            progress=1.0,
            owner_id=executor_id,
            updated_ts=20.0,
        ),
    )

    status_complete = cross(
        "execution.status.succeeded",
        ExecutionStatusReport(
            execution_id=execution.execution_id,
            dispatch_id=dispatch_id,
            executor_id=executor_id,
            phase=ExecutionPhase.SUCCEEDED,
            progress=1.0,
            task_delta=task_complete,
            reported_at=20.0,
        ),
    )

    assignment_complete = cross(
        "assignment.complete",
        Assignment(
            record=record_meta("record.assignment.route6.3", 21.0),
            assignment_id=assignment.assignment_id,
            task_id=task.task_id,
            assignee_id=executor_id,
            plan_id=plan.plan_id,
            authority_id=authority.authority_id,
            assigned_by=operator_id,
            assigned_at=4.0,
            accepted_at=8.0,
            status=AssignmentStatus.COMPLETE,
            constraints=[],
        ),
    )

    objective_complete = cross(
        "objective.complete",
        Objective(
            record=record_meta("record.objective.route6.2", 22.0),
            objective_id=objective.objective_id,
            name=objective.name,
            intent=objective.intent,
            desired_state=objective.desired_state,
            success_criteria=[],
            target_refs=objective.target_refs,
            constraints=[],
            status=TaskStatus.COMPLETE,
            owner_id=operator_id,
        ),
    )

    result.records.update(
        objective=objective,
        task=task,
        authority=authority,
        assignment=assignment,
        plan=plan,
        execution=execution,
        command_message=command_message,
        acceptance=acceptance,
        assignment_active=assignment_active,
        execution_running=execution_running,
        task_running=task_running,
        status_running=status_running,
        execution_complete=execution_complete,
        task_complete=task_complete,
        status_complete=status_complete,
        assignment_complete=assignment_complete,
        objective_complete=objective_complete,
    )

    result.assertions.update(
        task_keeps_instruction=task.instruction.startswith("Search Route 6"),
        task_is_unassigned=not hasattr(task, "assignee_id"),
        assignment_references_task=assignment.task_id == task.task_id,
        assignment_references_authority=assignment.authority_id == authority.authority_id,
        execution_references_assignment=execution.assignment_id == assignment.assignment_id,
        dispatch_correlates=acceptance.dispatch_id == command.dispatch_id == status_complete.dispatch_id,
        ids_remain_distinct=(
            task.task_id != assignment.assignment_id
            and assignment.assignment_id != execution.execution_id
        ),
        closed_loop=(
            objective_complete.status == TaskStatus.COMPLETE
            and assignment_complete.status == AssignmentStatus.COMPLETE
            and execution_complete.phase == ExecutionPhase.SUCCEEDED
            and task_complete.phase == TaskPhase.DONE_OK
        ),
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_scenario()
    if args.json:
        print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
        return
    for entry in result.trace:
        print(f"{entry.label}: {entry.model} id={entry.model_id} bytes={entry.wire_bytes}")
    print("assertions:")
    for name, passed in result.assertions.items():
        print(f"  {name}: {'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
