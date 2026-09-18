from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from occid.contract import (
    ContractError,
    build_manifest,
    changed_symbols,
    current_manifest,
    generate_consumer_manifest,
    load_manifest,
    main,
    model_hashes_for_ids,
    scan_used_symbols,
    symbol_statuses,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ContractManifestTests(unittest.TestCase):
    def test_checked_in_occid_marker_matches_schema(self) -> None:
        self.assertEqual(
            current_manifest()["global_hash"],
            build_manifest(REPO_ROOT)["global_hash"],
        )

    def test_load_manifest_uses_imported_occid(self) -> None:
        self.assertEqual(
            load_manifest()["global_hash"],
            current_manifest()["global_hash"],
        )

    def test_model_hashes_for_ids(self) -> None:
        manifest = current_manifest()
        entity = manifest["symbols"]["Drone"]
        model_id = entity["model_id"]
        self.assertEqual(
            model_hashes_for_ids(manifest, [model_id]),
            {model_id: entity["hash"]},
        )

    def test_dependency_change_cascades_through_full_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("0.0.2\n", encoding="utf-8")
            schema = root / "occid.yaml"
            schema.write_text(
                """version: 1
type: occid
vocabulary:
  Mode:
    package: test
    values:
      - OFF = 0
      - ON = 1
models:
  Parent:
    model_id: 1
    package: test
    semantic_role: concept
    fields:
      mode: Mode
  Child:
    model_id: 2
    package: test
    semantic_role: representation
    type: Mode
maps: {}
""",
                encoding="utf-8",
            )
            before = build_manifest(root)
            schema.write_text(
                schema.read_text(encoding="utf-8").replace("ON = 1", "ON = 2"),
                encoding="utf-8",
            )
            after = build_manifest(root)
            self.assertNotEqual(before["symbols"]["Mode"]["hash"], after["symbols"]["Mode"]["hash"])
            self.assertNotEqual(before["symbols"]["Parent"]["hash"], after["symbols"]["Parent"]["hash"])
            self.assertNotEqual(before["symbols"]["Child"]["hash"], after["symbols"]["Child"]["hash"])

    def test_taxonomy_growth_does_not_change_parent_structural_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("0.0.2\n", encoding="utf-8")
            schema = root / "occid.yaml"
            schema.write_text(
                """version: 1
type: occid
vocabulary: {}
models:
  Parent:
    model_id: 1
    package: test
    semantic_role: concept
    children: [Child]
    fields:
      value: int
  Child:
    model_id: 2
    package: test
    semantic_role: concept
    parent: Parent
    fields:
      value: int
maps: {}
""",
                encoding="utf-8",
            )
            before = build_manifest(root)
            schema.write_text(
                """version: 1
type: occid
vocabulary: {}
models:
  Parent:
    model_id: 1
    package: test
    semantic_role: concept
    children: [Child, Added]
    fields:
      value: int
  Child:
    model_id: 2
    package: test
    semantic_role: concept
    parent: Parent
    fields:
      value: int
  Added:
    model_id: 3
    package: test
    semantic_role: concept
    parent: Parent
    fields:
      value: int
maps: {}
""",
                encoding="utf-8",
            )
            after = build_manifest(root)
            self.assertNotEqual(before["global_hash"], after["global_hash"])
            self.assertEqual(before["symbols"]["Parent"]["hash"], after["symbols"]["Parent"]["hash"])

    def test_release_label_does_not_change_schema_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "VERSION").write_text("0.0.2\n", encoding="utf-8")
            (root / "occid.yaml").write_text(
                """version: 1
type: occid
vocabulary: {}
models:
  Thing:
    model_id: 1
    package: test
    semantic_role: concept
    fields:
      value: int
maps: {}
""",
                encoding="utf-8",
            )
            before = build_manifest(root)
            (root / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            after = build_manifest(root)
            self.assertEqual(before["global_hash"], after["global_hash"])
            self.assertEqual(before["symbols"]["Thing"]["hash"], after["symbols"]["Thing"]["hash"])

    def test_scan_common_occid_import_forms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consumer.py").write_text(
                """import occid as o
import occid.schema as schema
from occid import schema as schema2
from occid.schema import EntityState

A = o.Drone
B = o.schema.Task
C = schema.Plan
D = schema2.Assignment
""",
                encoding="utf-8",
            )
            used = scan_used_symbols(root)
            self.assertTrue(
                {"Drone", "Task", "Plan", "Assignment", "EntityState"} <= used
            )

    def test_generate_and_check_consumer_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consumer.py").write_text(
                "from occid import Drone, EntityState\n",
                encoding="utf-8",
            )

            receipt = generate_consumer_manifest(root)
            self.assertEqual(set(receipt["symbols"]), {"Drone", "EntityState"})
            self.assertEqual(
                symbol_statuses(root),
                (("Drone", "OK"), ("EntityState", "OK")),
            )
            self.assertEqual(changed_symbols(root), ())

            path = root / "OCCID_CONTRACT"
            broken = json.loads(path.read_text(encoding="utf-8"))
            broken["global_hash"] = "different"
            broken["symbols"]["EntityState"] = "different"
            path.write_text(
                json.dumps(broken, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                symbol_statuses(root),
                (("Drone", "OK"), ("EntityState", "CHANGED")),
            )
            self.assertEqual(changed_symbols(root), ("EntityState",))

    def test_check_rejects_untracked_current_source_symbol(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "consumer.py"
            source.write_text("from occid import Drone\n", encoding="utf-8")
            generate_consumer_manifest(root)

            source.write_text(
                "from occid import Drone, EntityState\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ContractError, "EntityState"):
                symbol_statuses(root)

    def test_check_reports_ok_changed_and_missing_symbols(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consumer.py").write_text(
                "from occid import Drone, EntityState, GoneModel\n",
                encoding="utf-8",
            )
            current = current_manifest()
            path = root / "OCCID_CONTRACT"
            path.write_text(
                json.dumps(
                    {
                        "format": 1,
                        "global_hash": "old-global",
                        "symbols": {
                            "Drone": current["symbols"]["Drone"]["hash"],
                            "EntityState": "old-hash",
                            "GoneModel": "old-hash",
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                symbol_statuses(root),
                (
                    ("Drone", "OK"),
                    ("EntityState", "CHANGED"),
                    ("GoneModel", "MISSING"),
                ),
            )
            self.assertEqual(changed_symbols(root), ("EntityState", "GoneModel"))

            stderr = io.StringIO()
            with redirect_stderr(stderr):
                result = main(["check", str(root)])
            output = stderr.getvalue()
            self.assertEqual(result, 1)
            self.assertIn("Drone", output)
            self.assertIn("OK", output)
            self.assertIn("EntityState", output)
            self.assertIn("CHANGED", output)
            self.assertIn("GoneModel", output)
            self.assertIn("MISSING ***", output)

    def test_check_rejects_legacy_empty_manifest_after_global_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consumer.py").write_text(
                "from occid import Drone\n",
                encoding="utf-8",
            )
            path = root / "OCCID_CONTRACT"
            path.write_text(
                json.dumps(
                    {
                        "format": 1,
                        "global_hash": "old-global",
                        "symbols": {},
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ContractError):
                symbol_statuses(root)


if __name__ == "__main__":
    unittest.main()
