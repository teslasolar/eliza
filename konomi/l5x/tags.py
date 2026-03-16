"""
L5X Tag Provider — Ignition-style tags for the PLC compiler.

Exposes compilation state, program/rung counts, export status,
and instruction statistics.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class L5XTagProvider(TagProvider):
    """Tag provider for the L5X compiler."""

    def __init__(self):
        super().__init__(prefix="L5X")
        self.register(Tag(path="Project_Name", type=TagType.STRING,
                          desc="Active L5X project name"))
        self.register(Tag(path="Programs", type=TagType.INTEGER,
                          desc="Number of PLC programs"))
        self.register(Tag(path="Routines", type=TagType.INTEGER,
                          desc="Total ladder routines"))
        self.register(Tag(path="Rungs", type=TagType.INTEGER,
                          desc="Total rungs across all routines"))
        self.register(Tag(path="DataTypes", type=TagType.INTEGER,
                          desc="User-defined data types"))
        self.register(Tag(path="Controller_Tags", type=TagType.INTEGER,
                          desc="Controller-scoped tags"))
        self.register(Tag(path="Last_Export", type=TagType.STRING,
                          desc="Last L5X export timestamp"))
        self.register(Tag(path="Validation_Errors", type=TagType.INTEGER,
                          desc="Errors in last validation pass"))
        # Defaults
        self.get("L5X_Project_Name").write("KONOMI")
        self.get("L5X_Validation_Errors").write(0)


def create_provider() -> L5XTagProvider:
    return L5XTagProvider()
