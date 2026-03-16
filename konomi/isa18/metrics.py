"""
ISA-18.2 Alarm Metrics — KPIs for alarm system health.

Provides calculation methods for alarm rate, flood detection,
stale alarms, chattering, bad actors, and priority distribution.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class AlarmEvent:
    """Lightweight record of an alarm activation for metric analysis."""
    alarm_id: str
    priority: int
    ts_in: float        # epoch seconds
    ts_out: float = 0.0
    transitions: int = 1


# ---------------------------------------------------------------------------
# ISA-18.2 benchmark targets
# ---------------------------------------------------------------------------

BENCHMARKS: Dict[str, float] = {
    "avg_alarms_per_op_per_hr": 6.0,
    "peak_alarms_per_op_per_hr": 12.0,
    "flood_threshold_count": 10,
    "flood_threshold_window_s": 600.0,      # 10 minutes
    "stale_threshold_s": 86400.0,           # 24 hours
    "chatter_threshold_per_min": 3.0,
    "p1_max_pct": 5.0,
    "p2_max_pct": 15.0,
    "p3_max_pct": 25.0,
    "p4_min_pct": 55.0,
}


class AlarmMetrics:
    """Calculator for ISA-18.2 alarm management KPIs.

    Feed alarm events via ``load()`` then call individual metric methods.
    """

    def __init__(self):
        self.events: List[AlarmEvent] = []

    def load(self, events: List[AlarmEvent]):
        """Load alarm events for analysis."""
        self.events = list(events)

    # --- Alarm rate ---

    def alarm_rate(self, operator_count: int = 1,
                   window_s: float = 3600.0) -> float:
        """Average alarms per operator per hour within the time window.

        Uses the last ``window_s`` seconds of loaded events.
        """
        if not self.events or operator_count < 1:
            return 0.0
        cutoff = max(e.ts_in for e in self.events) - window_s
        count = sum(1 for e in self.events if e.ts_in >= cutoff)
        hours = window_s / 3600.0
        return count / (operator_count * hours)

    # --- Flood detection ---

    def flood_intervals(self, threshold: int = 10,
                        window_s: float = 600.0) -> List[float]:
        """Return start timestamps of flood intervals.

        A flood is >=``threshold`` alarms within ``window_s`` seconds.
        """
        sorted_events = sorted(self.events, key=lambda e: e.ts_in)
        floods: List[float] = []
        for i, ev in enumerate(sorted_events):
            window_end = ev.ts_in + window_s
            count = sum(
                1 for e in sorted_events[i:]
                if e.ts_in <= window_end
            )
            if count >= threshold:
                if not floods or ev.ts_in - floods[-1] > window_s:
                    floods.append(ev.ts_in)
        return floods

    # --- Stale alarms ---

    def stale_alarms(self, now: float,
                     threshold_s: float = 86400.0) -> List[str]:
        """Return IDs of alarms active longer than ``threshold_s``."""
        stale: List[str] = []
        for e in self.events:
            if e.ts_out == 0.0 and (now - e.ts_in) > threshold_s:
                stale.append(e.alarm_id)
        return stale

    # --- Chattering alarms ---

    def chattering_alarms(self, threshold_per_min: float = 3.0) -> List[str]:
        """Return IDs of alarms exceeding transition-rate threshold."""
        chattering: List[str] = []
        for e in self.events:
            if e.ts_out > e.ts_in:
                duration_min = (e.ts_out - e.ts_in) / 60.0
                if duration_min > 0:
                    rate = e.transitions / duration_min
                    if rate > threshold_per_min:
                        chattering.append(e.alarm_id)
        return chattering

    # --- Bad actors ---

    def bad_actors(self, top_n: int = 10) -> List[tuple]:
        """Return top-N most frequent alarm IDs as (id, count) pairs."""
        counts: Dict[str, int] = {}
        for e in self.events:
            counts[e.alarm_id] = counts.get(e.alarm_id, 0) + 1
        ranked = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_n]

    # --- Priority distribution ---

    def percent_by_priority(self) -> Dict[str, float]:
        """Return percentage of alarms at each priority level.

        ISA-18.2 targets: P1 <5%, P2 <15%, P3 <25%, P4 >55%.
        """
        if not self.events:
            return {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
        total = len(self.events)
        counts = {1: 0, 2: 0, 3: 0, 4: 0}
        for e in self.events:
            if e.priority in counts:
                counts[e.priority] += 1
        return {
            f"P{k}": round(v / total * 100, 1) for k, v in counts.items()
        }

    def priority_compliant(self) -> bool:
        """Check if priority distribution meets ISA-18.2 benchmarks."""
        pct = self.percent_by_priority()
        return (
            pct["P1"] <= BENCHMARKS["p1_max_pct"]
            and pct["P2"] <= BENCHMARKS["p2_max_pct"]
            and pct["P3"] <= BENCHMARKS["p3_max_pct"]
            and pct["P4"] >= BENCHMARKS["p4_min_pct"]
        )

    # --- Summary ---

    def summary(self, operator_count: int = 1,
                now: float = 0.0) -> Dict[str, object]:
        """Generate a full KPI summary dict."""
        return {
            "alarm_rate_per_op_hr": round(self.alarm_rate(operator_count), 2),
            "flood_count": len(self.flood_intervals()),
            "stale_count": len(self.stale_alarms(now)) if now else 0,
            "chattering_count": len(self.chattering_alarms()),
            "bad_actors": self.bad_actors(),
            "priority_pct": self.percent_by_priority(),
            "priority_compliant": self.priority_compliant(),
        }
