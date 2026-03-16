# L5X Compiler

Generate Rockwell Studio 5000 PLC programs from KONOMI definitions — ladder logic, UDTs, tags, tasks.

## Key Classes

- **L5XCompiler** — Main compiler that generates .L5X XML files
- **L5XProgram** — A PLC program with routines
- **Rung** — A ladder logic rung with instructions
- **Instruction** — XIC, XIO, OTE, OTL, OTU, TON, CTU, MOV, ADD, etc.
- **L5XDataType** — UDT definitions for the PLC
- **L5XTag** — Controller and program-scoped tags
- **L5XTask** — Continuous, periodic, or event tasks

## Core Concepts

- **From KONOMI to PLC**: Define your factory in KONOMI → compile to .L5X → import into Studio 5000
- **UDT Generation**: KONOMI UDTs become Rockwell UDTs automatically
- **Tag Mapping**: KONOMI tags become PLC tags with correct data types and scoping
- **Ladder Logic**: Generate rungs from state machines and procedures
