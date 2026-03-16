# Meta-Standard

Layer 0 — how standards define themselves. The meta layer provides primitives that all other KONOMI packages use.

## Key Classes

- **Standard** — A standard definition with UDTs, state machines, entities, relations, rules
- **UDT** — User Defined Type with typed fields, validation, inheritance
- **Field** — Named field with type, unit, range, constraints
- **StateMachine** — Named states and transitions with guards and actions
- **Entity** — A named thing with properties, relations, and hierarchy
- **Relation** — Typed link between entities (contains, references, triggers)
- **Rule** — Compliance rule with pattern, check, severity
- **RuleEngine** — Evaluates rules against targets

## Why It Matters

Without meta, every standard would define its own structure differently. Meta gives them a shared vocabulary: UDTs, state machines, entities, rules. This is what makes crosswalking, validation, and code generation possible.
