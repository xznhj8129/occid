from __future__ import annotations

import math
import unittest

from occid import AltitudeDatum, GlobalPosition, MotionCommand, MotionOperation
from interop.mavsdk import goto_command_to_fields


ENTITY_UID = bytes.fromhex("cbdf5f3e0e874bd0a50f9422ac87b686")


def move_to(position: GlobalPosition, yaw_rad: float | None = None) -> MotionCommand:
    return MotionCommand(
        target_uid=ENTITY_UID,
        constraints=[],
        operation=MotionOperation.MOVE_TO,
        destination=position,
        yaw_rad=yaw_rad,
    )


class MavsdkGotoMappingTests(unittest.TestCase):
    def test_sea_level_target_maps_directly(self) -> None:
        command = move_to(
            GlobalPosition(lat=45.5017, lon=-73.5673, alt=123.4, alt_frame=AltitudeDatum.SEA_LEVEL),
            yaw_rad=math.pi / 2.0,
        )
        fields = goto_command_to_fields(command)
        self.assertAlmostEqual(fields.latitude_deg, 45.5017)
        self.assertAlmostEqual(fields.longitude_deg, -73.5673)
        self.assertAlmostEqual(fields.absolute_altitude_m, 123.4)
        self.assertAlmostEqual(fields.yaw_deg, 90.0)

    def test_relative_target_uses_current_altitude_pair(self) -> None:
        command = move_to(
            GlobalPosition(lat=47.0, lon=8.0, alt=40.0, alt_frame=AltitudeDatum.RELATIVE)
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
        command = move_to(
            GlobalPosition(lat=47.0, lon=8.0, alt=40.0, alt_frame=AltitudeDatum.RELATIVE)
        )
        with self.assertRaisesRegex(ValueError, "current absolute and relative altitude"):
            goto_command_to_fields(command)

    def test_unspecified_yaw_defaults_to_zero(self) -> None:
        command = move_to(
            GlobalPosition(lat=47.0, lon=8.0, alt=500.0, alt_frame=AltitudeDatum.SEA_LEVEL)
        )
        self.assertEqual(goto_command_to_fields(command).yaw_deg, 0.0)

    def test_non_move_to_operation_is_rejected(self) -> None:
        command = MotionCommand(
            target_uid=ENTITY_UID,
            constraints=[],
            operation=MotionOperation.STOP,
        )
        with self.assertRaisesRegex(ValueError, "MOVE_TO"):
            goto_command_to_fields(command)


if __name__ == "__main__":
    unittest.main()
