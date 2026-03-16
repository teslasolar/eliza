"""python -m konomi.opcua — run the OPC-UA directory."""
import sys
from konomi.serve import run_directory
from konomi.opcua.tags import create_provider

sys.exit(run_directory(
    name="opcua",
    desc="OPC-UA Industrial Communication",
    provides=["NodeClass", "AccessLevel", "OPCNode", "OPCVariable",
              "OPCMethod", "AddressSpace", "Subscription", "COMPANIONS"],
    tag_provider=create_provider(),
) or 0)
