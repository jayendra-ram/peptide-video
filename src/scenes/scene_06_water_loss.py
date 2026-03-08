"""Scene 6: proton transfer and water loss.

Starts from tetrahedral intermediate. Proton relay, water departure, and
remaining atoms settle to amide product with chemical equation.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    PI,
    RIGHT,
    ReplacementTransform,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    np,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_06_water_loss"

from src.manim.scene_base import PeptideSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from src.manim.arrow_mobject import CurlyArrow
from src.manim.equation_helpers import water_departure_equation
from src.chemistry.molecules import (
    AMIDE_PRODUCT,
    TETRAHEDRAL_TS,
)


class WaterLossScene(PeptideSceneBase):
    """10-second scene: proton transfer, water departure, amide formation."""

    def construct(self) -> None:
        # ── Build tetrahedral intermediate ────────────────────────────────
        ts_mol = MoleculeMobject(
            TETRAHEDRAL_TS,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            show_bonds=True,
            scale_factor=1.0,
            offset=(0, 0, 0),
            label_font_size=18,
        )

        # ── Step 1: FadeIn tetrahedral intermediate (1s) ──────────────────
        self.play(FadeIn(ts_mol), run_time=1.0)

        # ── Step 2: Write title (0.8s) ────────────────────────────────────
        title = Text(
            "Proton Transfer & Water Loss",
            font_size=34,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Step 3: CurlyArrow for proton relay H on N2 -> O (1s) ────────
        # The proton H_N2b transfers from N2 toward OH1 (the departing hydroxyl)
        h_n2b_center = ts_mol.get_atom_center("H_N2b")
        oh1_center = ts_mol.get_atom_center("OH1")

        proton_arrow = CurlyArrow(
            start=h_n2b_center,
            end=oh1_center,
            color=self.ORBITAL_DONOR,
            angle=PI / 4,
            stroke_width=3,
            tip_length=0.10,
        )
        self.play(FadeIn(proton_arrow), run_time=1.0)

        # ── Step 4: Animate water atoms departing (1.5s) ──────────────────
        # Water atoms: OH1, H_OH, and the transferred H_N2b
        water_labels = ["OH1", "H_OH", "H_N2b"]
        water_atoms = VGroup()
        for label in water_labels:
            if label in ts_mol.atom_mobjects:
                water_atoms.add(ts_mol.atom_mobjects[label])
            if label in ts_mol.label_mobjects:
                water_atoms.add(ts_mol.label_mobjects[label])

        # Also collect bonds involving water atoms to fade them
        water_bonds = VGroup()
        for (label_a, label_b), bond_group in ts_mol.bond_mobjects.items():
            if label_a in water_labels or label_b in water_labels:
                water_bonds.add(bond_group)

        departure_target = UP * 2.0 + RIGHT * 3.0

        self.play(
            water_atoms.animate.shift(departure_target),
            water_bonds.animate.shift(departure_target).set_opacity(0),
            FadeOut(proton_arrow),
            run_time=1.5,
        )

        # ── Step 5: Write H2O label next to departing water (0.5s) ────────
        water_label = Text(
            "H\u2082O",
            font_size=28,
            color=self.ATOM_COLORS["O"],
        )
        water_label.move_to(water_atoms.get_center())
        self.play(
            FadeOut(water_atoms),
            FadeIn(water_label),
            run_time=0.5,
        )

        # ── Step 6: Transform remaining to amide product (1.5s) ──────────
        product_mol = MoleculeMobject(
            AMIDE_PRODUCT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            show_bonds=True,
            scale_factor=1.0,
            offset=(0, 0, 0),
            label_font_size=18,
        )

        # Collect remaining (non-water) parts of the TS molecule
        remaining = VGroup()
        for label, circle in ts_mol.atom_mobjects.items():
            if label not in water_labels:
                remaining.add(circle)
        for label, txt in ts_mol.label_mobjects.items():
            if label not in water_labels:
                remaining.add(txt)
        for (label_a, label_b), bond_group in ts_mol.bond_mobjects.items():
            if label_a not in water_labels and label_b not in water_labels:
                remaining.add(bond_group)

        self.play(
            ReplacementTransform(remaining, product_mol),
            run_time=1.5,
        )

        # ── Step 7: Write water departure equation at bottom (1s) ─────────
        eq = water_departure_equation(font_size=24, color=WHITE)
        eq.to_edge(DOWN, buff=0.5)
        self.play(Write(eq), run_time=1.0)

        # ── Step 8: Wait remaining ───────────────────────────────────────
        # Total so far: 1.0 + 0.8 + 1.0 + 1.5 + 0.5 + 1.5 + 1.0 = 7.3s
        # Need 10s total, minus 1s for fade out = 1.7s remaining
        self.wait(1.7)

        # ── Step 9: FadeOut (1s) ──────────────────────────────────────────
        self.play(
            FadeOut(title),
            FadeOut(product_mol),
            FadeOut(water_label),
            FadeOut(eq),
            run_time=1.0,
        )
