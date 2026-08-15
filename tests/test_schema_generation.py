from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class SchemaGenerationTests(unittest.TestCase):
    def test_checked_in_generated_files_match_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "schema"
            subprocess.run(
                [sys.executable, "generate_pydantic.py", "--output-dir", str(output_dir)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            generated_contracts = (
                "common.py",
                "object.py",
                "capability.py",
                "condition.py",
                "constraint.py",
                "command.py",
                "task.py",
                "plan.py",
                "assignment.py",
                "authority.py",
                "objective.py",
                "gnc.py",
                "health.py",
                "activation.py",
                "validation.py",
                "cue.py",
                "robot.py",
                "telemetry.py",
            )
            for relative in generated_contracts:
                with self.subTest(relative=relative):
                    self.assertEqual(
                        (output_dir / relative).read_text(),
                        (REPO_ROOT / "schema" / relative).read_text(),
                    )


if __name__ == "__main__":
    unittest.main()
