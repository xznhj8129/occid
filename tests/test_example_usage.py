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
)


class ExampleFixtureTests(unittest.TestCase):
    def test_raw_cot_fixture_is_real_input(self) -> None:
        cot = parse_cot_xml(COT_XML)
        self.assertEqual(cot.uid, "contact-route6-1")
        self.assertEqual(cot.callsign, "CONTACT-1")
        self.assertAlmostEqual(cot.point.lat_deg, 45.5024)
        self.assertAlmostEqual(cot.point.lon_deg, -73.5665)
        self.assertAlmostEqual(cot.point.ce_m, 6.0)

    def test_raw_mavlink_fixture_is_parsed_and_crc_checked(self) -> None:
        mavlink = parse_mavlink_global_position(MAVLINK_GLOBAL_POSITION_INT)
        self.assertEqual(mavlink.system_id, 7)
        self.assertEqual(mavlink.component_id, 1)
        self.assertEqual(mavlink.time_boot_ms, 123456)
        self.assertAlmostEqual(mavlink.latitude_deg, 45.5017)
        self.assertAlmostEqual(mavlink.longitude_deg, -73.5673)
        self.assertAlmostEqual(mavlink.absolute_altitude_m, 120.0)
        self.assertAlmostEqual(mavlink.relative_altitude_m, 40.0)


if __name__ == "__main__":
    unittest.main()
