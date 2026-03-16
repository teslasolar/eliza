"""
ACG-KCC: Guild Chain
Konomi Cube Coin Private Fork for AI Craftspeople Guild Operations

"The protected register is on-chain. Good luck retaliating against a blockchain."

Network: Permissioned Multi-Layer PoA/PoS
Total Supply: 510,510 GLD (Guild Tokens)
Parent Architecture: Konomi Cube Coin v3.0

Run: python -m guild-chain          # info
     python -m guild-chain --serve   # HTTP API
     python -m guild-chain --mcp     # MCP stdio
"""

from guild_chain.tokens import GLD, GLD_SUPPLY
from guild_chain.layers import Layer1, Layer2, CrossLayerBridge
from guild_chain.agents import GuildAgent, GUILD_AGENTS
from guild_chain.contracts import EthicalRefusal, VettingSession, Certification
from guild_chain.refusal import RefusalRegister, RetaliationDetector
from guild_chain.tags import create_provider
from guild_chain.vectors import (
    VectorChain, VectorBlock, Vector3D,
    DomainAxis, AbstractionAxis, LifecycleAxis,
    KONOMI_VECTORS, ACG_VECTORS, build_standard_chain,
)
