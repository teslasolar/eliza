# Sandbox HTTP Server — REST API

REST wrapper around the sandbox tool registry.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/tools` | GET | List all tools (MCP tools/list) |
| `/call` | POST | Call a tool `{name, arguments}` |
| `/health` | GET | Health check |

```python
import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class _Handler(BaseHTTPRequestHandler):
    registry = None

    def do_GET(self):
        path = self.path.rstrip("/")
        if path == "/tools":
            self._json(200, {"tools": self.registry.list_tools()})
        elif path == "/health":
            self._json(200, {"status": "ok",
                             "tools": self.registry.count})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        path = self.path.rstrip("/")
        if path == "/call":
            body = self._read_body()
            name = body.get("name", "")
            args = body.get("arguments", {})
            result = self.registry.call_tool(name, args)
            self._json(200, result)
        else:
            self._json(404, {"error": "not found"})

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return {}

    def _json(self, code: int, data: dict):
        body = json.dumps(data, indent=2, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[sandbox] {args[0]} {args[1]} {args[2]}")


def serve(registry, host: str = "127.0.0.1", port: int = 8078):
    """Start the sandbox HTTP server."""
    _Handler.registry = registry
    server = HTTPServer((host, port), _Handler)
    print(f"[sandbox] HTTP server on http://{host}:{port}")
    print(f"[sandbox] {registry.count} tools available")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[sandbox] Shutting down.")
        server.server_close()
```
