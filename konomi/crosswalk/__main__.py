"""python -m konomi.crosswalk — run the crosswalk directory."""
import sys
from konomi.serve import run_directory
from konomi.crosswalk.tags import create_provider

sys.exit(run_directory(
    name="crosswalk",
    desc="Cross-standard mappings between ISA-88/95/18/101",
    provides=["Crosswalk", "CrosswalkEntry", "MappingType"],
    tag_provider=create_provider(),
) or 0)
