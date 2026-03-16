"""
Unit — a process unit within a production line.
Contains equipment, process tags, batch tags, and alarms.
This is the lowest level of the ISA-95 hierarchy that matters for control.
"""

from dataclasses import dataclass, field
from konomi.tags.process import ProcessTags
from konomi.tags.equipment import EquipmentTags
from konomi.tags.batch import BatchTags
from konomi.tags.alarm import AlarmTags
from konomi.tags.factory_tags import FactoryTagDatabase


@dataclass
class Unit:
    """A process unit (ISA-95 WorkUnit / ISA-88 Unit)."""
    name: str
    area: str = ""
    desc: str = ""
    tag_db: FactoryTagDatabase = field(default_factory=FactoryTagDatabase)
    process: ProcessTags = field(default=None, repr=False)
    equipment: EquipmentTags = field(default=None, repr=False)
    batch: BatchTags = field(default=None, repr=False)
    alarms: AlarmTags = field(default=None, repr=False)

    def __post_init__(self):
        self.process = ProcessTags(self.area, self.name)
        self.equipment = EquipmentTags(self.area, self.name)
        self.batch = BatchTags(self.area, self.name)
        self.alarms = AlarmTags(self.area, self.name)
        self.tag_db.register_provider(f"{self.name}_process", self.process)
        self.tag_db.register_provider(f"{self.name}_equipment", self.equipment)
        self.tag_db.register_provider(f"{self.name}_batch", self.batch)
        self.tag_db.register_provider(f"{self.name}_alarms", self.alarms)

    def setup_mixing_unit(self):
        """Configure as a typical mixing/reactor unit."""
        self.process.add_temperature("Jacket", setpoint=75.0, unit="degC",
                                     desc="Jacket temperature")
        self.process.add_temperature("Product", setpoint=70.0, unit="degC",
                                     desc="Product temperature")
        self.process.add_pressure("Vessel", setpoint=14.7, unit="PSI",
                                  desc="Vessel pressure")
        self.process.add_level("Tank", setpoint=50.0, unit="pct",
                               desc="Tank level")
        self.equipment.add_motor("Agitator", rated_amps=12.0)
        self.equipment.add_valve("Inlet")
        self.equipment.add_valve("Outlet")
        self.equipment.add_pump("Feed", rated_flow=50.0)
        self.batch.add_batch_id()
        self.batch.add_phase_state()
        self.batch.add_step_counter()
        self.batch.add_recipe_param("Temperature", 75.0, "degC")
        self.batch.add_recipe_param("MixTime", 300.0, "s")
        self.alarms.add_alarm("TempHi", priority=2, setpoint=85.0,
                              alarm_type="HI",
                              message="Product temperature high",
                              consequence="Product degradation",
                              response="Check cooling water supply")
        self.alarms.add_alarm("LevelHiHi", priority=1, setpoint=95.0,
                              alarm_type="HIHI",
                              message="Tank level critical high",
                              consequence="Overflow, environmental release",
                              response="Close inlet valve, open drain")
        self.alarms.add_alarm("PressHi", priority=2, setpoint=50.0,
                              alarm_type="HI",
                              message="Vessel pressure high",
                              consequence="Vessel overpressure",
                              response="Check vent valve, reduce feed")

    def setup_filling_unit(self):
        """Configure as a filling/packaging unit."""
        self.process.add_flow("Filler", setpoint=120.0, unit="ml/s",
                              desc="Fill flow rate")
        self.process.add_level("Hopper", setpoint=60.0, unit="pct",
                               desc="Hopper level")
        self.equipment.add_motor("Conveyor", rated_amps=8.0)
        self.equipment.add_valve("FillValve")
        self.equipment.add_motor("Capper", rated_amps=5.0)
        self.batch.add_batch_id()
        self.batch.add_step_counter()
        self.alarms.add_alarm("HopperLo", priority=3, setpoint=10.0,
                              alarm_type="LO",
                              message="Hopper level low",
                              consequence="Line starvation",
                              response="Check supply feed")

    @property
    def path(self) -> str:
        return f"{self.area}/{self.name}"

    def __repr__(self):
        return f"Unit({self.path}, tags={self.tag_db.tag_count})"
