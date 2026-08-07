from __future__ import annotations

import math
import unittest
from pathlib import Path

import yaml

from schema import (
    AltitudeDatum,
    ArmCommand,
    BodyReferenceFrame,
    ControlAttitudeSetpoint,
    ControlOverride,
    FlightCommand,
    GlobalPosition,
    GoToCommand,
    InertialReferenceFrame,
    LowLevelFlightCommand,
    OCCID_MODEL_ID_BY_CLASS,
    SetControlAttitudeCommand,
    SetControlOverrideCommand,
    SetModeCommand,
    SetTakeoffAltitudeCommand,
    StandardFlightMode,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class LowLevelFlightContractTests(unittest.TestCase):
    def test_low_level_commands_are_distinct_from_task_lifecycle(self) -> None:
        self.assertTrue(issubclass(LowLevelFlightCommand, FlightCommand))
        self.assertTrue(issubclass(ArmCommand, LowLevelFlightCommand))
        self.assertTrue(issubclass(SetControlAttitudeCommand, LowLevelFlightCommand))
        self.assertTrue(issubclass(SetControlOverrideCommand, LowLevelFlightCommand))

    def test_attitude_control_is_radians_with_explicit_optional_frames(self) -> None:
        fields = ControlAttitudeSetpoint.model_fields
        self.assertIn("roll_rad", fields)
        self.assertIn("pitch_rad", fields)
        self.assertIn("yaw_rad", fields)
        self.assertIn("thrust_normalized", fields)
        self.assertIn("body_frame", fields)
        self.assertIn("reference_frame", fields)
        self.assertNotIn("roll_deg", fields)
        self.assertNotIn("pitch_deg", fields)
        self.assertNotIn("yaw_deg", fields)

        setpoint = ControlAttitudeSetpoint(
            roll_rad=math.radians(12.0),
            pitch_rad=math.radians(-8.0),
            yaw_rad=math.radians(95.0),
            thrust_normalized=0.62,
            body_frame=BodyReferenceFrame.FRD,
            reference_frame=InertialReferenceFrame.NED,
        )
        command = SetControlAttitudeCommand(setpoint=setpoint)
        decoded = SetControlAttitudeCommand.decode(command.encode())
        self.assertEqual(decoded, command)
        self.assertEqual(decoded.setpoint.body_frame, BodyReferenceFrame.FRD)
        self.assertEqual(decoded.setpoint.reference_frame, InertialReferenceFrame.NED)

    def test_control_override_round_trips_as_semantic_input(self) -> None:
        override = ControlOverride(
            roll=0.15,
            pitch=-0.25,
            yaw=0.05,
            throttle=0.6,
            aux=[],
        )
        command = SetControlOverrideCommand(override=override)
        self.assertEqual(SetControlOverrideCommand.decode(command.encode()), command)

    def test_standard_mode_is_portable_and_native_mode_is_opaque(self) -> None:
        self.assertEqual(StandardFlightMode.NON_STANDARD.value, 0)
        self.assertEqual(StandardFlightMode.POSITION_HOLD.value, 1)
        self.assertEqual(StandardFlightMode.ORBIT.value, 2)
        self.assertEqual(StandardFlightMode.CRUISE.value, 3)
        self.assertEqual(StandardFlightMode.ALTITUDE_HOLD.value, 4)
        self.assertEqual(StandardFlightMode.SAFE_RECOVERY.value, 5)
        self.assertEqual(StandardFlightMode.MISSION.value, 6)
        self.assertEqual(StandardFlightMode.LAND.value, 7)
        self.assertEqual(StandardFlightMode.TAKEOFF.value, 8)

        command = SetModeCommand(
            standard_mode=StandardFlightMode.EXTERNAL_CONTROL,
            native_mode_name="OFFBOARD",
            native_mode_code=6,
        )
        self.assertEqual(SetModeCommand.decode(command.encode()), command)
        self.assertEqual(command.standard_mode, StandardFlightMode.EXTERNAL_CONTROL)
        self.assertEqual(command.native_mode_name, "OFFBOARD")

    def test_goto_yaw_and_takeoff_altitude_are_unambiguous(self) -> None:
        goto_fields = GoToCommand.model_fields
        self.assertIn("yaw_rad", goto_fields)
        self.assertNotIn("yaw_deg", goto_fields)

        position = GlobalPosition(
            lat=45.5017,
            lon=-73.5673,
            alt=120.0,
            alt_frame=AltitudeDatum.RELATIVE,
        )
        command = GoToCommand(position=position, yaw_rad=math.pi / 2.0)
        self.assertEqual(GoToCommand.decode(command.encode()), command)

        altitude_fields = SetTakeoffAltitudeCommand.model_fields
        self.assertIn("relative_altitude_m", altitude_fields)
        self.assertNotIn("altitude_m", altitude_fields)
        takeoff_altitude = SetTakeoffAltitudeCommand(relative_altitude_m=30.0)
        self.assertEqual(SetTakeoffAltitudeCommand.decode(takeoff_altitude.encode()), takeoff_altitude)

    def test_new_models_have_permanent_ids(self) -> None:
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[LowLevelFlightCommand], 287)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[SetControlAttitudeCommand], 288)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[SetControlOverrideCommand], 289)

    def test_source_schema_matches_generated_contract(self) -> None:
        command_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/control/command.schema.yaml").read_text()
        )
        input_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/data/state/input.schema.yaml").read_text()
        )
        guidance_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/data/state/guidance.schema.yaml").read_text()
        )
        spatial_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/spatial.schema.yaml").read_text()
        )

        commands = command_schema["models"]
        self.assertEqual(commands["ArmCommand"]["parent"], "LowLevelFlightCommand")
        self.assertEqual(
            commands["SetControlAttitudeCommand"]["fields"]["setpoint"],
            "ControlAttitudeSetpoint",
        )
        self.assertEqual(
            commands["SetControlOverrideCommand"]["fields"]["override"],
            "ControlOverride",
        )
        self.assertIn("yaw_rad", commands["GoToCommand"]["fields"])
        self.assertIn("relative_altitude_m", commands["SetTakeoffAltitudeCommand"]["fields"])

        attitude_fields = input_schema["models"]["ControlAttitudeSetpoint"]["fields"]
        self.assertIn("roll_rad", attitude_fields)
        self.assertIn("body_frame", attitude_fields)
        self.assertIn("reference_frame", attitude_fields)

        self.assertIn("StandardFlightMode", guidance_schema["enums"])
        self.assertNotIn("FlightMode", guidance_schema["enums"])

        euler_fields = spatial_schema["models"]["EulerAngles"]["fields"]
        self.assertIn("roll_rad", euler_fields)
        self.assertIn("body_frame", euler_fields)
        self.assertIn("reference_frame", euler_fields)


if __name__ == "__main__":
    unittest.main()
