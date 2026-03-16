# Factory Tag Database

Aggregates all tag providers for a facility. Supports hierarchical aggregation via child databases for the ISA-95 Site/Area/Line/Unit structure.

```python
"""
Factory Tag Database — aggregates all tag providers for a facility.
Supports hierarchical aggregation via child databases.
"""

from konomi.tags.provider import TagProvider, Tag
from konomi.base.value import Value


class FactoryTagDatabase:
    """
    Central registry for all tags in a facility.
    Supports both direct providers and child databases for hierarchy.
    """

    def __init__(self):
        self._providers: dict[str, TagProvider] = {}
        self._children: list["FactoryTagDatabase"] = []

    def register_provider(self, name: str, provider: TagProvider):
        """Register a tag provider."""
        self._providers[name] = provider

    def add_child(self, child: "FactoryTagDatabase"):
        """Add a child database (for hierarchical aggregation)."""
        self._children.append(child)

    def get_provider(self, name: str) -> TagProvider:
        """Get a tag provider by name."""
        return self._providers.get(name)

    def _all_providers(self) -> dict[str, TagProvider]:
        """Get all providers including from children (recursive)."""
        result = dict(self._providers)
        for child in self._children:
            result.update(child._all_providers())
        return result

    def get_tag(self, path: str) -> Tag:
        """Look up a tag by full path across all providers."""
        for provider in self._all_providers().values():
            tag = provider.get(path)
            if tag:
                return tag
        return None

    def read_tag(self, path: str) -> Value:
        """Read a single tag value."""
        tag = self.get_tag(path)
        if tag:
            return tag.read()
        return None

    def read_all(self) -> dict[str, Value]:
        """Read all tags from all providers (including children)."""
        result = {}
        for provider in self._all_providers().values():
            result.update(provider.read_all())
        return result

    def all_paths(self) -> list[str]:
        """Get all tag paths in the database."""
        paths = []
        for provider in self._all_providers().values():
            paths.extend(provider.paths())
        return sorted(paths)

    def search(self, pattern: str) -> list[str]:
        """Search tag paths by substring match."""
        pattern_lower = pattern.lower()
        return [p for p in self.all_paths() if pattern_lower in p.lower()]

    @property
    def tag_count(self) -> int:
        return sum(p.count for p in self._all_providers().values())

    @property
    def provider_count(self) -> int:
        return len(self._all_providers())

    def summary(self) -> dict:
        """Database summary."""
        all_p = self._all_providers()
        return {
            "total_tags": sum(p.count for p in all_p.values()),
            "providers": {name: p.count for name, p in all_p.items()},
        }

    def __repr__(self):
        return f"FactoryTagDatabase(providers={self.provider_count}, tags={self.tag_count})"
```
