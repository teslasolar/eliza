# Directory Server — Shared Subpackage Runner

Every konomi subpackage can run itself as a CLI tool, HTTP API server, or MCP stdio server. This module is the single-point-of-truth runner that powers all those modes. It accepts a package name, description, and optional tag provider, then dispatches to the appropriate handler based on command-line flags (`--serve`, `--mcp`, `--tags`, `--json`, `--read`).

When no flags are given, it prints a summary of the directory and available run modes. The HTTP server and MCP server are both built entirely on the standard library, with no external dependencies.

## Argument Parsing and Dispatch

```python
"""
Shared directory server — every konomi subpackage can run itself.

    python -m konomi.isa88          # CLI: list tags, describe, status
    python -m konomi.isa88 --serve  # HTTP API for this directory
    python -m konomi.isa88 --mcp    # MCP stdio server for this directory
    python -m konomi.isa88 --tags   # dump all tags from this provider
    python -m konomi.isa88 --json   # JSON export of the directory

This is the single-point-of-truth runner: __init__.py is both the
documentation AND the executable entry point.
"""

import argparse
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


def run_directory(name: str, desc: str, provides: list[str],
                  tag_provider=None, extras: dict = None):
    """Generic runner for any konomi subdirectory.

    Args:
        name: package name (e.g. "isa88")
        desc: one-line description
        provides: list of exported symbols
        tag_provider: optional TagProvider instance
        extras: optional dict of extra data to expose
    """
    parser = argparse.ArgumentParser(
        prog=f"konomi.{name}",
        description=f"KONOMI · {name} — {desc}",
    )
    parser.add_argument("--serve", action="store_true",
                        help="Start HTTP API server")
    parser.add_argument("--port", type=int, default=8080,
                        help="HTTP port (default: 8080)")
    parser.add_argument("--mcp", action="store_true",
                        help="Run as MCP stdio server")
    parser.add_argument("--tags", action="store_true",
                        help="List all tags from this provider")
    parser.add_argument("--json", action="store_true",
                        help="JSON export of directory metadata")
    parser.add_argument("--read", type=str,
                        help="Read a specific tag by path")

    args = parser.parse_args()
    info = _build_info(name, desc, provides, tag_provider, extras)

    if args.json:
        print(json.dumps(info, indent=2, default=str))
        return 0

    if args.tags:
        return _cmd_tags(tag_provider, name)

    if args.read:
        return _cmd_read(tag_provider, args.read)

    if args.serve:
        return _cmd_serve(info, tag_provider, args.port, name)

    if args.mcp:
        return _cmd_mcp(info, tag_provider, name)

    # Default: print directory info
    _print_info(name, desc, provides, tag_provider)
    return 0
```

## Directory Info Helpers

```python
def _build_info(name, desc, provides, tp, extras):
    info = {
        "package": f"konomi.{name}",
        "description": desc,
        "provides": provides,
        "tag_count": tp.count if tp else 0,
    }
    if extras:
        info["extras"] = extras
    if tp:
        info["tags"] = tp.paths()
    return info


def _print_info(name, desc, provides, tp):
    print(f"╔══ konomi.{name} ══╗")
    print(f"║ {desc}")
    print(f"║ Provides: {', '.join(provides[:6])}")
    if len(provides) > 6:
        print(f"║          +{len(provides) - 6} more")
    if tp:
        print(f"║ Tags: {tp.count}")
    print(f"╚{'═' * (len(name) + 14)}╝")
    print(f"\nRun modes:")
    print(f"  python -m konomi.{name} --tags")
    print(f"  python -m konomi.{name} --json")
    print(f"  python -m konomi.{name} --serve --port 8080")
    print(f"  python -m konomi.{name} --mcp")
```

## CLI Commands — Tags and Read

```python
def _cmd_tags(tp, name):
    if not tp:
        print(f"No tag provider for {name}")
        return 1
    print(f"[{name.upper()}] {tp.count} tags:")
    for path in tp.paths():
        tag = tp.get(path)
        v = tag.read()
        print(f"  {path}: {v.v} ({tag.type.value})")
    return 0


def _cmd_read(tp, path):
    if not tp:
        print("No tag provider"); return 1
    tag = tp.get(path)
    if not tag:
        print(f"Tag not found: {path}"); return 1
    v = tag.read()
    print(json.dumps({"path": path, "value": v.v, "quality": str(v.q),
                       "unit": v.unit}, default=str))
    return 0
```

## HTTP Server

```python
def _cmd_serve(info, tp, port, name):
    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            p = self.path.rstrip("/")
            if p in ("", "/"):
                self._j(200, info)
            elif p == "/tags" and tp:
                self._j(200, {"tags": tp.paths(),
                              "values": {k: str(v) for k, v
                                         in tp.read_all().items()}})
            elif p.startswith("/tags/") and tp:
                tag_path = p[6:]
                tag = tp.get(tag_path)
                if tag:
                    v = tag.read()
                    self._j(200, {"path": tag_path, "value": v.v,
                                  "unit": v.unit})
                else:
                    self._j(404, {"error": f"tag not found: {tag_path}"})
            else:
                self._j(404, {"error": "not found"})

        def _j(self, code, data):
            body = json.dumps(data, indent=2, default=str).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *a):
            print(f"[{name}] {a[0]} {a[1]} {a[2]}")

    srv = HTTPServer(("127.0.0.1", port), H)
    print(f"[{name}] HTTP on http://127.0.0.1:{port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[{name}] Stopped.")
        srv.server_close()
    return 0
```

## MCP Stdio Server

```python
def _cmd_mcp(info, tp, name):
    """Minimal MCP stdio server for this directory."""
    tools = [
        {"name": f"{name}_info", "description": info["description"],
         "inputSchema": {"type": "object", "properties": {}}},
        {"name": f"{name}_tags", "description": f"List all {name} tags",
         "inputSchema": {"type": "object", "properties": {}}},
    ]
    if tp:
        tools.append({
            "name": f"{name}_read",
            "description": f"Read a {name} tag by path",
            "inputSchema": {"type": "object",
                            "properties": {"path": {"type": "string"}},
                            "required": ["path"]},
        })

    sys.stderr.write(f"[{name}] MCP stdio ready\n")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        method = msg.get("method", "")
        mid = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            _mcp_out({"id": mid, "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": f"konomi.{name}", "version": "1.0"},
            }})
        elif method == "tools/list":
            _mcp_out({"id": mid, "result": {"tools": tools}})
        elif method == "tools/call":
            tname = params.get("name", "")
            targs = params.get("arguments", {})
            if tname == f"{name}_info":
                _mcp_out({"id": mid, "result": {"content": [
                    {"type": "text", "text": json.dumps(info, indent=2,
                                                         default=str)}]}})
            elif tname == f"{name}_tags" and tp:
                _mcp_out({"id": mid, "result": {"content": [
                    {"type": "text", "text": "\n".join(tp.paths())}]}})
            elif tname == f"{name}_read" and tp:
                tag = tp.get(targs.get("path", ""))
                if tag:
                    v = tag.read()
                    _mcp_out({"id": mid, "result": {"content": [
                        {"type": "text", "text": json.dumps(
                            {"value": v.v, "unit": v.unit},
                            default=str)}]}})
                else:
                    _mcp_out({"id": mid, "result": {
                        "content": [{"type": "text", "text": "not found"}],
                        "isError": True}})
            elif method != "notifications/initialized":
                _mcp_out({"id": mid, "error": {
                    "code": -32601, "message": f"unknown: {tname}"}})
    return 0


def _mcp_out(data):
    data.setdefault("jsonrpc", "2.0")
    sys.stdout.write(json.dumps(data) + "\n")
    sys.stdout.flush()
```
