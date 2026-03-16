# OPC-UA Communication

Industrial communication standard — nodes, methods, subscriptions, and companion specifications.

## Key Classes

- **NodeClass** — Object, Variable, Method, View, DataType, ReferenceType
- **AccessLevel** — Read, Write, HistoryRead, HistoryWrite
- **OPCNode** — A node in the address space
- **OPCVariable** — A variable node with value and data type
- **OPCMethod** — A callable method with input/output arguments
- **AddressSpace** — The full node tree
- **Subscription** — Monitored items with sampling intervals

## Core Concepts

- **Address Space**: Tree of nodes — everything is a node (objects, variables, methods)
- **Browse/Read/Write**: Navigate the tree, read values, write commands
- **Subscriptions**: Don't poll — subscribe to changes with configurable deadband
- **Companion Specs**: ISA-95, ISA-88, PackML all have OPC-UA companion specifications
