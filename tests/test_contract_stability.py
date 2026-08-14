from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from occid import (
    Assignment,
    Control,
    IdentifierType,
    OCCID_MODEL_ID_BY_CLASS,
    PlanStep,
    RecordMeta,
    State,
    StringID,
    SuccessCriterion,
    TaskDelta,
    TaskPhase,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def sid(value: str) -> StringID:
    return StringID(id_type=IdentifierType.DB_ID, value=value)


def record_meta(value: str) -> RecordMeta:
    return RecordMeta(
        record_id=sid(value),
        created_ts=1.0,
        updated_ts=1.0,
        origin_system="occid.tests",
        provenance=[],
    )


class ContractStabilityTests(unittest.TestCase):
    def test_record_identity_is_distinct_from_domain_identity(self) -> None:
        self.assertIn("record_id", RecordMeta.model_fields)
        self.assertNotIn("uid", RecordMeta.model_fields)
        delta = TaskDelta(
            record=record_meta("record.task.delta.1"),
            task_id=sid("task.1"),
            phase=TaskPhase.RUNNING,
            updated_ts=2.0,
        )
        self.assertNotEqual(delta.record.record_id, delta.task_id)

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
            record=record_meta("record.task.delta.2"),
            task_id=sid("task.2"),
            task_rev=3,
            phase=TaskPhase.RUNNING,
            progress=0.5,
            owner_id=sid("entity.operator.1"),
            updated_ts=3.0,
        )
        self.assertEqual(TaskDelta.decode(delta.encode()), delta)

    def test_source_and_generated_contracts_match(self) -> None:
        record_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/record.schema.yaml").read_text())
        objective_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/objective.schema.yaml").read_text())
        plan_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/plan.schema.yaml").read_text())
        assignment_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/assignment.schema.yaml").read_text())
        execution_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/data/state/execution.schema.yaml").read_text())

        self.assertIn("record_id", record_schema["models"]["RecordMeta"]["fields"])
        self.assertNotIn("uid", record_schema["models"]["RecordMeta"]["fields"])
        self.assertNotIn("satisfied", objective_schema["models"]["SuccessCriterion"]["fields"])
        self.assertNotIn("status", plan_schema["models"]["PlanStep"]["fields"])
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
