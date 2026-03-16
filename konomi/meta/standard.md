# Standard

Meta-Standard: the structure that all standards follow. Every ISA/OPC/ACG standard is an instance of this structure.

## Data Model

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Standard:
    """A self-describing industrial standard."""
    id: str                          # unique key (ISA-95, ISA-88, etc.)
    scope: str                       # what it covers
    version: str = "1.0"
    udts: list = field(default_factory=list)           # user defined types
    hierarchy: list = field(default_factory=list)       # levels/layers
    state_machines: list = field(default_factory=list)  # state models
    entities: list = field(default_factory=list)        # core objects
    relations: list = field(default_factory=list)       # how entities connect
    rules: list = field(default_factory=list)           # constraints, validations
    crosswalks: dict = field(default_factory=dict)      # mappings to other standards
```

## Registration Methods

```python
    def add_udt(self, udt):
        """Register a UDT with this standard."""
        self.udts.append(udt)
        return udt

    def add_entity(self, entity):
        """Register an entity with this standard."""
        self.entities.append(entity)
        return entity

    def add_rule(self, rule):
        """Register a validation rule."""
        self.rules.append(rule)
        return rule

    def add_state_machine(self, sm):
        """Register a state machine."""
        self.state_machines.append(sm)
        return sm

    def add_crosswalk(self, target_std_id, mapping):
        """Add a mapping to another standard."""
        self.crosswalks[target_std_id] = mapping
```

## Validation and Lookup

```python
    def validate(self, entity_data: dict) -> list:
        """Validate entity data against all rules. Returns list of violations."""
        violations = []
        for rule in self.rules:
            result = rule.check(entity_data)
            if result:
                violations.append(result)
        return violations

    def get_udt(self, name: str):
        """Look up a UDT by name."""
        for udt in self.udts:
            if udt.name == name:
                return udt
        return None

    def get_entity(self, name: str):
        """Look up an entity by name."""
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None
```

## Introspection

```python
    def describe(self) -> dict:
        """Self-describe this standard as a dict."""
        return {
            "id": self.id,
            "scope": self.scope,
            "version": self.version,
            "udt_count": len(self.udts),
            "entity_count": len(self.entities),
            "rule_count": len(self.rules),
            "state_machine_count": len(self.state_machines),
            "crosswalk_targets": list(self.crosswalks.keys()),
        }

    def __repr__(self):
        return f"Standard({self.id}, udts={len(self.udts)}, rules={len(self.rules)})"
```
