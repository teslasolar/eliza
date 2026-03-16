"""python -m konomi.base — run the base primitives directory."""
import sys
from konomi.serve import run_directory
from konomi.base.tags import create_provider

sys.exit(run_directory(
    name="base",
    desc="Primitive types: identifiers, timestamps, quality, values",
    provides=["Identifier", "TagPath", "Timestamp", "Quality",
              "QualityFlags", "Value", "Range", "Quantity", "Status"],
    tag_provider=create_provider(),
) or 0)
