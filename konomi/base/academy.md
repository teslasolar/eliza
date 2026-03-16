# Base Types

Primitive types shared across all KONOMI packages — identifiers, timestamps, quality, values.

## Key Classes

- **Identifier** — UUID, path, tag, or URN-based naming
- **TagPath** — Hierarchical dot/slash path for tag addressing
- **Timestamp** — Multi-format (ISO8601, epoch ms, OPC filetime)
- **Quality** — Good/bad/uncertain with granular flags
- **Value** — A value with quality and timestamp attached
- **Range** — Numeric bounds with inclusive/exclusive endpoints
- **Quantity** — Value + engineering unit + uncertainty
- **Status** — Operational status enumeration

## Why It Matters

Every tag reading, every alarm state, every batch parameter uses these primitives. They're the atoms of the industrial data model.
