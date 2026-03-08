"""Scene 2: introduce amino acid reactants.

Two glycine molecules side by side with partial charges, curly arrow, and equation.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    Create,
    LEFT,
    MathTex,
    RIGHT,
    Text,
    UP,
    WHITE,
    Write,
    np,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_02_reactants"

from src.manim.scene_base import PeptideSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from src.manim.arrow_mobject import CurlyArrow
from src.manim.equation_helpers import peptide_formation_equation
from src.chemistry.molecules import GLYCINE_A_REACTANT, GLYCINE_B_REACTANT


class ReactantsScene(PeptideSceneBase):
    """13-second scene: two glycine reactants with charges, arrow, and equation."""

    def construct(self) -> None:
        # ── Draw two glycine molecules side by side ──────────────────────
        mol_a = MoleculeMobject(
            GLYCINE_A_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            scale_factor=1.0,
            offset=(-1.0, 0, 0),
            label_font_size=18,
        )

        mol_b = MoleculeMobject(
            GLYCINE_B_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            scale_factor=1.0,
            offset=(0, 0, 0),
            label_font_size=18,
        )

        # ── Step 1: FadeIn both molecules (1.5s) ────────────────────────
        self.play(FadeIn(mol_a), FadeIn(mol_b), run_time=1.5)

        # ── Step 2: Write labels for amine/carbonyl (1s) ────────────────
        # Label the amine group (nucleophile) near N2
        n2_center = mol_b.get_atom_center("N2")
        amine_label = Text(
            "Amine (nucleophile)",
            font_size=20,
            color=self.ORBITAL_DONOR,
            weight="BOLD",
        ).next_to(n2_center, UP, buff=0.5)

        # Label the carbonyl group (electrophile) near C1
        c1_center = mol_a.get_atom_center("C1")
        carbonyl_label = Text(
            "Carbonyl (electrophile)",
            font_size=20,
            color=self.ORBITAL_ACCEPTOR,
            weight="BOLD",
        ).next_to(c1_center, UP, buff=0.5)

        self.play(Write(amine_label), Write(carbonyl_label), run_time=1.0)

        # ── Step 3: Write partial charge annotations (1.5s) ──────────────
        # delta+ on C1 (electrophilic carbon)
        delta_plus_c1 = MathTex(
            r"\delta^+",
            font_size=28,
            color=self.CHARGE_POS,
        ).next_to(c1_center, DOWN, buff=0.15)

        # delta- on O1 (carbonyl oxygen)
        o1_center = mol_a.get_atom_center("O1")
        delta_minus_o1 = MathTex(
            r"\delta^-",
            font_size=28,
            color=self.CHARGE_NEG,
        ).next_to(o1_center, UP, buff=0.15)

        # delta- on N2 (nucleophilic nitrogen)
        delta_minus_n2 = MathTex(
            r"\delta^-",
            font_size=28,
            color=self.CHARGE_NEG,
        ).next_to(n2_center, DOWN, buff=0.15)

        self.play(
            Write(delta_plus_c1),
            Write(delta_minus_o1),
            Write(delta_minus_n2),
            run_time=1.5,
        )

        # ── Step 4: Create CurlyArrow N2 -> C1 (1.5s) ───────────────────
        arrow = CurlyArrow(
            start=n2_center,
            end=c1_center,
            color=self.ENERGY_COLOR,
            stroke_width=3.5,
            tip_length=0.14,
        )
        self.play(Create(arrow), run_time=1.5)

        # ── Step 5: Write balanced equation at bottom (1.5s) ─────────────
        equation = peptide_formation_equation(font_size=26)
        equation.to_edge(DOWN, buff=0.6)
        self.play(Write(equation), run_time=1.5)

        # ── Step 6: Wait remaining time ──────────────────────────────────
        # Total so far: 1.5 + 1.0 + 1.5 + 1.5 + 1.5 = 7.0s
        # Need 13s total, minus 1s for fade out = 5.0s remaining
        self.wait(5.0)

        # ── Step 7: FadeOut everything (1s) ──────────────────────────────
        self.play(
            FadeOut(mol_a),
            FadeOut(mol_b),
            FadeOut(amine_label),
            FadeOut(carbonyl_label),
            FadeOut(delta_plus_c1),
            FadeOut(delta_minus_o1),
            FadeOut(delta_minus_n2),
            FadeOut(arrow),
            FadeOut(equation),
            run_time=1.0,
        )
