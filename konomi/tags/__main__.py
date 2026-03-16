"""python -m konomi.tags — run the tags directory."""
import sys
from konomi.serve import run_directory
from konomi.tags.tags import create_provider

sys.exit(run_directory(
    name="tags",
    desc="Tag system — the nervous system of the factory",
    provides=["TagProvider", "Tag", "TagType", "ProcessTags",
              "EquipmentTags", "BatchTags", "AlarmTags",
              "FactoryTagDatabase", "DirectoryTagRegistry"],
    tag_provider=create_provider(),
) or 0)
