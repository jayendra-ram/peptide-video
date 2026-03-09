"""Scene 3: donor/acceptor orbital logic.

N lone pair (purple donor) and C=O pi* (orange acceptor) lobes with energy diagram.
"""

from __future__ import annotations

from manim import (
    Create,
    DashedLine,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Write,
    np,
)

from src.manim.scene_base import ExplainerSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from src.manim.orbital_mobject import OrbitalLobe, EnergyLevelDiagram
from src.manim.equation_helpers import fmo_label
from data.molecules import GLYCINE_A_REACTANT, GLYCINE_B_REACTANT


class OrbitalsScene(ExplainerSceneBase):
    """13-second scene: orbital lobes on molecules + energy level diagram."""

    def construct(self) -> None:
        # ── Draw molecules on the left side ──────────────────────────────
        mol_a = MoleculeMobject(
            GLYCINE_A_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            scale_factor=0.9,
            offset=(-3.5, 0, 0),
            label_font_size=16,
        )

        mol_b = MoleculeMobject(
            GLYCINE_B_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            scale_factor=0.9,
            offset=(-2.5, 0, 0),
            label_font_size=16,
        )

        # ── Energy level diagram on the right side ───────────────────────
        energy_diagram = EnergyLevelDiagram(
            levels=[
                ("N lone pair (HOMO)", -9.5, str(self.ORBITAL_DONOR), 2),
                (r"C=O $\pi^*$ (LUMO)", -1.0, str(self.ORBITAL_ACCEPTOR), 0),
            ],
            width=2.2,
            height=2.5,
            show_arrow=True,
        ).shift(RIGHT * 3.5)

        # Separate HOMO and LUMO lines for staged animation
        # We'll animate the whole diagram in parts using the level_lines dict
        homo_level_name = "N lone pair (HOMO)"
        lumo_level_name = r"C=O $\pi^*$ (LUMO)"

        # ── Step 1: FadeIn molecules on left (1s) ────────────────────────
        self.play(FadeIn(mol_a), FadeIn(mol_b), run_time=1.0)

        # ── Step 2: GrowFromCenter purple lobe + Write HOMO level (2s) ───
        # Purple OrbitalLobe on N2 (nitrogen lone pair, HOMO)
        n2_center = mol_b.get_atom_center("N2")
        homo_lobe = OrbitalLobe(
            center=n2_center,
            width=0.6,
            height=0.9,
            color=self.ORBITAL_DONOR,
            opacity=0.35,
            label="HOMO",
        )

        # Build HOMO part of energy diagram
        # We animate the full diagram but show it growing alongside the lobe
        # First, create just the HOMO portion (we'll add LUMO separately)
        homo_diagram = EnergyLevelDiagram(
            levels=[
                ("N lone pair (HOMO)", -9.5, str(self.ORBITAL_DONOR), 2),
            ],
            width=2.2,
            height=2.5,
            show_arrow=False,
        ).shift(RIGHT * 3.5 + DOWN * 0.5)

        self.play(
            GrowFromCenter(homo_lobe),
            Write(homo_diagram),
            run_time=2.0,
        )

        # ── Step 3: GrowFromCenter orange lobe + Write LUMO level (2s) ──
        # Orange OrbitalLobe on C=O midpoint (pi*, LUMO)
        c1_center = mol_a.get_atom_center("C1")
        o1_center = mol_a.get_atom_center("O1")
        co_midpoint = (c1_center + o1_center) / 2

        lumo_lobe = OrbitalLobe(
            center=co_midpoint,
            width=0.5,
            height=0.7,
            color=self.ORBITAL_ACCEPTOR,
            opacity=0.35,
            label="LUMO",
        )

        lumo_diagram = EnergyLevelDiagram(
            levels=[
                (r"C=O $\pi^*$ (LUMO)", -1.0, str(self.ORBITAL_ACCEPTOR), 0),
            ],
            width=2.2,
            height=2.5,
            show_arrow=False,
        ).shift(RIGHT * 3.5 + UP * 0.5)

        self.play(
            GrowFromCenter(lumo_lobe),
            Write(lumo_diagram),
            run_time=2.0,
        )

        # ── Step 4: Dashed arrow between lobes showing overlap (1.5s) ───
        # Arrow from HOMO lobe (N2) toward LUMO lobe (C=O midpoint)
        overlap_arrow = DashedLine(
            start=n2_center,
            end=co_midpoint,
            color=self.ENERGY_COLOR,
            stroke_width=3,
            dash_length=0.1,
        )
        # Add a small arrow tip by extending slightly
        from manim import Arrow
        overlap_tip = Arrow(
            start=n2_center,
            end=co_midpoint,
            color=self.ENERGY_COLOR,
            stroke_width=2,
            buff=0.0,
            max_tip_length_to_length_ratio=0.15,
        ).set_opacity(0)
        # Use dashed line for the body, show the direction
        overlap_tip.tip.set_opacity(1)

        self.play(
            Create(overlap_arrow),
            FadeIn(overlap_tip.tip),
            run_time=1.5,
        )

        # ── Step 5: Write FMO theory label at bottom (1.5s) ──────────────
        fmo_text = fmo_label(font_size=24)
        fmo_text.to_edge(DOWN, buff=0.5)

        self.play(Write(fmo_text), run_time=1.5)

        # ── Step 6: Wait remaining time ──────────────────────────────────
        # Total so far: 1.0 + 2.0 + 2.0 + 1.5 + 1.5 = 8.0s
        # Need 13s total, minus 1s for fade out = 4.0s remaining
        self.wait(4.0)

        # ── Step 7: FadeOut everything (1s) ──────────────────────────────
        self.play(
            FadeOut(mol_a),
            FadeOut(mol_b),
            FadeOut(homo_lobe),
            FadeOut(lumo_lobe),
            FadeOut(homo_diagram),
            FadeOut(lumo_diagram),
            FadeOut(overlap_arrow),
            FadeOut(overlap_tip.tip),
            FadeOut(fmo_text),
            run_time=1.0,
        )
