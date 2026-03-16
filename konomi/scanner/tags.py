"""
Scanner Tag Provider — Ignition-style tags for compliance scanning.

Exposes scan results, rule counts, compliance scores,
and violation breakdowns.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class ScannerTagProvider(TagProvider):
    """Tag provider for the compliance scanner."""

    def __init__(self):
        super().__init__(prefix="SCAN")
        self.register(Tag(path="Rules_Total", type=TagType.INTEGER,
                          desc="Total registered compliance rules"))
        self.register(Tag(path="Last_Score", type=TagType.ANALOG,
                          desc="Last scan compliance score", unit="%"))
        self.register(Tag(path="Is_Compliant", type=TagType.DISCRETE,
                          desc="Last scan passed compliance"))
        self.register(Tag(path="Violations_Fatal", type=TagType.INTEGER,
                          desc="Fatal violations in last scan"))
        self.register(Tag(path="Violations_Error", type=TagType.INTEGER,
                          desc="Error violations in last scan"))
        self.register(Tag(path="Violations_Warn", type=TagType.INTEGER,
                          desc="Warning violations in last scan"))
        self.register(Tag(path="Violations_Info", type=TagType.INTEGER,
                          desc="Info violations in last scan"))
        self.register(Tag(path="Scans_Total", type=TagType.INTEGER,
                          desc="Total scans performed"))
        # Defaults
        self.get("SCAN_Is_Compliant").write(True)
        self.get("SCAN_Scans_Total").write(0)


def create_provider() -> ScannerTagProvider:
    return ScannerTagProvider()
