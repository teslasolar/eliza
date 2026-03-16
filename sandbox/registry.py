"""
Sandbox Registry — aggregates tools and provides MCP-compatible interface.
"""

from typing import Optional
from sandbox.tools import TOOLS, SandboxTool, call_tool


class SandboxRegistry:
    """Central registry of sandbox tools."""

    def __init__(self):
        self._tools: dict[str, SandboxTool] = {}
        for t in TOOLS:
            self._tools[t.name] = t

    def list_tools(self) -> list[dict]:
        """MCP tools/list response."""
        return [t.to_dict() for t in self._tools.values()]

    def call_tool(self, name: str, arguments: dict = None) -> dict:
        """MCP tools/call response."""
        tool = self._tools.get(name)
        if not tool:
            return {"content": [{"type": "text",
                                 "text": f"Unknown tool: {name}"}],
                    "isError": True}
        return call_tool(tool, arguments or {})

    def get(self, name: str) -> Optional[SandboxTool]:
        return self._tools.get(name)

    @property
    def count(self) -> int:
        return len(self._tools)

    def __repr__(self):
        return f"SandboxRegistry(tools={self.count})"
