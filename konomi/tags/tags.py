"""
Tags Tag Provider — meta tag provider for the tag system itself.

Exposes total tag counts, provider counts, and registry health.
The tag system monitoring its own tags — turtles all the way down.
"""

from konomi.tags.provider import TagProvider, Tag, TagType


class TagsTagProvider(TagProvider):
    """Tag provider for the tag system meta-layer."""

    def __init__(self):
        super().__init__(prefix="TAGS")
        self.register(Tag(path="Provider_Count", type=TagType.INTEGER,
                          desc="Number of active tag providers"))
        self.register(Tag(path="Total_Tags", type=TagType.INTEGER,
                          desc="Total tags across all providers"))
        self.register(Tag(path="Directory_Providers", type=TagType.INTEGER,
                          desc="Per-directory providers registered"))
        self.register(Tag(path="Equipment_Tags", type=TagType.INTEGER,
                          desc="Equipment tag count"))
        self.register(Tag(path="Process_Tags", type=TagType.INTEGER,
                          desc="Process tag count"))
        self.register(Tag(path="Batch_Tags", type=TagType.INTEGER,
                          desc="Batch tag count"))
        self.register(Tag(path="Alarm_Tags", type=TagType.INTEGER,
                          desc="Alarm tag count"))
        self.register(Tag(path="Quality_Good_Pct", type=TagType.ANALOG,
                          desc="Tags with GOOD quality", unit="%"))
        # Defaults
        self.get("TAGS_Quality_Good_Pct").write(100.0)


def create_provider() -> TagsTagProvider:
    return TagsTagProvider()
