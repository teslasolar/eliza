"""python -m konomi.meta — run the meta-standard directory."""
import sys
from konomi.serve import run_directory
from konomi.meta.tags import create_provider

sys.exit(run_directory(
    name="meta",
    desc="Layer 0: Meta-Standard — how standards define themselves",
    provides=["Standard", "UDT", "Field", "StateMachine", "Transition",
              "Entity", "Relation", "Rule", "RuleEngine"],
    tag_provider=create_provider(),
) or 0)
