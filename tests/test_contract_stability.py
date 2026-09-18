from __future__ import annotations

import unittest
from pathlib import Path

import occid

import yaml

from occid import (
    Assignment,
    Execution,
    ExecutionPhase,
    OCCID_MODEL_ID_BY_CLASS,
    Record,
    SuccessCriterion,
    Timestamp,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
RECORD_UID_1 = bytes.fromhex("726b19e572144cef99e6c00a70c9320b")
RECORD_UID_2 = bytes.fromhex("90ca3bc1d94442e98d11c0faf4b9264b")
EXECUTION_UID_1 = bytes.fromhex("6ce34dc4b3524d75a16a96b505110458")
EXECUTION_UID_2 = bytes.fromhex("fe8a7c3cafde41bb8ec6cde9a3af6b04")
ASSIGNMENT_UID = bytes.fromhex("922651f437bb4aa1bf5812d6ade5f22d")
OWNER_UID = bytes.fromhex("a511e0f3cbb94a6f9e2a6b3c1d5e7f01")


def ts(value: float) -> Timestamp:
    return Timestamp(utime=value, tz=0)


def make_record(record_uid: bytes, record_id: int) -> Record:
    return Record(
        uid=record_uid,
        id=record_id,
        created_ts=ts(1.0),
        updated_ts=ts(1.0),
        origin_system="occid.tests",
        provenance=[],
    )


def make_execution(record_uid: bytes, record_id: int, execution_uid: bytes) -> Execution:
    return Execution(
        record=make_record(record_uid, record_id),
        uid=execution_uid,
        id=1,
        assignment_uid=ASSIGNMENT_UID,
        executor_uid=OWNER_UID,
        phase=ExecutionPhase.RUNNING,
        started_at=ts(2.0),
        completed_at=ts(2.0),
        external_job_refs=[],
    )


class ContractStabilityTests(unittest.TestCase):
    def test_record_identity_is_distinct_from_domain_identity(self) -> None:
        self.assertIn("uid", Record.model_fields)
        self.assertIn("id", Record.model_fields)
        execution = make_execution(RECORD_UID_1, 1, EXECUTION_UID_1)
        self.assertNotEqual(execution.record.uid, execution.uid)
        self.assertNotEqual(execution.record.uid, execution.assignment_uid)

    def test_definitions_do_not_embed_runtime_assessment(self) -> None:
        self.assertNotIn("satisfied", SuccessCriterion.model_fields)
        self.assertNotIn("status", SuccessCriterion.model_fields)

    def test_assignment_and_execution_are_flat_runtime_models(self) -> None:
        self.assertIn("Control", occid.__all__)
        self.assertIn("Data", occid.__all__)
        self.assertEqual(Assignment.__occid_semantic_role__, "concept")
        self.assertEqual(Execution.__occid_semantic_role__, "concept")
        for model in (Assignment, Execution):
            self.assertIn("record", model.model_fields)
            self.assertIn("uid", model.model_fields)
            self.assertIn("id", model.model_fields)

    def test_execution_msgpack_round_trip(self) -> None:
        execution = Execution(
            record=make_record(RECORD_UID_2, 2),
            uid=EXECUTION_UID_2,
            id=1,
            assignment_uid=ASSIGNMENT_UID,
            executor_uid=OWNER_UID,
            attempt=3,
            phase=ExecutionPhase.RUNNING,
            progress=0.5,
            started_at=ts(3.0),
            completed_at=ts(3.0),
            external_job_refs=[],
        )
        self.assertEqual(Execution.decode(execution.encode()), execution)

    def test_source_and_generated_contracts_match(self) -> None:
        record_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/record.schema.yaml").read_text())
        objective_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/objective.schema.yaml").read_text())
        plan_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/plan.schema.yaml").read_text())
        assignment_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/control/assignment.schema.yaml").read_text())
        execution_schema = yaml.safe_load((REPO_ROOT / "lib/schema/core/data/execution.schema.yaml").read_text())

        self.assertEqual(record_schema["models"]["Record"]["fields"]["uid"], "UID")
        self.assertEqual(record_schema["models"]["Record"]["fields"]["id"], "IntID(Record)")
        self.assertNotIn("satisfied", objective_schema["models"]["SuccessCriterion"]["fields"])
        self.assertEqual(objective_schema["models"]["SuccessCriterion"]["fields"]["statement"], "string")
        self.assertNotIn("status", plan_schema["models"]["Plan"]["fields"])
        self.assertEqual(assignment_schema["models"]["Assignment"]["parent"], "Control")
        self.assertEqual(execution_schema["models"]["Execution"]["parent"], "Data")

    def test_compiled_model_ids_match_generated_models(self) -> None:
        compiled = yaml.safe_load((REPO_ROOT / "occid.yaml").read_text())
        model_ids = {
            name: spec["model_id"]
            for name, spec in compiled["models"].items()
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
