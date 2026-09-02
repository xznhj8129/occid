from __future__ import annotations

import unittest
from pathlib import Path

import occid

import yaml

from occid import (
    Assignment,
    OCCID_MODEL_ID_BY_CLASS,
    PlanStep,
    RecordMeta,
    SuccessCriterion,
    TaskDelta,
    TaskPhase,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RECORD_UID_1 = bytes.fromhex("726b19e572144cef99e6c00a70c9320b")
RECORD_UID_2 = bytes.fromhex("90ca3bc1d94442e98d11c0faf4b9264b")
TASK_UID_1 = bytes.fromhex("6ce34dc4b3524d75a16a96b505110458")
TASK_UID_2 = bytes.fromhex("fe8a7c3cafde41bb8ec6cde9a3af6b04")
OWNER_UID = bytes.fromhex("922651f437bb4aa1bf5812d6ade5f22d")


def record_meta(record_uid: bytes, record_id: int) -> RecordMeta:
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

    def test_assignment_and_task_delta_are_flat_runtime_models(self) -> None:
        self.assertNotIn("Control", occid.__all__)
        self.assertNotIn("State", occid.__all__)
        self.assertEqual(Assignment.__occid_semantic_role__, "type")
        self.assertEqual(TaskDelta.__occid_semantic_role__, "representation")
        self.assertIn("record", Assignment.model_fields)
        self.assertIn("uid", Assignment.model_fields)
        self.assertIn("id", Assignment.model_fields)
        self.assertIn("record", TaskDelta.model_fields)

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

    def test_compiled_model_ids_match_generated_models(self) -> None:
        compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
        model_ids = {
            name: spec["model_id"]
            for section in ("types", "representations")
            for name, spec in compiled[section].items()
        }
        self.assertEqual(len(model_ids.values()), len(set(model_ids.values())))
        self.assertEqual(set(model_ids.values()), set(range(1, len(model_ids) + 1)))
        self.assertEqual(
            [name for name, _ in sorted(model_ids.items(), key=lambda item: item[1])],
            sorted(model_ids),
        )
        for model, model_id in OCCID_MODEL_ID_BY_CLASS.items():
            self.assertEqual(model_ids[model.__name__], model_id)


if __name__ == "__main__":
    unittest.main()
