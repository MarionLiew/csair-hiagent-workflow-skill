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
    parser.add_argument("--report-lengths", action="store_true")
    parser.add_argument("--max-code-bytes", type=int)
    args = parser.parse_args()
    data = json.loads(args.workflow.read_text(encoding="utf-8"))
    assert "Name" in data, "workflow must use case-sensitive top-level Name"
    nodes = data.get("Nodes")
    assert isinstance(nodes, list) and nodes, "workflow must contain a non-empty Nodes list"

    identities = [node.get("Code") or node.get("ID") for node in nodes]
    assert all(identities), "every node needs Code or ID"
    assert len(identities) == len(set(identities)), "node identities must be unique"
    known = set(identities)

    starts = [node for node in nodes if node.get("Type") == "Start"]
    ends = [node for node in nodes if node.get("Type") == "End"]
    assert len(starts) == 1 and starts[0].get("Name") == "Start", "Start node name must be Start"
    assert starts[0].get("Title") in (None, "", "Start"), "remove or normalize localized Start Title"
    assert len(ends) == 1 and ends[0].get("Name") == "End", "End node name must be End"

    field_lengths = []
    for node in nodes:
        node_name = node.get("Name") or node.get("Code") or "<unnamed>"
        field_lengths.append((len(str(node.get("Code") or "").encode("utf-8")), node_name, "Node.Code"))
        for dependency in node.get("Depends", []):
            assert dependency.get("NodeCode") in known, f"unknown dependency in {node.get('Name')}"
        for item in walk(node.get("Configs", {})):
            if item.get("RefType") == "node_field":
                assert item.get("NodeCode") in known, f"unknown variable source in {node.get('Name')}"

        if node.get("Type") == "Code":
            config = node.get("Configs", {}).get("Code", {})
            embedded_code = config.get("Code", "")
            code_bytes = len(embedded_code.encode("utf-8"))
            field_lengths.append((code_bytes, node_name, "Configs.Code.Code"))
            if args.max_code_bytes is not None:
                assert code_bytes <= args.max_code_bytes, (
                    f"embedded code exceeds {args.max_code_bytes} UTF-8 bytes in {node_name}: {code_bytes}"
                )
            declared = {v.get("Name") for v in config.get("InputVariables", [])}
            used = set(re.findall(r"params\.([A-Za-z_][A-Za-z0-9_]*)", embedded_code))
            assert used <= declared, f"undeclared code inputs in {node.get('Name')}: {sorted(used - declared)}"
            if shutil.which("node"):
                with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as script:
                    script.write(embedded_code)
                    script.flush()
                    result = subprocess.run(["node", "--check", script.name], capture_output=True, text=True)
                assert result.returncode == 0, f"JavaScript syntax error in {node.get('Name')}: {result.stderr}"

        if node.get("Type") == "LLM":
            config = node.get("Configs", {}).get("LLM", {})
            output_schema = config.get("OutputSchema")
            assert output_schema is None or isinstance(output_schema, list), (
                f"LLM OutputSchema must be a HiAgent parameter array or absent in {node_name}"
            )
            for key in ("SystemPrompt", "Prompt"):
                field_lengths.append((len(str(config.get(key) or "").encode("utf-8")), node_name, f"Configs.LLM.{key}"))

    if args.report_lengths:
        print("Largest serialized text fields (UTF-8 bytes):")
        for size, node_name, field in sorted(field_lengths, reverse=True)[:15]:
            print(f"{size:>7}  {field:<26}  {node_name}")

    print(f"OK: {len(nodes)} nodes passed static validation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
