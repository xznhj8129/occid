from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from example_usage import (
    COT_XML,
    MAVLINK_GLOBAL_POSITION_INT,
    parse_cot_xml,
    parse_mavlink_global_position,
    run_example,
)
from occid import AltitudeDatum, ObservationKind


class ExampleUsageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = run_example()

    def test_raw_cot_example_is_actually_parsed(self) -> None:
        cot = parse_cot_xml(COT_XML)
        self.assertEqual(cot.uid, "contact-route6-1")
        self.assertEqual(cot.callsign, "CONTACT-1")
        self.assertAlmostEqual(cot.point.lat_deg, 45.5024)
        self.assertAlmostEqual(cot.point.lon_deg, -73.5665)
        self.assertAlmostEqual(cot.point.ce_m, 6.0)

    def test_raw_mavlink_example_is_actually_parsed_and_checked(self) -> None:
        mavlink = parse_mavlink_global_position(MAVLINK_GLOBAL_POSITION_INT)
        self.assertEqual(mavlink.system_id, 7)
        self.assertEqual(mavlink.component_id, 1)
        self.assertEqual(mavlink.time_boot_ms, 123456)
        self.assertAlmostEqual(mavlink.latitude_deg, 45.5017)
        self.assertAlmostEqual(mavlink.longitude_deg, -73.5673)
        self.assertAlmostEqual(mavlink.absolute_altitude_m, 120.0)
        self.assertAlmostEqual(mavlink.relative_altitude_m, 40.0)

    def test_protocol_inputs_become_different_semantic_records(self) -> None:
        observation = self.result.records["contact_observation"]
        uav_state = self.result.records["uav_state"]

        self.assertEqual(observation.observation_kind, ObservationKind.TRACK)
        self.assertEqual(observation.position.alt_frame, AltitudeDatum.WGS84_ELLIPSOID)
        self.assertEqual(uav_state.position.position.alt_frame, AltitudeDatum.SEA_LEVEL)
        self.assertEqual(uav_state.subject_id, self.result.records["uav"].entity_id)

    def test_control_flow_uses_normalized_records(self) -> None:
        observation = self.result.records["contact_observation"]
        task = self.result.records["task"]
        assignment = self.result.records["assignment"]
        execution = self.result.records["execution"]
        uav = self.result.records["uav"]

        self.assertIn(observation.track_id, task.target_refs)
        self.assertEqual(assignment.task_id, task.task_id)
        self.assertEqual(assignment.assignee_id, uav.entity_id)
        self.assertEqual(execution.assignment_id, assignment.assignment_id)

    def test_outbound_operation_uses_semantics_not_blind_field_copying(self) -> None:
        observation = self.result.records["contact_observation"]
        move = self.result.records["move"]
        goto = self.result.outbound_goto

        self.assertEqual(move.destination.alt_frame, AltitudeDatum.RELATIVE)
        self.assertAlmostEqual(move.destination.alt, 60.0)
        self.assertAlmostEqual(goto.latitude_deg, observation.position.lat)
        self.assertAlmostEqual(goto.longitude_deg, observation.position.lon)
        self.assertAlmostEqual(goto.absolute_altitude_m, 140.0)
        self.assertNotAlmostEqual(goto.absolute_altitude_m, observation.position.alt)

    def test_occid_round_trips_and_story_checks_pass(self) -> None:
        self.assertGreaterEqual(len(self.result.trace), 9)
        self.assertTrue(all(entry.wire_bytes > 0 for entry in self.result.trace))
        self.assertTrue(all(self.result.assertions.values()))


if __name__ == "__main__":
    unittest.main()
