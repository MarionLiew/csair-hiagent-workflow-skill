#!/usr/bin/env python3
"""Static, vendor-neutral checks for an exported HiAgent workflow JSON."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workflow", type=Path)
    args = parser.parse_args()
    data = json.loads(args.workflow.read_text(encoding="utf-8"))
    nodes = data.get("Nodes")
    assert isinstance(nodes, list) and nodes, "workflow must contain a non-empty Nodes list"

    identities = [node.get("Code") or node.get("ID") for node in nodes]
    assert all(identities), "every node needs Code or ID"
    assert len(identities) == len(set(identities)), "node identities must be unique"
    known = set(identities)

    starts = [node for node in nodes if node.get("Type") == "Start"]
    ends = [node for node in nodes if node.get("Type") == "End"]
    assert len(starts) == 1 and starts[0].get("Name") == "Start", "Start node name must be Start"
    assert len(ends) == 1 and ends[0].get("Name") == "End", "End node name must be End"

    for node in nodes:
        for dependency in node.get("Depends", []):
            assert dependency.get("NodeCode") in known, f"unknown dependency in {node.get('Name')}"
        for item in walk(node.get("Configs", {})):
            if item.get("RefType") == "node_field":
                assert item.get("NodeCode") in known, f"unknown variable source in {node.get('Name')}"

        if node.get("Type") == "Code":
            config = node.get("Configs", {}).get("Code", {})
            declared = {v.get("Name") for v in config.get("InputVariables", [])}
            used = set(re.findall(r"params\.([A-Za-z_][A-Za-z0-9_]*)", config.get("Code", "")))
            assert used <= declared, f"undeclared code inputs in {node.get('Name')}: {sorted(used - declared)}"
            if shutil.which("node"):
                with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as script:
                    script.write(config.get("Code", ""))
                    script.flush()
                    result = subprocess.run(["node", "--check", script.name], capture_output=True, text=True)
                assert result.returncode == 0, f"JavaScript syntax error in {node.get('Name')}: {result.stderr}"

    print(f"OK: {len(nodes)} nodes passed static validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
