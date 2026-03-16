"""python -m konomi.femto — run the FemtoLLM directory."""
import sys
from konomi.serve import run_directory
from konomi.femto.tags import create_provider

sys.exit(run_directory(
    name="femto",
    desc="FemtoLLM — tiny ML model for industrial classification",
    provides=["FemtoLLM"],
    tag_provider=create_provider(),
) or 0)
