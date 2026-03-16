"""
Site — the top-level factory entity.
Contains areas, lines, units. Hosts the tag database and sim engine.
ISA-95 Site level.

Usage:
    site = Site.create_brewery("AcmeBrew")
    site.sim.run_sync(ticks=100)
    print(site.tag_db.read_all())
"""

from dataclasses import dataclass, field
from konomi.factory.area import Area
from konomi.factory.sim import SimEngine, SimMode
from konomi.tags.factory_tags import FactoryTagDatabase
from konomi.kpi.oee import OEE


@dataclass
class Site:
    """A factory site (ISA-95 Site). Top of the hierarchy."""
    name: str
    desc: str = ""
    areas: list = field(default_factory=list)
    tag_db: FactoryTagDatabase = field(default_factory=FactoryTagDatabase)
    sim: SimEngine = field(default_factory=SimEngine)
    oee: OEE = field(default_factory=OEE)

    def __post_init__(self):
        self.sim.attach(self)

    def add_area(self, name: str, desc: str = "") -> Area:
        """Add a production area."""
        area = Area(name=name, site=self.name, desc=desc)
        self.areas.append(area)
        self.tag_db.add_child(area.tag_db)
        return area

    def get_area(self, name: str) -> Area:
        for area in self.areas:
            if area.name == name:
                return area
        return None

    def status(self) -> dict:
        """Full site status."""
        return {
            "site": self.name,
            "mode": self.sim.mode.value,
            "areas": len(self.areas),
            "total_tags": self.tag_db.tag_count,
            "sim_ticks": self.sim.total_ticks,
            "oee": self.oee.report() if self.oee.total_units > 0 else None,
        }

    @classmethod
    def create_brewery(cls, name: str = "AcmeBrew") -> "Site":
        """Create a simulated brewery site."""
        site = cls(name=name, desc="Simulated brewery")

        brew = site.add_area("Brewing", "Brewhouse area")
        line1 = brew.add_line("Line1", "Primary brew line")
        line1.setup_batch_line()

        pkg = site.add_area("Packaging", "Filling and packaging")
        fill_line = pkg.add_line("Fill1", "Bottle filling line")
        fill_line.setup_continuous_line()

        site.oee = OEE(run_time=20, downtime=2, actual_rate=900,
                       ideal_rate=1000, good_units=880, total_units=900)
        return site

    @classmethod
    def create_pharma(cls, name: str = "PharmaCo") -> "Site":
        """Create a simulated pharmaceutical site."""
        site = cls(name=name, desc="Simulated pharma plant")

        api = site.add_area("API", "Active ingredient production")
        reactor_line = api.add_line("Reactor", "API synthesis")
        reactor_line.setup_batch_line()

        formulation = site.add_area("Formulation", "Drug formulation")
        form_line = formulation.add_line("FormLine1", "Tablet formulation")
        form_line.setup_batch_line()

        packaging = site.add_area("Packaging", "Final packaging")
        pack_line = packaging.add_line("Pack1", "Blister packaging")
        pack_line.setup_continuous_line()

        return site

    @classmethod
    def create_food(cls, name: str = "FoodWorks") -> "Site":
        """Create a simulated food processing site."""
        site = cls(name=name, desc="Simulated food plant")

        prep = site.add_area("Prep", "Raw material preparation")
        prep_line = prep.add_line("PrepLine", "Wash and prep")
        prep_line.setup_continuous_line()

        cook = site.add_area("Cooking", "Cooking and processing")
        cook_line = cook.add_line("CookLine", "Main cooking line")
        cook_line.setup_batch_line()

        pack = site.add_area("Pack", "Packaging")
        pack_line = pack.add_line("PackLine", "Fill and seal")
        pack_line.setup_continuous_line()

        return site

    def __repr__(self):
        return (f"Site({self.name}, areas={len(self.areas)}, "
                f"tags={self.tag_db.tag_count}, "
                f"mode={self.sim.mode.value})")
