#!/usr/bin/env python3
"""SessionStart hook: load memory forest, run health check, report status.

Called automatically at session start via Claude Code SessionStart hook.
Output goes to stderr so it doesn't interfere with hook protocol.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_forest import forest_health, status_report, gc_check, _today


def main():
    # 1. Health check
    health = forest_health()
    if not health["healthy"]:
        print(f"[{_today()}] Memory forest has {len(health['issues'])} issue(s)!", file=sys.stderr)
        for i in health["issues"]:
            print(f"  ISSUE: {i}", file=sys.stderr)

    # 2. GC candidates
    eligible = gc_check()
    urgent = [e for e in eligible if e["node"]["frontmatter"].get("layer") in ("L1",)]
    if urgent:
        print(f"[{_today()}] GC pending: {len(urgent)} urgent, {len(eligible)} total", file=sys.stderr)

    # 3. Status summary
    print(f"[{_today()}] 森林就绪: {health['total_nodes']}节点, {'健康' if health['healthy'] else '需关注'}", file=sys.stderr)

    # Also output a machine-readable status for the hook system to potentially use
    if health["warnings"]:
        print(f"  Warnings: {len(health['warnings'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
