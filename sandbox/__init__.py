"""
Sandbox — isolated MCP tool environment for ELIZA.

Provides tools that ELIZA can call during vetting sessions,
separate from her own core interview logic. Each tool is a
self-contained operation ELIZA can invoke via MCP.

Run as server:
    python -m sandbox            # MCP stdio server
    python -m sandbox --http     # HTTP API on :8078
    python -m sandbox --list     # list available tools
"""

from sandbox.tools import TOOLS, SandboxTool, call_tool
from sandbox.registry import SandboxRegistry
