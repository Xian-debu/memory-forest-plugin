#!/usr/bin/env python3
"""Memory Forest core library — parse, query, and update memory nodes."""

import os
import re
import datetime
from typing import Optional

import yaml

MEMORY_ROOT = os.path.expanduser("~/.claude/projects/-root/memory")


def _today() -> str:
    return datetime.date.today().isoformat()


def _node_id(tree: str, node_type: str, n: int) -> str:
    return f"{tree.upper()}-{node_type.upper()}-{n:04d}"


def _next_number(tree: str, node_type: str, existing_ids: set) -> int:
    prefix = f"{tree.upper()}-{node_type.upper()}-"
    nums = []
    for nid in existing_ids:
        if nid.startswith(prefix):
            try:
                nums.append(int(nid.split("-")[-1]))
            except ValueError:
                pass
    return max(nums) + 1 if nums else 1


def parse_frontmatter(filepath: str) -> dict:
    """Parse a memory node file, returning {frontmatter, body, filepath}."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    fm = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                pass
            body = parts[2].strip()

    return {"frontmatter": fm, "body": body, "filepath": filepath}


def save_node(filepath: str, frontmatter: dict, body: str) -> None:
    """Write a memory node file with YAML frontmatter."""
    fm_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False).strip()
    content = f"---\n{fm_str}\n---\n{body}\n"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()
    except FileNotFoundError:
        original = ""
    if original != content:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def collect_all_nodes(memory_root: str = MEMORY_ROOT) -> list[dict]:
    """Walk the memory root and parse all .md files as memory nodes."""
    nodes = []
    for dirpath, dirnames, filenames in os.walk(memory_root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fname in filenames:
            if fname.endswith(".md"):
                fp = os.path.join(dirpath, fname)
                node = parse_frontmatter(fp)
                if node["frontmatter"].get("id"):
                    nodes.append(node)
    return nodes


def node_by_id(node_id: str, nodes: list[dict] = None) -> Optional[dict]:
    if nodes is None:
        nodes = collect_all_nodes()
    for n in nodes:
        if n["frontmatter"].get("id") == node_id:
            return n
    return None


# ── Heartbeat ────────────────────────────────────────────────────

def heartbeat_node(node: dict, dry_run: bool = False) -> list[str]:
    """Heartbeat a single node. Returns list of status change messages."""
    fm = node["frontmatter"]
    changes = []
    old_heartbeat = fm.get("heartbeat", "never")
    new_heartbeat = _today()

    if old_heartbeat == new_heartbeat and fm.get("status") not in ("ACTIVE", "DORMANT"):
        return changes

    nid = fm.get("id", "unknown")
    changes.append(f"  {nid}: heartbeat {old_heartbeat} → {new_heartbeat}")
    fm["heartbeat"] = new_heartbeat

    # Check if node should be marked COMPLETED (if it has all tasks done)
    body = node["body"]
    has_tasks = bool(re.search(r"\[ \]", body))  # unchecked tasks
    has_completed = bool(re.search(r"\[x\]", body))  # completed tasks
    if has_completed and not has_tasks and fm.get("status") in ("ACTIVE", "DORMANT"):
        old_status = fm["status"]
        fm["status"] = "COMPLETED"
        fm["completed"] = new_heartbeat
        changes.append(f"  {nid}: status {old_status} → COMPLETED (all tasks done)")

    # Check DORMANT timeout (>30 days)
    if fm.get("status") == "DORMANT" and old_heartbeat != "never":
        try:
            hb_date = datetime.date.fromisoformat(str(old_heartbeat))
            if (datetime.date.today() - hb_date).days > 30:
                fm["status"] = "ORPHANED"
                changes.append(f"  {nid}: DORMANT >30 days → ORPHANED")
        except (ValueError, TypeError):
            pass

    if not dry_run:
        save_node(node["filepath"], fm, node["body"])

    return changes


def heartbeat_all(memory_root: str = MEMORY_ROOT, dry_run: bool = False) -> list[str]:
    """Heartbeat all ACTIVE and DORMANT nodes. Returns change log."""
    nodes = collect_all_nodes(memory_root)
    log = []
    for n in nodes:
        status = n["frontmatter"].get("status", "")
        if status in ("ACTIVE", "DORMANT"):
            changes = heartbeat_node(n, dry_run=dry_run)
            log.extend(changes)
    return log


def ascend_heartbeat(node: dict, all_nodes: list[dict], dry_run: bool = False) -> list[str]:
    """After a child completes, propagate heartbeat upward."""
    fm = node["frontmatter"]
    parent_id = fm.get("parent")
    if not parent_id:
        return []

    parent = node_by_id(parent_id, all_nodes)
    if not parent:
        return [f"  WARN: parent {parent_id} not found for {fm.get('id')}"]

    pfm = parent["frontmatter"]
    children_ids = pfm.get("children", [])
    all_done = True
    for cid in children_ids:
        child = node_by_id(cid, all_nodes)
        if child and child["frontmatter"].get("status") not in ("COMPLETED", "ARCHIVED", "ORPHANED"):
            all_done = False
            break

    if all_done and pfm.get("type") == "BRANCH":
        pfm["status"] = "COMPLETED"
        pfm["completed"] = _today()
        changes = [f"  {pfm['id']}: all children done → BRANCH COMPLETED"]
        if not dry_run:
            save_node(parent["filepath"], pfm, parent["body"])
        changes.extend(ascend_heartbeat(parent, all_nodes, dry_run))
        return changes

    if all_done and pfm.get("type") == "ROOT":
        pfm["status"] = "COMPLETED"
        pfm["completed"] = _today()
        changes = [f"  {pfm['id']}: all branches done → ROOT COMPLETED"]
        if not dry_run:
            save_node(parent["filepath"], pfm, parent["body"])
        return changes

    # Just update parent heartbeat
    pfm["heartbeat"] = _today()
    if not dry_run:
        save_node(parent["filepath"], pfm, parent["body"])
    return []


# ── Garbage Collection ───────────────────────────────────────────

def gc_check(memory_root: str = MEMORY_ROOT) -> list[dict]:
    """Scan for nodes eligible for garbage collection. Returns list of {node, reason}."""
    nodes = collect_all_nodes(memory_root)
    today = datetime.date.today()
    eligible = []

    for n in nodes:
        fm = n["frontmatter"]
        status = fm.get("status", "")
        layer = fm.get("layer", "")

        raw_hb = fm.get("heartbeat")
        if not raw_hb:
            raw_hb = fm.get("created", str(today))
        try:
            hb = datetime.date.fromisoformat(str(raw_hb))
        except (ValueError, TypeError):
            hb = today

        days_since = (today - hb).days

        reason = None
        if layer == "L1" and status == "COMPLETED" and days_since > 7:
            reason = f"L1 COMPLETED, heartbeat {days_since}d ago (>7d)"
        elif layer == "L1" and status == "ORPHANED":
            reason = "L1 ORPHANED"
        elif layer == "L2" and status == "ARCHIVED" and days_since > 30:
            reason = f"L2 ARCHIVED, heartbeat {days_since}d ago (>30d)"
        elif layer == "L3" and days_since > 90:
            reason = f"L3 heartbeat {days_since}d ago (>90d)"
        elif layer == "L4" and days_since > 365:
            reason = f"L4 heartbeat {days_since}d ago (>365d)"
        elif status == "ORPHANED" and not fm.get("parent"):
            reason = "ORPHANED with no parent reference"

        if reason:
            eligible.append({"node": n, "reason": reason, "days_since": days_since})

    return sorted(eligible, key=lambda x: x["days_since"], reverse=True)


def gc_run(memory_root: str = MEMORY_ROOT, dry_run: bool = True) -> list[str]:
    """Execute garbage collection. Returns action log."""
    eligible = gc_check(memory_root)
    log = []

    for entry in eligible:
        n = entry["node"]
        fm = n["frontmatter"]
        nid = fm.get("id", "unknown")
        layer = fm.get("layer", "")

        if layer in ("L1",) and entry["reason"].startswith("L1 COMPLETED"):
            action = f"  {nid}: compress to summary ({entry['reason']})"
            log.append(action)
            if not dry_run:
                # Compress: keep frontmatter, truncate body to 5-line summary
                lines = n["body"].split("\n")
                summary = "\n".join(lines[:5]) + "\n\n<details>\n<summary>Archived</summary>\n" + "\n".join(lines[5:100]) + "\n</details>\n"
                save_node(n["filepath"], fm, summary)

        elif layer in ("L1",) and "ORPHANED" in entry["reason"]:
            action = f"  {nid}: mark for deletion ({entry['reason']})"
            log.append(action)
            if not dry_run:
                trash_dir = os.path.join(memory_root, ".trash")
                os.makedirs(trash_dir, exist_ok=True)
                fm["status"] = "ARCHIVED"
                fm["archived_date"] = _today()
                save_node(n["filepath"], fm, n["body"])

        else:
            action = f"  {nid}: needs review ({entry['reason']})"
            log.append(action)

    return log


# ── Forest Status ─────────────────────────────────────────────────

def forest_status(memory_root: str = MEMORY_ROOT) -> dict:
    """Generate a status report for the entire memory forest."""
    nodes = collect_all_nodes(memory_root)
    trees = {}
    status_counts = {"ACTIVE": 0, "DORMANT": 0, "COMPLETED": 0, "ORPHANED": 0, "ARCHIVED": 0, "UNKNOWN": 0}
    layer_counts = {}

    for n in nodes:
        fm = n["frontmatter"]
        tree = fm.get("tree", "unknown")
        node_type = fm.get("type", "unknown")
        status = fm.get("status", "UNKNOWN")
        layer = fm.get("layer", "")
        nid = fm.get("id", "?")

        if tree not in trees:
            trees[tree] = {"nodes": [], "root": None, "active": 0, "dormant": 0}

        info = {"id": nid, "type": node_type, "status": status, "layer": layer,
                "heartbeat": fm.get("heartbeat", "?"), "title": n["body"].split("\n")[0].lstrip("# ") if n["body"] else "?"}
        trees[tree]["nodes"].append(info)

        if node_type == "ROOT":
            trees[tree]["root"] = info

        if status == "ACTIVE":
            trees[tree]["active"] += 1
        elif status == "DORMANT":
            trees[tree]["dormant"] += 1

        status_counts[status] = status_counts.get(status, 0) + 1
        layer_counts[layer] = layer_counts.get(layer, 0) + 1

    return {
        "trees": trees,
        "total_nodes": len(nodes),
        "status_counts": status_counts,
        "layer_counts": layer_counts,
        "active_trees": sum(1 for t in trees.values() if t["active"] > 0),
        "pending_nodes": status_counts.get("DORMANT", 0),
    }


def status_report(memory_root: str = MEMORY_ROOT) -> str:
    """Human-readable forest status report."""
    s = forest_status(memory_root)
    lines = [
        f"记忆森林状态 @ {_today()}",
        f"  节点总数: {s['total_nodes']}",
        f"  活跃树: {s['active_trees']}棵",
        f"  状态分布: ACTIVE={s['status_counts'].get('ACTIVE', 0)} DORMANT={s['status_counts'].get('DORMANT', 0)} COMPLETED={s['status_counts'].get('COMPLETED', 0)} ORPHANED={s['status_counts'].get('ORPHANED', 0)} ARCHIVED={s['status_counts'].get('ARCHIVED', 0)}",
    ]
    for tree_name, tree_info in sorted(s["trees"].items()):
        root = tree_info["root"]
        root_line = root["title"] if root else "?"
        lines.append(f"  [{tree_name}] {root_line} (活跃:{tree_info['active']} 休眠:{tree_info['dormant']})")

    if s["pending_nodes"] > 0:
        lines.append(f"\n  ⚠ {s['pending_nodes']} 个待处理节点 (DORMANT)")

    eligible = gc_check(memory_root)
    if eligible:
        lines.append(f"\n  GC 候选: {len(eligible)} 个节点可回收")

    return "\n".join(lines)


# ── Search ────────────────────────────────────────────────────────

def search_nodes(query: str, memory_root: str = MEMORY_ROOT, limit: int = 20) -> list[dict]:
    """Full-text search across memory nodes. Returns matching nodes with relevance."""
    nodes = collect_all_nodes(memory_root)
    results = []
    q = query.lower()

    for n in nodes:
        score = 0
        fm = n["frontmatter"]
        body = n["body"].lower()

        # Tags match (highest weight)
        tags = fm.get("tags", [])
        for tag in tags:
            if q in str(tag).lower():
                score += 10

        # Title match
        title = body.split("\n")[0].lstrip("# ").lower()
        if q in title:
            score += 8

        # ID match
        if q in fm.get("id", "").lower():
            score += 6

        # Body match
        score += body.count(q)

        if score > 0:
            results.append({"node": n, "score": score, "id": fm.get("id", "?"),
                           "title": title, "status": fm.get("status", "?"),
                           "heartbeat": fm.get("heartbeat", "?")})

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


# ── Node Creation ─────────────────────────────────────────────────

def create_node(tree: str, node_type: str, title: str, parent_id: str = None,
                layer: str = "L1", priority: str = "MEDIUM",
                memory_root: str = MEMORY_ROOT) -> dict:
    """Create a new memory node. Returns the created node info."""
    existing = collect_all_nodes(memory_root)
    existing_ids = {n["frontmatter"].get("id", "") for n in existing}

    nid = _node_id(tree, node_type, _next_number(tree, node_type, existing_ids))

    # Determine file path
    if tree == "forest":
        subdir = ""
        fname = {
            "ROOT": "forest-root.md",
            "BRANCH": f"BRANCH-{nid}.md",
        }.get(node_type, f"{nid}.md")
    elif tree == "system":
        subdir = "system-tree"
        fname = {
            "ROOT": "ROOT.md",
        }.get(node_type, f"{nid}.md")
    elif tree == "experiences":
        subdir = f"experiences-tree/{'core' if layer == 'L4' else 'patterns'}"
        fname = f"{nid}.md"
    elif tree == "projects":
        subdir = "projects-tree"
        fname = {
            "ROOT": "ROOT.md",
        }.get(node_type, f"{nid}.md")
    else:
        subdir = tree
        fname = f"{nid}.md"

    filepath = os.path.join(memory_root, subdir, fname)

    frontmatter = {
        "id": nid,
        "type": node_type,
        "tree": tree,
        "layer": layer,
        "status": "ACTIVE",
        "parent": parent_id,
        "children": [],
        "created": _today(),
        "heartbeat": _today(),
        "priority": priority,
        "tags": [],
    }

    body = f"# {title}\n\n## 目标\n\n\n## 当前状态\n新建于 {_today()}\n\n## 任务清单\n"

    if parent_id:
        # Update parent's children list
        parent = node_by_id(parent_id, existing)
        if parent:
            pfm = parent["frontmatter"]
            children = pfm.get("children", [])
            if nid not in children:
                children.append(nid)
                pfm["children"] = children
                save_node(parent["filepath"], pfm, parent["body"])

    save_node(filepath, frontmatter, body)
    return {"id": nid, "filepath": filepath, "frontmatter": frontmatter}


# ── Experience Extraction ─────────────────────────────────────────

def extract_experience(node: dict, all_nodes: list[dict] = None) -> Optional[str]:
    """Suggest experience extraction from a completed node. Returns suggestion or None."""
    fm = node["frontmatter"]
    if fm.get("status") not in ("COMPLETED",):
        return None

    # Check if experience already extracted
    existing_refs = fm.get("experience_refs", [])
    if existing_refs:
        return None

    # Simple heuristic: look for sections that might contain lessons
    body = node["body"]
    patterns = []
    for keyword in ["教训", "经验", "lesson", "关键决策", "阻塞项", "问题", "错误"]:
        if keyword in body:
            patterns.append(keyword)

    if patterns:
        return f"节点 {fm.get('id')} 可能包含可提炼经验 (关键词: {', '.join(patterns)})"

    return None


# ── Health Check ──────────────────────────────────────────────────

def forest_health(memory_root: str = MEMORY_ROOT) -> dict:
    """Comprehensive health check of the memory forest."""
    nodes = collect_all_nodes(memory_root)
    issues = []
    warnings = []

    id_map = {}
    for n in nodes:
        fm = n["frontmatter"]
        nid = fm.get("id")
        if nid:
            if nid in id_map:
                issues.append(f"Duplicate ID: {nid}")
            id_map[nid] = n

    for n in nodes:
        fm = n["frontmatter"]
        nid = fm.get("id", "?")
        parent_id = fm.get("parent")

        # Orphan check
        if parent_id and parent_id not in id_map:
            issues.append(f"{nid}: parent {parent_id} not found")

        # Missing heartbeat
        if not fm.get("heartbeat"):
            warnings.append(f"{nid}: missing heartbeat")

        # Empty children on BRANCH
        if fm.get("type") == "BRANCH" and not fm.get("children"):
            warnings.append(f"{nid}: BRANCH with no children")

        # ROOT without children
        if fm.get("type") == "ROOT" and not fm.get("children"):
            warnings.append(f"{nid}: ROOT with no children registered")

    return {
        "healthy": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "total_nodes": len(nodes),
        "duplicate_ids": len(issues),
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        print(status_report())
    elif len(sys.argv) > 1 and sys.argv[1] == "heartbeat":
        dry = "--dry-run" in sys.argv
        changes = heartbeat_all(dry_run=dry)
        if changes:
            print("\n".join(changes))
        else:
            print("No heartbeat changes needed.")
    elif len(sys.argv) > 1 and sys.argv[1] == "gc":
        dry = "--dry-run" in sys.argv or "-n" in sys.argv
        actions = gc_run(dry_run=dry)
        if actions:
            print("\n".join(actions))
        else:
            print("No GC candidates found.")
    else:
        print(status_report())
