# Scanner Engine

The compliance scanning engine and rule sets — validates code against industrial standards and ACG Manifesto.

## Key Classes

- **Scanner** — Main scanning coordinator
- **ScanResult** — Result with findings, severity, line numbers
- **ScanEngine** — Rule evaluation engine

## Rule Sets

- **ISA-88**: State machine completeness, recipe structure, naming
- **ISA-95**: Level assignments, equipment model, production scheduling
- **ISA-18**: Alarm priority distribution, shelving policies, flood detection
- **ISA-101**: Color usage, navigation depth, element consistency
- **OPC-UA**: Node class usage, namespace conventions, security
- **Sparkplug**: Topic structure, birth/death certificates, metric types
- **Modbus**: Register alignment, function code safety
- **ACG**: Transparency disclosure, AI labeling, refusal documentation
