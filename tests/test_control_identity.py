from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import (
    Execution,
    ExecutionPhase,
    Record,
    SuccessCriterion,
    Task,
    TaskPhase,
    Timestamp,
)


RECORD_UID = bytes.fromhex("0ea050c77b6543f7baaafcc0dc0f94ce")
TASK_UID = bytes.fromhex("fe8823f2a76b4f92a8989d76d4f093de")
ACTOR_UID = bytes.fromhex("9f33ea2a81344f14bdd4d0d84169cebc")
EXECUTION_UID = bytes.fromhex("f8524789a7c645769ea1cab788bdaed7")
EXECUTOR_UID = bytes.fromhex("f27d4d7e263d4a80ada248e10fedb01d")
ASSIGNMENT_UID = bytes.fromhex("3c9f1e2a5b7d4c6e8a9f0b1c2d3e4f50")


def ts(value: float) -> Timestamp:
    return Timestamp(utime=value, tz=0)


def record() -> Record:
    return Record(
        uid=RECORD_UID,
        id=1,
        created_ts=ts(0.0),
        updated_ts=ts(0.0),
        origin_system="test",
        provenance=[],
    )


class ControlIdentityTests(unittest.TestCase):
    def test_task_uses_uid_and_human_number(self) -> None:
        task = Task(
            record=record(),
            uid=TASK_UID,
            id=42,
            instruction="Search sector Bravo",
            target_uids=[ACTOR_UID],
            location_uids=[],
            constraints=[],
            phase=TaskPhase.CREATED,
        )
        self.assertEqual(task.uid.root, TASK_UID)
        self.assertEqual(task.id.root, 42)
        self.assertEqual([uid.root for uid in task.target_uids], [ACTOR_UID])

        with self.assertRaises(ValidationError):
            Task(
                record=record(),
                uid="task-42",
                id=42,
                instruction="Search sector Bravo",
                target_uids=[],
                location_uids=[],
                constraints=[],
                phase=TaskPhase.CREATED,
            )

    def test_success_criterion_is_embedded_definition_without_identity(self) -> None:
        criterion = SuccessCriterion(statement="Sector searched")
        self.assertEqual(criterion.statement, "Sector searched")
        self.assertNotIn("id", SuccessCriterion.model_fields)
        self.assertNotIn("uid", SuccessCriterion.model_fields)
        self.assertNotIn("criterion_id", SuccessCriterion.model_fields)

    def test_external_job_refs_are_correlation_strings(self) -> None:
        execution = Execution(
            record=record(),
            uid=EXECUTION_UID,
            id=1,
            assignment_uid=ASSIGNMENT_UID,
            executor_uid=EXECUTOR_UID,
            phase=ExecutionPhase.CREATED,
            started_at=ts(1.0),
            completed_at=ts(1.0),
            external_job_refs=["dispatch-7"],
        )
        self.assertEqual(execution.external_job_refs, ["dispatch-7"])
        self.assertNotIn("dispatch_ref", Execution.model_fields)


if __name__ == "__main__":
    unittest.main()
