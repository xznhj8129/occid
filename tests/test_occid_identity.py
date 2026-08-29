from __future__ import annotations

import unittest

from pydantic import BaseModel, ValidationError

from occid import OCCIDID


class _IdentityHolder(BaseModel):
    value: OCCIDID


class OCCIDIdentityTests(unittest.TestCase):
    def test_occid_id_accepts_and_normalizes_uuid4(self) -> None:
        holder = _IdentityHolder(value="6BEAAC77-7230-4C9E-B578-0ED9E62355F4")
        self.assertEqual(holder.value, "6beaac77-7230-4c9e-b578-0ed9e62355f4")

    def test_occid_id_rejects_non_uuid4_values(self) -> None:
        invalid_values = (
            "entity.uav.7",
            "6beaac77-7230-5c9e-b578-0ed9e62355f4",
            "6beaac77-7230-4c9e-7578-0ed9e62355f4",
            17,
        )
        for value in invalid_values:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    _IdentityHolder(value=value)


if __name__ == "__main__":
    unittest.main()
