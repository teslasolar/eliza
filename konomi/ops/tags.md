# Operations CLI/API/MCP Tags

Tag provider for the operations layer. Exposes API health, request counts, MCP tool invocations, and CLI command history.

```python
"""
Ops Tag Provider — Ignition-style tags for CLI/API/MCP operations.

Exposes API health, request counts, MCP tool invocations,
and CLI command history.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class OpsTagProvider(TagProvider):
    """Tag provider for the operations layer."""

    def __init__(self):
        super().__init__(prefix="OPS")
        self.register(Tag(path="API_Status", type=TagType.STRING,
                          desc="REST API server status"))
        self.register(Tag(path="API_Port", type=TagType.INTEGER,
                          desc="REST API port number"))
        self.register(Tag(path="API_Requests", type=TagType.INTEGER,
                          desc="Total API requests served"))
        self.register(Tag(path="MCP_Tools", type=TagType.INTEGER,
                          desc="Number of registered MCP tools"))
        self.register(Tag(path="MCP_Calls", type=TagType.INTEGER,
                          desc="Total MCP tool invocations"))
        self.register(Tag(path="CLI_Commands", type=TagType.INTEGER,
                          desc="Total CLI commands executed"))
        self.register(Tag(path="Last_Command", type=TagType.STRING,
                          desc="Last CLI command run"))
        # Defaults
        self.get("OPS_API_Status").write("stopped")
        self.get("OPS_API_Port").write(8077)
        self.get("OPS_MCP_Tools").write(8)


def create_provider() -> OpsTagProvider:
    return OpsTagProvider()
```
