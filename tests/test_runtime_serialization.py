from __future__ import annotations

import unittest

import msgpack

from occid import (
    ArmCommand,
    GoToCommand,
    GlobalPosition,
    AltitudeDatum,
    OCCID_SCHEMA_VERSION,
    decode_model,
)


class RuntimeSerializationTests(unittest.TestCase):
    def test_generic_decoder_recovers_concrete_model(self) -> None:
        command = GoToCommand(
            position=GlobalPosition(
                lat=45.5017,
                lon=-73.5673,
                alt=120.0,
                alt_frame=AltitudeDatum.RELATIVE,
            ),
            yaw_rad=1.25,
        )
        decoded = decode_model(command.encode())
        self.assertIs(type(decoded), GoToCommand)
        self.assertEqual(decoded, command)

    def test_typed_decoder_still_rejects_wrong_model(self) -> None:
        payload = ArmCommand().encode()
        with self.assertRaisesRegex(ValueError, "does not identify GoToCommand"):
            GoToCommand.decode(payload)

    def test_generic_decoder_rejects_unknown_model_id(self) -> None:
        payload = msgpack.packb(
            {
                "schema_version": list(OCCID_SCHEMA_VERSION),
                "model_id": 999999,
                "fields": {},
            },
            use_bin_type=True,
        )
        with self.assertRaisesRegex(ValueError, "unknown OCCID model ID"):
            decode_model(payload)

    def test_generic_decoder_rejects_schema_mismatch(self) -> None:
        payload = msgpack.packb(
            {
                "schema_version": [99, 0, 0],
                "model_id": 0,
                "fields": {},
            },
            use_bin_type=True,
        )
        with self.assertRaisesRegex(ValueError, "unsupported OCCID schema version"):
            decode_model(payload)


if __name__ == "__main__":
    unittest.main()
