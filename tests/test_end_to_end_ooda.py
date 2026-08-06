from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from end_to_end_ooda import run_scenario
from schema import AssignmentStatus, ExecutionPhase, TaskPhase, TaskStatus


class EndToEndOodaScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run_scenario()

    def test_all_scenario_invariants_pass(self) -> None:
        self.assertTrue(all(self.result.assertions.values()))

    def test_closed_loop_reaches_successful_operational_state(self) -> None:
        self.assertEqual(self.result.records["objective_complete"].status, TaskStatus.COMPLETE)
        self.assertEqual(self.result.records["assignment_complete"].status, AssignmentStatus.COMPLETE)
        self.assertEqual(self.result.records["execution_complete"].phase, ExecutionPhase.SUCCEEDED)
        self.assertEqual(self.result.records["task_complete"].phase, TaskPhase.DONE_OK)

    def test_identity_and_runtime_state_remain_separate(self) -> None:
        initial_state = self.result.records["initial_state"]
        final_state = self.result.records["final_state"]
        executor = self.result.records["executor"]
        self.assertEqual(initial_state.subject_id, executor.entity_id)
        self.assertEqual(final_state.subject_id, executor.entity_id)
        self.assertNotEqual(initial_state.record.record_id, final_state.record.record_id)

    def test_control_records_remain_distinct_and_correlated(self) -> None:
        objective = self.result.records["objective"]
        task = self.result.records["task"]
        plan = self.result.records["plan"]
        assignment = self.result.records["assignment"]
        execution = self.result.records["execution"]

        self.assertIn(objective.objective_id, plan.objective_ids)
        self.assertIn(task.task_id, plan.task_ids)
        self.assertIn(assignment.assignment_id, plan.assignments)
        self.assertEqual(execution.assignment_id, assignment.assignment_id)
        self.assertNotEqual(task.task_id, assignment.assignment_id)
        self.assertNotEqual(assignment.assignment_id, execution.execution_id)

    def test_every_trace_entry_crossed_a_real_occid_boundary(self) -> None:
        self.assertGreaterEqual(len(self.result.trace), 20)
        self.assertTrue(all(entry.model_id >= 0 for entry in self.result.trace))
        self.assertTrue(all(entry.wire_bytes > 0 for entry in self.result.trace))

    def test_observation_closes_the_feedback_loop(self) -> None:
        result = self.result.records["isr_result"]
        self.assertGreaterEqual(len(result.observations), 1)
        self.assertIsNotNone(result.observations[0].position)
        self.assertGreaterEqual(len(result.track_updates), 1)


if __name__ == "__main__":
    unittest.main()
