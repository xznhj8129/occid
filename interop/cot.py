"""Deterministic Cursor-on-Target structure conversions.

The caller owns XML parsing/serialization, external identity mapping, record
identity, provenance, network sessions, and publication policy. This module only
maps the CoT point representation to and from OCCID spatial structures.
"""

from __future__ import annotations

from dataclasses import dataclass

from schema import AltitudeDatum, GlobalPosition, LocationState, LocationUncertainty

from .common import require_finite


@dataclass(frozen=True)
class CotPointFields:
    """Protocol-native CoT point fields in engineering units."""

    lat_deg: float
    lon_deg: float
    hae_m: float
    ce_m: float | None = None
    le_m: float | None = None


def cot_point_to_location_state(point: CotPointFields) -> LocationState:
    ce = None if point.ce_m is None else require_finite(point.ce_m, "ce_m")
    le = None if point.le_m is None else require_finite(point.le_m, "le_m")
    return LocationState(
        position=GlobalPosition(
            lat=require_finite(point.lat_deg, "lat_deg"),
            lon=require_finite(point.lon_deg, "lon_deg"),
            alt=require_finite(point.hae_m, "hae_m"),
            alt_frame=AltitudeDatum.SEA_LEVEL,
        ),
        uncertainty=LocationUncertainty(horiz_err_m=ce, vert_err_m=le),
    )


def location_state_to_cot_point(location: LocationState) -> CotPointFields:
    if location.position is None:
        raise ValueError("LocationState requires a global position for CoT conversion")
    position = location.position
    if position.alt_frame != AltitudeDatum.SEA_LEVEL:
        raise ValueError(f"CoT requires SEA_LEVEL/HAE altitude, got {position.alt_frame}")
    uncertainty = location.uncertainty
    return CotPointFields(
        lat_deg=require_finite(position.lat, "lat"),
        lon_deg=require_finite(position.lon, "lon"),
        hae_m=require_finite(position.alt, "alt"),
        ce_m=None if uncertainty is None or uncertainty.horiz_err_m is None else require_finite(uncertainty.horiz_err_m, "horiz_err_m"),
        le_m=None if uncertainty is None or uncertainty.vert_err_m is None else require_finite(uncertainty.vert_err_m, "vert_err_m"),
    )


def global_position_to_cot_point(position: GlobalPosition, *, ce_m: float | None = None, le_m: float | None = None) -> CotPointFields:
    if position.alt_frame != AltitudeDatum.SEA_LEVEL:
        raise ValueError(f"CoT requires SEA_LEVEL/HAE altitude, got {position.alt_frame}")
    return CotPointFields(
        lat_deg=require_finite(position.lat, "lat"),
        lon_deg=require_finite(position.lon, "lon"),
        hae_m=require_finite(position.alt, "alt"),
        ce_m=None if ce_m is None else require_finite(ce_m, "ce_m"),
        le_m=None if le_m is None else require_finite(le_m, "le_m"),
    )
