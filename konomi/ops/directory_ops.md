# Directory Operations — Core Logic Layer

This module is the single operations layer that the CLI, REST API, and MCP provider all delegate to. It provides CRUD-style operations on konomi subpackages, tags, and L5X compilation through the `DirectoryOps` class. Every method returns a standardized `OpResult` dataclass, making it straightforward for any interface layer to translate results into its own format.

## Result Type

```python
"""
Directory Operations — the core logic layer.

Provides CRUD-style operations on konomi subpackages, tags, UDTs,
L5X compilation, and the directory tag registry. CLI, API, and MCP
all delegate to this single class.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from konomi import PACKAGES
from konomi.tags.directory_provider import (
    DirectoryTagRegistry, DirectoryTagProvider, DirectoryMeta, build_registry,
)


@dataclass
class OpResult:
    """Standardized result from any directory operation."""
    ok: bool
    data: Any = None
    error: str = ""

    def to_dict(self) -> dict:
        d = {"ok": self.ok}
        if self.data is not None:
            d["data"] = self.data
        if self.error:
            d["error"] = self.error
        return d
```

## DirectoryOps — Package and Tag Operations

```python
class DirectoryOps:
    """Unified operations layer for all konomi subpackages."""

    def __init__(self):
        self._registry = build_registry()

    # ── Package listing ──────────────────────────────────────────────

    def list_packages(self) -> OpResult:
        """List all konomi subpackages with descriptions."""
        items = []
        for name, info in PACKAGES.items():
            items.append({
                "name": name,
                "desc": info["desc"],
                "provides": info["provides"],
            })
        return OpResult(ok=True, data=items)

    def get_package(self, name: str) -> OpResult:
        """Get details of a specific package."""
        info = PACKAGES.get(name)
        if not info:
            return OpResult(ok=False, error=f"Unknown package: {name}")
        provider = self._registry.get_provider(name)
        tag_count = provider.count if provider else 0
        return OpResult(ok=True, data={
            "name": name,
            "desc": info["desc"],
            "provides": info["provides"],
            "tag_count": tag_count,
        })

    # ── Tag operations ───────────────────────────────────────────────

    def list_tags(self, package: str = None) -> OpResult:
        """List tags, optionally filtered by package."""
        if package:
            provider = self._registry.get_provider(package)
            if not provider:
                return OpResult(ok=False, error=f"No provider: {package}")
            return OpResult(ok=True, data=provider.paths())
        return OpResult(ok=True, data=self._registry.all_paths())

    def read_tag(self, path: str) -> OpResult:
        """Read a specific tag value."""
        for prov in self._registry._providers.values():
            tag = prov.get(path)
            if tag:
                v = tag.read()
                return OpResult(ok=True, data={
                    "path": path,
                    "value": v.v,
                    "quality": str(v.q),
                    "timestamp": str(v.t),
                    "unit": v.unit,
                })
        return OpResult(ok=False, error=f"Tag not found: {path}")

    def search_tags(self, pattern: str) -> OpResult:
        """Search tags by pattern."""
        matches = self._registry.search(pattern)
        return OpResult(ok=True, data=matches)
```

## L5X Compilation and Export

```python
    def compile_l5x(self, package: str = None,
                    project_name: str = "KONOMI") -> OpResult:
        """Compile tags from a package (or all) to L5X XML."""
        from konomi.l5x.compiler import L5XCompiler

        compiler = L5XCompiler(project_name=project_name)
        if package:
            provider = self._registry.get_provider(package)
            if not provider:
                return OpResult(ok=False, error=f"No provider: {package}")
            compiler.compile_tags(provider)
        else:
            for prov in self._registry._providers.values():
                compiler.compile_tags(prov)

        errors = compiler.validate()
        if errors:
            return OpResult(ok=False, error="; ".join(errors))
        return OpResult(ok=True, data=compiler.to_xml())

    def export_l5x(self, path: str, package: str = None,
                   project_name: str = "KONOMI") -> OpResult:
        """Compile and write L5X to a file."""
        result = self.compile_l5x(package, project_name)
        if not result.ok:
            return result
        try:
            with open(path, "w") as f:
                f.write(result.data)
            return OpResult(ok=True, data={"path": path})
        except OSError as e:
            return OpResult(ok=False, error=str(e))
```

## Registry Summary

```python
    def summary(self) -> OpResult:
        """Full system summary."""
        return OpResult(ok=True, data={
            "packages": len(PACKAGES),
            "directories_with_tags": self._registry.directory_count,
            "total_tags": self._registry.total_tags,
            "detail": self._registry.summary(),
        })
```
