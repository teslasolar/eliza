"""python -m konomi.scanner — run the scanner directory."""
import sys
from konomi.serve import run_directory
from konomi.scanner.tags import create_provider

sys.exit(run_directory(
    name="scanner",
    desc="Standards compliance scanning engine + rule sets",
    provides=["Scanner", "ScanResult"],
    tag_provider=create_provider(),
) or 0)
