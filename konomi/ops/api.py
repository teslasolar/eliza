"""
API Server — lightweight REST-style interface for konomi directory ops.

Uses only stdlib (http.server) so there are no external dependencies.
Start: python -m konomi.ops.api [--port 8077]

Endpoints:
    GET  /packages              — list all subpackages
    GET  /packages/<name>       — package details
    GET  /tags                  — all tags (query: ?package=isa88)
    GET  /tags/<path>           — read a tag
    GET  /search?q=<pattern>    — search tags
    POST /compile               — compile to L5X (body: {package, project})
    GET  /summary               — system summary
"""

import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from konomi.ops.directory_ops import DirectoryOps


class _Handler(BaseHTTPRequestHandler):
    """HTTP handler delegating to DirectoryOps."""

    ops: DirectoryOps = None  # set by APIServer before serving

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        qs = parse_qs(parsed.query)

        if path == "/packages":
            self._respond(self.ops.list_packages())
        elif path.startswith("/packages/"):
            name = path.split("/")[-1]
            self._respond(self.ops.get_package(name))
        elif path == "/tags":
            pkg = qs.get("package", [None])[0]
            self._respond(self.ops.list_tags(pkg))
        elif path.startswith("/tags/"):
            tag_path = path[len("/tags/"):]
            self._respond(self.ops.read_tag(tag_path))
        elif path == "/search":
            pattern = qs.get("q", [""])[0]
            self._respond(self.ops.search_tags(pattern))
        elif path == "/summary":
            self._respond(self.ops.summary())
        else:
            self._respond_json(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path == "/compile":
            body = self._read_body()
            pkg = body.get("package")
            project = body.get("project", "KONOMI")
            self._respond(self.ops.compile_l5x(pkg, project))
        else:
            self._respond_json(404, {"error": "not found"})

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def _respond(self, result):
        code = 200 if result.ok else 400
        self._respond_json(code, result.to_dict())

    def _respond_json(self, code: int, data: dict):
        body = json.dumps(data, indent=2, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[API] {args[0]} {args[1]} {args[2]}")


class APIServer:
    """Lightweight REST API server for konomi ops."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8077):
        self.host = host
        self.port = port
        self.ops = DirectoryOps()

    def serve(self):
        """Start serving (blocking)."""
        _Handler.ops = self.ops
        server = HTTPServer((self.host, self.port), _Handler)
        print(f"[API] KONOMI API on http://{self.host}:{self.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n[API] Shutting down.")
            server.server_close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="KONOMI REST API")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8077)
    args = parser.parse_args()
    APIServer(host=args.host, port=args.port).serve()


if __name__ == "__main__":
    main()
