# MCP Stdio Transport — JSON-RPC over stdin/stdout

Reads JSON-RPC from stdin, writes to stdout.
Implements the minimal MCP protocol: `initialize`, `tools/list`, `tools/call`.

```python
import json
import sys


def run_stdio(registry):
    """Run MCP server over stdio (JSON-RPC 2.0)."""
    sys.stderr.write("[sandbox] MCP stdio server ready\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            _respond({"error": {"code": -32700, "message": "Parse error"}})
            continue

        method = msg.get("method", "")
        params = msg.get("params", {})
        msg_id = msg.get("id")

        if method == "initialize":
            _respond({
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": "sandbox",
                        "version": "1.0.0",
                    },
                },
            })
        elif method == "tools/list":
            _respond({
                "id": msg_id,
                "result": {"tools": registry.list_tools()},
            })
        elif method == "tools/call":
            name = params.get("name", "")
            args = params.get("arguments", {})
            result = registry.call_tool(name, args)
            _respond({"id": msg_id, "result": result})
        elif method == "notifications/initialized":
            pass  # client ack, no response needed
        else:
            _respond({
                "id": msg_id,
                "error": {"code": -32601,
                          "message": f"Unknown method: {method}"},
            })


def _respond(data: dict):
    """Write JSON-RPC response to stdout."""
    data.setdefault("jsonrpc", "2.0")
    sys.stdout.write(json.dumps(data) + "\n")
    sys.stdout.flush()
```
