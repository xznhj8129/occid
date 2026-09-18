"""Pure OCCID <-> MAVSDK representation conversions.

This module does not connect to MAVSDK and does not choose which MAVSDK action
or offboard operation to call. Callers select the operation; these helpers only
convert the selected operation's typed values.
"""

from __future__ import annotations

from dataclasses import dataclass

from occid import (
    AltitudeDatum,
    AltitudeState,
    AngularVelocityVector,
    BodyReferenceFrame,
    ControlAttitudeSetpoint,
    EulerAngles,
    GlobalPosition,
    GnssFixType,
    InertialReferenceFrame,
    LocationState,
    MotionCommand,
    MotionOperation,
    NavigationValidity,
    StandardFlightMode,
)

from .common import degrees_to_radians, radians_to_degrees, require_finite


@dataclass(frozen=True)
class MavsdkAttitudeFields:
    roll_deg: float
    pitch_deg: float
    yaw_deg: float
    thrust_value: float


@dataclass(frozen=True)
class MavsdkPositionFields:
    latitude_deg: float
    longitude_deg: float
    absolute_altitude_m: float
    relative_altitude_m: float


@dataclass(frozen=True)
class MavsdkGotoFields:
    latitude_deg: float
    longitude_deg: float
    absolute_altitude_m: float
    yaw_deg: float


def standard_mode_from_native_name(native_name: str) -> StandardFlightMode:
    name = str(native_name).upper()
    mapping = {
        "HOLD": StandardFlightMode.POSITION_HOLD,
        "POSCTL": StandardFlightMode.POSITION_HOLD,
        "POSHOLD": StandardFlightMode.POSITION_HOLD,
        "LOITER": StandardFlightMode.POSITION_HOLD,
        "ORBIT": StandardFlightMode.ORBIT,
        "CRUISE": StandardFlightMode.CRUISE,
        "ALTCTL": StandardFlightMode.ALTITUDE_HOLD,
        "ALT_HOLD": StandardFlightMode.ALTITUDE_HOLD,
        "RETURN_TO_LAUNCH": StandardFlightMode.SAFE_RECOVERY,
        "RTL": StandardFlightMode.SAFE_RECOVERY,
        "RTH": StandardFlightMode.SAFE_RECOVERY,
        "MISSION": StandardFlightMode.MISSION,
        "AUTO_MISSION": StandardFlightMode.MISSION,
        "LAND": StandardFlightMode.LAND,
        "LANDING": StandardFlightMode.LAND,
        "TAKEOFF": StandardFlightMode.TAKEOFF,
        "OFFBOARD": StandardFlightMode.EXTERNAL_CONTROL,
        "GUIDED": StandardFlightMode.EXTERNAL_CONTROL,
    }
    return mapping.get(name, StandardFlightMode.NON_STANDARD)


def gnss_fix_type_from_native_value(native_value: int) -> GnssFixType:
    mapping = {
        0: GnssFixType.NONE,
        1: GnssFixType.NO_FIX,
        2: GnssFixType.FIX_2D,
        3: GnssFixType.FIX_3D,
        4: GnssFixType.DGPS,
        5: GnssFixType.RTK_FLOAT,
        6: GnssFixType.RTK_FIXED,
    }
    return mapping.get(int(native_value), GnssFixType.NONE)


def attitude_from_euler_degrees(roll_deg: float, pitch_deg: float, yaw_deg: float) -> EulerAngles:
    return EulerAngles(
        roll_rad=degrees_to_radians(roll_deg, "roll_deg"),
        pitch_rad=degrees_to_radians(pitch_deg, "pitch_deg"),
        yaw_rad=degrees_to_radians(yaw_deg, "yaw_deg"),
        body_frame=BodyReferenceFrame.FRD,
        reference_frame=InertialReferenceFrame.NED,
    )


def angular_velocity_from_body_rates(
    roll_rad_s: float,
    pitch_rad_s: float,
    yaw_rad_s: float,
) -> AngularVelocityVector:
    return AngularVelocityVector(
        x_rad_s=require_finite(roll_rad_s, "roll_rad_s"),
        y_rad_s=require_finite(pitch_rad_s, "pitch_rad_s"),
        z_rad_s=require_finite(yaw_rad_s, "yaw_rad_s"),
        frame=BodyReferenceFrame.FRD,
    )


def position_to_location_state(
    fields: MavsdkPositionFields,
    *,
    navigation_validity: NavigationValidity | None = None,
) -> LocationState:
    absolute_altitude = require_finite(fields.absolute_altitude_m, "absolute_altitude_m")
    relative_altitude = require_finite(fields.relative_altitude_m, "relative_altitude_m")
    return LocationState(
        inertial_frame=InertialReferenceFrame.NED,
        body_frame=BodyReferenceFrame.FRD,
        position=GlobalPosition(
            lat=require_finite(fields.latitude_deg, "latitude_deg"),
            lon=require_finite(fields.longitude_deg, "longitude_deg"),
            alt=absolute_altitude,
            alt_frame=AltitudeDatum.SEA_LEVEL,
        ),
        altitude=AltitudeState(
            absolute_m=absolute_altitude,
            absolute_datum=AltitudeDatum.SEA_LEVEL,
            relative_m=relative_altitude,
            relative_datum=AltitudeDatum.RELATIVE,
        ),
        navigation_validity=navigation_validity,
    )


def goto_command_to_fields(
    command: MotionCommand,
    *,
    current_absolute_altitude_m: float | None = None,
    current_relative_altitude_m: float | None = None,
    current_yaw_rad: float | None = None,
) -> MavsdkGotoFields:
    """Convert an OCCID MOVE_TO MotionCommand to MAVSDK goto_location fields.

    MAVSDK's ``goto_location`` accepts absolute sea-level altitude. OCCID can
    express either sea-level or relative altitude, so conversion of a relative
    target requires the caller's current absolute and relative altitude samples.
    The caller still owns connection state, retries, and execution policy; this
    helper owns only the deterministic representation conversion.
    """
    if command.operation != MotionOperation.MOVE_TO:
        raise ValueError(f"MAVSDK goto requires MotionOperation.MOVE_TO, got {command.operation}")
    if command.destination is None:
        raise ValueError("MAVSDK goto requires MotionCommand.destination")

    position = command.destination
    latitude_deg = require_finite(position.lat, "destination.lat")
    longitude_deg = require_finite(position.lon, "destination.lon")
    target_altitude_m = require_finite(position.alt, "destination.alt")

    if position.alt_frame == AltitudeDatum.SEA_LEVEL:
        absolute_altitude_m = target_altitude_m
    elif position.alt_frame == AltitudeDatum.RELATIVE:
        if current_absolute_altitude_m is None or current_relative_altitude_m is None:
            raise ValueError(
                "relative MAVSDK goto requires current absolute and relative altitude"
            )
        current_absolute = require_finite(
            current_absolute_altitude_m, "current_absolute_altitude_m"
        )
        current_relative = require_finite(
            current_relative_altitude_m, "current_relative_altitude_m"
        )
        absolute_altitude_m = current_absolute + (target_altitude_m - current_relative)
    else:
        raise ValueError(f"unsupported MAVSDK goto altitude datum {position.alt_frame}")

    if command.yaw_rad is not None:
        yaw_rad = command.yaw_rad
    elif current_yaw_rad is not None:
        yaw_rad = current_yaw_rad
    else:
        yaw_rad = 0.0

    return MavsdkGotoFields(
        latitude_deg=latitude_deg,
        longitude_deg=longitude_deg,
        absolute_altitude_m=require_finite(absolute_altitude_m, "absolute_altitude_m"),
        yaw_deg=radians_to_degrees(yaw_rad, "yaw_rad"),
    )


def attitude_setpoint_to_fields(setpoint: ControlAttitudeSetpoint) -> MavsdkAttitudeFields:
    if setpoint.body_frame != BodyReferenceFrame.FRD:
        raise ValueError(f"MAVSDK attitude setpoint requires FRD body frame, got {setpoint.body_frame}")
    if setpoint.reference_frame != InertialReferenceFrame.NED:
        raise ValueError(
            f"MAVSDK attitude setpoint requires NED reference frame, got {setpoint.reference_frame}"
        )
    thrust = require_finite(setpoint.thrust_normalized, "thrust_normalized")
    if thrust < 0.0 or thrust > 1.0:
        raise ValueError(f"thrust_normalized {thrust} outside [0, 1]")
    return MavsdkAttitudeFields(
        roll_deg=radians_to_degrees(setpoint.roll_rad, "roll_rad"),
        pitch_deg=radians_to_degrees(setpoint.pitch_rad, "pitch_rad"),
        yaw_deg=radians_to_degrees(setpoint.yaw_rad, "yaw_rad"),
        thrust_value=thrust,
    )
