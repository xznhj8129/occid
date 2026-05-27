"""Generated from core/schemav2."""
from __future__ import annotations
from .common import *

from .state import State

### Models

class Position(State):
    'Position in space, address or placement'

class LocationState(Position):
    inertial_frame: InertialReferenceFrame | None = None
    body_frame: BodyReferenceFrame | None = None
    position: GlobalPosition | None = None
    uncertainty: LocationUncertainty | None = None
    attitude: EulerAngles | None = None
    altitude: AltitudeState | None = None
    velocity: VelocityVector | None = None
    navigation_validity: NavigationValidity | None = None
    gnss: GnssSolution | None = None

class SpotterOrigin(Position):
    position: GlobalPosition
    attitude: EulerAngles | None = None
    look_vector: LocalDirection | None = None
