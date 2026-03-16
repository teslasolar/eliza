# OPC-UA Communication Tags

Tag provider for OPC-UA communication. Exposes server status, node counts, subscription health, and companion spec activation.

```python
"""
OPC-UA Tag Provider — Ignition-style tags for OPC-UA communication.

Exposes server status, node counts, subscription health,
and companion spec activation.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class OPCUATagProvider(TagProvider):
    """Tag provider for OPC-UA."""

    def __init__(self):
        super().__init__(prefix="OPCUA")
        self.register(Tag(path="Server_State", type=TagType.STRING,
                          desc="OPC-UA server state"))
        self.register(Tag(path="Node_Count", type=TagType.INTEGER,
                          desc="Total nodes in address space"))
        self.register(Tag(path="Variable_Count", type=TagType.INTEGER,
                          desc="Variable nodes (data points)"))
        self.register(Tag(path="Method_Count", type=TagType.INTEGER,
                          desc="Callable method nodes"))
        self.register(Tag(path="Active_Subscriptions", type=TagType.INTEGER,
                          desc="Active monitored subscriptions"))
        self.register(Tag(path="Monitored_Items", type=TagType.INTEGER,
                          desc="Total monitored items across subscriptions"))
        self.register(Tag(path="Companions_Loaded", type=TagType.INTEGER,
                          desc="Companion specs loaded (ISA-95, PackML, etc.)"))
        self.register(Tag(path="Publish_Interval_Ms", type=TagType.ANALOG,
                          desc="Default publish interval", unit="ms"))
        # Defaults
        self.get("OPCUA_Server_State").write("Running")
        self.get("OPCUA_Publish_Interval_Ms").write(1000.0)


def create_provider() -> OPCUATagProvider:
    return OPCUATagProvider()
```
