from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class SchemaGenerationTests(unittest.TestCase):
    def test_checked_in_compiled_and_generated_files_match_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            compiled = tmp / "occid.yaml"
            output_dir = tmp / "schema"
            ontology = tmp / "ontology.yaml"

            subprocess.run(
                [sys.executable, "compile_occid.py", "--output", str(compiled)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(compiled.read_text(), (REPO_ROOT / "occid.yaml").read_text())

            subprocess.run(
                [
                    sys.executable,
                    "generate_pydantic.py",
                    "--input",
                    str(compiled),
                    "--output-dir",
                    str(output_dir),
                    "--ontology-output",
                    str(ontology),
                ],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )

            ontology_text = ontology.read_text()
            self.assertTrue(ontology_text.endswith("\n\n"))
            self.assertIsInstance(yaml.safe_load(ontology_text), dict)
            self.assertEqual(ontology_text, (REPO_ROOT / "ontology.yaml").read_text())

            checked_in = REPO_ROOT / "schema"
            generated_files = sorted(path.name for path in output_dir.glob("*.py"))
            checked_in_files = sorted(path.name for path in checked_in.glob("*.py"))
            self.assertEqual(generated_files, checked_in_files)
            for relative in generated_files:
                with self.subTest(relative=relative):
                    self.assertEqual(
                        (output_dir / relative).read_text(),
                        (checked_in / relative).read_text(),
                    )


if __name__ == "__main__":
    unittest.main()
