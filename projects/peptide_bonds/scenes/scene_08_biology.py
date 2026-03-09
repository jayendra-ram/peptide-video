"""Scene 8: biological context.

ATP activation equation, ribosome schematic, and rate comparison.
"""

from __future__ import annotations

from manim import (
    DOWN,
    DashedLine,
    FadeIn,
    FadeOut,
    LEFT,
    RIGHT,
    RoundedRectangle,
    Text,
    UP,
    VGroup,
    WHITE,
    Write,
    np,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equation_helpers import atp_activation_equation


class BiologyScene(ExplainerSceneBase):
    """11-second scene: ATP activation, ribosome diagram, and rate comparison."""

    def construct(self) -> None:
        # ── Step 1: Write title (0.8s) ─────────────────────────────────────
        title = Text(
            "Biological Context",
            font_size=42,
            color=WHITE,
            weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Step 2: Write ATP activation equation (1.5s) ───────────────────
        atp_eq = atp_activation_equation(font_size=24)
        atp_eq.next_to(title, DOWN, buff=0.5)
        self.play(Write(atp_eq), run_time=1.5)

        # ── Step 3: Draw ribosome diagram (2s) ─────────────────────────────
        ribosome = VGroup()

        # Large subunit (60S)
        large_sub = RoundedRectangle(
            corner_radius=0.3,
            width=3.2,
            height=1.6,
            fill_color="#2c3e50",
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2,
        )
        large_label = Text("Large subunit (60S)", font_size=14, color=WHITE)
        large_label.move_to(large_sub.get_center())

        # Small subunit (40S)
        small_sub = RoundedRectangle(
            corner_radius=0.25,
            width=3.2,
            height=1.0,
            fill_color="#34495e",
            fill_opacity=0.8,
            stroke_color=WHITE,
            stroke_width=2,
        )
        small_sub.next_to(large_sub, DOWN, buff=0.08)
        small_label = Text("Small subunit (40S)", font_size=14, color=WHITE)
        small_label.move_to(small_sub.get_center())

        # A-site and P-site labels
        a_site_label = Text("A-site", font_size=16, color=self.CHARGE_POS, weight="BOLD")
        a_site_label.move_to(large_sub.get_center() + np.array([0.7, 0.35, 0]))

        p_site_label = Text("P-site", font_size=16, color=self.ORBITAL_DONOR, weight="BOLD")
        p_site_label.move_to(large_sub.get_center() + np.array([-0.7, 0.35, 0]))

        # Dashed divider between sites
        divider = DashedLine(
            large_sub.get_top(),
            small_sub.get_bottom(),
            color=WHITE,
            stroke_width=1.5,
            dash_length=0.08,
        )

        ribosome.add(large_sub, large_label, small_sub, small_label,
                      a_site_label, p_site_label, divider)
        ribosome.move_to(DOWN * 0.8)

        self.play(FadeIn(ribosome), run_time=2.0)

        # ── Step 4: Write rate comparison texts (1.5s each) ────────────────
        rate_uncat = Text(
            "Uncatalyzed: t\u00bd ~ years",
            font_size=22,
            color=WHITE,
        )
        rate_uncat.next_to(ribosome, RIGHT, buff=0.6).shift(UP * 0.3)

        self.play(Write(rate_uncat), run_time=1.5)

        rate_ribo = Text(
            "Ribosome: ~20 peptide bonds/sec",
            font_size=22,
            color=self.ENERGY_COLOR,
        )
        rate_ribo.next_to(rate_uncat, DOWN, buff=0.3)

        self.play(Write(rate_ribo), run_time=1.5)

        # ── Step 5: Wait remaining ─────────────────────────────────────────
        # Total so far: 0.8 + 1.5 + 2.0 + 1.5 + 1.5 = 7.3s
        # Need 11s total minus 1s fadeout = 2.7s remaining
        self.wait(2.7)

        # ── Step 6: FadeOut (1s) ───────────────────────────────────────────
        self.play(
            FadeOut(title),
            FadeOut(atp_eq),
            FadeOut(ribosome),
            FadeOut(rate_uncat),
            FadeOut(rate_ribo),
            run_time=1.0,
        )
