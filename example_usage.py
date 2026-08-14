"""Small OCCID Control refactor usage example."""

from __future__ import annotations

from occid import (
    AltitudeDatum,
    Assignment,
    AssignmentStatus,
    Authority,
    Execution,
    ExecutionCommand,
    ExecutionOperation,
    GlobalPosition,
    IdentifierType,
    MotionCommand,
    MotionOperation,
    RecordMeta,
    StringID,
    Task,
    TaskIntent,
    TaskType,
)


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


def meta(value: str) -> RecordMeta:
    return RecordMeta(
        record_id=sid(value),
        created_ts=1.0,
        updated_ts=1.0,
        origin_system="occid.example",
        provenance=[],
    )


def main() -> None:
    operator_id = sid("entity.operator.1")
    uav_id = sid("entity.uav.7")

    task = Task(
        record=meta("record.task.1"),
        task_id=sid("task.bridge.observe"),
        instruction="Move to the north side of the bridge and observe westbound traffic.",
        task_type=TaskType.INFORMATION,
        task_intent=TaskIntent.OBSERVE,
        target_refs=[],
        location_refs=[sid("location.bridge.north")],
        constraints=[],
    )

    authority = Authority(
        record=meta("record.authority.1"),
        authority_id=sid("authority.operator.uav7"),
        holder_id=operator_id,
        granted_by=operator_id,
        scope_refs=[uav_id, task.task_id],
        constraints=[],
    )

    assignment = Assignment(
        record=meta("record.assignment.1"),
        assignment_id=sid("assignment.bridge.observe.uav7"),
        task_id=task.task_id,
        assignee_id=uav_id,
        authority_id=authority.authority_id,
        assigned_by=operator_id,
        assigned_at=1.0,
        status=AssignmentStatus.ASSIGNED,
        constraints=[],
    )

    execution = Execution(
        record=meta("record.execution.1"),
        execution_id=sid("execution.bridge.observe.1"),
        assignment_id=assignment.assignment_id,
        executor_id=uav_id,
        external_job_refs=[],
    )

    move = MotionCommand(
        target_ref=uav_id,
        constraints=[],
        operation=MotionOperation.MOVE_TO,
        destination=GlobalPosition(
            lat=45.5017,
            lon=-73.5673,
            alt=120.0,
            alt_frame=AltitudeDatum.RELATIVE,
        ),
    )

    execute = ExecutionCommand(
        target_ref=execution.execution_id,
        constraints=[],
        operation=ExecutionOperation.EXECUTE,
        dispatch_id=sid("dispatch.bridge.observe.1"),
    )

    for value in (task, authority, assignment, execution, move, execute):
        decoded = type(value).decode(value.encode())
        print(type(decoded).__name__, decoded)


if __name__ == "__main__":
    main()
