"""python -m konomi.factory — run the factory directory."""
import sys
from konomi.serve import run_directory
from konomi.factory.tags import create_provider

sys.exit(run_directory(
    name="factory",
    desc="Factory hierarchy: Site → Area → Line → Unit + simulation",
    provides=["Site", "Area", "Line", "Unit", "SimEngine", "SimMode"],
    tag_provider=create_provider(),
) or 0)
