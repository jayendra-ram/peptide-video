"""Scene 8: Cosmological redshift.

Expanding space, galaxy moving away, redshift z formula.
"""

from __future__ import annotations

from manim import (
    Create,
    DOWN,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    ManimColor,
    RIGHT,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import redshift_z


class CosmologicalScene(ExplainerSceneBase):
    """11-second scene: expanding universe + redshift z."""

    def construct(self) -> None:
        # ── Title ─────────────────────────────────────────────────────
        title = Text(
            "Cosmological Redshift",
            font_size=36, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Stylized galaxy ───────────────────────────────────────────
        galaxy = Ellipse(
            width=1.5, height=0.6,
            fill_color=ManimColor("#9b59b6"),
            fill_opacity=0.6,
            stroke_color=ManimColor("#bb8fce"),
            stroke_width=2,
        ).move_to(LEFT * 4 + UP * 1.0)

        # Galaxy glow (larger, dim ellipse behind)
        glow = Ellipse(
            width=2.2, height=1.0,
            fill_color=ManimColor("#9b59b6"),
            fill_opacity=0.15,
            stroke_width=0,
        ).move_to(galaxy.get_center())

        galaxy_label = Text(
            "Distant Galaxy", font_size=18, color=ManimColor("#bb8fce"),
        ).next_to(galaxy, UP, buff=0.2)

        self.play(FadeIn(glow), FadeIn(galaxy), FadeIn(galaxy_label), run_time=1.0)

        # ── Trailing wavefronts shifting from blue to red ─────────────
        wave_colors = ["#3498db", "#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"]
        waves = VGroup()
        for i, color in enumerate(wave_colors):
            # Vertical sine-ish wave segments represented as lines
            x_pos = galaxy.get_center()[0] + 1.5 + i * 1.4
            wave_line = Line(
                start=[x_pos, 0.5, 0],
                end=[x_pos, 1.5, 0],
                stroke_color=ManimColor(color),
                stroke_width=3,
                stroke_opacity=0.7,
            )
            waves.add(wave_line)

        stretch_label = Text(
            "Wavelengths stretch as space expands →",
            font_size=18, color=ManimColor("#e74c3c"),
        ).move_to(UP * 2.2)

        self.play(FadeIn(waves), FadeIn(stretch_label), run_time=1.5)

        # ── Galaxy moves rightward (space expanding) ──────────────────
        self.play(
            galaxy.animate.shift(RIGHT * 2),
            glow.animate.shift(RIGHT * 2),
            galaxy_label.animate.shift(RIGHT * 2),
            *[waves[i].animate.shift(RIGHT * (0.3 * (i + 1))) for i in range(len(wave_colors))],
            run_time=2.0,
        )

        # ── Redshift z formula ────────────────────────────────────────
        z_eq = redshift_z().scale(0.85)
        z_eq.move_to(DOWN * 1.5)
        box = SurroundingRectangle(
            z_eq, color=ManimColor("#f1c40f"),
            buff=0.2, stroke_width=2,
        )

        self.play(Write(z_eq), run_time=1.5)
        self.play(Create(box), run_time=0.5)

        # ── Expanding dots (galaxy clusters) ──────────────────────────
        clusters = VGroup()
        import numpy as np
        np.random.seed(42)
        for _ in range(8):
            dot = Dot(
                color=ManimColor("#ecf0f1"), radius=0.05,
            ).move_to([
                np.random.uniform(-3, 3),
                np.random.uniform(-2.5, -0.5),
                0,
            ])
            clusters.add(dot)

        self.play(FadeIn(clusters), run_time=0.5)

        # Dots move apart
        self.play(
            *[d.animate.shift(
                (d.get_center() - DOWN * 1.5) * 0.3
            ) for d in clusters],
            run_time=1.5,
        )

        self.wait(0.2)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
