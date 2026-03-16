# Self-Defining Standards

## The Meta Layer Problem

Industrial standards (ISA-88, ISA-95, etc.) are written in English PDFs. When you implement them in code, you're *interpreting* the standard. Two teams will implement the same standard differently.

## KONOMI's Solution

KONOMI's meta layer provides primitives that standards use to define themselves:

```javascript
// The meta primitives
const meta = {
  Standard:     "A standard definition — name, version, scope, UDTs",
  UDT:          "User Defined Type — named fields with types and validation",
  Field:        "A field within a UDT — name, type, unit, range",
  StateMachine: "Named states + transitions with guards",
  Transition:   "From state → to state with guard condition",
  Entity:       "A named thing with properties and relations",
  Relation:     "A typed link between entities",
  Rule:         "A compliance rule — pattern, check, severity",
  RuleEngine:   "Evaluates rules against a target",
};

console.log("Meta primitives:", Object.keys(meta).length);
Object.entries(meta).forEach(([k,v]) => console.log(`  ${k}: ${v}`));
```

## How ISA-88 Defines Itself

ISA-88 (Batch Control) uses the meta layer to declare its own structure:

- **UDTs**: Recipe, Procedure, Unit Procedure, Operation, Phase
- **StateMachine**: The PackML state model (Idle → Running → Complete etc.)
- **Entities**: Equipment Module, Control Module, Process Cell
- **Relations**: "Equipment Module contains Control Modules"
- **Rules**: "Every Procedure must have at least one Unit Procedure"

## Why This Matters

Once standards define themselves through the meta layer:
1. **Validation is automatic** — the scanner checks rules the standard declared
2. **Crosswalking works** — mapping ISA-88 → ISA-95 uses entity relations
3. **Code generation works** — L5X compiler reads UDTs to generate PLC types
4. **Everything stays in sync** — change the standard definition, everything updates
