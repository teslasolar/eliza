# Directory Tag Provider

One TagProvider per konomi subpackage. Each subdirectory registers its own local tags, and the DirectoryTagRegistry aggregates them all for a unified view while keeping ownership local.

## DirectoryMeta and DirectoryTagProvider

```python
"""
Directory Tag Provider — one TagProvider per konomi subpackage.

Each subdirectory can register its own local tags. The DirectoryTagRegistry
aggregates them all, giving a unified view while keeping ownership local.
"""

from dataclasses import dataclass, field
from typing import Optional
from konomi.tags.provider import TagProvider, Tag, TagType
from konomi.base.value import Value


@dataclass
class DirectoryMeta:
    """Metadata about a directory's tag namespace."""
    package: str        # e.g. "isa88"
    prefix: str         # tag path prefix e.g. "ISA88"
    desc: str = ""
    version: str = "1.0"


class DirectoryTagProvider(TagProvider):
    """A TagProvider scoped to a single konomi subdirectory."""

    def __init__(self, meta: DirectoryMeta):
        super().__init__(prefix=meta.prefix)
        self.meta = meta
        self._status_tags: dict[str, Tag] = {}
        self._register_builtin()

    def _register_builtin(self):
        """Every directory gets standard status tags."""
        self._status_tags["_LOADED"] = self.register(Tag(
            path="_LOADED", type=TagType.DISCRETE,
            desc=f"{self.meta.package} module loaded",
        ))
        self._status_tags["_VERSION"] = self.register(Tag(
            path="_VERSION", type=TagType.STRING,
            desc=f"{self.meta.package} version",
        ))
        self._status_tags["_TAG_COUNT"] = self.register(Tag(
            path="_TAG_COUNT", type=TagType.INTEGER,
            desc="Number of registered tags",
        ))
        # Set initial values
        self._status_tags["_LOADED"].write(True)
        self._status_tags["_VERSION"].write(self.meta.version)

    def refresh_count(self):
        """Update the tag-count meta tag."""
        self._status_tags["_TAG_COUNT"].write(self.count)

    @property
    def package_name(self) -> str:
        return self.meta.package
```

## DirectoryTagRegistry

```python
class DirectoryTagRegistry:
    """Aggregates DirectoryTagProviders from all subpackages."""

    def __init__(self):
        self._providers: dict[str, DirectoryTagProvider] = {}

    def register(self, provider: DirectoryTagProvider):
        """Register a directory provider."""
        provider.refresh_count()
        self._providers[provider.package_name] = provider

    def get_provider(self, package: str) -> Optional[DirectoryTagProvider]:
        """Get the provider for a specific package."""
        return self._providers.get(package)

    def read_all(self) -> dict[str, Value]:
        """Read all tags from every directory."""
        result = {}
        for prov in self._providers.values():
            result.update(prov.read_all())
        return result

    def all_paths(self) -> list[str]:
        """All tag paths across all directories."""
        paths = []
        for prov in self._providers.values():
            paths.extend(prov.paths())
        return sorted(paths)

    def search(self, pattern: str) -> list[str]:
        """Search tag paths by substring."""
        return [p for p in self.all_paths() if pattern.upper() in p.upper()]

    @property
    def total_tags(self) -> int:
        return sum(p.count for p in self._providers.values())

    @property
    def directory_count(self) -> int:
        return len(self._providers)

    def summary(self) -> str:
        lines = [f"DirectoryTagRegistry: {self.directory_count} dirs, "
                 f"{self.total_tags} tags", ""]
        for name, prov in sorted(self._providers.items()):
            lines.append(f"  {name:<14s} {prov.count:>4d} tags  "
                         f"{prov.meta.desc}")
        return "\n".join(lines)

    def __repr__(self):
        return f"DirectoryTagRegistry(dirs={self.directory_count}, tags={self.total_tags})"
```

## Pre-built Directory Providers

```python
# ── Pre-built directory providers ────────────────────────────────────

_DIRECTORY_DEFS = [
    DirectoryMeta("meta",      "META",      "Meta-standard framework"),
    DirectoryMeta("base",      "BASE",      "Primitive types and values"),
    DirectoryMeta("tags",      "TAGS",      "Tag system core"),
    DirectoryMeta("factory",   "FAC",       "Factory hierarchy + simulation"),
    DirectoryMeta("isa88",     "ISA88",     "Batch control"),
    DirectoryMeta("isa95",     "ISA95",     "Enterprise/control integration"),
    DirectoryMeta("isa18",     "ISA18",     "Alarm management"),
    DirectoryMeta("isa101",    "ISA101",    "HMI design"),
    DirectoryMeta("opcua",     "OPCUA",     "OPC-UA communication"),
    DirectoryMeta("sparkplug", "SPKPLG",    "MQTT/Sparkplug B"),
    DirectoryMeta("modbus",    "MODBUS",    "Modbus field protocol"),
    DirectoryMeta("kpi",       "KPI",       "Performance metrics"),
    DirectoryMeta("crosswalk", "XWALK",     "Cross-standard mappings"),
    DirectoryMeta("scanner",   "SCAN",      "Compliance scanning"),
    DirectoryMeta("evgpu",     "EVGPU",     "CPU-based compute"),
    DirectoryMeta("femto",     "FEMTO",     "Tiny ML model"),
    DirectoryMeta("l5x",       "L5X",       "Rockwell PLC compiler"),
    DirectoryMeta("ops",       "OPS",       "CLI/API/MCP operations"),
]


def build_registry() -> DirectoryTagRegistry:
    """Build the default registry with one provider per directory."""
    registry = DirectoryTagRegistry()
    for meta in _DIRECTORY_DEFS:
        registry.register(DirectoryTagProvider(meta))
    return registry
```
