# ISA-88 Batch Control

## What Is ISA-88?

ISA-88 is the standard for batch manufacturing control. It defines how recipes, procedures, and equipment work together to make things — from beer to pharmaceuticals.

## The Hierarchy

```javascript
const hierarchy = {
  "Process Cell":   "Top level — the batch process area",
  "Unit":           "Major piece of equipment (reactor, mixer)",
  "Equipment Module": "Functional group within a unit (agitator, valve cluster)",
  "Control Module":   "Single device (valve, motor, sensor)",
};

Object.entries(hierarchy).forEach(([k,v]) =>
  console.log(`  ${k}: ${v}`)
);
```

## Recipes vs Procedures

- **Recipe**: What to make (ingredients, parameters, steps)
- **Procedure**: How to make it (equipment actions, state transitions)

A recipe says "mix 100L water at 60C for 10 minutes." A procedure says "open valve V-101, start agitator M-201 at 60 RPM, monitor TT-301."

## PackML State Machine

ISA-88 uses PackML states for equipment control:

```javascript
const states = {
  IDLE:       "Waiting for command",
  STARTING:   "Transitioning to execute",
  EXECUTE:    "Running the procedure",
  COMPLETING: "Finishing up",
  COMPLETE:   "Done — ready for reset",
  STOPPING:   "Controlled stop",
  STOPPED:    "Stopped — needs restart",
  ABORTING:   "Emergency stop in progress",
  ABORTED:    "Emergency stopped",
  HOLDING:    "Paused — held condition",
  HELD:       "Waiting to resume",
  RESETTING:  "Returning to idle",
};

console.log("PackML states:", Object.keys(states).length);
```

## In KONOMI

```python
# Python usage (view only — run with: python -m konomi)
from konomi.isa88 import BatchControl, Procedure, Recipe, BatchStates
```

The ISA-88 package connects to the tag system (every valve is a tag), the factory hierarchy (units belong to areas), and the crosswalk (mapping to ISA-95 production segments).
