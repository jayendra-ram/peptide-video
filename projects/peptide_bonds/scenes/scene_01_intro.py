"""Scene 1: establish the peptide bond question.

Protein backbone as 4 repeating amide units, camera zooms to isolate one bond.
"""

from __future__ import annotations

from manim import (
    Circle,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Text,
    UP,
    WHITE,
    Write,
    YELLOW,
    np,
)

from src.manim.scene_base import ExplainerSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from data.molecules import AMIDE_PRODUCT


class IntroScene(ExplainerSceneBase):
    """12-second intro: 4 repeating amide backbone units, zoom to central C-N bond."""

    def construct(self) -> None:
        # ── Draw 4 repeating amide backbone units ────────────────────────
        chain = []
        for i in range(4):
            offset = (i * 2.8 - 4.2, 0, 0)
            mol = MoleculeMobject(
                AMIDE_PRODUCT,
                atom_colors=self.ATOM_COLORS,
                atom_radii=self.ATOM_RADII,
                show_labels=True,
                scale_factor=0.85,
                offset=offset,
                label_font_size=14,
            )
            chain.append(mol)

        chain_group = chain[0]
        for m in chain[1:]:
            chain_group = chain_group.copy().add(*m.submobjects)
        # Use a fresh VGroup for clean handling
        from manim import VGroup
        backbone = VGroup(*[m for m in chain])

        # ── Step 1: FadeIn chain (1.5s) ──────────────────────────────────
        self.play(FadeIn(backbone), run_time=1.5)

        # ── Step 2: Write title (1s) ─────────────────────────────────────
        title = Text(
            "What IS a peptide bond?",
            font_size=42,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        # ── Step 3: Create highlight circle on central C1-N2 bond (0.8s) ─
        # Unit 1 (index 1): C1 and N2 are the amide bond atoms
        unit1 = chain[1]
        c1_center = unit1.get_atom_center("C1")
        n2_center = unit1.get_atom_center("N2")
        bond_midpoint = (c1_center + n2_center) / 2

        highlight = Circle(
            radius=0.45,
            color=YELLOW,
            stroke_width=4,
            fill_opacity=0.15,
            fill_color=YELLOW,
        ).move_to(bond_midpoint)

        self.play(GrowFromCenter(highlight), run_time=0.8)

        # ── Step 4: Camera zoom to the highlighted bond (2s) ─────────────
        self.play(
            self.camera.frame.animate.set(width=5).move_to(bond_midpoint),
            run_time=2.0,
        )

        # ── Step 5: FadeIn description + Write formula (1.5s) ────────────
        formula = Text(
            "--NH--C(=O)--",
            font_size=30,
            color=WHITE,
        ).next_to(bond_midpoint, DOWN, buff=0.6)

        description = Text(
            "Protein backbone: repeating -NH-CO- amide units",
            font_size=18,
            color=WHITE,
        ).next_to(formula, DOWN, buff=0.25)

        self.play(
            FadeIn(description),
            Write(formula),
            run_time=1.5,
        )

        # ── Step 6: Wait remaining time ──────────────────────────────────
        # Total so far: 1.5 + 1.0 + 0.8 + 2.0 + 1.5 = 6.8s
        # Need 12s total, minus 1s for fade out = 4.2s remaining
        self.wait(4.2)

        # ── Step 7: FadeOut title, formula, description (1s) ─────────────
        self.play(
            FadeOut(title),
            FadeOut(formula),
            FadeOut(description),
            FadeOut(highlight),
            run_time=1.0,
        )
