"""
Modbus Register Types — the four register areas that define the
Modbus data model: coils, discrete inputs, holding registers, input registers.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class RegisterType(Enum):
    """The four Modbus register types."""
    COIL = "coil"
    DISCRETE_INPUT = "discrete_input"
    HOLDING_REGISTER = "holding_register"
    INPUT_REGISTER = "input_register"


class Access(Enum):
    """Register access mode."""
    READ_ONLY = "RO"
    READ_WRITE = "RW"


@dataclass(frozen=True)
class RegisterDef:
    """Definition of a Modbus register type with function code mappings."""
    register_type: RegisterType
    address_min: int
    address_max: int
    access: Access
    data_width: str          # "bit" or "uint16"
    fc_read: int             # function code for single/multi read
    fc_write_single: Optional[int] = None
    fc_write_multi: Optional[int] = None
    description: str = ""

    @property
    def is_writable(self) -> bool:
        return self.access == Access.READ_WRITE

    @property
    def is_bit(self) -> bool:
        return self.data_width == "bit"

    @property
    def is_register(self) -> bool:
        return self.data_width == "uint16"

    def valid_address(self, addr: int) -> bool:
        """Check if an address is in valid range."""
        return self.address_min <= addr <= self.address_max

    def __repr__(self):
        return (f"RegisterDef({self.register_type.value}, "
                f"{self.access.value}, FC_read={self.fc_read})")


# Standard Modbus register type definitions
COIL = RegisterDef(
    register_type=RegisterType.COIL,
    address_min=0, address_max=65535,
    access=Access.READ_WRITE,
    data_width="bit",
    fc_read=1,
    fc_write_single=5,
    fc_write_multi=15,
    description="Read/write single-bit coils",
)

DISCRETE_INPUT = RegisterDef(
    register_type=RegisterType.DISCRETE_INPUT,
    address_min=0, address_max=65535,
    access=Access.READ_ONLY,
    data_width="bit",
    fc_read=2,
    description="Read-only single-bit discrete inputs",
)

HOLDING_REGISTER = RegisterDef(
    register_type=RegisterType.HOLDING_REGISTER,
    address_min=0, address_max=65535,
    access=Access.READ_WRITE,
    data_width="uint16",
    fc_read=3,
    fc_write_single=6,
    fc_write_multi=16,
    description="Read/write 16-bit holding registers",
)

INPUT_REGISTER = RegisterDef(
    register_type=RegisterType.INPUT_REGISTER,
    address_min=0, address_max=65535,
    access=Access.READ_ONLY,
    data_width="uint16",
    fc_read=4,
    description="Read-only 16-bit input registers",
)

REGISTER_TYPES: dict[RegisterType, RegisterDef] = {
    RegisterType.COIL: COIL,
    RegisterType.DISCRETE_INPUT: DISCRETE_INPUT,
    RegisterType.HOLDING_REGISTER: HOLDING_REGISTER,
    RegisterType.INPUT_REGISTER: INPUT_REGISTER,
}
