from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from end_to_end_ooda import run_scenario
from occid import AssignmentStatus, ExecutionPhase, TaskPhase, TaskStatus


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

    def test_control_records_remain_distinct_and_correlated(self) -> None:
        objective = self.result.records["objective"]
        task = self.result.records["task"]
        authority = self.result.records["authority"]
        plan = self.result.records["plan"]
        assignment = self.result.records["assignment"]
        execution = self.result.records["execution"]

        self.assertEqual(task.objective_id, objective.objective_id)
        self.assertIn(objective.objective_id, plan.objective_ids)
        self.assertIn(task.task_id, plan.task_ids)
        self.assertIn(assignment.assignment_id, plan.assignments)
        self.assertEqual(assignment.authority_id, authority.authority_id)
        self.assertEqual(execution.assignment_id, assignment.assignment_id)
        self.assertNotEqual(task.task_id, assignment.assignment_id)
        self.assertNotEqual(assignment.assignment_id, execution.execution_id)

    def test_task_survives_assignment_and_execution_without_assignee_field(self) -> None:
        task = self.result.records["task"]
        self.assertFalse(hasattr(task, "assignee_id"))
        self.assertIn("Search Route 6", task.instruction)

    def test_every_trace_entry_crossed_a_real_occid_boundary(self) -> None:
        self.assertGreaterEqual(len(self.result.trace), 15)
        self.assertTrue(all(entry.model_id >= 0 for entry in self.result.trace))
        self.assertTrue(all(entry.wire_bytes > 0 for entry in self.result.trace))


if __name__ == "__main__":
    unittest.main()
