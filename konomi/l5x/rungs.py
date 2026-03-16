"""
Rungs and Routines — the structural elements of ladder logic.

A Rung is a single line of logic (inputs → outputs).
A LadderRoutine is a named sequence of rungs within a program.
"""

from dataclasses import dataclass, field
from typing import Optional
from konomi.l5x.instructions import Instruction, InstructionSet, RungPosition


@dataclass
class RungElement:
    """One instruction placed on a rung with its operands."""
    instruction: Instruction
    operands: list[str] = field(default_factory=list)
    comment: str = ""

    def validate(self) -> Optional[str]:
        return self.instruction.validate_operands(self.operands)

    def to_text(self) -> str:
        return self.instruction.format_operands(self.operands)

    def to_xml(self) -> str:
        ops = "".join(f" Operand{i+1}=\"{o}\""
                      for i, o in enumerate(self.operands))
        return f"<{self.instruction.mnemonic}{ops}/>"


@dataclass
class Rung:
    """A single rung of ladder logic."""
    number: int
    elements: list[RungElement] = field(default_factory=list)
    comment: str = ""

    def add(self, instruction: Instruction, operands: list[str],
            comment: str = "") -> "Rung":
        """Add an element to this rung. Returns self for chaining."""
        self.elements.append(RungElement(instruction, operands, comment))
        return self

    def xic(self, tag: str) -> "Rung":
        """Examine If Closed shorthand."""
        return self.add(InstructionSet.XIC, [tag])

    def xio(self, tag: str) -> "Rung":
        """Examine If Open shorthand."""
        return self.add(InstructionSet.XIO, [tag])

    def ote(self, tag: str) -> "Rung":
        """Output Energize shorthand."""
        return self.add(InstructionSet.OTE, [tag])

    def otl(self, tag: str) -> "Rung":
        """Output Latch shorthand."""
        return self.add(InstructionSet.OTL, [tag])

    def otu(self, tag: str) -> "Rung":
        """Output Unlatch shorthand."""
        return self.add(InstructionSet.OTU, [tag])

    def ton(self, tag: str, preset: str, accum: str = "0") -> "Rung":
        """Timer On Delay shorthand."""
        return self.add(InstructionSet.TON, [tag, preset, accum])

    def ctu(self, tag: str, preset: str, accum: str = "0") -> "Rung":
        """Count Up shorthand."""
        return self.add(InstructionSet.CTU, [tag, preset, accum])

    def mov(self, src: str, dest: str) -> "Rung":
        """Move shorthand."""
        return self.add(InstructionSet.MOV, [src, dest])

    def grt(self, a: str, b: str) -> "Rung":
        """Greater Than shorthand."""
        return self.add(InstructionSet.GRT, [a, b])

    def les(self, a: str, b: str) -> "Rung":
        """Less Than shorthand."""
        return self.add(InstructionSet.LES, [a, b])

    @property
    def inputs(self) -> list[RungElement]:
        return [e for e in self.elements
                if e.instruction.position == RungPosition.INPUT]

    @property
    def outputs(self) -> list[RungElement]:
        return [e for e in self.elements
                if e.instruction.position == RungPosition.OUTPUT]

    def validate(self) -> list[str]:
        errors = []
        for e in self.elements:
            err = e.validate()
            if err:
                errors.append(f"Rung {self.number}: {err}")
        if not self.outputs:
            errors.append(f"Rung {self.number}: no output instruction")
        return errors

    def to_text(self) -> str:
        parts = [e.to_text() for e in self.elements]
        line = " ".join(parts)
        if self.comment:
            return f"// {self.comment}\n{line} ;"
        return f"{line} ;"

    def to_xml(self) -> str:
        comment = ""
        if self.comment:
            comment = f"\n      <Comment>{self.comment}</Comment>"
        inner = "".join(e.to_xml() for e in self.elements)
        text = " ".join(e.to_text() for e in self.elements) + " ;"
        return (f"    <Rung Number=\"{self.number}\" Type=\"N\">"
                f"{comment}\n"
                f"      <Text>{text}</Text>\n"
                f"    </Rung>")


@dataclass
class LadderRoutine:
    """A named routine containing an ordered sequence of rungs."""
    name: str
    desc: str = ""
    _rungs: list[Rung] = field(default_factory=list)

    def rung(self, comment: str = "") -> Rung:
        """Create and append a new rung."""
        r = Rung(number=len(self._rungs), comment=comment)
        self._rungs.append(r)
        return r

    @property
    def rungs(self) -> list[Rung]:
        return list(self._rungs)

    @property
    def rung_count(self) -> int:
        return len(self._rungs)

    def validate(self) -> list[str]:
        errors = []
        for r in self._rungs:
            errors.extend(r.validate())
        return errors

    def to_xml(self) -> str:
        rungs_xml = "\n".join(r.to_xml() for r in self._rungs)
        return (f"  <Routine Name=\"{self.name}\" Type=\"RLL\">\n"
                f"    <Description>{self.desc}</Description>\n"
                f"    <RLLContent>\n{rungs_xml}\n"
                f"    </RLLContent>\n"
                f"  </Routine>")

    def __repr__(self):
        return f"LadderRoutine({self.name}, rungs={self.rung_count})"
