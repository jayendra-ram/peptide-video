"""Scene 9: summary montage.

Three molecular states side by side (reactants, TS, product) with reaction arrows,
animated bullet points, and a final balanced equation.
"""

from __future__ import annotations

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    np,
)

from src.manim.scene_base import ExplainerSceneBase
from src.manim.molecule_mobject import MoleculeMobject
from data.molecules import (
    AMIDE_PRODUCT,
    GLYCINE_A_REACTANT,
    TETRAHEDRAL_TS,
)


class SummaryScene(ExplainerSceneBase):
    """12-second summary: three states, bullet points, and final equation."""

    def construct(self) -> None:
        # ── Step 1: FadeIn three molecules with labels (2s) ────────────────
        configs = [
            (GLYCINE_A_REACTANT, (-4.5, 0, 0), "Reactants"),
            (TETRAHEDRAL_TS, (0, 0, 0), "Transition State"),
            (AMIDE_PRODUCT, (4.5, 0, 0), "Peptide Bond"),
        ]

        molecules = VGroup()
        labels = VGroup()
        for geom, offset, label_text in configs:
            mol = MoleculeMobject(
                geom,
                atom_colors=self.ATOM_COLORS,
                atom_radii=self.ATOM_RADII,
                show_labels=True,
                scale_factor=0.7,
                offset=offset,
                label_font_size=14,
            )
            molecules.add(mol)

            label = Text(
                label_text,
                font_size=18,
                color=WHITE,
            ).next_to(mol, DOWN, buff=0.3)
            labels.add(label)

        mol_group = VGroup(molecules, labels)
        mol_group.shift(DOWN * 0.3)

        self.play(FadeIn(mol_group), run_time=2.0)

        # ── Step 2: Write arrows between molecules (1s) ────────────────────
        # Arrow 1: between reactants and TS
        arrow1 = Text(
            "\u2192 attack",
            font_size=24,
            color=WHITE,
        )
        mol_left = molecules[0]
        mol_center = molecules[1]
        arrow1.move_to(
            (mol_left.get_right() + mol_center.get_left()) / 2
        )

        # Arrow 2: between TS and product
        arrow2 = Text(
            "\u2192 \u2212H\u2082O",
            font_size=24,
            color=WHITE,
        )
        mol_right = molecules[2]
        arrow2.move_to(
            (mol_center.get_right() + mol_right.get_left()) / 2
        )

        self.play(Write(arrow1), Write(arrow2), run_time=1.0)

        # ── Step 3: Sequentially write 3 bullet points (1.5s each) ─────────
        bullets_data = [
            "\u2022 HOMO/LUMO overlap drives nucleophilic attack",
            "\u2022 \u0394G\u2021 requires catalysis (ribosome)",
            "\u2022 Amide resonance \u2192 planar backbone",
        ]

        bullet_mobjects = []
        for i, text in enumerate(bullets_data):
            bullet = Text(text, font_size=22, color=WHITE)

            if i == 0:
                bullet.to_edge(UP, buff=0.4).shift(LEFT * 0.5)
            else:
                bullet.next_to(bullet_mobjects[i - 1], DOWN, buff=0.2, aligned_edge=LEFT)

            bullet_mobjects.append(bullet)
            self.play(Write(bullet), run_time=1.5)

        # ── Step 4: Write final equation (1.5s) ───────────────────────────
        final_eq = Text(
            "2 Gly \u2192 Gly-Gly + H\u2082O,  \u0394G\u00b0 \u2248 +10 kJ/mol",
            font_size=26,
            color=self.ENERGY_COLOR,
        )
        final_eq.to_edge(DOWN, buff=0.5)

        self.play(Write(final_eq), run_time=1.5)

        # ── Step 5: Wait remaining ─────────────────────────────────────────
        # Total so far: 2.0 + 1.0 + 3*1.5 + 1.5 = 9.0s
        # Need 12s total minus 1s fadeout = 2.0s remaining
        self.wait(2.0)

        # ── Step 6: FadeOut (1s) ───────────────────────────────────────────
        all_objects = VGroup(
            mol_group, arrow1, arrow2, final_eq,
            *bullet_mobjects,
        )
        self.play(FadeOut(all_objects), run_time=1.0)
