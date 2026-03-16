"""python -m konomi.isa88 — run the ISA-88 batch control directory."""
import sys
from konomi.serve import run_directory
from konomi.isa88.tags import create_provider

sys.exit(run_directory(
    name="isa88",
    desc="ISA-88 Batch Control: equipment, recipes, procedures, states",
    provides=["Equipment", "Recipe", "Procedure", "UnitProcedure",
              "Operation", "Phase", "Batch", "BatchState"],
    tag_provider=create_provider(),
) or 0)
