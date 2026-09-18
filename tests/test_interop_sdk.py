from __future__ import annotations

import math
import unittest

from interop.common import normalized_to_pwm, pwm_to_normalized
from interop.cot import CotPointFields, cot_point_to_location_state, location_state_to_cot_point
from interop.mavsdk import (
    attitude_from_euler_degrees,
    attitude_setpoint_to_fields,
    gnss_fix_type_from_native_value,
    position_to_location_state,
    MavsdkPositionFields,
    standard_mode_from_native_name,
)
from interop.msp import (
    InavGpsFields,
    angular_velocity_from_fru_degrees_s,
    attitude_from_degrees,
    gps_to_occid,
    rc_sequence_to_control_axes,
    standard_mode_from_native_names,
)
from occid import (
    AltitudeDatum,
    BodyReferenceFrame,
    ControlAttitudeSetpoint,
    GnssFixType,
    InertialReferenceFrame,
    NavigationValidity,
    StandardFlightMode,
)


class InteropSdkTests(unittest.TestCase):
    def test_pwm_normalization_round_trip(self) -> None:
        self.assertEqual(pwm_to_normalized(1000, 1000, 2000), -1.0)
        self.assertEqual(pwm_to_normalized(1500, 1000, 2000), 0.0)
        self.assertEqual(pwm_to_normalized(2000, 1000, 2000), 1.0)
        self.assertEqual(normalized_to_pwm(-1.0, 1000, 2000), 1000)
        self.assertEqual(normalized_to_pwm(0.0, 1000, 2000), 1500)
        self.assertEqual(normalized_to_pwm(1.0, 1000, 2000), 2000)
        with self.assertRaises(ValueError):
            pwm_to_normalized(999, 1000, 2000)
        with self.assertRaises(ValueError):
            normalized_to_pwm(1.01, 1000, 2000)
        with self.assertRaises(ValueError):
            normalized_to_pwm(-1.01, 1000, 2000)

    def test_cot_point_round_trip_preserves_hae_and_uncertainty(self) -> None:
        point = CotPointFields(
            lat_deg=45.5017,
            lon_deg=-73.5673,
            hae_m=124.5,
            ce_m=7.0,
            le_m=11.0,
        )
        location = cot_point_to_location_state(point)
        self.assertEqual(location.position.alt_frame, AltitudeDatum.WGS84_ELLIPSOID)
        self.assertEqual(location.position.alt, 124.5)
        self.assertEqual(location.uncertainty.horiz_err_m, 7.0)
        self.assertEqual(location.uncertainty.vert_err_m, 11.0)
        self.assertEqual(location_state_to_cot_point(location), point)

    def test_mavsdk_position_keeps_absolute_and_relative_datums_distinct(self) -> None:
        location = position_to_location_state(
            MavsdkPositionFields(
                latitude_deg=45.5,
                longitude_deg=-73.5,
                absolute_altitude_m=135.0,
                relative_altitude_m=15.0,
            )
        )
        self.assertEqual(location.altitude.absolute_m, 135.0)
        self.assertEqual(location.altitude.absolute_datum, AltitudeDatum.SEA_LEVEL)
        self.assertEqual(location.altitude.relative_m, 15.0)
        self.assertEqual(location.altitude.relative_datum, AltitudeDatum.RELATIVE)

    def test_mavsdk_euler_and_attitude_setpoint_conversion(self) -> None:
        attitude = attitude_from_euler_degrees(12.0, -8.0, 95.0)
        self.assertAlmostEqual(attitude.roll_rad, math.radians(12.0))
        self.assertEqual(attitude.body_frame, BodyReferenceFrame.FRD)
        self.assertEqual(attitude.reference_frame, InertialReferenceFrame.NED)

        fields = attitude_setpoint_to_fields(
            ControlAttitudeSetpoint(
                roll_rad=math.radians(12.0),
                pitch_rad=math.radians(-8.0),
                yaw_rad=math.radians(95.0),
                thrust_normalized=0.62,
                body_frame=BodyReferenceFrame.FRD,
                reference_frame=InertialReferenceFrame.NED,
            )
        )
        self.assertAlmostEqual(fields.roll_deg, 12.0)
        self.assertAlmostEqual(fields.pitch_deg, -8.0)
        self.assertAlmostEqual(fields.yaw_deg, 95.0)
        self.assertEqual(fields.thrust_value, 0.62)

    def test_mavsdk_enum_normalization(self) -> None:
        self.assertEqual(standard_mode_from_native_name("OFFBOARD"), StandardFlightMode.EXTERNAL_CONTROL)
        self.assertEqual(standard_mode_from_native_name("RTL"), StandardFlightMode.SAFE_RECOVERY)
        self.assertEqual(standard_mode_from_native_name("made_up_mode"), StandardFlightMode.NON_STANDARD)
        self.assertEqual(gnss_fix_type_from_native_value(3), GnssFixType.FIX_3D)
        self.assertEqual(gnss_fix_type_from_native_value(6), GnssFixType.RTK_FIXED)

    def test_msp_attitude_and_fru_rate_conversion(self) -> None:
        attitude = attitude_from_degrees(10.0, -5.0, 180.0)
        self.assertAlmostEqual(attitude.roll_rad, math.radians(10.0))
        self.assertEqual(attitude.body_frame, BodyReferenceFrame.FRD)
        rates = angular_velocity_from_fru_degrees_s(90.0, -45.0, 30.0)
        self.assertAlmostEqual(rates.x_rad_s, math.radians(90.0))
        self.assertAlmostEqual(rates.y_rad_s, math.radians(-45.0))
        self.assertAlmostEqual(rates.z_rad_s, -math.radians(30.0))
        self.assertEqual(rates.frame, BodyReferenceFrame.FRD)

    def test_msp_raw_rc_sequence_is_normalized_using_endpoint_bounds(self) -> None:
        controls = rc_sequence_to_control_axes(
            [900, 1500, 2100, 1200, 1800],
            pwm_min_us=900,
            pwm_max_us=2100,
        )
        self.assertEqual(controls.roll, -1.0)
        self.assertEqual(controls.pitch, 0.0)
        self.assertEqual(controls.throttle, 1.0)
        self.assertEqual(controls.yaw, -0.5)
        self.assertEqual(controls.aux, [0.5])

    def test_msp_gps_struct_conversion(self) -> None:
        validity = NavigationValidity(local_position_ok=True, global_position_ok=True, home_position_ok=True)
        location, gnss = gps_to_occid(
            InavGpsFields(
                latitude_deg=45.5,
                longitude_deg=-73.5,
                absolute_altitude_m=135.0,
                relative_altitude_m=15.0,
                fix_name="GPS_FIX_3D",
                fix_code=2,
                satellites_used=12,
                ground_speed_m_s=4.2,
                ground_course_deg=123.0,
                hdop=0.9,
            ),
            navigation_validity=validity,
        )
        self.assertEqual(location.position.alt_frame, AltitudeDatum.SEA_LEVEL)
        self.assertEqual(location.altitude.absolute_datum, AltitudeDatum.SEA_LEVEL)
        self.assertEqual(location.altitude.relative_m, 15.0)
        self.assertEqual(location.altitude.relative_datum, AltitudeDatum.RELATIVE)
        self.assertEqual(gnss.fix_type, GnssFixType.FIX_3D)
        self.assertEqual(gnss.satellites_used, 12)
        self.assertEqual(location.navigation_validity, validity)

    def test_inav_mode_normalization(self) -> None:
        self.assertEqual(
            standard_mode_from_native_names(["NAV_RTH"]),
            StandardFlightMode.SAFE_RECOVERY,
        )
        self.assertEqual(
            standard_mode_from_native_names(["NAV_POSHOLD"]),
            StandardFlightMode.POSITION_HOLD,
        )


if __name__ == "__main__":
    unittest.main()
