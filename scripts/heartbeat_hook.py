#!/usr/bin/env python3
"""Stop hook: heartbeat all active memory nodes and run GC check.

Called automatically at session end via Claude Code Stop hook.
Output goes to stderr so it doesn't interfere with hook protocol.
Environment variables provided by Claude Code:
  CLAUDE_SESSION_ID, CLAUDE_PROJECT_DIR
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_forest import heartbeat_all, gc_check, status_report, _today


def main():
    session_id = os.environ.get("CLAUDE_SESSION_ID", "unknown")

    # 1. Heartbeat all active/dormant nodes
    changes = heartbeat_all(dry_run=False)
    if changes:
        print(f"[{_today()}] Heartbeat: {len(changes)} change(s)", file=sys.stderr)
        for c in changes:
            print(c, file=sys.stderr)

    # 2. GC check (report only, no destructive actions)
    eligible = gc_check()
    if eligible:
        urgent = [e for e in eligible if e["node"]["frontmatter"].get("layer") in ("L1",)]
        if urgent:
            print(f"[{_today()}] GC: {len(eligible)} candidates ({len(urgent)} urgent)", file=sys.stderr)
            for e in urgent[:3]:
                nid = e["node"]["frontmatter"].get("id", "?")
                print(f"  GC candidate: {nid} — {e['reason']}", file=sys.stderr)

    # 3. Brief status
    print(f"记忆森林: session={session_id[:8]}... heartbeat={_today()}", file=sys.stderr)


if __name__ == "__main__":
    main()
