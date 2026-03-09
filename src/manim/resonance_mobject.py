"""Resonance structure pair with double-headed arrow."""

from __future__ import annotations

from manim import (
    VGroup,
    Text,
    WHITE,
    LEFT,
    RIGHT,
    DOWN,
    np,
)

from src.manim.molecule_mobject import MoleculeMobject
from src.chemistry.molecules import MolGeom


class ResonancePair(VGroup):
    """Two resonance structures side by side with a double-headed arrow.

    Optionally shows formal charges and a resonance hybrid below.
    """

    def __init__(
        self,
        geom_a: MolGeom,
        geom_b: MolGeom,
        atom_colors: dict | None = None,
        label_a: str = "",
        label_b: str = "",
        charges_a: dict[str, str] | None = None,
        charges_b: dict[str, str] | None = None,
        separation: float = 5.0,
    ) -> None:
        super().__init__()

        # Left structure
        self.mol_a = MoleculeMobject(
            geom_a,
            atom_colors=atom_colors,
            scale_factor=0.9,
        )
        self.mol_a.shift(LEFT * separation / 2)
        self.add(self.mol_a)

        # Right structure
        self.mol_b = MoleculeMobject(
            geom_b,
            atom_colors=atom_colors,
            scale_factor=0.9,
        )
        self.mol_b.shift(RIGHT * separation / 2)
        self.add(self.mol_b)

        # Double-headed resonance arrow
        self.arrow = Text("\u27f7", font_size=36, color=WHITE)
        self.arrow.move_to((self.mol_a.get_right() + self.mol_b.get_left()) / 2)
        self.add(self.arrow)

        # Labels
        if label_a:
            la = Text(label_a, font_size=18, color=WHITE)
            la.next_to(self.mol_a, DOWN, buff=0.3)
            self.add(la)
        if label_b:
            lb = Text(label_b, font_size=18, color=WHITE)
            lb.next_to(self.mol_b, DOWN, buff=0.3)
            self.add(lb)

        # Formal charges
        if charges_a:
            self._add_charges(self.mol_a, charges_a)
        if charges_b:
            self._add_charges(self.mol_b, charges_b)

    @staticmethod
    def _add_charges(mol: MoleculeMobject, charges: dict[str, str]) -> None:
        for atom_label, charge_str in charges.items():
            if atom_label in mol.atom_mobjects:
                atom = mol.atom_mobjects[atom_label]
                charge_tex = Text(charge_str, font_size=18, color=WHITE)
                charge_tex.next_to(atom, RIGHT + np.array([0, 0.15, 0]), buff=0.05)
                mol.add(charge_tex)
