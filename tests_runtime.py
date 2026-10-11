"""Exercise identity, validation, and the real compact codec."""
from pathlib import Path
import tempfile
import unittest

import msgpack
from pydantic import ValidationError
import yaml

from compiler import compile_schema
from occid2 import (
    BooleanLogic, BooleanOperator, GlobalPosition, Machine, Mark, Objective,
    Person, Plan, Predicate, Task, TaskIntent, UID, decode, new_store,
)

ROOT = Path(__file__).parent


class RuntimeTests(unittest.TestCase):
    def test_uid_and_subject_identity(self):
        uid = UID.new()
        self.assertEqual(len(uid), 16)
        self.assertEqual(uid, UID(bytes(uid)))
        for invalid in ("uav-1", b"short", bytes(17)):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                UID(invalid)
        store = new_store()
        store.ref(uid, Person)
        with self.assertRaises(ValueError):
            store.ref(uid, Machine)
        mark = store.ref(UID.new(), Mark)
        with self.assertRaises(ValueError):
            mark.set(Mark(uid=UID.new(), lat=36.530440, lon=-83.216383, h=0.0))

    def test_validation_on_creation_and_assignment(self):
        for bad in ("36.5", True, float("nan"), float("inf")):
            with self.subTest(latitude=bad), self.assertRaises(ValidationError):
                GlobalPosition(lat=bad, lon=-83.216383, h=0.0)
        point = GlobalPosition(lat=36.530440, lon=-83.216383, h=0.0)
        with self.assertRaises(ValidationError):
            point.lat = "bad"
        with self.assertRaises(ValidationError):
            GlobalPosition(lat=36.530440, lon=-83.216383, h=0.0, unknown=1)
        with self.assertRaises(ValidationError):
            BooleanLogic(operator=BooleanOperator.AND, terms=[Plan(uid=UID.new())])

    def test_wire_round_trip_and_field_presence(self):
        uid = UID.new()
        omitted = Mark(uid=uid, lat=36.530440, lon=-83.216383, h=0.0)
        explicit = Mark(uid=uid, name=None, lat=36.530440, lon=-83.216383, h=0.0)
        for value in (omitted, explicit, Task(uid=UID.new(), instruction="move", intent=TaskIntent.MOVE)):
            restored = decode(value.encode())
            self.assertEqual(value, restored)
            self.assertEqual(value.model_fields_set, restored.model_fields_set)
            self.assertEqual(type(value), type(restored))
        self.assertNotEqual(omitted.encode(), explicit.encode())
        envelope = msgpack.unpackb(omitted.encode(), raw=False, strict_map_key=False)
        self.assertIs(type(envelope[0]), int)
        self.assertEqual(envelope[1][0], bytes(uid))
        with self.assertRaises(ValueError):
            Plan.decode(omitted.encode())

    def test_nested_values_and_mutated_default_lists(self):
        value = BooleanLogic(operator=BooleanOperator.AND, terms=[Predicate(value=3.5)])
        restored = decode(value.encode())
        self.assertIs(type(restored.terms[0]), Predicate)
        self.assertEqual(value, restored)
        objective = Objective(uid=UID.new(), name="test")
        objective.criteria.append(Predicate(value=4.5))
        self.assertEqual(decode(objective.encode()).criteria[0].value, 4.5)
        objective.criteria.append("invalid condition")
        with self.assertRaises(ValidationError):
            objective.encode()

    def test_reject_malformed_wire(self):
        for envelope in ([True, {}], [999999, {}], [Mark._model_id, {99: None}], [Mark._model_id, {"0": bytes(16)}], [Mark._model_id, {}]):
            with self.subTest(envelope=envelope), self.assertRaises((ValueError, ValidationError)):
                decode(msgpack.packb(envelope, use_bin_type=True))
        duplicate = bytes.fromhex("92018200010002")
        with self.assertRaises(ValueError):
            decode(duplicate)

    def test_compiler_diagnostics(self):
        original = yaml.safe_load((ROOT / "occid2.schema.yaml").read_text())
        for change in ("boolean_enum", "bad_identity", "bad_equation", "unknown_region", "missing_scheme", "misspelled_key"):
            schema = yaml.safe_load(yaml.safe_dump(original))
            if change == "boolean_enum":
                schema["enums"]["Test"] = [True]
            elif change == "bad_identity":
                schema["models"]["Entity"]["fields"]["uid"] = "string"
            elif change == "bad_equation":
                schema["expressions"]["MOVE"]["equations"] = ["not an equation"]
            elif change == "unknown_region":
                schema["expressions"]["MOVE"]["given"] = {"actor": "Unknown"}
            elif change == "missing_scheme":
                schema["expressions"]["MOVE"]["of"] = "Unknown"
            else:
                schema["models"]["Entity"]["fieds"] = {}
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "schema.yaml"
                path.write_text(yaml.safe_dump(schema))
                with self.assertRaises(ValueError):
                    compile_schema(path, Path(directory) / "output")
                self.assertFalse((Path(directory) / "output").exists())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "schema.yaml"
            path.write_text("version: 2\nversion: 2\ntype: schema\n")
            with self.assertRaisesRegex(ValueError, "duplicate YAML key"):
                compile_schema(path, Path(directory) / "output")

    def test_removed_storage_scaffolding(self):
        import occid2
        self.assertFalse(hasattr(occid2, "Record"))
        self.assertFalse(hasattr(occid2, "StrID"))
        for model in occid2.MODEL_BY_ID.values():
            self.assertNotIn("id", model.model_fields)
            self.assertNotIn("record", model.model_fields)


if __name__ == "__main__":
    unittest.main()
