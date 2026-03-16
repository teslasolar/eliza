# L5X Instructions — Rockwell PLC Instruction Set

This module defines the full set of Rockwell ladder-logic instruction primitives used in L5X compilation. It covers relay logic, timers, counters, compare, math, move, and program flow instructions. Each instruction knows its mnemonic, operand count, and where it can appear on a rung (input side, output side, or either).

The `InstructionSet` class serves as a registry: you can look up instructions by mnemonic, filter by category, or iterate all available instructions.

## Enums and Instruction Dataclass

```python
"""
L5X Instruction Set — Rockwell ladder-logic instruction primitives.

Covers relay logic, timers, counters, compare, math, move, and program flow.
Each instruction knows its mnemonic, operand count, and rung position rules.
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class InstructionCategory(Enum):
    """Instruction categories matching Studio 5000."""
    BIT = "bit"             # XIC, XIO, OTE, OTL, OTU, ONS
    TIMER = "timer"         # TON, TOF, RTO
    COUNTER = "counter"     # CTU, CTD, RES
    COMPARE = "compare"     # EQU, NEQ, GRT, GEQ, LES, LEQ, LIM
    MATH = "math"           # ADD, SUB, MUL, DIV, MOD, NEG, ABS, SQR
    MOVE = "move"           # MOV, MVM, SWPB, BTDT
    LOGICAL = "logical"     # AND, OR, XOR, NOT
    PROGRAM = "program"     # JSR, RET, SBR, JMP, LBL, MCR, AFI, NOP, TND
    IO = "io"               # MSG, GSV, SSV


class RungPosition(Enum):
    """Where the instruction can appear in a rung."""
    INPUT = "input"         # on the condition side
    OUTPUT = "output"       # on the output side
    EITHER = "either"


@dataclass(frozen=True)
class Instruction:
    """A single PLC instruction."""
    mnemonic: str
    category: InstructionCategory
    position: RungPosition
    operand_count: int
    desc: str = ""

    def format_operands(self, operands: list[str]) -> str:
        """Format instruction with operands as L5X text."""
        if not operands:
            return f"{self.mnemonic}()"
        return f"{self.mnemonic}({','.join(operands)})"

    def validate_operands(self, operands: list[str]) -> Optional[str]:
        """Return error message if operand count is wrong."""
        if len(operands) != self.operand_count:
            return (f"{self.mnemonic} expects {self.operand_count} "
                    f"operands, got {len(operands)}")
        return None
```

## InstructionSet — The Full Registry

```python
class InstructionSet:
    """The full Rockwell instruction set relevant to L5X compilation."""

    # ── Bit Instructions ─────────────────────────────────────────────
    XIC = Instruction("XIC", InstructionCategory.BIT, RungPosition.INPUT, 1,
                      "Examine If Closed")
    XIO = Instruction("XIO", InstructionCategory.BIT, RungPosition.INPUT, 1,
                      "Examine If Open")
    OTE = Instruction("OTE", InstructionCategory.BIT, RungPosition.OUTPUT, 1,
                      "Output Energize")
    OTL = Instruction("OTL", InstructionCategory.BIT, RungPosition.OUTPUT, 1,
                      "Output Latch")
    OTU = Instruction("OTU", InstructionCategory.BIT, RungPosition.OUTPUT, 1,
                      "Output Unlatch")
    ONS = Instruction("ONS", InstructionCategory.BIT, RungPosition.INPUT, 1,
                      "One-Shot")

    # ── Timer Instructions ───────────────────────────────────────────
    TON = Instruction("TON", InstructionCategory.TIMER, RungPosition.OUTPUT, 3,
                      "Timer On Delay — tag, preset, accum")
    TOF = Instruction("TOF", InstructionCategory.TIMER, RungPosition.OUTPUT, 3,
                      "Timer Off Delay — tag, preset, accum")
    RTO = Instruction("RTO", InstructionCategory.TIMER, RungPosition.OUTPUT, 3,
                      "Retentive Timer On — tag, preset, accum")

    # ── Counter Instructions ─────────────────────────────────────────
    CTU = Instruction("CTU", InstructionCategory.COUNTER, RungPosition.OUTPUT, 3,
                      "Count Up — tag, preset, accum")
    CTD = Instruction("CTD", InstructionCategory.COUNTER, RungPosition.OUTPUT, 3,
                      "Count Down — tag, preset, accum")
    RES = Instruction("RES", InstructionCategory.COUNTER, RungPosition.OUTPUT, 1,
                      "Reset timer/counter")

    # ── Compare Instructions ─────────────────────────────────────────
    EQU = Instruction("EQU", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Equal")
    NEQ = Instruction("NEQ", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Not Equal")
    GRT = Instruction("GRT", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Greater Than")
    GEQ = Instruction("GEQ", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Greater Than or Equal")
    LES = Instruction("LES", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Less Than")
    LEQ = Instruction("LEQ", InstructionCategory.COMPARE, RungPosition.INPUT, 2,
                      "Less Than or Equal")

    # ── Math Instructions ────────────────────────────────────────────
    ADD = Instruction("ADD", InstructionCategory.MATH, RungPosition.OUTPUT, 3,
                      "Add — A + B → dest")
    SUB = Instruction("SUB", InstructionCategory.MATH, RungPosition.OUTPUT, 3,
                      "Subtract — A - B → dest")
    MUL = Instruction("MUL", InstructionCategory.MATH, RungPosition.OUTPUT, 3,
                      "Multiply — A * B → dest")
    DIV = Instruction("DIV", InstructionCategory.MATH, RungPosition.OUTPUT, 3,
                      "Divide — A / B → dest")
    MOV = Instruction("MOV", InstructionCategory.MOVE, RungPosition.OUTPUT, 2,
                      "Move — source → dest")
    NEG = Instruction("NEG", InstructionCategory.MATH, RungPosition.OUTPUT, 2,
                      "Negate — -source → dest")

    # ── Program Flow ─────────────────────────────────────────────────
    JSR = Instruction("JSR", InstructionCategory.PROGRAM, RungPosition.OUTPUT, 1,
                      "Jump to Subroutine")
    RET = Instruction("RET", InstructionCategory.PROGRAM, RungPosition.OUTPUT, 0,
                      "Return from Subroutine")
    NOP = Instruction("NOP", InstructionCategory.PROGRAM, RungPosition.EITHER, 0,
                      "No Operation")
    AFI = Instruction("AFI", InstructionCategory.PROGRAM, RungPosition.INPUT, 0,
                      "Always False Instruction")

    @classmethod
    def all(cls) -> list[Instruction]:
        """Return all defined instructions."""
        return [v for v in vars(cls).values() if isinstance(v, Instruction)]

    @classmethod
    def by_category(cls, cat: InstructionCategory) -> list[Instruction]:
        """Filter instructions by category."""
        return [i for i in cls.all() if i.category == cat]

    @classmethod
    def get(cls, mnemonic: str) -> Optional[Instruction]:
        """Look up instruction by mnemonic."""
        return getattr(cls, mnemonic, None)
```
