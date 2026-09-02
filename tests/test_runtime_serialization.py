from __future__ import annotations

import unittest

import msgpack

from occid import (
    AltitudeDatum,
    GlobalPosition,
    MotionCommand,
    MotionOperation,
    OCCID_MODEL_ID_BY_CLASS,
    StateChangeCommand,
    StateChangeOperation,
    UID,
    decode_model,
)


TARGET_UID = UID(bytes.fromhex("93bf5775604d4e878f2bee3675b6e80c"))


def move_to(position: GlobalPosition) -> MotionCommand:
    return MotionCommand(
        target_uid=TARGET_UID,
        constraints=[],
        operation=MotionOperation.MOVE_TO,
        destination=position,
    )


class RuntimeSerializationTests(unittest.TestCase):
    def test_generic_decoder_recovers_concrete_model(self) -> None:
        command = move_to(
            GlobalPosition(
                lat=45.5017,
                lon=-73.5673,
                alt=120.0,
                alt_frame=AltitudeDatum.RELATIVE,
            )
        )
        decoded = decode_model(command.encode())
        self.assertIs(type(decoded), MotionCommand)
        self.assertEqual(decoded, command)

    def test_compact_wire_has_numeric_model_and_field_ids(self) -> None:
        command = move_to(
            GlobalPosition(
                lat=45.5017,
                lon=-73.5673,
                alt=120.0,
                alt_frame=AltitudeDatum.RELATIVE,
            )
        )
        envelope = msgpack.unpackb(
            command.encode(),
            raw=False,
            strict_map_key=False,
        )
        self.assertEqual(envelope[0], OCCID_MODEL_ID_BY_CLASS[MotionCommand])
        self.assertIs(type(envelope[1]), dict)
        self.assertTrue(all(type(field_id) is int for field_id in envelope[1]))

    def test_uid_is_bin16_on_wire(self) -> None:
        command = MotionCommand(
            target_uid=TARGET_UID,
            constraints=[],
            operation=MotionOperation.STOP,
        )
        envelope = msgpack.unpackb(
            command.encode(),
            raw=False,
            strict_map_key=False,
        )
        target_field = tuple(MotionCommand.model_fields).index("target_uid")
        self.assertEqual(envelope[1][target_field], TARGET_UID.root)
        self.assertEqual(len(envelope[1][target_field]), 16)

    def test_compact_wire_contains_no_schema_field_names(self) -> None:
        command = MotionCommand(
            target_uid=TARGET_UID,
            constraints=[],
            operation=MotionOperation.STOP,
        )
        envelope = msgpack.unpackb(
            command.encode(),
            raw=False,
            strict_map_key=False,
        )
        self.assertNotIn("model_id", envelope)
        self.assertNotIn("fields", envelope)
        self.assertNotIn("target_uid", envelope[1])

    def test_typed_decoder_still_rejects_wrong_model(self) -> None:
        payload = StateChangeCommand(
            target_uid=TARGET_UID,
            constraints=[],
            operation=StateChangeOperation.ENABLE,
            property_name="armed",
        ).encode()
        with self.assertRaisesRegex(ValueError, "does not identify MotionCommand"):
            MotionCommand.decode(payload)

    def test_generic_decoder_rejects_unknown_model_id(self) -> None:
        payload = msgpack.packb([999999, {}], use_bin_type=True)
        with self.assertRaisesRegex(ValueError, "unknown OCCID model ID"):
            decode_model(payload)


if __name__ == "__main__":
    unittest.main()
