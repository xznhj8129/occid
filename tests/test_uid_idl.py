from __future__ import annotations

import unittest
from pathlib import Path

import yaml

from generate_pydantic import SchemaError, TypeParser, collect_type_refs, parse_model, python_type_expr


class AtomicRepresentationIDLTests(unittest.TestCase):
    def test_named_atomic_representation_uses_model_level_type(self) -> None:
        model = parse_model(
            "UID",
            {
                "semantic_role": "representation",
                "parent": "ID",
                "type": "bytes[16]",
            },
        )
        self.assertIsNotNone(model.value_type)
        self.assertEqual(model.value_type.kind, "fixed_bytes")
        self.assertEqual(model.value_type.size, 16)
        self.assertEqual(model.fields, [])

    def test_fixed_bytes_type_is_exact_length(self) -> None:
        node = TypeParser("bytes[16]").parse()
        self.assertEqual(node.kind, "fixed_bytes")
        self.assertEqual(node.size, 16)
        self.assertEqual(collect_type_refs(node), set())
        self.assertEqual(
            python_type_expr(node, {}),
            "Annotated[bytes, Field(strict=True, min_length=16, max_length=16)]",
        )

    def test_invalid_fixed_and_generic_type_shapes_fail_at_parse_time(self) -> None:
        invalid = (
            "bytes[string]",
            "bytes[0]",
            "Foo[Bar]",
            "list[int, string]",
            "map[string]",
            "map[string, int, bool]",
            "tuple[int]",
        )
        for text in invalid:
            with self.subTest(text=text):
                with self.assertRaises(SchemaError):
                    TypeParser(text).parse()


    def test_intid_namespace_is_a_semantic_type_argument(self) -> None:
        node = TypeParser("IntID(Entity)").parse()
        self.assertEqual(node.kind, "semantic")
        self.assertEqual(node.name, "IntID")
        self.assertEqual(node.semantic_args, ["Entity"])
        self.assertEqual(collect_type_refs(node), {"IntID"})
        self.assertEqual(
            python_type_expr(node, {}),
            "Annotated[IntID, IDNamespace('Entity')]",
        )

    def test_structural_types_can_contain_namespaced_intids(self) -> None:
        node = TypeParser("list[IntID(Task)]").parse()
        self.assertEqual(node.kind, "list")
        self.assertEqual(node.args[0].kind, "semantic")
        self.assertEqual(node.args[0].semantic_args, ["Task"])
        self.assertEqual(collect_type_refs(node), {"IntID"})

    def test_named_representation_is_a_schema_reference_not_a_primitive(self) -> None:
        uid = TypeParser("UID").parse()
        self.assertEqual(collect_type_refs(uid), {"UID"})
        self.assertEqual(python_type_expr(uid, {}), "UID")
        self.assertEqual(collect_type_refs(TypeParser("list[UID]").parse()), {"UID"})

    def test_type_and_fields_are_mutually_exclusive(self) -> None:
        with self.assertRaisesRegex(SchemaError, "type or fields"):
            parse_model(
                "Bad",
                {
                    "semantic_role": "representation",
                    "parent": "Struct",
                    "type": "int",
                    "fields": {"value": "int"},
                },
            )

    def test_concept_cannot_declare_model_level_type(self) -> None:
        with self.assertRaisesRegex(SchemaError, "only valid on a representation"):
            parse_model(
                "BadConcept",
                {
                    "semantic_role": "concept",
                    "parent": "Struct",
                    "type": "int",
                },
            )

    def test_compiled_schema_preserves_atomic_shape(self) -> None:
        compiled = yaml.safe_load((Path(__file__).resolve().parents[1] / "occid.yaml").read_text())
        uid = compiled["representations"]["UID"]
        self.assertEqual(uid["type"], "bytes[16]")
        self.assertNotIn("fields", uid)
        self.assertEqual(compiled["representations"]["IntID"]["type"], "int")
        self.assertEqual(compiled["representations"]["StringName"]["type"], "string")
        self.assertEqual(compiled["types"]["Node"]["fields"]["id"], "IntID(Node)")
        bootstrap = compiled["representations"]["IdentityBootstrap"]["fields"]
        self.assertEqual(bootstrap["node_id"], "IntID(Node)")
        self.assertEqual(bootstrap["entity_id"], "IntID(Entity)")
        self.assertEqual(bootstrap["organization_id"], "IntID(Organization)")


if __name__ == "__main__":
    unittest.main()
