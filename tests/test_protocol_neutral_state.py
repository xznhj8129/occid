from __future__ import annotations

import unittest

import occid
from occid import (
    Airspeed,
    ElectricalResourceState,
    EntityState,
    FlightControlState,
    GnssSolution,
    Link,
    LinkState,
    Measurement,
    MeshLink,
    State,
)


class ProtocolNeutralStateTests(unittest.TestCase):
    def test_protocol_native_escape_hatches_are_not_state_fields(self) -> None:
        self.assertFalse(hasattr(occid, "TelemetryState"))

        for field in (
            "native_mode_name",
            "native_mode_code",
            "native_active_mode_codes",
            "native_active_mode_names",
            "native_nav_state_code",
            "native_system_state_code",
        ):
            self.assertNotIn(field, FlightControlState.model_fields)

        for field in ("fix_code", "last_message_dt", "errors", "timeouts", "eph", "epv"):
            self.assertNotIn(field, GnssSolution.model_fields)

        for field in ("battery_id", "rssi"):
            self.assertNotIn(field, ElectricalResourceState.model_fields)

    def test_static_link_definition_is_separate_from_link_state(self) -> None:
        self.assertNotIn("condition", Link.model_fields)
        self.assertNotIn("connection_status", Link.model_fields)
        self.assertTrue(issubclass(LinkState, State))
        self.assertTrue(issubclass(MeshLink, LinkState))

    def test_entity_state_is_a_semantic_aggregate(self) -> None:
        self.assertNotIn("telemetry", EntityState.model_fields)
        self.assertNotIn("links", EntityState.model_fields)
        self.assertNotIn("telemetry_received_ts", EntityState.model_fields)
        self.assertIn("airspeed", EntityState.model_fields)
        self.assertIn("link_states", EntityState.model_fields)
        self.assertIn("received_ts", EntityState.model_fields)
        self.assertTrue(issubclass(Airspeed, Measurement))


if __name__ == "__main__":
    unittest.main()
