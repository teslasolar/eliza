# ISA-88 Batch Control

Procedures, recipes, and state machines for batch manufacturing — from beer to pharmaceuticals.

## Key Classes

- **BatchControl** — Top-level batch control coordinator
- **Procedure** — Equipment procedure with unit procedures and operations
- **Recipe** — What to make: ingredients, parameters, steps
- **BatchStates** — PackML state machine (IDLE → RUNNING → COMPLETE)

## Core Concepts

- **Recipe vs Procedure**: Recipe says what, procedure says how
- **Equipment Hierarchy**: Process Cell → Unit → Equipment Module → Control Module
- **PackML States**: 12 states (IDLE, STARTING, EXECUTE, COMPLETING, COMPLETE, STOPPING, STOPPED, ABORTING, ABORTED, HOLDING, HELD, RESETTING)
- **S88 Model**: Separates recipe from equipment so recipes are portable across units
