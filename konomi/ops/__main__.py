"""python -m konomi.ops — run the ops directory."""
import sys
from konomi.serve import run_directory
from konomi.ops.tags import create_provider

sys.exit(run_directory(
    name="ops",
    desc="CLI / REST API / MCP wrappers for directory operations",
    provides=["DirectoryOps", "CLI", "APIServer", "MCPProvider"],
    tag_provider=create_provider(),
) or 0)
