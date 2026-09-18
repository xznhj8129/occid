from __future__ import annotations

import unittest

import msgpack
from pydantic import BaseModel, ValidationError

from occid import IntID, OCCID_MODEL_ID_BY_CLASS, OCCIDValue, StringName, UID, decode_model


class _IdentityHolder(BaseModel):
    value: UID


class AtomicValueTests(unittest.TestCase):
    def test_named_string_representation_is_the_string_not_a_wrapper_record(self) -> None:
        name = StringName("Raven 1")
        self.assertIsInstance(name, OCCIDValue)
        self.assertEqual(name.root, "Raven 1")
        self.assertEqual(name.model_dump(), "Raven 1")

    def test_named_integer_representation_is_the_integer_not_a_wrapper_record(self) -> None:
        identifier = IntID(38)
        self.assertIsInstance(identifier, OCCIDValue)
        self.assertEqual(identifier.root, 38)
        self.assertEqual(identifier.model_dump(), 38)


class UIDTests(unittest.TestCase):
    def test_uid_is_named_exactly_sixteen_byte_value(self) -> None:
        raw = bytes.fromhex("6beaac7772304c9eb5780ed9e62355f4")
        holder = _IdentityHolder(value=raw)
        self.assertIsInstance(holder.value, UID)
        self.assertIsInstance(holder.value, OCCIDValue)
        self.assertEqual(holder.value.root, raw)
        self.assertEqual(holder.model_dump(), {"value": raw})

    def test_uid_has_no_uuid_version_semantics(self) -> None:
        raw = bytes.fromhex("6beaac7772305c9eb5780ed9e62355f4")
        self.assertEqual(UID(raw).root, raw)

    def test_uid_rejects_text_even_when_text_is_sixteen_characters(self) -> None:
        with self.assertRaises(ValidationError):
            UID("1234567890abcdef")

    def test_uid_rejects_wrong_length(self) -> None:
        for value in (b"short", b"x" * 17):
            with self.subTest(length=len(value)):
                with self.assertRaises(ValidationError):
                    UID(value)

    def test_atomic_uid_round_trips_as_top_level_value(self) -> None:
        raw = bytes.fromhex("93bf5775604d4e878f2bee3675b6e80c")
        uid = UID(raw)
        envelope = msgpack.unpackb(uid.encode(), raw=False, strict_map_key=False)
        self.assertEqual(envelope, [OCCID_MODEL_ID_BY_CLASS[UID], raw])
        self.assertEqual(decode_model(uid.encode()), uid)

    def test_uid_field_rejects_non_binary_identity_values(self) -> None:
        for value in ("entity.uav.7", 17):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    _IdentityHolder(value=value)


if __name__ == "__main__":
    unittest.main()
