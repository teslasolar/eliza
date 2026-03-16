"""
ISA-88 Recipe Hierarchy — product definition model.

Recipe levels: GeneralRecipe -> SiteRecipe -> MasterRecipe -> ControlRecipe

A Recipe contains a Formula (materials in/out and process parameters)
and references a Procedure (the procedural control logic).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RecipeLevel(Enum):
    """ISA-88 recipe hierarchy levels."""
    GENERAL = "GeneralRecipe"
    SITE = "SiteRecipe"
    MASTER = "MasterRecipe"
    CONTROL = "ControlRecipe"


# ---------------------------------------------------------------------------
# Formula components
# ---------------------------------------------------------------------------

@dataclass
class MaterialCharge:
    """A material input or output in a formula."""
    material: str
    quantity: float
    uom: str                    # unit of measure (kg, L, etc.)
    lot: str = ""
    desc: str = ""


@dataclass
class ProcessParam:
    """A process parameter in a formula."""
    name: str
    value: float
    uom: str = ""
    desc: str = ""


@dataclass
class Formula:
    """ISA-88 Formula — defines materials and parameters for a recipe.

    Contains:
        inputs:  list of material charges consumed
        outputs: list of material charges produced
        params:  list of process parameters (temperature, speed, etc.)
    """
    inputs: List[MaterialCharge] = field(default_factory=list)
    outputs: List[MaterialCharge] = field(default_factory=list)
    params: List[ProcessParam] = field(default_factory=list)

    def add_input(self, material: str, quantity: float,
                  uom: str, **kw) -> "Formula":
        self.inputs.append(MaterialCharge(
            material=material, quantity=quantity, uom=uom, **kw))
        return self

    def add_output(self, material: str, quantity: float,
                   uom: str, **kw) -> "Formula":
        self.outputs.append(MaterialCharge(
            material=material, quantity=quantity, uom=uom, **kw))
        return self

    def add_param(self, name: str, value: float,
                  uom: str = "", **kw) -> "Formula":
        self.params.append(ProcessParam(
            name=name, value=value, uom=uom, **kw))
        return self

    def scale(self, factor: float) -> "Formula":
        """Return a new Formula scaled by the given factor."""
        return Formula(
            inputs=[MaterialCharge(
                material=m.material, quantity=m.quantity * factor,
                uom=m.uom, lot=m.lot, desc=m.desc) for m in self.inputs],
            outputs=[MaterialCharge(
                material=m.material, quantity=m.quantity * factor,
                uom=m.uom, lot=m.lot, desc=m.desc) for m in self.outputs],
            params=list(self.params),  # params are not scaled
        )

    def describe(self) -> dict:
        return {
            "inputs": len(self.inputs),
            "outputs": len(self.outputs),
            "params": len(self.params),
        }


# ---------------------------------------------------------------------------
# Equipment requirement
# ---------------------------------------------------------------------------

@dataclass
class EquipmentRequirement:
    """Specifies what equipment a recipe needs."""
    unit_class: str             # logical class (e.g. "Reactor", "Mixer")
    capabilities: List[str] = field(default_factory=list)
    min_volume: Optional[float] = None
    max_volume: Optional[float] = None
    volume_uom: str = "L"

    def matches(self, unit_class: str,
                capabilities: List[str] = None) -> bool:
        """Check whether a unit satisfies this requirement."""
        if unit_class != self.unit_class:
            return False
        if self.capabilities:
            caps = set(capabilities or [])
            if not set(self.capabilities).issubset(caps):
                return False
        return True


# ---------------------------------------------------------------------------
# Recipe
# ---------------------------------------------------------------------------

@dataclass
class Recipe:
    """ISA-88 Recipe — the complete product definition at a given level.

    Attributes:
        id:            unique recipe identifier
        name:          human-readable name
        version:       recipe version string
        level:         hierarchy level (General/Site/Master/Control)
        product:       product identifier this recipe produces
        procedure_id:  reference to a Procedure (procedural model)
        formula:       material and parameter definitions
        equipment_req: list of equipment requirements
        parent_id:     reference to parent recipe (higher level)
        approved:      whether the recipe is approved for use
    """
    id: str
    name: str
    version: str = "1.0"
    level: RecipeLevel = RecipeLevel.GENERAL
    product: str = ""
    procedure_id: Optional[str] = None
    formula: Formula = field(default_factory=Formula)
    equipment_req: List[EquipmentRequirement] = field(default_factory=list)
    parent_id: Optional[str] = None
    approved: bool = False

    def add_equipment_req(self, unit_class: str,
                          **kw) -> "Recipe":
        self.equipment_req.append(
            EquipmentRequirement(unit_class=unit_class, **kw))
        return self

    def derive(self, new_id: str, new_level: RecipeLevel,
               **overrides) -> "Recipe":
        """Derive a lower-level recipe from this one."""
        return Recipe(
            id=new_id,
            name=overrides.get("name", self.name),
            version=overrides.get("version", self.version),
            level=new_level,
            product=self.product,
            procedure_id=overrides.get("procedure_id", self.procedure_id),
            formula=overrides.get("formula", self.formula),
            equipment_req=overrides.get("equipment_req", list(self.equipment_req)),
            parent_id=self.id,
            approved=False,
        )

    def describe(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "level": self.level.value,
            "product": self.product,
            "formula": self.formula.describe(),
            "equipment_req": len(self.equipment_req),
            "approved": self.approved,
        }

    def __repr__(self):
        return (f"Recipe({self.id}, {self.name}, "
                f"level={self.level.value}, v{self.version})")
