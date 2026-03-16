"""Run sandbox as: python -m sandbox"""
import sys
from sandbox import SandboxRegistry


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sandbox MCP Tools for ELIZA")
    parser.add_argument("--list", action="store_true", help="List all tools")
    parser.add_argument("--call", type=str, help="Call a tool by name")
    parser.add_argument("--args", type=str, default="{}", help="JSON args")
    parser.add_argument("--http", action="store_true", help="Start HTTP server")
    parser.add_argument("--port", type=int, default=8078, help="HTTP port")
    args = parser.parse_args()

    reg = SandboxRegistry()

    if args.list:
        for t in reg.list_tools():
            print(f"  {t['name']:<28s} {t['description']}")
        return 0

    if args.call:
        import json
        params = json.loads(args.args)
        result = reg.call_tool(args.call, params)
        print(json.dumps(result, indent=2, default=str))
        return 0

    if args.http:
        from sandbox.server import serve
        serve(reg, port=args.port)
        return 0

    # Default: MCP stdio mode
    from sandbox.mcp_stdio import run_stdio
    run_stdio(reg)
    return 0


sys.exit(main() or 0)
