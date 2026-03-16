# KONOMI Academy

The Self-Defining Industrial Standards System — 18 packages covering ISA-88, ISA-95, ISA-18.2, ISA-101, OPC-UA, Sparkplug, Modbus, and more.

## What You'll Learn

- How industrial standards interconnect (crosswalking)
- ISA-88 batch control: procedures, recipes, state machines
- The tag system — the nervous system of the factory
- Self-defining meta-standards: standards that describe standards
- Factory hierarchy: Site → Area → Line → Unit
- PLC code generation with the L5X compiler
- Edge inference with eVGPU and FemtoLLM

## Prerequisites

- Basic understanding of manufacturing or process control
- Python 3.10+ for running the standard implementations
- Familiarity with any one ISA standard is helpful but not required

## Key Concepts

**Self-Defining**: KONOMI's meta layer lets standards define their own structure using UDTs (User Defined Types), state machines, entities, relations, and rules. The meta layer is itself a standard.

**Tag System**: Every value in a factory is a tag. Tags have paths (like `Site1/Area2/Line3/Motor/Speed`), types, quality flags, and timestamps. The tag provider is the nervous system connecting everything.

**Crosswalking**: Mapping concepts between standards. An ISA-88 equipment module maps to an ISA-95 equipment segment. KONOMI's crosswalk package tracks these relationships automatically.

**L5X Compiler**: Generate Rockwell Studio 5000 PLC programs from KONOMI definitions. Ladder logic rungs, instructions, UDTs, and tasks — all from Python.

## Package Map

| Package | Domain | Key Classes |
|---------|--------|-------------|
| meta | Self-description | Standard, UDT, Field, StateMachine |
| base | Primitives | Identifier, Timestamp, Quality, Value |
| tags | Tag system | TagProvider, Tag, TagType |
| factory | Hierarchy | Site, Area, Line, Unit, SimEngine |
| isa88 | Batch control | BatchControl, Procedure, Recipe |
| isa95 | Enterprise | Equipment, Production, Material |
| isa18 | Alarms | Alarm, AlarmPriority, AlarmState |
| isa101 | HMI | HMIScreen, HMIElement |
| opcua | Communication | OPCNode, AddressSpace, Subscription |
| sparkplug | MQTT | SparkplugTopic, SparkplugPayload |
| modbus | Field protocol | RegisterType, ModbusMap |
| kpi | Metrics | OEE, Energy, Production, Reliability |
| crosswalk | Mapping | Crosswalk, Mapping |
| scanner | Compliance | Scanner, ScanResult |
| evgpu | Edge compute | eVGPU, Tensor |
| femto | Tiny ML | FemtoLLM |
| l5x | PLC codegen | L5XCompiler, L5XProgram, Rung |
| ops | Operations | CLI, APIServer, MCPProvider |
