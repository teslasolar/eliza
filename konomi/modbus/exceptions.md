# Modbus Exception Codes

Error responses from Modbus devices. When a request fails, the device returns the function code + 0x80 followed by one of these exception codes.

```python
"""
Modbus Exception Codes — error responses from Modbus devices.
When a request fails, the device returns the function code + 0x80
followed by one of these exception codes.
"""

from enum import IntEnum


class ModbusException(IntEnum):
    """Standard Modbus exception codes."""
    ILLEGAL_FUNCTION = 0x01
    ILLEGAL_DATA_ADDRESS = 0x02
    ILLEGAL_DATA_VALUE = 0x03
    SERVER_DEVICE_FAILURE = 0x04
    ACKNOWLEDGE = 0x05
    SERVER_DEVICE_BUSY = 0x06
    MEMORY_PARITY_ERROR = 0x08
    GATEWAY_PATH_UNAVAILABLE = 0x0A
    GATEWAY_TARGET_FAILED = 0x0B

    @property
    def hex_code(self) -> str:
        return f"0x{self.value:02X}"

    @property
    def description(self) -> str:
        """Human-readable description of the exception."""
        descriptions = {
            0x01: "Function code not supported by device",
            0x02: "Register address not valid or out of range",
            0x03: "Value in data field not acceptable",
            0x04: "Unrecoverable error in device while processing",
            0x05: "Request accepted, processing in progress (long operation)",
            0x06: "Device busy with another long-duration operation",
            0x08: "Memory parity error in extended memory area",
            0x0A: "Gateway could not allocate path to target device",
            0x0B: "Gateway target device failed to respond",
        }
        return descriptions.get(self.value, "Unknown exception")

    @property
    def is_retryable(self) -> bool:
        """Whether the request might succeed if retried."""
        return self in (
            ModbusException.ACKNOWLEDGE,
            ModbusException.SERVER_DEVICE_BUSY,
            ModbusException.GATEWAY_TARGET_FAILED,
        )

    @property
    def is_fatal(self) -> bool:
        """Whether this indicates a non-recoverable condition."""
        return self in (
            ModbusException.SERVER_DEVICE_FAILURE,
            ModbusException.MEMORY_PARITY_ERROR,
        )

    def __repr__(self):
        return f"ModbusException({self.hex_code}: {self.name})"
```
