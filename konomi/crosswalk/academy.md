# Crosswalk Mapping

Cross-standard mappings between ISA-88, ISA-95, ISA-18.2, ISA-101, and communication protocols.

## Key Classes

- **Crosswalk** — A mapping between two standards
- **Mapping** — Individual concept mapping (source → target) with confidence
- **CrosswalkEngine** — Evaluates and applies crosswalk mappings

## Core Concepts

- **ISA-88 ↔ ISA-95**: Equipment Module → Equipment Segment, Recipe → Production Rule
- **ISA-18 ↔ ISA-101**: Alarm Priority → HMI Color, Alarm State → Display Element
- **Tags ↔ OPC-UA**: Tag path → OPC-UA node browse path
- **Tags ↔ Sparkplug**: Tag path → Sparkplug topic + metric name
- **Tags ↔ Modbus**: Tag path → Register address + data type

Crosswalking is what makes KONOMI a *system* instead of a collection of independent standards.
