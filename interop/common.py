"""Pure conversion helpers shared by OCCID interoperability modules.

This module contains deterministic representation conversion only. It must not
perform I/O, endpoint discovery, retries, sequencing, or operation selection.
"""

from __future__ import annotations

import math


def require_finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def degrees_to_radians(value: float, name: str = "angle_deg") -> float:
    return math.radians(require_finite(value, name))


def radians_to_degrees(value: float, name: str = "angle_rad") -> float:
    return math.degrees(require_finite(value, name))


def fru_to_frd_vector(x: float, y: float, z_up: float) -> tuple[float, float, float]:
    """Convert a body Forward-Right-Up vector to Forward-Right-Down."""
    return (
        require_finite(x, "x"),
        require_finite(y, "y"),
        -require_finite(z_up, "z_up"),
    )


def pwm_to_normalized(value_us: float, pwm_min_us: float, pwm_max_us: float) -> float:
    """Convert a PWM value to the normalized [0, 1] representation."""
    value = require_finite(value_us, "value_us")
    low = require_finite(pwm_min_us, "pwm_min_us")
    high = require_finite(pwm_max_us, "pwm_max_us")
    if high <= low:
        raise ValueError("pwm_max_us must be greater than pwm_min_us")
    if value < low or value > high:
        raise ValueError(f"PWM value {value} outside [{low}, {high}]")
    return (value - low) / (high - low)


def normalized_to_pwm(value: float, pwm_min_us: float, pwm_max_us: float) -> int:
    """Convert normalized [0, 1] input to a rounded PWM value."""
    normalized = require_finite(value, "value")
    low = require_finite(pwm_min_us, "pwm_min_us")
    high = require_finite(pwm_max_us, "pwm_max_us")
    if high <= low:
        raise ValueError("pwm_max_us must be greater than pwm_min_us")
    if normalized < 0.0 or normalized > 1.0:
        raise ValueError(f"normalized value {normalized} outside [0, 1]")
    return int(round(low + normalized * (high - low)))
