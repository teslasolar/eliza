"""
SimEngine — simulation mode for the factory.
Default mode is SIM. No hardcoded values.
All values come from sim functions or tag providers.
"""

import time
import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Callable


class SimMode(Enum):
    """Factory operating mode."""
    SIM = "sim"         # simulated values from tag sim functions
    LIVE = "live"       # real values from OPC-UA/Modbus/MQTT connections
    REPLAY = "replay"   # replaying historical data


@dataclass
class SimEngine:
    """
    Drives the factory simulation.
    Default mode: SIM. Ticks tag providers at configurable rate.
    """
    mode: SimMode = SimMode.SIM
    tick_rate_hz: float = 1.0       # ticks per second
    _running: bool = field(default=False, repr=False)
    _tick_count: int = field(default=0, repr=False)
    _callbacks: list = field(default_factory=list, repr=False)
    _factory: Optional[object] = field(default=None, repr=False)

    def attach(self, factory):
        """Attach to a factory (Site) for tag updates."""
        self._factory = factory

    def on_tick(self, callback: Callable):
        """Register a callback for each sim tick."""
        self._callbacks.append(callback)

    def tick(self):
        """Execute one simulation tick. Reads all tags (triggers sim fns)."""
        if self.mode != SimMode.SIM:
            return

        self._tick_count += 1

        # Read all tags — this triggers their sim functions
        if self._factory and hasattr(self._factory, 'tag_db'):
            self._factory.tag_db.read_all()

        # Fire callbacks
        for cb in self._callbacks:
            cb(self._tick_count)

    def run_sync(self, ticks: int = 0):
        """
        Run simulation synchronously.
        ticks=0 means run until stop() is called.
        """
        self._running = True
        count = 0
        interval = 1.0 / self.tick_rate_hz

        while self._running:
            self.tick()
            count += 1
            if ticks > 0 and count >= ticks:
                break
            time.sleep(interval)

        self._running = False

    async def run_async(self, ticks: int = 0):
        """Run simulation asynchronously."""
        self._running = True
        count = 0
        interval = 1.0 / self.tick_rate_hz

        while self._running:
            self.tick()
            count += 1
            if ticks > 0 and count >= ticks:
                break
            await asyncio.sleep(interval)

        self._running = False

    def stop(self):
        """Stop the simulation."""
        self._running = False

    def set_mode(self, mode: SimMode):
        """Switch operating mode."""
        was_running = self._running
        if was_running:
            self.stop()
        self.mode = mode
        # LIVE and REPLAY modes would connect to external sources here

    @property
    def is_running(self) -> bool:
        return self._running

    @property
    def total_ticks(self) -> int:
        return self._tick_count

    def status(self) -> dict:
        return {
            "mode": self.mode.value,
            "running": self._running,
            "ticks": self._tick_count,
            "tick_rate_hz": self.tick_rate_hz,
        }

    def __repr__(self):
        return f"SimEngine(mode={self.mode.value}, ticks={self._tick_count})"
