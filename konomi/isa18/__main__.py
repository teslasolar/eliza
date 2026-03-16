"""python -m konomi.isa18 — run the ISA-18.2 alarm management directory."""
import sys
from konomi.serve import run_directory
from konomi.isa18.tags import create_provider

sys.exit(run_directory(
    name="isa18",
    desc="ISA-18.2 Alarm Management: lifecycle, priorities, metrics",
    provides=["Alarm", "AlarmClass", "AlarmPriority", "AlarmState",
              "AlarmMetrics", "ISA18_RULES"],
    tag_provider=create_provider(),
) or 0)
