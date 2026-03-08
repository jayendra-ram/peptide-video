"""Scene 7: amide resonance and planarity.

Two resonance canonical forms side by side, a resonance hybrid below,
and annotations showing partial double-bond character and restricted rotation.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    Circle,
    Cross,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    RIGHT,
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

SCENE_ID = "scene_07_resonance"

from src.manim.scene_base import PeptideSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from src.manim.resonance_mobject import ResonancePair
from src.chemistry.molecules import AMIDE_PRODUCT, MolGeom


def _make_resonance_b() -> MolGeom:
    """Create resonance structure B: C-O single bond, C=N double bond."""
    modified_bonds = []
    for label_a, label_b, order in AMIDE_PRODUCT.bonds:
        if label_a == "C1" and label_b == "O1":
            modified_bonds.append((label_a, label_b, 1.0))
        elif label_a == "C1" and label_b == "N2":
            modified_bonds.append((label_a, label_b, 2.0))
        else:
            modified_bonds.append((label_a, label_b, order))
    return MolGeom(atoms=list(AMIDE_PRODUCT.atoms), bonds=modified_bonds)


class ResonanceScene(PeptideSceneBase):
    """11-second scene: resonance structures, hybrid, and planarity annotations."""

    def construct(self) -> None:
        # Prepare resonance structures
        resonance_a = AMIDE_PRODUCT  # C=O (1.5), C-N (1.4) canonical form
        resonance_b = _make_resonance_b()  # C-O (1.0), C=N (2.0) canonical form

        # ── Step 1: Write title (0.8s) ─────────────────────────────────────
        title = Text(
            "Amide Resonance",
            font_size=42,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Step 2: FadeIn resonance structure A (left) (1s) ───────────────
        resonance_pair = ResonancePair(
            geom_a=resonance_a,
            geom_b=resonance_b,
            atom_colors=self.ATOM_COLORS,
            label_a="C=O, C\u2013N",
            label_b="C\u2013O\u207b, C=N\u207a",
            charges_b={"N2": "+", "O1": "-"},
            separation=5.5,
        )
        resonance_pair.shift(UP * 0.5)

        # Animate left structure first
        self.play(FadeIn(resonance_pair.mol_a), run_time=1.0)

        # ── Step 3: Write double-headed arrow (0.5s) ───────────────────────
        self.play(Write(resonance_pair.arrow), run_time=0.5)

        # ── Step 4: FadeIn structure B with formal charges (1s) ────────────
        # Gather everything in the pair except mol_a and arrow
        structure_b_parts = VGroup()
        for sub in resonance_pair.submobjects:
            if sub is not resonance_pair.mol_a and sub is not resonance_pair.arrow:
                structure_b_parts.add(sub)
        self.play(FadeIn(structure_b_parts), run_time=1.0)

        # ── Step 5: FadeIn hybrid structure below with annotation (2s) ─────
        hybrid = MoleculeMobject(
            AMIDE_PRODUCT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            scale_factor=0.85,
            label_font_size=16,
        )
        hybrid.shift(DOWN * 2.2)

        hybrid_label = Text(
            "Resonance Hybrid",
            font_size=22,
            color=WHITE,
        ).next_to(hybrid, DOWN, buff=0.25)

        self.play(
            FadeIn(hybrid),
            FadeIn(hybrid_label),
            run_time=2.0,
        )

        # ── Step 6: Write bond order and planarity annotations (1.5s) ──────
        bond_order_text = Text(
            "Bond order C\u2013N \u2248 1.3\u20131.4 (partial double bond)",
            font_size=20,
            color=WHITE,
        ).next_to(hybrid_label, DOWN, buff=0.3)

        planarity_text = Text(
            "Restricted rotation \u2192 planar backbone",
            font_size=20,
            color=WHITE,
        ).next_to(bond_order_text, DOWN, buff=0.2)

        # Crossed-out rotation symbol on the C-N bond area
        no_rotation = VGroup()
        cross_circle = Circle(
            radius=0.22,
            color=self.CHARGE_NEG,
            stroke_width=2.5,
        )
        cross_line = Line(
            cross_circle.get_corner(UP + LEFT) * 0.7 + cross_circle.get_center() * 0.3,
            cross_circle.get_corner(DOWN + RIGHT) * 0.7 + cross_circle.get_center() * 0.3,
            color=self.CHARGE_NEG,
            stroke_width=2.5,
        )
        no_rotation.add(cross_circle, cross_line)
        no_rot_label = Text("\u2717 rotation", font_size=16, color=self.CHARGE_NEG)
        no_rotation.add(no_rot_label)
        no_rot_label.next_to(cross_circle, RIGHT, buff=0.1)
        no_rotation.next_to(planarity_text, RIGHT, buff=0.4)

        self.play(
            Write(bond_order_text),
            Write(planarity_text),
            FadeIn(no_rotation),
            run_time=1.5,
        )

        # ── Step 7: Wait remaining ─────────────────────────────────────────
        # Total so far: 0.8 + 1.0 + 0.5 + 1.0 + 2.0 + 1.5 = 6.8s
        # Need 11s total minus 1s fadeout = 3.2s remaining
        self.wait(3.2)

        # ── Step 8: FadeOut (1s) ───────────────────────────────────────────
        self.play(
            FadeOut(title),
            FadeOut(resonance_pair),
            FadeOut(hybrid),
            FadeOut(hybrid_label),
            FadeOut(bond_order_text),
            FadeOut(planarity_text),
            FadeOut(no_rotation),
            run_time=1.0,
        )
