"""python -m konomi.kpi — run the KPI directory."""
import sys
from konomi.serve import run_directory
from konomi.kpi.tags import create_provider

sys.exit(run_directory(
    name="kpi",
    desc="KPI metrics: OEE, energy, production, reliability",
    provides=["OEE", "MTBF", "MTTR", "CycleTime",
              "Throughput", "FirstPassYield", "EnergyKPI"],
    tag_provider=create_provider(),
) or 0)
