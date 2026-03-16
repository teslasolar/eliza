"""
Modbus Function Codes — the operation codes that define reads,
writes, and diagnostics in the Modbus protocol.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class FunctionCategory(Enum):
    """Function code categories."""
    READ = "read"
    WRITE_SINGLE = "write_single"
    WRITE_MULTI = "write_multi"
    READ_WRITE = "read_write"
    DIAGNOSTIC = "diagnostic"


@dataclass(frozen=True)
class FunctionCode:
    """A Modbus function code definition."""
    code: int
    name: str
    category: FunctionCategory
    description: str = ""
    request_size: Optional[str] = None    # description of request PDU
    response_size: Optional[str] = None   # description of response PDU
    broadcast_allowed: bool = False

    @property
    def hex_code(self) -> str:
        return f"0x{self.code:02X}"

    @property
    def is_read(self) -> bool:
        return self.category in (FunctionCategory.READ, FunctionCategory.READ_WRITE)

    @property
    def is_write(self) -> bool:
        return self.category in (
            FunctionCategory.WRITE_SINGLE,
            FunctionCategory.WRITE_MULTI,
            FunctionCategory.READ_WRITE,
        )

    @property
    def exception_code(self) -> int:
        """Function code value in exception response (code + 0x80)."""
        return self.code + 0x80

    def __repr__(self):
        return f"FC{self.code:02d}({self.name})"


# Standard Modbus function codes
FC01 = FunctionCode(
    code=1, name="ReadCoils", category=FunctionCategory.READ,
    description="Read 1-2000 contiguous coils",
    request_size="4 bytes (addr + quantity)", response_size="N bytes (bit-packed)",
)

FC02 = FunctionCode(
    code=2, name="ReadDiscreteInputs", category=FunctionCategory.READ,
    description="Read 1-2000 contiguous discrete inputs",
    request_size="4 bytes (addr + quantity)", response_size="N bytes (bit-packed)",
)

FC03 = FunctionCode(
    code=3, name="ReadHoldingRegisters", category=FunctionCategory.READ,
    description="Read 1-125 contiguous holding registers",
    request_size="4 bytes (addr + quantity)", response_size="N*2 bytes",
)

FC04 = FunctionCode(
    code=4, name="ReadInputRegisters", category=FunctionCategory.READ,
    description="Read 1-125 contiguous input registers",
    request_size="4 bytes (addr + quantity)", response_size="N*2 bytes",
)

FC05 = FunctionCode(
    code=5, name="WriteSingleCoil", category=FunctionCategory.WRITE_SINGLE,
    description="Write a single coil (ON=0xFF00, OFF=0x0000)",
    request_size="4 bytes (addr + value)", response_size="4 bytes (echo)",
    broadcast_allowed=True,
)

FC06 = FunctionCode(
    code=6, name="WriteSingleRegister", category=FunctionCategory.WRITE_SINGLE,
    description="Write a single holding register",
    request_size="4 bytes (addr + value)", response_size="4 bytes (echo)",
    broadcast_allowed=True,
)

FC15 = FunctionCode(
    code=15, name="WriteMultipleCoils", category=FunctionCategory.WRITE_MULTI,
    description="Write 1-1968 contiguous coils",
    request_size="5+N bytes (addr + qty + values)", response_size="4 bytes (addr + qty)",
    broadcast_allowed=True,
)

FC16 = FunctionCode(
    code=16, name="WriteMultipleRegisters", category=FunctionCategory.WRITE_MULTI,
    description="Write 1-123 contiguous holding registers",
    request_size="5+N*2 bytes (addr + qty + values)", response_size="4 bytes (addr + qty)",
    broadcast_allowed=True,
)

FC23 = FunctionCode(
    code=23, name="ReadWriteMultipleRegisters", category=FunctionCategory.READ_WRITE,
    description="Atomically read and write holding registers in one transaction",
    request_size="9+N*2 bytes", response_size="N*2 bytes (read data)",
)

FUNCTION_CODES: dict[int, FunctionCode] = {
    fc.code: fc for fc in [FC01, FC02, FC03, FC04, FC05, FC06, FC15, FC16, FC23]
}
