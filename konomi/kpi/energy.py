"""
Energy KPIs — power consumption tracking.
"""

from dataclasses import dataclass, field


@dataclass
class EnergyKPI:
    """Energy consumption tracking."""
    kwh_total: float = 0.0
    units_produced: int = 0
    batches_completed: int = 0
    peak_demand_kw: float = 0.0
    power_factor: float = 1.0    # ratio of real to apparent power

    @property
    def kwh_per_unit(self) -> float:
        """Energy per unit produced."""
        if self.units_produced == 0:
            return 0.0
        return self.kwh_total / self.units_produced

    @property
    def kwh_per_batch(self) -> float:
        """Energy per batch completed."""
        if self.batches_completed == 0:
            return 0.0
        return self.kwh_total / self.batches_completed

    def record_consumption(self, kwh: float, units: int = 0,
                           batches: int = 0, peak_kw: float = 0):
        """Record an energy consumption period."""
        self.kwh_total += kwh
        self.units_produced += units
        self.batches_completed += batches
        if peak_kw > self.peak_demand_kw:
            self.peak_demand_kw = peak_kw

    def report(self) -> dict:
        return {
            "kwh_total": round(self.kwh_total, 1),
            "kwh_per_unit": round(self.kwh_per_unit, 2),
            "kwh_per_batch": round(self.kwh_per_batch, 2),
            "peak_demand_kw": round(self.peak_demand_kw, 1),
            "power_factor": round(self.power_factor, 3),
        }

    def __str__(self):
        return (f"Energy: {self.kwh_total:.0f} kWh total, "
                f"{self.kwh_per_unit:.2f} kWh/unit, "
                f"peak {self.peak_demand_kw:.0f} kW")
