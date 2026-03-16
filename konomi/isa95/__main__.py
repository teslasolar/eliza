"""python -m konomi.isa95 — run the ISA-95 enterprise/control directory."""
import sys
from konomi.serve import run_directory
from konomi.isa95.tags import create_provider

sys.exit(run_directory(
    name="isa95",
    desc="ISA-95 Enterprise/Control Integration",
    provides=["Level", "Equipment", "Material", "Personnel",
              "ProcessSegment", "ProductionSchedule", "DataFlow"],
    tag_provider=create_provider(),
) or 0)
