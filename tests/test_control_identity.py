from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import ExecutionAcceptance, PlanStep, RecordMeta, SuccessCriterion, Task


RECORD_UID = bytes.fromhex("0ea050c77b6543f7baaafcc0dc0f94ce")
TASK_UID = bytes.fromhex("fe8823f2a76b4f92a8989d76d4f093de")
ACTOR_UID = bytes.fromhex("9f33ea2a81344f14bdd4d0d84169cebc")
EXECUTION_UID = bytes.fromhex("f8524789a7c645769ea1cab788bdaed7")
EXECUTOR_UID = bytes.fromhex("f27d4d7e263d4a80ada248e10fedb01d")


def record() -> RecordMeta:
    return RecordMeta(
        uid=RECORD_UID,
        id=1,
        created_ts=0.0,
        updated_ts=0.0,
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
        )
        self.assertEqual(task.uid.root, TASK_UID)
        self.assertEqual(task.id, 42)
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
            )

    def test_embedded_plan_and_objective_ids_are_local(self) -> None:
        step = PlanStep(
            id=2,
            task_uid=TASK_UID,
            actor_uids=[ACTOR_UID],
            depends_on=[1],
            sequence=2,
        )
        criterion = SuccessCriterion(criterion_id=1, statement="Sector searched")
        self.assertEqual(step.id, 2)
        self.assertEqual(step.depends_on, [1])
        self.assertEqual(criterion.criterion_id, 1)

    def test_dispatch_ref_is_correlation_string(self) -> None:
        acceptance = ExecutionAcceptance(
            execution_uid=EXECUTION_UID,
            dispatch_ref="dispatch-7",
            executor_uid=EXECUTOR_UID,
            accepted=True,
            reported_at=1.0,
        )
        self.assertEqual(acceptance.execution_uid.root, EXECUTION_UID)
        self.assertEqual(acceptance.dispatch_ref, "dispatch-7")


if __name__ == "__main__":
    unittest.main()
