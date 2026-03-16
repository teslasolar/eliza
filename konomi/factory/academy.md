# Factory Hierarchy

Site → Area → Line → Unit — the ISA-95 compliant physical model of a manufacturing facility.

## Key Classes

- **Site** — Top-level facility with areas, tag database, simulation engine
- **Area** — Functional zone within a site (e.g., brewing, packaging)
- **Line** — Production line within an area
- **Unit** — Equipment unit within a line (reactor, mixer, filler)
- **SimEngine** — Simulation engine for running factory models

## Presets

Factory comes with pre-built configurations: `create_brewery()`, `create_pharma()`, `create_food()` — complete with tags, equipment, and simulation parameters.
