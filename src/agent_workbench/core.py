from __future__ import annotations
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")
STATUSES = {"todo", "doing", "blocked", "done"}

class WorkbenchError(ValueError):
    pass

def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def valid_name(value: str, label: str = "name") -> str:
    if not isinstance(value, str) or not NAME_RE.fullmatch(value):
        raise WorkbenchError(f"{label} must match {NAME_RE.pattern}")
    return value

@dataclass
class Task:
    id: int
    title: str
    status: str
    tags: list[str]
    notes: str
    created_at: str
    updated_at: str

class Workspace:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.data: dict[str, Any] = {"schema": 1, "name": "workspace", "created_at": now(), "tasks": [], "events": []}

    @classmethod
    def create(cls, path: str | Path, name: str, overwrite: bool = False) -> "Workspace":
        valid_name(name, "workspace name")
        ws = cls(path)
        if ws.path.exists() and not overwrite:
            raise WorkbenchError(f"workspace already exists: {ws.path}")
        ws.data["name"] = name
        ws.save()
        return ws

    @classmethod
    def load(cls, path: str | Path) -> "Workspace":
        ws = cls(path)
        try:
            raw = json.loads(ws.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise WorkbenchError(f"cannot read workspace: {exc}") from exc
        if not isinstance(raw, dict) or raw.get("schema") != 1 or not isinstance(raw.get("tasks"), list) or not isinstance(raw.get("events"), list):
            raise WorkbenchError("unsupported or malformed workspace")
        valid_name(raw.get("name"), "workspace name")
        ws.data = raw
        return ws

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp = self.path.with_name(self.path.name + ".tmp")
        temp.write_text(json.dumps(self.data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temp.replace(self.path)

    def _event(self, kind: str, task_id: int, detail: str = "") -> None:
        self.data["events"].append({"at": now(), "kind": kind, "task_id": task_id, "detail": detail})
        self.data["events"] = self.data["events"][-1000:]

    def add(self, title: str, tags: list[str] | None = None, notes: str = "") -> Task:
        title = title.strip()
        if not title or len(title) > 300:
            raise WorkbenchError("title must contain 1 to 300 characters")
        clean_tags = sorted({valid_name(t, "tag") for t in (tags or [])})
        if len(notes) > 20_000:
            raise WorkbenchError("notes exceed 20000 characters")
        task_id = max((int(t["id"]) for t in self.data["tasks"]), default=0) + 1
        stamp = now()
        task = Task(task_id, title, "todo", clean_tags, notes, stamp, stamp)
        self.data["tasks"].append(asdict(task)); self._event("created", task_id); self.save()
        return task

    def get(self, task_id: int) -> dict[str, Any]:
        for task in self.data["tasks"]:
            if task.get("id") == task_id:
                return task
        raise WorkbenchError(f"task not found: {task_id}")

    def set_status(self, task_id: int, status: str) -> dict[str, Any]:
        if status not in STATUSES:
            raise WorkbenchError(f"status must be one of: {', '.join(sorted(STATUSES))}")
        task = self.get(task_id); old = task["status"]; task["status"] = status; task["updated_at"] = now()
        self._event("status", task_id, f"{old}->{status}"); self.save(); return task

    def note(self, task_id: int, text: str) -> dict[str, Any]:
        text = text.strip()
        if not text or len(text) > 5000:
            raise WorkbenchError("note must contain 1 to 5000 characters")
        task = self.get(task_id)
        task["notes"] = (task.get("notes", "") + ("\n" if task.get("notes") else "") + text)[-20_000:]
        task["updated_at"] = now(); self._event("note", task_id); self.save(); return task

    def list_tasks(self, status: str | None = None, tag: str | None = None, query: str | None = None) -> list[dict[str, Any]]:
        if status is not None and status not in STATUSES:
            raise WorkbenchError("invalid status")
        q = query.casefold() if query else None
        result = []
        for task in self.data["tasks"]:
            if status and task["status"] != status: continue
            if tag and tag not in task.get("tags", []): continue
            if q and q not in (task["title"] + " " + task.get("notes", "")).casefold(): continue
            result.append(task)
        return result

    def summary(self) -> dict[str, Any]:
        counts = {s: 0 for s in sorted(STATUSES)}
        for task in self.data["tasks"]: counts[task["status"]] += 1
        return {"name": self.data["name"], "total": len(self.data["tasks"]), "by_status": counts, "events": len(self.data["events"])}

    def delete(self, task_id: int) -> None:
        self.get(task_id)
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        self._event("deleted", task_id); self.save()
