from __future__ import annotations

import math
import unittest

from occid import AltitudeDatum, GlobalPosition, GoToCommand
from interop.mavsdk import goto_command_to_fields


class MavsdkGotoMappingTests(unittest.TestCase):
    def test_sea_level_target_maps_directly(self) -> None:
        command = GoToCommand(
            position=GlobalPosition(
                lat=45.5017,
                lon=-73.5673,
                alt=123.4,
                alt_frame=AltitudeDatum.SEA_LEVEL,
            ),
            yaw_rad=math.pi / 2.0,
        )
        fields = goto_command_to_fields(command)
        self.assertAlmostEqual(fields.latitude_deg, 45.5017)
        self.assertAlmostEqual(fields.longitude_deg, -73.5673)
        self.assertAlmostEqual(fields.absolute_altitude_m, 123.4)
        self.assertAlmostEqual(fields.yaw_deg, 90.0)

    def test_relative_target_uses_current_altitude_pair(self) -> None:
        command = GoToCommand(
            position=GlobalPosition(
                lat=47.0,
                lon=8.0,
                alt=40.0,
                alt_frame=AltitudeDatum.RELATIVE,
            )
        )
        fields = goto_command_to_fields(
            command,
            current_absolute_altitude_m=510.0,
            current_relative_altitude_m=10.0,
            current_yaw_rad=math.pi,
        )
        self.assertAlmostEqual(fields.absolute_altitude_m, 540.0)
        self.assertAlmostEqual(fields.yaw_deg, 180.0)

    def test_relative_target_requires_reference_altitudes(self) -> None:
        command = GoToCommand(
            position=GlobalPosition(
                lat=47.0,
                lon=8.0,
                alt=40.0,
                alt_frame=AltitudeDatum.RELATIVE,
            )
        )
        with self.assertRaisesRegex(ValueError, "current absolute and relative altitude"):
            goto_command_to_fields(command)

    def test_unspecified_yaw_defaults_to_zero(self) -> None:
        command = GoToCommand(
            position=GlobalPosition(
                lat=47.0,
                lon=8.0,
                alt=500.0,
                alt_frame=AltitudeDatum.SEA_LEVEL,
            )
        )
        self.assertEqual(goto_command_to_fields(command).yaw_deg, 0.0)


if __name__ == "__main__":
    unittest.main()
