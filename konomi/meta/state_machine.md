# State Machine

Formal state transitions used across all standards. ISA-88 PhaseState, PackML, BatchState, and AlarmState all use this pattern.

## Transition

A state transition with optional guard condition and side-effect action.

```python
from dataclasses import dataclass, field
from typing import Optional, Callable, Any


@dataclass
class Transition:
    """A state transition with optional guard and action."""
    from_state: str
    to_state: str
    trigger: str                           # what causes this transition
    guard: Optional[Callable] = None       # condition that must be true
    action: Optional[Callable] = None      # side effect on transition
    desc: str = ""

    def can_fire(self, context: dict = None) -> bool:
        """Check if this transition can fire given context."""
        if self.guard is None:
            return True
        return self.guard(context or {})

    def fire(self, context: dict = None) -> str:
        """Execute the transition. Returns the new state."""
        if self.action:
            self.action(context or {})
        return self.to_state
```

## StateMachine

A formal state machine with named states, transitions, and trigger-based firing.

```python
@dataclass
class StateMachine:
    """A formal state machine with named states and transitions."""
    name: str
    states: list = field(default_factory=list)
    initial: str = ""
    transitions: list = field(default_factory=list)
    current: str = ""

    def __post_init__(self):
        if not self.current and self.initial:
            self.current = self.initial

    def add_state(self, name: str) -> "StateMachine":
        """Add a state. Returns self for chaining."""
        if name not in self.states:
            self.states.append(name)
        return self

    def add_transition(self, from_state: str, to_state: str,
                       trigger: str, **kwargs) -> "StateMachine":
        """Add a transition. Returns self for chaining."""
        self.transitions.append(
            Transition(from_state=from_state, to_state=to_state,
                       trigger=trigger, **kwargs)
        )
        return self

    def available_transitions(self) -> list:
        """Get transitions available from current state."""
        return [t for t in self.transitions if t.from_state == self.current]

    def can_transition(self, trigger: str, context: dict = None) -> bool:
        """Check if a trigger can fire from current state."""
        for t in self.available_transitions():
            if t.trigger == trigger and t.can_fire(context):
                return True
        return False

    def fire(self, trigger: str, context: dict = None) -> str:
        """Fire a trigger. Returns new state or raises ValueError."""
        for t in self.available_transitions():
            if t.trigger == trigger and t.can_fire(context):
                self.current = t.fire(context)
                return self.current
        valid = [t.trigger for t in self.available_transitions()]
        raise ValueError(
            f"Cannot fire '{trigger}' from '{self.current}'. "
            f"Valid triggers: {valid}"
        )

    def reset(self):
        """Reset to initial state."""
        self.current = self.initial

    def describe(self) -> dict:
        """Describe the state machine."""
        return {
            "name": self.name,
            "states": self.states,
            "initial": self.initial,
            "current": self.current,
            "transitions": [
                {"from": t.from_state, "to": t.to_state, "trigger": t.trigger}
                for t in self.transitions
            ],
        }

    def __repr__(self):
        return (f"StateMachine({self.name}, "
                f"state={self.current}, states={len(self.states)})")
```
