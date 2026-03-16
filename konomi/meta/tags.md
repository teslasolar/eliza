# Meta Framework Tags

Tag provider for the meta-standard layer. Exposes the state of the meta framework: how many standards, UDTs, entities, rules, and state machines are currently defined.

```python
"""
Meta Tag Provider — Ignition-style tag source for the meta-standard layer.

Tags expose the state of the meta framework: how many standards, UDTs,
entities, rules, and state machines are currently defined.

Usage:
    provider = MetaTagProvider()
    provider.read_all()
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class MetaTagProvider(TagProvider):
    """Tag provider for the meta-standard framework."""

    def __init__(self):
        super().__init__(prefix="META")
        self.register(Tag(path="Standards_Count", type=TagType.INTEGER,
                          desc="Number of registered standards"))
        self.register(Tag(path="UDT_Count", type=TagType.INTEGER,
                          desc="Number of User Defined Types"))
        self.register(Tag(path="Entity_Count", type=TagType.INTEGER,
                          desc="Number of entities across all standards"))
        self.register(Tag(path="Rule_Count", type=TagType.INTEGER,
                          desc="Number of validation rules"))
        self.register(Tag(path="StateMachine_Count", type=TagType.INTEGER,
                          desc="Number of state machines"))
        self.register(Tag(path="Field_Count", type=TagType.INTEGER,
                          desc="Total fields across all UDTs"))
        self.register(Tag(path="Crosswalk_Count", type=TagType.INTEGER,
                          desc="Number of cross-standard mappings"))
        self.register(Tag(path="Version", type=TagType.STRING,
                          desc="Meta framework version"))
        # Defaults
        self.get("META_Version").write("1.0.0")


def create_provider() -> MetaTagProvider:
    """Factory function for the directory tag registry."""
    return MetaTagProvider()
```
