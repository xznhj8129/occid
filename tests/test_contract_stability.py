from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from occid import (
    Assignment,
    Control,
    OCCID_MODEL_ID_BY_CLASS,
    PlanStep,
    RecordMeta,
    State,
    SuccessCriterion,
    TaskDelta,
    TaskPhase,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RECORD_UID_1 = "726b19e5-7214-4cef-99e6-c00a70c9320b"
RECORD_UID_2 = "90ca3bc1-d944-42e9-8d11-c0faf4b9264b"
TASK_UID_1 = "6ce34dc4-b352-4d75-a16a-96b505110458"
TASK_UID_2 = "fe8a7c3c-afde-41bb-8ec6-cde9a3af6b04"
OWNER_UID = "922651f4-37bb-4aa1-bf58-12d6ade5f22d"


def record_meta(record_uid: str, record_id: int) -> RecordMeta:
    return RecordMeta(
        uid=record_uid,
        id=record_id,
        created_ts=1.0,
        updated_ts=1.0,
        origin_system="occid.tests",
        provenance=[],
    )


class ContractStabilityTests(unittest.TestCase):
    def test_record_identity_is_distinct_from_domain_identity(self) -> None:
        self.assertIn("uid", RecordMeta.model_fields)
        self.assertIn("id", RecordMeta.model_fields)
        delta = TaskDelta(
            record=record_meta(RECORD_UID_1, 1),
            task_uid=TASK_UID_1,
            phase=TaskPhase.RUNNING,
            updated_ts=2.0,
        )
        self.assertNotEqual(delta.record.uid, delta.task_uid)

    def test_definitions_do_not_embed_runtime_assessment(self) -> None:
        self.assertNotIn("satisfied", SuccessCriterion.model_fields)
        self.assertNotIn("status", PlanStep.model_fields)

    def test_assignment_is_control_and_task_delta_is_state(self) -> None:
        self.assertTrue(issubclass(Assignment, Control))
        self.assertFalse(issubclass(Assignment, State))
        self.assertTrue(issubclass(TaskDelta, State))
        self.assertFalse(issubclass(TaskDelta, Assignment))

    def test_task_delta_msgpack_round_trip(self) -> None:
        delta = TaskDelta(
            record=record_meta(RECORD_UID_2, 2),
            task_uid=TASK_UID_2,
            task_rev=3,
            phase=TaskPhase.RUNNING,
            progress=0.5,
            owner_uid=OWNER_UID,
            updated_ts=3.0,
        )
        self.assertEqual(TaskDelta.decode(delta.encode()), delta)

    def test_source_and_generated_contracts_match(self) -> None:
        record_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/record.schema.yaml").read_text())
        objective_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/objective.schema.yaml").read_text())
        plan_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/plan.schema.yaml").read_text())
        assignment_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/assignment.schema.yaml").read_text())
        execution_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/data/state/execution.schema.yaml").read_text())

        self.assertEqual(record_schema["models"]["RecordMeta"]["fields"]["uid"], "UID")
        self.assertEqual(record_schema["models"]["RecordMeta"]["fields"]["id"], "int")
        self.assertNotIn("satisfied", objective_schema["models"]["SuccessCriterion"]["fields"])
        self.assertEqual(objective_schema["models"]["SuccessCriterion"]["fields"]["criterion_id"], "int")
        self.assertNotIn("status", plan_schema["models"]["PlanStep"]["fields"])
        self.assertEqual(plan_schema["models"]["PlanStep"]["fields"]["id"], "int")
        self.assertEqual(assignment_schema["models"]["Assignment"]["parent"], "Control")
        self.assertEqual(execution_schema["models"]["Execution"]["parent"], "State")
        self.assertEqual(execution_schema["models"]["TaskDelta"]["parent"], "State")

    def test_permanent_model_ids_match_generated_models(self) -> None:
        registry = yaml.safe_load((REPO_ROOT / "lib/model_ids.yaml").read_text())
        model_ids = registry["model_ids"]
        self.assertEqual(len(model_ids.values()), len(set(model_ids.values())))
        for model, model_id in OCCID_MODEL_ID_BY_CLASS.items():
            self.assertEqual(model_ids[model.__name__], model_id)


if __name__ == "__main__":
    unittest.main()
