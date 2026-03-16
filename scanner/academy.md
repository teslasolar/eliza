# Scanner Academy

KONOMI Scanner — standards compliance linter for source code and configurations.

## What You'll Learn

- Writing compliance rules for ISA-88/95/18/101
- AI-powered deep scan using local models
- OPC-UA, Sparkplug, and Modbus protocol validation
- ACG Manifesto compliance checking
- Rule severity levels and reporting

## Prerequisites

- Source code or configuration files to scan
- Understanding of at least one industrial standard
- Python 3.10+ for CLI scanning

## Key Concepts

**Rule Sets**: Each standard has rules. Rules check naming conventions, required fields, state machine completeness, and protocol compliance. Rules have severity: error, warning, info.

**AI Deep Scan**: Beyond regex matching — the scanner can use local LLMs to understand intent and flag subtle non-compliance that pattern matching would miss.

**Compliance Report**: The scanner produces structured JSON reports with file, line, rule ID, severity, message, and suggested fix for each finding.
