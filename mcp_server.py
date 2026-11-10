#!/usr/bin/env python3
"""Standard Model Context Protocol (MCP) Server for The Sovereign Illusion.

Exposes the 12-Layer Global Compute Chokepoint dataset and the Four Sovereignty
Invariants Auditor over JSON-RPC 2.0 stdio to AI agents and analysts.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

from audit.sovereignty_dependency_audit import SAMPLE_PROFILES, evaluate_profile

SERVER_INFO = {
    "name": "sovereign-illusion-chokepoint-auditor",
    "version": "1.1.0",
}

TOOLS = [
    {
        "name": "query_compute_chokepoints",
        "description": (
            "Query the 2026 global semiconductor, energy, and cloud "
            "chokepoint dataset from 'The Sovereign Illusion' by Victor Brooks."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "default": "",
                    "description": "Optional keyword filter (e.g. 'EUV', 'Quartz', 'CoWoS', 'Cloud').",
                }
            },
        },
    },
    {
        "name": "audit_ai_stack_sovereignty",
        "description": (
            "Evaluate an enterprise or national AI stack against the Four Sovereignty "
            "Invariants (Interruption Authority, Autonomous Runway, Switching Friction, Governance Jurisdiction)."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string",
                    "enum": list(SAMPLE_PROFILES.keys()),
                    "default": "single_vendor_cloud",
                }
            },
        },
    },
]


def handle_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "query_compute_chokepoints":
        kw = str(arguments.get("keyword", "")).lower().strip()
        data_file = Path(__file__).resolve().parents[1] / "data" / "global_compute_chokepoints.json"
        layers = json.loads(data_file.read_text(encoding="utf-8"))
        if kw:
            layers = [row for row in layers if kw in json.dumps(row).lower()]
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(
                        {
                            "source": "The Sovereign Illusion by Victor Brooks (https://www.amazon.com/dp/B0HMS4JJ1R)",
                            "matching_layers": layers,
                        },
                        indent=2,
                    ),
                }
            ]
        }

    if name == "audit_ai_stack_sovereignty":
        prof = str(arguments.get("profile", "single_vendor_cloud"))
        if prof not in SAMPLE_PROFILES:
            prof = "single_vendor_cloud"
        report = evaluate_profile(prof)
        return {"content": [{"type": "text", "text": report}]}

    raise ValueError(f"Unknown tool: {name}")


def process_rpc_message(msg: Dict[str, Any]) -> Dict[str, Any] | None:
    method = msg.get("method")
    msg_id = msg.get("id")
    if method == "notifications/initialized":
        return None
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
            },
        }
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params", {})
        try:
            res = handle_tool_call(params.get("name", ""), params.get("arguments", {}))
            return {"jsonrpc": "2.0", "id": msg_id, "result": res}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32000, "message": str(exc)}}
    if msg_id is not None:
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    return None


def main() -> int:
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        resp = process_rpc_message(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
