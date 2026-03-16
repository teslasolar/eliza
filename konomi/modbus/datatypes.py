"""
Modbus Data Type Mappings — how multi-register values are encoded
and decoded across the four byte-order conventions.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

from konomi.modbus.registers import RegisterType


class ByteOrder(Enum):
    """Byte ordering for multi-register values."""
    ABCD = "ABCD"   # Big-endian (most common)
    CDAB = "CDAB"   # Big-endian, word-swapped
    BADC = "BADC"   # Little-endian, word-swapped
    DCBA = "DCBA"   # Little-endian


@dataclass(frozen=True)
class ModbusDataType:
    """A data type and its register layout in Modbus."""
    name: str
    register_count: int      # number of 16-bit registers consumed
    bit_count: int           # total bits
    signed: bool = False
    floating: bool = False
    byte_order_applies: bool = False
    description: str = ""

    @property
    def byte_count(self) -> int:
        return self.bit_count // 8

    @property
    def is_multi_register(self) -> bool:
        return self.register_count > 1

    def __repr__(self):
        return f"ModbusDataType({self.name}, regs={self.register_count})"


# Standard Modbus data type definitions
BOOL = ModbusDataType(
    name="BOOL", register_count=0, bit_count=1,
    description="Single bit; 1 coil or 1 bit in register",
)

INT16 = ModbusDataType(
    name="INT16", register_count=1, bit_count=16, signed=True,
    description="Signed 16-bit integer; 1 register",
)

UINT16 = ModbusDataType(
    name="UINT16", register_count=1, bit_count=16,
    description="Unsigned 16-bit integer; 1 register",
)

INT32 = ModbusDataType(
    name="INT32", register_count=2, bit_count=32,
    signed=True, byte_order_applies=True,
    description="Signed 32-bit integer; 2 registers",
)

UINT32 = ModbusDataType(
    name="UINT32", register_count=2, bit_count=32,
    byte_order_applies=True,
    description="Unsigned 32-bit integer; 2 registers",
)

FLOAT32 = ModbusDataType(
    name="FLOAT32", register_count=2, bit_count=32,
    floating=True, byte_order_applies=True,
    description="IEEE 754 32-bit float; 2 registers",
)

INT64 = ModbusDataType(
    name="INT64", register_count=4, bit_count=64,
    signed=True, byte_order_applies=True,
    description="Signed 64-bit integer; 4 registers",
)

FLOAT64 = ModbusDataType(
    name="FLOAT64", register_count=4, bit_count=64,
    floating=True, byte_order_applies=True,
    description="IEEE 754 64-bit double; 4 registers",
)

STRING = ModbusDataType(
    name="STRING", register_count=0, bit_count=0,
    byte_order_applies=True,
    description="Variable-length string; 2 chars per register",
)

MODBUS_DATA_TYPES: dict[str, ModbusDataType] = {
    dt.name: dt for dt in [
        BOOL, INT16, UINT16, INT32, UINT32, FLOAT32, INT64, FLOAT64, STRING,
    ]
}


@dataclass
class ModbusMap:
    """A mapping from a tag path to a specific Modbus register location."""
    tag_path: str
    unit_id: int
    register_type: RegisterType
    address: int
    data_type: str                          # key into MODBUS_DATA_TYPES
    scale: float = 1.0
    offset: float = 0.0
    byte_order: ByteOrder = ByteOrder.ABCD
    description: str = ""

    @property
    def dtype(self) -> Optional[ModbusDataType]:
        """Resolve the ModbusDataType object."""
        return MODBUS_DATA_TYPES.get(self.data_type)

    @property
    def register_span(self) -> int:
        """Number of registers this mapping occupies."""
        dt = self.dtype
        if dt is None:
            return 1
        return max(dt.register_count, 1)

    def apply_scaling(self, raw: float) -> float:
        """Apply scale and offset: engineering = raw * scale + offset."""
        return raw * self.scale + self.offset

    def reverse_scaling(self, eng: float) -> float:
        """Reverse scale and offset: raw = (engineering - offset) / scale."""
        if self.scale == 0:
            raise ValueError("Scale factor cannot be zero")
        return (eng - self.offset) / self.scale

    def __repr__(self):
        return (f"ModbusMap({self.tag_path}, unit={self.unit_id}, "
                f"{self.register_type.value}@{self.address})")
