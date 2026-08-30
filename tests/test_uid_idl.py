from __future__ import annotations

import unittest

from generate_pydantic import TypeParser, collect_type_refs, python_type_expr


class UIDIDLTests(unittest.TestCase):
    def test_uid_is_builtin_scalar(self) -> None:
        uid = TypeParser("UID").parse()
        self.assertEqual(collect_type_refs(uid), set())
        self.assertEqual(python_type_expr(uid, {}), "UID")
        self.assertEqual(python_type_expr(TypeParser("list[UID]").parse(), {}), "list[UID]")


if __name__ == "__main__":
    unittest.main()
