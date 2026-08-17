from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from occid.contract import (
    ContractError,
    build_manifest,
    changed_symbols,
    current_manifest,
    generate_consumer_manifest,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


class ContractManifestTests(unittest.TestCase):
    def test_checked_in_occid_marker_matches_schema(self) -> None:
        self.assertEqual(
            current_manifest()["global_hash"],
            build_manifest(REPO_ROOT)["global_hash"],
        )

    def test_dependency_change_cascades_through_full_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "lib/schema/core").mkdir(parents=True)
            (root / "lib/schema/modules").mkdir(parents=True)
            (root / "VERSION").write_text("0.0.2\n", encoding="utf-8")
            (root / "lib/model_ids.yaml").write_text(
                "version: 1\nmodel_ids:\n  Parent: 1\n  Child: 2\n",
                encoding="utf-8",
            )
            schema = root / "lib/schema/core/test.schema.yaml"
            schema.write_text(
                """version: 1
type: schema
package: test
tags: [core]
root: Parent
enums:
  Mode:
    - OFF = 0
    - ON = 1
models:
  Parent:
    description: Parent model.
    fields:
      mode: Mode
    variants: [Child]
  Child:
    description: Child model.
    parent: Parent
    fields:
      value: int
""",
                encoding="utf-8",
            )
            before = build_manifest(root)
            schema.write_text(
                schema.read_text(encoding="utf-8").replace("ON = 1", "ON = 2"),
                encoding="utf-8",
            )
            after = build_manifest(root)
            self.assertNotEqual(
                before["symbols"]["Mode"]["hash"],
                after["symbols"]["Mode"]["hash"],
            )
            self.assertNotEqual(
                before["symbols"]["Parent"]["hash"],
                after["symbols"]["Parent"]["hash"],
            )
            self.assertNotEqual(
                before["symbols"]["Child"]["hash"],
                after["symbols"]["Child"]["hash"],
            )

    def test_release_label_does_not_change_schema_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "lib/schema/core").mkdir(parents=True)
            (root / "lib/schema/modules").mkdir(parents=True)
            (root / "VERSION").write_text("0.0.2\n", encoding="utf-8")
            (root / "lib/model_ids.yaml").write_text(
                "version: 1\nmodel_ids:\n  Thing: 1\n",
                encoding="utf-8",
            )
            (root / "lib/schema/core/test.schema.yaml").write_text(
                """version: 1
type: schema
package: test
tags: [core]
root: Thing
models:
  Thing:
    description: Thing.
    fields:
      value: int
""",
                encoding="utf-8",
            )
            before = build_manifest(root)
            (root / "VERSION").write_text("9.9.9\n", encoding="utf-8")
            after = build_manifest(root)
            self.assertEqual(before["global_hash"], after["global_hash"])
            self.assertEqual(
                before["symbols"]["Thing"]["hash"],
                after["symbols"]["Thing"]["hash"],
            )

    def test_generate_and_check_consumer_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "consumer.py").write_text(
                "from occid import Entity, EntityState\n",
                encoding="utf-8",
            )

            receipt = generate_consumer_manifest(root)
            self.assertEqual(set(receipt["symbols"]), {"Entity", "EntityState"})
            self.assertEqual(changed_symbols(root), ())

            path = root / "OCCID_CONTRACT"
            broken = json.loads(path.read_text(encoding="utf-8"))
            broken["global_hash"] = "different"
            broken["symbols"]["EntityState"] = "different"
            path.write_text(
                json.dumps(broken, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(changed_symbols(root), ("EntityState",))

    def test_check_rejects_legacy_empty_manifest_after_global_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
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
                changed_symbols(root)


if __name__ == "__main__":
    unittest.main()
