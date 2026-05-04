#!/usr/bin/env python3
"""MCP Server for Memory Forest — exposes memory operations as standardized MCP tools.

Implements JSON-RPC 2.0 over stdio (MCP protocol).
Uses only Python stdlib — no external dependencies.

Tools exposed:
  - memory_status      — Forest summary (trees, nodes, status counts, GC candidates)
  - memory_health      — Health check (issues, warnings)
  - memory_search      — Full-text search across all memory nodes
  - memory_read        — Read a specific node by ID
  - memory_heartbeat   — Heartbeat all active nodes or a specific node
  - memory_gc_check    — List GC candidates without executing
  - memory_list        — List all nodes in a tree (or all trees)
  - memory_create      — Create a new memory node (LEAF/BRANCH/EXPERIENCE)
"""

import sys
import os
import json
import traceback

# Ensure scripts directory is on path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory_forest import (
    forest_status as get_status,
    status_report,
    forest_health,
    search_nodes,
    node_by_id,
    collect_all_nodes,
    heartbeat_all,
    heartbeat_node,
    gc_check,
    gc_run,
    create_node,
    MEMORY_ROOT,
    _today,
)

VERSION = "1.0.0"
SERVER_NAME = "memory-forest-mcp"


def log(msg: str) -> None:
    """Log to stderr (stdout is the MCP transport)."""
    print(f"[{SERVER_NAME}] {msg}", file=sys.stderr, flush=True)


class DateEncoder(json.JSONEncoder):
    """JSON encoder that converts date objects to ISO strings."""
    def default(self, obj):
        import datetime as _dt
        if isinstance(obj, (_dt.date, _dt.datetime)):
            return obj.isoformat()
        return super().default(obj)


def safe_json_dumps(obj) -> str:
    """JSON dumps with date handling."""
    return json.dumps(obj, ensure_ascii=False, indent=2, cls=DateEncoder)


# ── Tool definitions ─────────────────────────────────────────────

TOOLS = [
    {
        "name": "memory_status",
        "description": "Get a summary of the entire memory forest: trees, node counts by status, any GC candidates.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "memory_health",
        "description": "Run a health check on the memory forest. Returns issues and warnings.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "memory_search",
        "description": "Search memory nodes by keyword. Searches tags, titles, IDs, and body text. Returns up to 20 results sorted by relevance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (keyword, phrase, tag)",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "memory_read",
        "description": "Read a specific memory node by its ID (e.g., EXP-CORE-0001, SYS-ROOT-0000).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node_id": {
                    "type": "string",
                    "description": "The memory node ID to read",
                },
            },
            "required": ["node_id"],
        },
    },
    {
        "name": "memory_heartbeat",
        "description": "Update heartbeat timestamps on active/dormant memory nodes. Optionally target a specific node.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "node_id": {
                    "type": "string",
                    "description": "Optional: heartbeat only this specific node. If omitted, heartbeats all active/dormant nodes.",
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, report what would change without writing.",
                    "default": False,
                },
            },
        },
    },
    {
        "name": "memory_gc_check",
        "description": "List garbage collection candidates without executing. Nodes eligible for cleanup based on layer and heartbeat age.",
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "memory_list",
        "description": "List memory nodes. Optionally filter by tree name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tree": {
                    "type": "string",
                    "description": "Optional: filter to a specific tree (forest, system, experiences, projects)",
                },
            },
        },
    },
    {
        "name": "memory_create",
        "description": "Create a new memory node (LEAF, BRANCH, or EXPERIENCE) in a memory tree.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "tree": {
                    "type": "string",
                    "description": "Target tree: forest, system, experiences, projects, or custom name",
                },
                "type": {
                    "type": "string",
                    "enum": ["LEAF", "BRANCH", "EXPERIENCE"],
                    "description": "Node type",
                },
                "title": {
                    "type": "string",
                    "description": "Title for the new node",
                },
                "parent": {
                    "type": "string",
                    "description": "Optional: parent node ID to attach to",
                },
                "layer": {
                    "type": "string",
                    "enum": ["L1", "L2", "L3", "L4"],
                    "description": "Memory layer (default: L1)",
                    "default": "L1",
                },
            },
            "required": ["tree", "type", "title"],
        },
    },
]


# ── Tool handlers ────────────────────────────────────────────────

def handle_memory_status(_args: dict) -> str:
    s = get_status()
    return safe_json_dumps(s)


def handle_memory_health(_args: dict) -> str:
    h = forest_health()
    return safe_json_dumps(h)


def handle_memory_search(args: dict) -> str:
    query = args.get("query", "")
    if not query:
        return safe_json_dumps({"error": "query is required"})
    results = search_nodes(query)
    output = []
    for r in results:
        output.append({
            "id": r["id"],
            "title": r["title"],
            "status": r["status"],
            "heartbeat": r["heartbeat"],
            "score": r["score"],
        })
    return safe_json_dumps(output)


def handle_memory_read(args: dict) -> str:
    nid = args.get("node_id", "")
    if not nid:
        return safe_json_dumps({"error": "node_id is required"})
    node = node_by_id(nid)
    if not node:
        return safe_json_dumps({"error": f"node '{nid}' not found"})
    fm = node["frontmatter"]
    return safe_json_dumps({
        "id": fm.get("id"),
        "type": fm.get("type"),
        "tree": fm.get("tree"),
        "layer": fm.get("layer"),
        "status": fm.get("status"),
        "priority": fm.get("priority"),
        "parent": fm.get("parent"),
        "children": fm.get("children", []),
        "created": fm.get("created"),
        "completed": fm.get("completed"),
        "heartbeat": fm.get("heartbeat"),
        "tags": fm.get("tags", []),
        "body": node["body"][:3000],
        "filepath": node["filepath"],
    })


def handle_memory_heartbeat(args: dict) -> str:
    dry = args.get("dry_run", False)
    nid = args.get("node_id")

    if nid:
        node = node_by_id(nid)
        if not node:
            return safe_json_dumps({"error": f"node '{nid}' not found"})
        changes = heartbeat_node(node, dry_run=dry)
    else:
        changes = heartbeat_all(dry_run=dry)

    return safe_json_dumps({
        "dry_run": dry,
        "changes": len(changes),
        "details": changes,
    })


def handle_memory_gc_check(_args: dict) -> str:
    eligible = gc_check()
    output = []
    for e in eligible:
        n = e["node"]
        fm = n["frontmatter"]
        output.append({
            "id": fm.get("id"),
            "status": fm.get("status"),
            "layer": fm.get("layer"),
            "reason": e["reason"],
            "days_since_heartbeat": e["days_since"],
        })
    return safe_json_dumps({
        "candidates": len(output),
        "items": output,
    })


def handle_memory_list(args: dict) -> str:
    tree_filter = args.get("tree")
    nodes = collect_all_nodes()
    output = []
    for n in nodes:
        fm = n["frontmatter"]
        t = fm.get("tree", "?")
        if tree_filter and t != tree_filter:
            continue
        title = n["body"].split("\n")[0].lstrip("# ")[:80] if n["body"] else "?"
        output.append({
            "id": fm.get("id"),
            "type": fm.get("type"),
            "tree": t,
            "layer": fm.get("layer"),
            "status": fm.get("status"),
            "heartbeat": fm.get("heartbeat"),
            "title": title,
        })
    return safe_json_dumps(output)


def handle_memory_create(args: dict) -> str:
    tree = args.get("tree", "")
    ntype = args.get("type", "LEAF")
    title = args.get("title", "")
    parent = args.get("parent")
    layer = args.get("layer", "L1")

    if not tree or not title:
        return safe_json_dumps({"error": "tree and title are required"})

    try:
        node = create_node(tree=tree, node_type=ntype, title=title,
                          parent_id=parent, layer=layer)
        return safe_json_dumps({
            "created": node["id"],
            "filepath": node["filepath"],
        })
    except Exception as exc:
        return safe_json_dumps({"error": str(exc)})


TOOL_HANDLERS = {
    "memory_status": handle_memory_status,
    "memory_health": handle_memory_health,
    "memory_search": handle_memory_search,
    "memory_read": handle_memory_read,
    "memory_heartbeat": handle_memory_heartbeat,
    "memory_gc_check": handle_memory_gc_check,
    "memory_list": handle_memory_list,
    "memory_create": handle_memory_create,
}


# ── JSON-RPC 2.0 over stdio ──────────────────────────────────────

def read_message() -> dict | None:
    """Read a JSON-RPC message from stdin. Returns None on EOF."""
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line.strip())
    except (json.JSONDecodeError, EOFError):
        return None


def write_message(msg: dict) -> None:
    """Write a JSON-RPC message to stdout."""
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def send_response(req_id, result) -> None:
    write_message({"jsonrpc": "2.0", "id": req_id, "result": result})


def send_error(req_id, code: int, message: str) -> None:
    write_message({"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}})


def handle_request(req: dict) -> None:
    method = req.get("method", "")
    req_id = req.get("id")
    params = req.get("params", {})

    log(f"→ {method} (id={req_id})")

    if method == "initialize":
        send_response(req_id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
            },
            "serverInfo": {
                "name": SERVER_NAME,
                "version": VERSION,
            },
        })
        return

    if method == "notifications/initialized":
        # No response for notifications
        return

    if method == "tools/list":
        send_response(req_id, {"tools": TOOLS})
        return

    if method == "tools/call":
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        handler = TOOL_HANDLERS.get(tool_name)

        if not handler:
            send_error(req_id, -32601, f"Unknown tool: {tool_name}")
            return

        try:
            result_text = handler(tool_args)
            send_response(req_id, {
                "content": [{"type": "text", "text": result_text}],
            })
        except Exception as exc:
            log(f"Tool error: {exc}")
            log(traceback.format_exc())
            send_response(req_id, {
                "content": [{"type": "text", "text": safe_json_dumps({"error": str(exc)})}],
                "isError": True,
            })
        return

    # Unknown method
    send_error(req_id, -32601, f"Method not found: {method}")


def main():
    log(f"MCP Server starting: {SERVER_NAME} v{VERSION}")
    log(f"Memory root: {MEMORY_ROOT}")

    for line in sys.stdin:
        req = None
        try:
            req = json.loads(line.strip())
        except json.JSONDecodeError:
            continue

        if not isinstance(req, dict):
            continue

        # Handle shutdown
        if req.get("method") == "exit":
            log("Shutting down.")
            break

        try:
            handle_request(req)
        except Exception as exc:
            log(f"Unhandled error: {exc}")
            log(traceback.format_exc())
            if req.get("id") is not None:
                send_error(req["id"], -32603, f"Internal error: {exc}")

    log("MCP Server stopped.")


if __name__ == "__main__":
    main()
