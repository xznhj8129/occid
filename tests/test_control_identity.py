from __future__ import annotations

import unittest

from pydantic import ValidationError

from occid import ExecutionAcceptance, PlanStep, RecordMeta, SuccessCriterion, Task


RECORD_UID = "0ea050c7-7b65-43f7-baaa-fcc0dc0f94ce"
TASK_UID = "fe8823f2-a76b-4f92-a898-9d76d4f093de"
ACTOR_UID = "9f33ea2a-8134-4f14-bdd4-d0d84169cebc"
EXECUTION_UID = "f8524789-a7c6-4576-9ea1-cab788bdaed7"
EXECUTOR_UID = "f27d4d7e-263d-4a80-ada2-48e10fedb01d"


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
        self.assertEqual(str(task.uid), TASK_UID)
        self.assertEqual(task.id, 42)
        self.assertEqual([str(uid) for uid in task.target_uids], [ACTOR_UID])

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
        self.assertEqual(str(acceptance.execution_uid), EXECUTION_UID)
        self.assertEqual(acceptance.dispatch_ref, "dispatch-7")


if __name__ == "__main__":
    unittest.main()
