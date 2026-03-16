# 3D Vector Space Blocks

Encoding standards and knowledge into immutable 3D spatial coordinates.

```python
from guild_chain.vectors import (
    build_standard_chain, Vector3D, KONOMI_VECTORS, ACG_VECTORS
)

chain = build_standard_chain()
print(f"Vector chain: {chain.height} blocks")
print(f"Integrity: {'VALID' if chain.verify() else 'BROKEN'}")
print()

# Show all blocks
for b in chain.blocks:
    print(f"  #{b.index:2d} {b.vector} [{b.category:<10s}] "
          f"{b.data.get('package', b.data.get('key', 'genesis'))}")

# Spatial query: find everything near ISA-88
print(f"\n--- Near ISA-88 (radius 300) ---")
isa88_center = KONOMI_VECTORS["isa88"]
nearby = chain.query_radius(isa88_center, 300)
for b in nearby:
    dist = b.vector.distance_to(isa88_center)
    print(f"  {b.vector} d={dist:.0f} — {b.data.get('package', b.data.get('key', '?'))}")

# Find nearest to a principle
print(f"\n--- 5 nearest to Principle 6 (Right to Refuse) ---")
p6 = ACG_VECTORS["principle_6_refuse"]
for b in chain.nearest(p6, 5):
    dist = b.vector.distance_to(p6)
    print(f"  {b.vector} d={dist:.0f} — {b.data.get('package', b.data.get('description', '?'))}")

# Axis query: everything at audit level (z >= 900)
print(f"\n--- Audit-level blocks (z >= 900) ---")
for b in chain.query_axis("z", 900, 1000):
    print(f"  {b.vector} — {b.data.get('package', b.data.get('key', '?'))}")
```
