"""python -m konomi.modbus — run the Modbus directory."""
import sys
from konomi.serve import run_directory
from konomi.modbus.tags import create_provider

sys.exit(run_directory(
    name="modbus",
    desc="Modbus field protocol: registers, function codes, data types",
    provides=["RegisterType", "RegisterDef", "ModbusDataType",
              "ModbusMap", "FunctionCode", "ModbusException"],
    tag_provider=create_provider(),
) or 0)
