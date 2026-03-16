# Modbus Field Protocol Tags

Tag provider for Modbus field protocol. Exposes connection status, register counts, poll rates, error tracking, and byte-order configuration.

```python
"""
Modbus Tag Provider — Ignition-style tags for Modbus field protocol.

Exposes connection status, register counts, poll rates,
error tracking, and byte-order configuration.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ModbusTagProvider(TagProvider):
    """Tag provider for Modbus."""

    def __init__(self):
        super().__init__(prefix="MODBUS")
        self.register(Tag(path="Connected", type=TagType.DISCRETE,
                          desc="Modbus connection active"))
        self.register(Tag(path="Unit_ID", type=TagType.INTEGER,
                          desc="Active Modbus unit/slave ID"))
        self.register(Tag(path="Coil_Count", type=TagType.INTEGER,
                          desc="Registered coil tags"))
        self.register(Tag(path="Holding_Count", type=TagType.INTEGER,
                          desc="Registered holding register tags"))
        self.register(Tag(path="Input_Count", type=TagType.INTEGER,
                          desc="Registered input register tags"))
        self.register(Tag(path="Discrete_Count", type=TagType.INTEGER,
                          desc="Registered discrete input tags"))
        self.register(Tag(path="Poll_Rate_Ms", type=TagType.ANALOG,
                          desc="Polling interval", unit="ms"))
        self.register(Tag(path="Errors_Total", type=TagType.INTEGER,
                          desc="Total communication errors"))
        self.register(Tag(path="Errors_Timeout", type=TagType.INTEGER,
                          desc="Timeout errors"))
        self.register(Tag(path="Errors_CRC", type=TagType.INTEGER,
                          desc="CRC mismatch errors"))
        self.register(Tag(path="Byte_Order", type=TagType.STRING,
                          desc="Active byte order (ABCD/CDAB/BADC/DCBA)"))
        # Defaults
        self.get("MODBUS_Connected").write(False)
        self.get("MODBUS_Unit_ID").write(1)
        self.get("MODBUS_Poll_Rate_Ms").write(1000.0)
        self.get("MODBUS_Byte_Order").write("ABCD")


def create_provider() -> ModbusTagProvider:
    return ModbusTagProvider()
```
