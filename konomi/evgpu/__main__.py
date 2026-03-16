"""python -m konomi.evgpu — run the eVGPU directory."""
import sys
from konomi.serve import run_directory
from konomi.evgpu.tags import create_provider

sys.exit(run_directory(
    name="evgpu",
    desc="eVGPU — CPU-based compute for edge inference",
    provides=["eVGPU", "Tensor"],
    tag_provider=create_provider(),
) or 0)
