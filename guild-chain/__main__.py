"""python -m guild-chain — run the guild chain directory."""
import sys

# guild-chain has a hyphen so we use konomi's serve framework
sys.path.insert(0, ".")
from konomi.serve import run_directory
from guild_chain.tags import create_provider

sys.exit(run_directory(
    name="guild-chain",
    desc="ACG-KCC: Guild Chain — immutable vetting, refusal register, blockchain",
    provides=["GLD", "Layer1", "Layer2", "EthicalRefusal",
              "VettingSession", "Certification", "RefusalRegister",
              "RetaliationDetector", "GuildAgent"],
    tag_provider=create_provider(),
    extras={
        "supply": "510,510 GLD",
        "consensus": "L1: PoA (5-11 elders), L2: DPoS (100+ GLD stake)",
        "agents": 8,
        "slots": 512,
        "total_agents": 6152,
    },
) or 0)
