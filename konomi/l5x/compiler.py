"""
L5X Compiler — assembles programs, tasks, tags, and UDTs into a
complete .L5X XML file that Rockwell Studio 5000 can import.

Also provides helpers to compile konomi Tag/UDT definitions directly
into PLC-ready structures.
"""

from dataclasses import dataclass, field
from typing import Optional
from konomi.l5x.program import L5XProgram, L5XTask, TaskType
from konomi.l5x.datatypes import (L5XDataType, L5XTag, L5XMember,
                                   CIPType, konomi_to_cip)
from konomi.l5x.rungs import LadderRoutine, Rung
from konomi.l5x.instructions import InstructionSet


@dataclass
class L5XProject:
    """A complete L5X project ready for export."""
    name: str
    processor: str = "1769-L33ER"       # CompactLogix default
    revision: str = "33.01"
    datatypes: list[L5XDataType] = field(default_factory=list)
    controller_tags: list[L5XTag] = field(default_factory=list)
    programs: list[L5XProgram] = field(default_factory=list)
    tasks: list[L5XTask] = field(default_factory=list)


class L5XCompiler:
    """Compiles konomi definitions into L5X XML."""

    def __init__(self, project_name: str = "KONOMI",
                 processor: str = "1769-L33ER"):
        self._project = L5XProject(name=project_name, processor=processor)

    # ── Building blocks ──────────────────────────────────────────────

    def add_datatype(self, dt: L5XDataType):
        """Add a UDT to the project."""
        self._project.datatypes.append(dt)

    def add_controller_tag(self, tag: L5XTag):
        """Add a controller-scoped tag."""
        self._project.controller_tags.append(tag)

    def add_program(self, program: L5XProgram):
        """Add a program to the project."""
        self._project.programs.append(program)

    def add_task(self, task: L5XTask):
        """Add a task to the project."""
        self._project.tasks.append(task)

    # ── Konomi → L5X converters ──────────────────────────────────────

    def compile_udt(self, udt) -> L5XDataType:
        """Convert a konomi UDT into an L5X DataType."""
        dt = L5XDataType(name=udt.name, desc=udt.desc)
        for f in udt.fields:
            cip = konomi_to_cip(f.type)
            dt.add_member(f.name, cip, desc=f.desc)
        self._project.datatypes.append(dt)
        return dt

    def compile_tags(self, provider) -> list[L5XTag]:
        """Convert a konomi TagProvider into L5X controller tags."""
        tags = []
        for tag in provider:
            cip = konomi_to_cip(tag.type.value)
            l5x_tag = L5XTag(
                name=tag.path.replace(".", "_"),
                data_type=cip.value,
                desc=tag.desc,
            )
            self._project.controller_tags.append(l5x_tag)
            tags.append(l5x_tag)
        return tags

    def compile_alarm_rung(self, tag_path: str, setpoint: str,
                           alarm_tag: str, compare: str = "GRT") -> Rung:
        """Generate a compare → alarm output rung."""
        instr = InstructionSet.get(compare) or InstructionSet.GRT
        rung = Rung(number=0, comment=f"Alarm: {tag_path} {compare} {setpoint}")
        rung.add(instr, [tag_path, setpoint])
        rung.ote(alarm_tag)
        return rung

    def compile_interlock(self, conditions: list[str],
                          output: str, latch: bool = False) -> Rung:
        """Generate a multi-condition interlock rung."""
        rung = Rung(number=0, comment=f"Interlock → {output}")
        for cond in conditions:
            rung.xic(cond)
        if latch:
            rung.otl(output)
        else:
            rung.ote(output)
        return rung

    # ── Validation ───────────────────────────────────────────────────

    def validate(self) -> list[str]:
        """Validate the entire project."""
        errors = []
        names = set()
        for dt in self._project.datatypes:
            if dt.name in names:
                errors.append(f"Duplicate DataType: {dt.name}")
            names.add(dt.name)
        for prog in self._project.programs:
            errors.extend(prog.validate())
        return errors

    # ── XML Export ────────────────────────────────────────────────────

    def to_xml(self) -> str:
        """Generate the complete .L5X XML document."""
        p = self._project
        sections = [self._xml_header(p)]
        if p.datatypes:
            sections.append(self._xml_datatypes(p.datatypes))
        if p.controller_tags:
            sections.append(self._xml_tags(p.controller_tags))
        if p.programs:
            sections.append(self._xml_programs(p.programs))
        if p.tasks:
            sections.append(self._xml_tasks(p.tasks))
        sections.append(self._xml_footer())
        return "\n".join(sections)

    def export(self, path: str):
        """Write the L5X file to disk."""
        xml = self.to_xml()
        with open(path, "w") as f:
            f.write(xml)

    # ── XML helpers ──────────────────────────────────────────────────

    @staticmethod
    def _xml_header(p: L5XProject) -> str:
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            f'<RSLogix5000Content SchemaRevision="1.0" '
            f'SoftwareRevision="{p.revision}" '
            f'TargetName="{p.name}" '
            f'TargetType="Controller" '
            f'ContainsContext="true">\n'
            f'<Controller Name="{p.name}" '
            f'ProcessorType="{p.processor}">'
        )

    @staticmethod
    def _xml_datatypes(dts: list[L5XDataType]) -> str:
        inner = "\n".join(dt.to_xml() for dt in dts)
        return f"<DataTypes>\n{inner}\n</DataTypes>"

    @staticmethod
    def _xml_tags(tags: list[L5XTag]) -> str:
        inner = "\n".join(t.to_xml() for t in tags)
        return f"<Tags>\n{inner}\n</Tags>"

    @staticmethod
    def _xml_programs(progs: list[L5XProgram]) -> str:
        inner = "\n".join(p.to_xml() for p in progs)
        return f"<Programs>\n{inner}\n</Programs>"

    @staticmethod
    def _xml_tasks(tasks: list[L5XTask]) -> str:
        inner = "\n".join(t.to_xml() for t in tasks)
        return f"<Tasks>\n{inner}\n</Tasks>"

    @staticmethod
    def _xml_footer() -> str:
        return "</Controller>\n</RSLogix5000Content>"

    def __repr__(self):
        p = self._project
        return (f"L5XCompiler({p.name}, datatypes={len(p.datatypes)}, "
                f"tags={len(p.controller_tags)}, "
                f"programs={len(p.programs)})")
