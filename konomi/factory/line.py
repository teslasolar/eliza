"""
Line — a production line within an area.
Contains multiple process units that work together.
ISA-95 WorkCenter level.
"""

from dataclasses import dataclass, field
from konomi.factory.unit import Unit
from konomi.tags.factory_tags import FactoryTagDatabase


@dataclass
class Line:
    """A production line (ISA-95 WorkCenter / ISA-88 ProcessCell)."""
    name: str
    area: str = ""
    desc: str = ""
    units: list = field(default_factory=list)
    tag_db: FactoryTagDatabase = field(default_factory=FactoryTagDatabase)

    def add_unit(self, name: str, desc: str = "") -> Unit:
        """Add a process unit to this line."""
        unit = Unit(name=name, area=f"{self.area}_{self.name}", desc=desc)
        self.units.append(unit)
        self.tag_db.add_child(unit.tag_db)
        return unit

    def setup_batch_line(self):
        """Configure as a typical batch production line."""
        reactor = self.add_unit("Reactor", "Main reactor vessel")
        reactor.setup_mixing_unit()

        blend = self.add_unit("BlendTank", "Post-reaction blending")
        blend.setup_mixing_unit()

        filler = self.add_unit("Filler", "Product filling station")
        filler.setup_filling_unit()

    def setup_continuous_line(self):
        """Configure as a continuous production line."""
        for i, (name, desc) in enumerate([
            ("Feed", "Raw material feed"),
            ("React", "Continuous reactor"),
            ("Separate", "Product separation"),
            ("Finish", "Product finishing"),
        ]):
            unit = self.add_unit(name, desc)
            unit.process.add_temperature(f"Stage{i}", setpoint=50 + i * 20,
                                         unit="degC")
            unit.process.add_pressure(f"Stage{i}", setpoint=14.7 + i * 5,
                                      unit="PSI")
            unit.process.add_flow(f"Stage{i}", setpoint=100 - i * 10,
                                  unit="GPM")
            unit.equipment.add_pump(f"P{i+1}", rated_flow=100 - i * 10)
            unit.equipment.add_valve(f"V{i+1}")

    def get_unit(self, name: str) -> Unit:
        """Get a unit by name."""
        for unit in self.units:
            if unit.name == name:
                return unit
        return None

    @property
    def path(self) -> str:
        return f"{self.area}/{self.name}"

    def __repr__(self):
        return (f"Line({self.path}, units={len(self.units)}, "
                f"tags={self.tag_db.tag_count})")
