"""
MCP Provider — Model Context Protocol tool definitions for konomi.

Exposes konomi directory operations as MCP tools that any MCP-compatible
client (Claude Code, Cursor, etc.) can discover and invoke.

Each tool maps 1:1 to a DirectoryOps method.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from konomi.ops.directory_ops import DirectoryOps, OpResult


@dataclass(frozen=True)
class MCPToolParam:
    """A single parameter for an MCP tool."""
    name: str
    type: str = "string"
    desc: str = ""
    required: bool = False


@dataclass(frozen=True)
class MCPToolDef:
    """An MCP tool definition."""
    name: str
    desc: str
    params: tuple[MCPToolParam, ...] = ()

    def schema(self) -> dict:
        """JSON Schema for this tool's input."""
        props = {}
        required = []
        for p in self.params:
            props[p.name] = {"type": p.type, "description": p.desc}
            if p.required:
                required.append(p.name)
        s = {"type": "object", "properties": props}
        if required:
            s["required"] = required
        return s

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.desc,
            "inputSchema": self.schema(),
        }


class MCPProvider:
    """MCP tool provider for konomi directory operations."""

    def __init__(self):
        self.ops = DirectoryOps()
        self._tools = self._build_tools()
        self._handlers: dict[str, Callable] = {
            "konomi_list_packages": lambda _: self.ops.list_packages(),
            "konomi_get_package": lambda p: self.ops.get_package(p["name"]),
            "konomi_list_tags": lambda p: self.ops.list_tags(p.get("package")),
            "konomi_read_tag": lambda p: self.ops.read_tag(p["path"]),
            "konomi_search_tags": lambda p: self.ops.search_tags(p["pattern"]),
            "konomi_compile_l5x": lambda p: self.ops.compile_l5x(
                p.get("package"), p.get("project", "KONOMI")),
            "konomi_export_l5x": lambda p: self.ops.export_l5x(
                p["path"], p.get("package"), p.get("project", "KONOMI")),
            "konomi_summary": lambda _: self.ops.summary(),
        }

    def _build_tools(self) -> list[MCPToolDef]:
        return [
            MCPToolDef("konomi_list_packages",
                       "List all konomi subpackages with descriptions"),
            MCPToolDef("konomi_get_package",
                       "Get details of a specific konomi package",
                       (MCPToolParam("name", "string",
                                     "Package name (e.g. isa88)", True),)),
            MCPToolDef("konomi_list_tags",
                       "List tags, optionally filtered by package",
                       (MCPToolParam("package", "string",
                                     "Filter by package name"),)),
            MCPToolDef("konomi_read_tag",
                       "Read a specific tag value by path",
                       (MCPToolParam("path", "string", "Tag path", True),)),
            MCPToolDef("konomi_search_tags",
                       "Search tags by substring pattern",
                       (MCPToolParam("pattern", "string",
                                     "Search pattern", True),)),
            MCPToolDef("konomi_compile_l5x",
                       "Compile konomi tags to Rockwell L5X XML",
                       (MCPToolParam("package", "string",
                                     "Package to compile (all if omitted)"),
                        MCPToolParam("project", "string",
                                     "L5X project name"),)),
            MCPToolDef("konomi_export_l5x",
                       "Compile and write L5X file to disk",
                       (MCPToolParam("path", "string",
                                     "Output file path", True),
                        MCPToolParam("package", "string",
                                     "Package to compile"),
                        MCPToolParam("project", "string",
                                     "L5X project name"),)),
            MCPToolDef("konomi_summary",
                       "Get full konomi system summary"),
        ]

    # ── MCP protocol methods ─────────────────────────────────────────

    def list_tools(self) -> list[dict]:
        """Return tool definitions for MCP tools/list."""
        return [t.to_dict() for t in self._tools]

    def call_tool(self, name: str, arguments: dict = None) -> dict:
        """Execute an MCP tool call. Returns MCP-formatted response."""
        handler = self._handlers.get(name)
        if not handler:
            return {"content": [{"type": "text",
                                 "text": f"Unknown tool: {name}"}],
                    "isError": True}
        result = handler(arguments or {})
        return self._format_result(result)

    @staticmethod
    def _format_result(result: OpResult) -> dict:
        """Convert OpResult to MCP tool response format."""
        import json
        if result.ok:
            if isinstance(result.data, str):
                text = result.data
            else:
                text = json.dumps(result.data, indent=2, default=str)
            return {"content": [{"type": "text", "text": text}]}
        return {"content": [{"type": "text", "text": result.error}],
                "isError": True}

    def __repr__(self):
        return f"MCPProvider(tools={len(self._tools)})"
