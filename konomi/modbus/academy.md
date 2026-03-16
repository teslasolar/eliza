# Modbus Protocol

The workhorse field protocol — registers, function codes, and data types for PLCs and field devices.

## Key Classes

- **RegisterType** — Coil, Discrete Input, Input Register, Holding Register
- **RegisterDef** — Register definition with address, type, scaling
- **ModbusDataType** — UINT16, INT16, FLOAT32, UINT32, etc.
- **ModbusMap** — Complete register map for a device
- **FunctionCode** — Read Coils (01), Read Holding (03), Write Single (06), Write Multiple (16)
- **ModbusException** — Error responses (Illegal Function, Illegal Data Address, etc.)

## Core Concepts

- **4 Register Types**: Coils (RW bits), Discrete Inputs (RO bits), Input Registers (RO 16-bit), Holding Registers (RW 16-bit)
- **Big-Endian by Default**: But many devices use word-swap for 32-bit floats — always check
- **Polling Model**: Modbus is request/response — you ask for data, the device replies
- **Address Offsets**: Modbus addresses are 0-based in protocol, but documentation often shows 1-based (40001 = holding register 0)
