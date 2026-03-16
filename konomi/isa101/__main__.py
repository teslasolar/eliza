"""python -m konomi.isa101 — run the ISA-101 HMI design directory."""
import sys
from konomi.serve import run_directory
from konomi.isa101.tags import create_provider

sys.exit(run_directory(
    name="isa101",
    desc="ISA-101 High Performance HMI Design",
    provides=["Principles", "HMILayer", "ColorMeaning",
              "GraphicElement", "Faceplate", "Trend"],
    tag_provider=create_provider(),
) or 0)
