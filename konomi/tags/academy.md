# Tag System

The nervous system of the factory — every value is a tag with a path, type, quality, and timestamp.

## Key Classes

- **TagProvider** — Central registry for all tags
- **Tag** — A named data point with type, value, quality, timestamp
- **TagType** — Enumeration of tag types (analog, digital, string, etc.)
- **ProcessTags** — Temperature, pressure, flow, level
- **EquipmentTags** — Motor speed, valve position, equipment status
- **BatchTags** — Recipe parameters, phase status, batch ID
- **AlarmTags** — Alarm state, priority, shelving status
- **FactoryTagDatabase** — Full tag database for a factory site

## Why It Matters

Tags are the universal interface. OPC-UA exposes them, Sparkplug publishes them, Modbus maps to them, L5X generates them, the scanner checks their naming. Everything speaks tags.
