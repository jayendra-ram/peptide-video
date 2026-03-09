"""Scene 5: nucleophilic attack.

Reactant molecules morph toward tetrahedral intermediate with curly arrows
showing electron flow and bond order annotations.
"""

from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    PI,
    ReplacementTransform,
    RIGHT,
    Text,
    UP,
    WHITE,
    Write,
    np,
)

from src.manim.scene_base import ExplainerSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from src.manim.arrow_mobject import CurlyArrow
from src.manim.equation_helpers import bond_order_annotation
from data.molecules import (
    GLYCINE_A_REACTANT,
    GLYCINE_B_REACTANT,
    TETRAHEDRAL_TS,
)


class AttackScene(ExplainerSceneBase):
    """12-second scene: nucleophilic attack with electron-flow arrows."""

    def construct(self) -> None:
        # ── Build reactant molecules ──────────────────────────────────────
        mol_a = MoleculeMobject(
            GLYCINE_A_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            show_bonds=True,
            scale_factor=1.0,
            offset=(-0.5, 0, 0),
            label_font_size=18,
        )

        mol_b = MoleculeMobject(
            GLYCINE_B_REACTANT,
            atom_colors=self.ATOM_COLORS,
            atom_radii=self.ATOM_RADII,
            show_labels=True,
            show_bonds=True,
            scale_factor=1.0,
            offset=(0, 0, 0),
            label_font_size=18,
        )

        # ── Step 1: FadeIn reactant molecules (1s) ────────────────────────
        self.play(FadeIn(mol_a), FadeIn(mol_b), run_time=1.0)

        # ── Step 2: Write title (0.8s) ────────────────────────────────────
        title = Text(
            "Nucleophilic Attack",
            font_size=36,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Step 3: CurlyArrow N2 -> C1 (nucleophilic attack) (1.5s) ─────
        n2_center = mol_b.get_atom_center("N2")
        c1_center = mol_a.get_atom_center("C1")

        arrow_nc = CurlyArrow(
            start=n2_center,
            end=c1_center,
            color=self.ORBITAL_DONOR,
            angle=PI / 3,
            stroke_width=3,
            tip_length=0.12,
        )
        self.play(FadeIn(arrow_nc), run_time=1.5)

        # ── Step 4: CurlyArrow C=O -> O (pi electrons to oxygen) (1s) ────
        o1_center = mol_a.get_atom_center("O1")
        # Arrow from C=O bond midpoint toward O1
        co_midpoint = (c1_center + o1_center) / 2
        arrow_co = CurlyArrow(
            start=co_midpoint,
            end=o1_center,
            color=self.ORBITAL_ACCEPTOR,
            angle=-PI / 4,
            stroke_width=3,
            tip_length=0.10,
        )
        self.play(FadeIn(arrow_co), run_time=1.0)

        # ── Step 5: Bond order annotations (1.5s) ────────────────────────
        bo_cn = bond_order_annotation("C-N", r"0 \rightarrow 0.6", font_size=22, color=WHITE)
        bo_co = bond_order_annotation("C=O", r"2.0 \rightarrow 1.0", font_size=22, color=WHITE)

        # Position near the forming bonds
        cn_midpoint = (c1_center + n2_center) / 2
        bo_cn.next_to(cn_midpoint, DOWN, buff=0.4)
        bo_co.next_to(co_midpoint, UP + LEFT, buff=0.3)

        self.play(Write(bo_cn), Write(bo_co), run_time=1.5)

        # ── Step 6: Transform to tetrahedral intermediate (2s) ────────────
        # Fade out arrows and annotations before morphing
        self.play(
            FadeOut(arrow_nc),
            FadeOut(arrow_co),
            FadeOut(bo_cn),
            FadeOut(bo_co),
            run_time=0.5,
        )

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

        from manim import VGroup
        reactants = VGroup(mol_a, mol_b)
        self.play(ReplacementTransform(reactants, ts_mol), run_time=2.0)

        # ── Step 7: Write "Tetrahedral Intermediate" label (1s) ──────────
        ts_label = Text(
            "Tetrahedral Intermediate",
            font_size=28,
            color=WHITE,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(ts_label), run_time=1.0)

        # ── Step 8: Wait remaining ───────────────────────────────────────
        # Total so far: 1.0 + 0.8 + 1.5 + 1.0 + 1.5 + 0.5 + 2.0 + 1.0 = 9.3s
        # Need 12s total, minus 1s for fade out = 1.7s remaining
        self.wait(1.7)

        # ── Step 9: FadeOut (1s) ──────────────────────────────────────────
        self.play(
            FadeOut(title),
            FadeOut(ts_mol),
            FadeOut(ts_label),
            run_time=1.0,
        )
