"""Pure OCCID <-> MSP/INAV representation conversions.

The caller owns MSP transport, polling, mode activation, waypoint operations,
arming/takeoff/landing sequences, and recovery. These helpers only normalize
protocol-native values into OCCID structures or convert OCCID control values to
protocol-native scalar representations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from schema import (
    AltitudeDatum,
    AltitudeState,
    AngularVelocityVector,
    BodyReferenceFrame,
    ControlAxisSet,
    EulerAngles,
    GlobalPosition,
    GnssFixType,
    GnssSolution,
    InertialReferenceFrame,
    LocationState,
    NavigationValidity,
    StandardFlightMode,
)

from .common import degrees_to_radians, fru_to_frd_vector, pwm_to_normalized, require_finite


@dataclass(frozen=True)
class InavGpsFields:
    latitude_deg: float
    longitude_deg: float
    absolute_altitude_m: float | None
    relative_altitude_m: float | None
    fix_name: str
    fix_code: int
    satellites_used: int
    ground_speed_m_s: float | None = None
    ground_course_deg: float | None = None
    hdop: float | None = None


def standard_mode_from_native_names(native_names: Sequence[str]) -> StandardFlightMode:
    names = {str(name).upper().replace("_", " ") for name in native_names}
    if any(name in names for name in {"NAV POSHOLD", "POSHOLD", "LOITER"}):
        return StandardFlightMode.POSITION_HOLD
    if any(name in names for name in {"RTH", "NAV RTH"}):
        return StandardFlightMode.SAFE_RECOVERY
    if any(name in names for name in {"NAV WP", "MISSION"}):
        return StandardFlightMode.MISSION
    if any(name in names for name in {"NAV LAND", "LAND"}):
        return StandardFlightMode.LAND
    if any(name in names for name in {"NAV CRUISE", "CRUISE"}):
        return StandardFlightMode.CRUISE
    if any(name in names for name in {"ALT HOLD", "ALTHOLD"}):
        return StandardFlightMode.ALTITUDE_HOLD
    return StandardFlightMode.NON_STANDARD


def gnss_fix_type_from_native_name(native_name: str) -> GnssFixType:
    name = str(native_name).upper()
    if "RTK_FIXED" in name:
        return GnssFixType.RTK_FIXED
    if "RTK_FLOAT" in name:
        return GnssFixType.RTK_FLOAT
    if "DGPS" in name:
        return GnssFixType.DGPS
    if "3D" in name:
        return GnssFixType.FIX_3D
    if "2D" in name:
        return GnssFixType.FIX_2D
    if "NO_FIX" in name or "NONE" in name:
        return GnssFixType.NO_FIX
    return GnssFixType.NONE


def attitude_from_degrees(roll_deg: float, pitch_deg: float, yaw_deg: float) -> EulerAngles:
    return EulerAngles(
        roll_rad=degrees_to_radians(roll_deg, "roll_deg"),
        pitch_rad=degrees_to_radians(pitch_deg, "pitch_deg"),
        yaw_rad=degrees_to_radians(yaw_deg, "yaw_deg"),
        body_frame=BodyReferenceFrame.FRD,
        reference_frame=InertialReferenceFrame.NED,
    )


def angular_velocity_from_fru_degrees_s(
    x_deg_s: float,
    y_deg_s: float,
    z_deg_s: float,
) -> AngularVelocityVector:
    x, y, z = fru_to_frd_vector(
        degrees_to_radians(x_deg_s, "x_deg_s"),
        degrees_to_radians(y_deg_s, "y_deg_s"),
        degrees_to_radians(z_deg_s, "z_deg_s"),
    )
    return AngularVelocityVector(
        x_rad_s=x,
        y_rad_s=y,
        z_rad_s=z,
        frame=BodyReferenceFrame.FRD,
    )


def gps_to_occid(
    fields: InavGpsFields,
    *,
    navigation_validity: NavigationValidity | None = None,
) -> tuple[LocationState, GnssSolution]:
    absolute_altitude = (
        None
        if fields.absolute_altitude_m is None
        else require_finite(fields.absolute_altitude_m, "absolute_altitude_m")
    )
    relative_altitude = (
        None
        if fields.relative_altitude_m is None
        else require_finite(fields.relative_altitude_m, "relative_altitude_m")
    )
    position = GlobalPosition(
        lat=require_finite(fields.latitude_deg, "latitude_deg"),
        lon=require_finite(fields.longitude_deg, "longitude_deg"),
        alt=0.0 if absolute_altitude is None else absolute_altitude,
        alt_frame=AltitudeDatum.SEA_LEVEL,
    )
    altitude = AltitudeState(
        absolute_m=absolute_altitude,
        relative_m=relative_altitude,
        datum=AltitudeDatum.RELATIVE,
    )
    location = LocationState(
        inertial_frame=InertialReferenceFrame.NED,
        body_frame=BodyReferenceFrame.FRD,
        position=position,
        altitude=altitude,
        navigation_validity=navigation_validity,
    )
    gnss = GnssSolution(
        fix_type=gnss_fix_type_from_native_name(fields.fix_name),
        fix_code=int(fields.fix_code),
        satellites_used=int(fields.satellites_used),
        position=position,
        altitude=altitude,
        ground_speed_ms=None if fields.ground_speed_m_s is None else require_finite(fields.ground_speed_m_s, "ground_speed_m_s"),
        ground_course_deg=None if fields.ground_course_deg is None else require_finite(fields.ground_course_deg, "ground_course_deg"),
        hdop=None if fields.hdop is None else require_finite(fields.hdop, "hdop"),
    )
    return location, gnss


def rc_pwm_mapping_to_control_axes(
    channels: Mapping[str, float],
    *,
    roll_channel: str,
    pitch_channel: str,
    yaw_channel: str,
    throttle_channel: str,
    aux_channels: Sequence[str] = (),
    pwm_min_us: float,
    pwm_max_us: float,
) -> ControlAxisSet:
    return ControlAxisSet(
        roll=pwm_to_normalized(channels[roll_channel], pwm_min_us, pwm_max_us),
        pitch=pwm_to_normalized(channels[pitch_channel], pwm_min_us, pwm_max_us),
        yaw=pwm_to_normalized(channels[yaw_channel], pwm_min_us, pwm_max_us),
        throttle=pwm_to_normalized(channels[throttle_channel], pwm_min_us, pwm_max_us),
        aux=[
            pwm_to_normalized(channels[channel], pwm_min_us, pwm_max_us)
            for channel in aux_channels
            if channel in channels
        ],
    )


def rc_sequence_to_control_axes(
    values: Sequence[float],
    *,
    pwm_min_us: float = 1000.0,
    pwm_max_us: float = 2000.0,
) -> ControlAxisSet:
    """Convert a raw PWM AETR sequence [roll, pitch, throttle, yaw, ...aux]."""
    if len(values) < 4:
        raise ValueError("RC sequence requires at least four AETR values")
    return ControlAxisSet(
        roll=pwm_to_normalized(values[0], pwm_min_us, pwm_max_us),
        pitch=pwm_to_normalized(values[1], pwm_min_us, pwm_max_us),
        yaw=pwm_to_normalized(values[3], pwm_min_us, pwm_max_us),
        throttle=pwm_to_normalized(values[2], pwm_min_us, pwm_max_us),
        aux=[
            pwm_to_normalized(value, pwm_min_us, pwm_max_us)
            for value in values[4:]
        ],
    )
