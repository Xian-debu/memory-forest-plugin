#!/usr/bin/env python3
"""n8n Workflow Manager - Manage n8n workflows from the command line."""
import os, sys, json, argparse
from urllib.request import Request, urlopen
from urllib.error import URLError

N8N_URL = os.environ.get("N8N_URL", "http://localhost:5678")
COOKIE_FILE = "/tmp/n8n_cookies.txt"

class N8nManager:
    def __init__(self):
        self.base = N8N_URL.rstrip("/")
        self.cookies = self._load_cookies()

    def _load_cookies(self):
        """Load n8n auth cookie from Netscape cookie file."""
        if not os.path.exists(COOKIE_FILE):
            return ""
        with open(COOKIE_FILE) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Handle HttpOnly prefix (e.g. "#HttpOnly_localhost")
                if line.startswith("#HttpOnly_"):
                    line = line.split("_", 1)[1] if "_" in line else line[1:]
                elif line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 7 and parts[5] == "n8n-auth":
                    return f"n8n-auth={parts[6]}"
        return ""

    def _request(self, method, path, data=None):
        url = f"{self.base}/rest{path}"
        headers = {}
        if data is not None:
            headers["Content-Type"] = "application/json"
        if self.cookies:
            headers["Cookie"] = self.cookies
        body = json.dumps(data).encode() if data is not None else None
        req = Request(url, data=body, headers=headers, method=method)
        try:
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except URLError as e:
            return {"error": str(e)}

    def list_workflows(self):
        result = self._request("GET", "/workflows")
        if "error" in result:
            print(f"Error: {result['error']}")
            return []
        workflows = result.get("data", [])
        if not workflows:
            print("No workflows found.")
            return []
        print(f"{'ID':20} {'Active':8} {'Name'}")
        print("-" * 60)
        for wf in workflows:
            print(f"{wf['id']:20} {'YES' if wf['active'] else 'no':8} {wf['name']}")
        return workflows

    def get_workflow(self, wf_id):
        result = self._request("GET", f"/workflows/{wf_id}")
        if "data" in result:
            return result["data"]
        print(f"Error: {result}")
        return None

    def create_workflow(self, json_file):
        with open(json_file) as f:
            data = json.load(f)
        result = self._request("POST", "/workflows", data)
        if "data" in result:
            wf = result["data"]
            print(f"Created: {wf['id']} - {wf['name']} (active={wf['active']})")
            return wf
        print(f"Error creating workflow: {result}")
        return None

    def toggle_workflow(self, wf_id, active):
        result = self._request("PATCH", f"/workflows/{wf_id}", {"active": active})
        if "data" in result:
            print(f"Workflow {wf_id[:12]}... active={result['data']['active']}")
        else:
            print(f"Error: {result}")

    def status(self):
        result = self._request("GET", "/workflows")
        if "error" in result:
            print(f"n8n API error: {result['error']}")
            return
        workflows = result.get("data", [])
        active = sum(1 for w in workflows if w["active"])
        print(f"n8n: {result.get('count', 0)} workflows ({active} active)")
        print(f"URL: {self.base}")

    def stats(self):
        result = self._request("GET", "/workflows")
        if "error" in result:
            print(f"Error: {result}")
            return
        workflows = result.get("data", [])
        active = [w for w in workflows if w["active"]]
        inactive = [w for w in workflows if not w["active"]]
        print(f"Active workflows: {len(active)}")
        for w in active:
            print(f"  - {w['name']} ({w['id'][:12]}...)")
        print(f"\nInactive workflows: {len(inactive)}")
        for w in inactive:
            print(f"  - {w['name']} ({w['id'][:12]}...)")


def main():
    parser = argparse.ArgumentParser(description="n8n Workflow Manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all workflows")
    sub.add_parser("status", help="Show n8n status overview")
    sub.add_parser("stats", help="Show workflow statistics")

    show_p = sub.add_parser("show", help="Show workflow details")
    show_p.add_argument("id", help="Workflow ID")

    toggle_p = sub.add_parser("toggle", help="Toggle workflow active state")
    toggle_p.add_argument("id", help="Workflow ID")
    toggle_p.add_argument("state", choices=["on", "off"])

    create_p = sub.add_parser("create", help="Create workflow from JSON file")
    create_p.add_argument("file", help="JSON file path")

    args = parser.parse_args()
    mgr = N8nManager()

    if args.command == "list":
        mgr.list_workflows()
    elif args.command == "show":
        wf = mgr.get_workflow(args.id)
        if wf:
            print(json.dumps(wf, indent=2))
    elif args.command == "toggle":
        mgr.toggle_workflow(args.id, args.state == "on")
    elif args.command == "create":
        mgr.create_workflow(args.file)
    elif args.command == "status":
        mgr.status()
    elif args.command == "stats":
        mgr.stats()
    else:
        # Default: show status
        mgr.status()
        print()
        mgr.list_workflows()

if __name__ == "__main__":
    main()
