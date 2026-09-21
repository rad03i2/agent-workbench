from __future__ import annotations
import argparse
import json
import sys
from .core import STATUSES, WorkbenchError, Workspace

VERSION = "1.0.0"

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent-workbench", description="Local workbench for tracking agent tasks and run notes.")
    p.add_argument("--version", action="version", version=f"Agent Workbench {VERSION} — Radwan Abdulhadi Ahmed / @rad03i2")
    p.add_argument("--file", default=".agent-workbench.json", help="workspace JSON path")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    sub = p.add_subparsers(dest="command", required=True)
    i = sub.add_parser("init", help="create a workspace"); i.add_argument("name"); i.add_argument("--force", action="store_true")
    a = sub.add_parser("add", help="add a task"); a.add_argument("title"); a.add_argument("--tag", action="append", default=[]); a.add_argument("--notes", default="")
    l = sub.add_parser("list", help="list tasks"); l.add_argument("--status", choices=sorted(STATUSES)); l.add_argument("--tag"); l.add_argument("--query")
    s = sub.add_parser("status", help="change task status"); s.add_argument("id", type=int); s.add_argument("value", choices=sorted(STATUSES))
    n = sub.add_parser("note", help="append a task note"); n.add_argument("id", type=int); n.add_argument("text")
    d = sub.add_parser("delete", help="delete a task"); d.add_argument("id", type=int); d.add_argument("--yes", action="store_true")
    sub.add_parser("summary", help="show workspace summary")
    sub.add_parser("events", help="show recent audit events").add_argument("--limit", type=int, default=20)
    return p

def emit(value, as_json: bool) -> None:
    if as_json:
        print(json.dumps(value, indent=2, ensure_ascii=False))
    elif isinstance(value, list):
        if not value: print("No items.")
        for item in value: print(f"#{item['id']:>3}  {item['status']:<7}  {item['title']}" + (f"  [{', '.join(item.get('tags', []))}]" if item.get('tags') else ""))
    elif isinstance(value, dict):
        print(json.dumps(value, indent=2, ensure_ascii=False))
    else: print(value)

def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            ws = Workspace.create(args.file, args.name, args.force); emit({"created": str(ws.path), "name": ws.data["name"]}, args.json); return 0
        ws = Workspace.load(args.file)
        if args.command == "add": emit(ws.add(args.title, args.tag, args.notes).__dict__, args.json)
        elif args.command == "list": emit(ws.list_tasks(args.status, args.tag, args.query), args.json)
        elif args.command == "status": emit(ws.set_status(args.id, args.value), args.json)
        elif args.command == "note": emit(ws.note(args.id, args.text), args.json)
        elif args.command == "delete":
            if not args.yes: raise WorkbenchError("deletion requires --yes")
            ws.delete(args.id); emit({"deleted": args.id}, args.json)
        elif args.command == "summary": emit(ws.summary(), args.json)
        elif args.command == "events":
            if not 1 <= args.limit <= 1000: raise WorkbenchError("limit must be between 1 and 1000")
            emit(ws.data["events"][-args.limit:], True if args.json else True)
        return 0
    except WorkbenchError as exc:
        print(f"error: {exc}", file=sys.stderr); return 2

if __name__ == "__main__": raise SystemExit(main())
