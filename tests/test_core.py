import json
import tempfile
import unittest
from pathlib import Path
from agent_workbench.core import WorkbenchError, Workspace

class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "workbench.json"
        self.ws = Workspace.create(self.path, "demo")

    def tearDown(self): self.tmp.cleanup()

    def test_lifecycle_and_persistence(self):
        task = self.ws.add("Review API", ["api", "review"], "first note")
        self.assertEqual(task.id, 1)
        self.ws.set_status(1, "doing")
        self.ws.note(1, "second note")
        loaded = Workspace.load(self.path)
        self.assertEqual(loaded.get(1)["status"], "doing")
        self.assertIn("second note", loaded.get(1)["notes"])
        self.assertEqual(loaded.summary()["total"], 1)

    def test_filters(self):
        self.ws.add("Alpha task", ["backend"])
        self.ws.add("Beta task", ["frontend"])
        self.ws.set_status(2, "done")
        self.assertEqual(len(self.ws.list_tasks(status="done")), 1)
        self.assertEqual(len(self.ws.list_tasks(tag="backend")), 1)
        self.assertEqual(self.ws.list_tasks(query="alpha")[0]["id"], 1)

    def test_delete_is_persistent(self):
        self.ws.add("Disposable")
        self.ws.delete(1)
        self.assertEqual(Workspace.load(self.path).list_tasks(), [])

    def test_validation(self):
        with self.assertRaises(WorkbenchError): self.ws.add("")
        with self.assertRaises(WorkbenchError): self.ws.add("x", ["bad tag"])
        with self.assertRaises(WorkbenchError): self.ws.set_status(99, "done")
        with self.assertRaises(WorkbenchError): Workspace.create(self.path, "again")

    def test_corrupt_workspace_rejected(self):
        self.path.write_text('{"schema": 99}', encoding="utf-8")
        with self.assertRaises(WorkbenchError): Workspace.load(self.path)

if __name__ == "__main__": unittest.main()
