from __future__ import annotations

import unittest

from pydantic import BaseModel, ValidationError

from occid import UID


class _IdentityHolder(BaseModel):
    value: UID


class UIDTests(unittest.TestCase):
    def test_uid_is_a_uuid4_value_not_a_string(self) -> None:
        holder = _IdentityHolder(value="6BEAAC77-7230-4C9E-B578-0ED9E62355F4")
        self.assertIsInstance(holder.value, UID)
        self.assertEqual(str(holder.value), "6beaac77-7230-4c9e-b578-0ed9e62355f4")
        self.assertEqual(len(holder.value.bytes), 16)

    def test_uid_constructor_rejects_non_uuid4(self) -> None:
        with self.assertRaises(ValueError):
            UID("6beaac77-7230-5c9e-b578-0ed9e62355f4")

    def test_uid_field_rejects_non_identity_values(self) -> None:
        for value in ("entity.uav.7", 17):
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    _IdentityHolder(value=value)


if __name__ == "__main__":
    unittest.main()
