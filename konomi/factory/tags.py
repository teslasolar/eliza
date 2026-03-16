"""
Factory Tag Provider — Ignition-style tags for factory simulation.

Exposes site/area/line/unit counts, sim engine state,
tick counters, and running mode.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class FactoryTagProvider(TagProvider):
    """Tag provider for factory hierarchy + simulation."""

    def __init__(self):
        super().__init__(prefix="FAC")
        self.register(Tag(path="Site_Name", type=TagType.STRING,
                          desc="Active site name"))
        self.register(Tag(path="Area_Count", type=TagType.INTEGER,
                          desc="Number of areas in site"))
        self.register(Tag(path="Line_Count", type=TagType.INTEGER,
                          desc="Number of production lines"))
        self.register(Tag(path="Unit_Count", type=TagType.INTEGER,
                          desc="Number of process units"))
        self.register(Tag(path="Sim_Mode", type=TagType.STRING,
                          desc="Simulation mode (SIM/LIVE/REPLAY)"))
        self.register(Tag(path="Sim_Running", type=TagType.DISCRETE,
                          desc="Simulation engine running"))
        self.register(Tag(path="Sim_Tick", type=TagType.INTEGER,
                          desc="Current simulation tick count"))
        self.register(Tag(path="Total_Tags", type=TagType.INTEGER,
                          desc="Total tags across all units"))
        # Defaults
        self.get("FAC_Sim_Mode").write("SIM")
        self.get("FAC_Sim_Running").write(False)
        self.get("FAC_Sim_Tick").write(0)


def create_provider() -> FactoryTagProvider:
    return FactoryTagProvider()
