# Guild Chain Tags — Ignition-Style Tag Provider

Exposes chain health, refusal register state, SLA timers,
agent status, and token metrics as real-time tags.

```python
from konomi.tags.provider import TagProvider, Tag, TagType


class GuildChainTagProvider(TagProvider):
    """Tag provider for the guild chain."""

    def __init__(self):
        super().__init__(prefix="GCHAIN")
        # Chain health
        self.register(Tag(path="L1_Height", type=TagType.INTEGER,
                          desc="Layer 1 block height"))
        self.register(Tag(path="L2_Height", type=TagType.INTEGER,
                          desc="Layer 2 block height"))
        self.register(Tag(path="L1_Authorities", type=TagType.INTEGER,
                          desc="Active L1 authority nodes"))
        self.register(Tag(path="L2_Validators", type=TagType.INTEGER,
                          desc="Active L2 validator nodes"))
        # Refusal register
        self.register(Tag(path="Refusals_Total", type=TagType.INTEGER,
                          desc="Total ethical refusals filed"))
        self.register(Tag(path="Refusals_Pending", type=TagType.INTEGER,
                          desc="Refusals pending review"))
        self.register(Tag(path="Refusals_Upheld", type=TagType.INTEGER,
                          desc="Refusals upheld"))
        self.register(Tag(path="SLA_Breaches", type=TagType.INTEGER,
                          desc="Active SLA breaches"))
        self.register(Tag(path="Retaliation_Flags", type=TagType.INTEGER,
                          desc="Retaliation patterns detected"))
        # Vetting
        self.register(Tag(path="Active_Vettings", type=TagType.INTEGER,
                          desc="ELIZA vettings in progress"))
        self.register(Tag(path="Seals_Issued", type=TagType.INTEGER,
                          desc="Total ACG Vetted seals issued"))
        # Tokens
        self.register(Tag(path="GLD_Circulating", type=TagType.INTEGER,
                          desc="GLD tokens in circulation"))
        self.register(Tag(path="GLD_Staked", type=TagType.INTEGER,
                          desc="GLD tokens staked"))
        # Agents
        self.register(Tag(path="Agents_Active", type=TagType.INTEGER,
                          desc="Active guild agents"))
        self.register(Tag(path="Slots_In_Use", type=TagType.INTEGER,
                          desc="Operation slots currently active"))
        # Defaults
        self.get("GCHAIN_L1_Height").write(0)
        self.get("GCHAIN_L2_Height").write(0)
        self.get("GCHAIN_Refusals_Total").write(0)
        self.get("GCHAIN_SLA_Breaches").write(0)
        self.get("GCHAIN_Agents_Active").write(8)


def create_provider() -> GuildChainTagProvider:
    return GuildChainTagProvider()
```
