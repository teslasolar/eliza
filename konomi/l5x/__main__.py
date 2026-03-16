"""python -m konomi.l5x — run the L5X compiler directory."""
import sys
from konomi.serve import run_directory
from konomi.l5x.tags import create_provider

sys.exit(run_directory(
    name="l5x",
    desc="L5X Compiler — Rockwell PLC program generation",
    provides=["L5XCompiler", "L5XProgram", "Rung", "Instruction",
              "L5XDataType", "L5XTag", "L5XTask"],
    tag_provider=create_provider(),
) or 0)
