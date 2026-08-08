from __future__ import annotations

import math
import unittest
from pathlib import Path

import yaml

import occid
from occid import (
    AltitudeDatum,
    ArmCommand,
    AutopilotMissionWaypoint,
    BeginDirectControlCommand,
    BodyReferenceFrame,
    Command,
    ControlAttitudeSetpoint,
    ControlOverride,
    DirectControlCommand,
    DirectControlMode,
    EndDirectControlCommand,
    FlightCommand,
    GlobalPosition,
    GoToCommand,
    Input,
    InertialReferenceFrame,
    ModeCommand,
    NavigationCommand,
    OCCID_MODEL_ID_BY_CLASS,
    SetModeCommand,
    SetTakeoffAltitudeCommand,
    SetWaypointCommand,
    StandardFlightMode,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class FlightControlContractTests(unittest.TestCase):
    def test_command_families_are_semantically_decomposed(self) -> None:
        self.assertTrue(issubclass(ArmCommand, FlightCommand))
        self.assertTrue(issubclass(GoToCommand, NavigationCommand))
        self.assertTrue(issubclass(SetModeCommand, ModeCommand))
        self.assertTrue(issubclass(BeginDirectControlCommand, DirectControlCommand))
        self.assertTrue(issubclass(EndDirectControlCommand, DirectControlCommand))
        self.assertFalse(hasattr(occid, "LowLevelFlightCommand"))
        self.assertFalse(hasattr(occid, "StartOffboardCommand"))
        self.assertFalse(hasattr(occid, "StopOffboardCommand"))

    def test_high_rate_control_samples_are_inputs_not_commands(self) -> None:
        self.assertTrue(issubclass(ControlAttitudeSetpoint, Input))
        self.assertTrue(issubclass(ControlOverride, Input))
        self.assertFalse(issubclass(ControlAttitudeSetpoint, Command))
        self.assertFalse(issubclass(ControlOverride, Command))
        self.assertFalse(hasattr(occid, "SetControlAttitudeCommand"))
        self.assertFalse(hasattr(occid, "SetControlOverrideCommand"))

        setpoint = ControlAttitudeSetpoint(
            roll_rad=math.radians(12.0),
            pitch_rad=math.radians(-8.0),
            yaw_rad=math.radians(95.0),
            thrust_normalized=0.62,
            body_frame=BodyReferenceFrame.FRD,
            reference_frame=InertialReferenceFrame.NED,
        )
        self.assertEqual(ControlAttitudeSetpoint.decode(setpoint.encode()), setpoint)

    def test_direct_control_session_is_endpoint_neutral(self) -> None:
        begin = BeginDirectControlCommand(mode=DirectControlMode.ATTITUDE_THRUST)
        self.assertEqual(BeginDirectControlCommand.decode(begin.encode()), begin)
        end = EndDirectControlCommand()
        self.assertEqual(EndDirectControlCommand.decode(end.encode()), end)

    def test_mode_activation_is_distinct_from_actions(self) -> None:
        command = SetModeCommand(
            native_mode_name="NAV POSHOLD",
            enabled=False,
        )
        self.assertEqual(SetModeCommand.decode(command.encode()), command)
        self.assertFalse(command.enabled)
        self.assertIsNone(command.standard_mode)

        portable = SetModeCommand(
            standard_mode=StandardFlightMode.POSITION_HOLD,
            enabled=True,
        )
        self.assertEqual(portable.standard_mode, StandardFlightMode.POSITION_HOLD)

    def test_navigation_commands_include_explicit_waypoint_write(self) -> None:
        position = GlobalPosition(
            lat=45.5017,
            lon=-73.5673,
            alt=120.0,
            alt_frame=AltitudeDatum.RELATIVE,
        )
        goto = GoToCommand(position=position, yaw_rad=math.pi / 2.0)
        self.assertEqual(GoToCommand.decode(goto.encode()), goto)

        waypoint = AutopilotMissionWaypoint(
            waypoint_index=4,
            action_code=1,
            position=position,
            param1=0,
            param2=0,
            param3=0,
            flag=0,
        )
        command = SetWaypointCommand(waypoint=waypoint)
        self.assertEqual(SetWaypointCommand.decode(command.encode()), command)

    def test_takeoff_altitude_remains_explicit(self) -> None:
        altitude_fields = SetTakeoffAltitudeCommand.model_fields
        self.assertIn("relative_altitude_m", altitude_fields)
        self.assertNotIn("altitude_m", altitude_fields)

    def test_new_model_ids_do_not_reuse_retired_ids(self) -> None:
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[NavigationCommand], 290)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[SetWaypointCommand], 291)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[ModeCommand], 292)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[DirectControlCommand], 293)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[BeginDirectControlCommand], 294)
        self.assertEqual(OCCID_MODEL_ID_BY_CLASS[EndDirectControlCommand], 295)
        self.assertEqual(occid.OCCID_SCHEMA_VERSION, (4, 0, 0))

    def test_source_schema_matches_generated_contract(self) -> None:
        command_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/control/command.schema.yaml").read_text()
        )
        spatial_schema = yaml.safe_load(
            (REPO_ROOT / "lib/schema/core/spatial.schema.yaml").read_text()
        )

        commands = command_schema["models"]
        self.assertEqual(commands["ArmCommand"]["parent"], "FlightCommand")
        self.assertEqual(commands["GoToCommand"]["parent"], "NavigationCommand")
        self.assertEqual(commands["SetModeCommand"]["parent"], "ModeCommand")
        self.assertEqual(commands["BeginDirectControlCommand"]["parent"], "DirectControlCommand")
        self.assertEqual(commands["EndDirectControlCommand"]["parent"], "DirectControlCommand")
        self.assertNotIn("LowLevelFlightCommand", commands)
        self.assertNotIn("StartOffboardCommand", commands)
        self.assertNotIn("SetControlAttitudeCommand", commands)

        altitude_fields = spatial_schema["models"]["AltitudeState"]["fields"]
        self.assertEqual(altitude_fields["absolute_datum"], "optional AltitudeDatum")
        self.assertEqual(altitude_fields["relative_datum"], "optional AltitudeDatum")
        self.assertNotIn("datum", altitude_fields)


if __name__ == "__main__":
    unittest.main()
