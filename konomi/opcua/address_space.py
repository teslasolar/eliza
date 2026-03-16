"""
OPC-UA Address Space — the hierarchical tree that organizes all nodes.
Standard structure: Root -> Objects, Types, Views with well-known folders.
"""

from dataclasses import dataclass, field
from typing import Optional

from konomi.opcua.nodes import OPCNode, NodeClass


# Well-known node IDs per OPC-UA spec
_ROOT_ID = "i=84"
_OBJECTS_ID = "i=85"
_TYPES_ID = "i=86"
_VIEWS_ID = "i=87"


def _folder(node_id: str, name: str, parent: str) -> OPCNode:
    """Create a folder node."""
    return OPCNode(
        node_id=node_id,
        browse_name=name,
        display_name=name,
        node_class=NodeClass.OBJECT,
        parent=parent,
    )


@dataclass
class AddressSpace:
    """
    The OPC-UA address space tree.

    Root
    +-- Objects
    |   +-- Server
    |   +-- DeviceSet
    |   +-- Aliases
    +-- Types
    |   +-- ObjectTypes
    |   +-- VariableTypes
    |   +-- DataTypes
    |   +-- ReferenceTypes
    +-- Views
        +-- Engineering
        +-- Operations
        +-- Maintenance
    """
    nodes: dict[str, OPCNode] = field(default_factory=dict)
    _next_ns_id: int = 1000

    def __post_init__(self):
        self._build_standard_tree()

    def _build_standard_tree(self):
        """Construct the well-known OPC-UA folder hierarchy."""
        # Root
        root = OPCNode(
            node_id=_ROOT_ID, browse_name="Root",
            display_name="Root", node_class=NodeClass.OBJECT,
        )
        self._add(root)

        # Root -> Objects
        objects = _folder(_OBJECTS_ID, "Objects", _ROOT_ID)
        self._add(objects)
        for nid, name in [
            ("i=2253", "Server"),
            ("ns=1;s=DeviceSet", "DeviceSet"),
            ("ns=1;s=Aliases", "Aliases"),
        ]:
            self._add(_folder(nid, name, _OBJECTS_ID))

        # Root -> Types
        types = _folder(_TYPES_ID, "Types", _ROOT_ID)
        self._add(types)
        for nid, name in [
            ("i=58", "ObjectTypes"),
            ("i=62", "VariableTypes"),
            ("i=24", "DataTypes"),
            ("i=31", "ReferenceTypes"),
        ]:
            self._add(_folder(nid, name, _TYPES_ID))

        # Root -> Views
        views = _folder(_VIEWS_ID, "Views", _ROOT_ID)
        self._add(views)
        for nid, name in [
            ("ns=1;s=Engineering", "Engineering"),
            ("ns=1;s=Operations", "Operations"),
            ("ns=1;s=Maintenance", "Maintenance"),
        ]:
            self._add(_folder(nid, name, _VIEWS_ID))

    def _add(self, node: OPCNode):
        """Insert a node into the address space."""
        self.nodes[node.node_id] = node

    def add_node(self, node: OPCNode) -> OPCNode:
        """Add a user-defined node to the address space."""
        self._add(node)
        if node.parent and node.parent in self.nodes:
            self.nodes[node.parent].add_reference(node.node_id, "HasComponent")
        return node

    def get(self, node_id: str) -> Optional[OPCNode]:
        """Retrieve a node by ID."""
        return self.nodes.get(node_id)

    def children_of(self, parent_id: str) -> list[OPCNode]:
        """Return all nodes whose parent is the given ID."""
        return [n for n in self.nodes.values() if n.parent == parent_id]

    def browse(self, node_id: str, depth: int = 1) -> list[OPCNode]:
        """Browse the tree from a node to the specified depth."""
        result = []
        if depth <= 0:
            return result
        kids = self.children_of(node_id)
        result.extend(kids)
        if depth > 1:
            for kid in kids:
                result.extend(self.browse(kid.node_id, depth - 1))
        return result

    def allocate_id(self, namespace: int = 1) -> str:
        """Allocate a new unique node ID."""
        nid = f"ns={namespace};i={self._next_ns_id}"
        self._next_ns_id += 1
        return nid

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    def __repr__(self):
        return f"AddressSpace(nodes={self.node_count})"
