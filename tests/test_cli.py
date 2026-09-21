import tempfile
import unittest
from pathlib import Path
from agent_workbench.cli import main

class CliTests(unittest.TestCase):
    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            path = str(Path(d) / "ws.json")
            self.assertEqual(main(["--file", path, "init", "sample"]), 0)
            self.assertEqual(main(["--file", path, "add", "Ship release", "--tag", "release"]), 0)
            self.assertEqual(main(["--file", path, "status", "1", "done"]), 0)
            self.assertEqual(main(["--file", path, "summary"]), 0)
            self.assertEqual(main(["--file", path, "delete", "1"]), 2)
            self.assertEqual(main(["--file", path, "delete", "1", "--yes"]), 0)

if __name__ == "__main__": unittest.main()
