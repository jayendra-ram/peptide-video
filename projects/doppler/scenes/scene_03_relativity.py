"""Scene 3: Enter relativity — speed of light postulate and beta.

Introduce the constant speed of light, define beta = v/c,
and show why classical Doppler breaks down as v -> c.
"""

from __future__ import annotations

from manim import (
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    ManimColor,
    Rectangle,
    RIGHT,
    Text,
    UP,
    VGroup,
    Write,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import beta_definition, classical_doppler_beta


class RelativityScene(ExplainerSceneBase):
    """12-second scene: speed of light postulate + beta gauge."""

    def construct(self) -> None:
        # ── Step 1: Speed of light postulate (3s) ─────────────────────
        postulate = Text(
            "The speed of light is constant\nfor all observers",
            font_size=34, color=ManimColor("#ecf0f1"),
            line_spacing=1.4,
        ).move_to(UP * 1.5)
        self.play(Write(postulate), run_time=2.0)
        self.wait(1.0)

        # ── Step 2: Introduce beta (3s) ───────────────────────────────
        self.play(postulate.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=0.5)

        beta_eq = beta_definition().scale(1.0)
        beta_eq.move_to(UP * 0.5)
        self.play(Write(beta_eq), run_time=1.0)

        # Manual beta gauge (avoiding NumberLine which needs LaTeX)
        gauge_left = LEFT * 4
        gauge_right = RIGHT * 4
        gauge_y = DOWN * 1.0
        gauge_line = Line(
            start=gauge_left + gauge_y,
            end=gauge_right + gauge_y,
            color=ManimColor("#7f8c8d"),
            stroke_width=2,
        )

        # Tick marks and labels
        gauge_labels = VGroup()
        for val in [0, 0.2, 0.4, 0.6, 0.8, 1.0]:
            x = gauge_left[0] + val * (gauge_right[0] - gauge_left[0])
            tick = Line(
                start=[x, gauge_y[1] - 0.1, 0],
                end=[x, gauge_y[1] + 0.1, 0],
                color=ManimColor("#7f8c8d"), stroke_width=2,
            )
            label = Text(
                f"{val:.1f}", font_size=18, color=ManimColor("#7f8c8d"),
            ).move_to([x, gauge_y[1] - 0.35, 0])
            gauge_labels.add(tick, label)

        beta_label = Text(
            "\u03b2", font_size=28, color=ManimColor("#3498db"),
        ).next_to(gauge_line, LEFT, buff=0.3)

        self.play(
            Create(gauge_line), FadeIn(gauge_labels), FadeIn(beta_label),
            run_time=1.5,
        )

        # ── Step 3: Highlight danger zone near beta=1 (3s) ────────────
        # Red zone from 0.8 to 1.0
        x_08 = gauge_left[0] + 0.8 * (gauge_right[0] - gauge_left[0])
        x_10 = gauge_right[0]
        danger_zone = Rectangle(
            width=x_10 - x_08,
            height=0.4,
            fill_color=ManimColor("#e74c3c"),
            fill_opacity=0.3,
            stroke_width=0,
        ).move_to([(x_08 + x_10) / 2, gauge_y[1], 0])

        danger_label = Text(
            "Classical breaks down",
            font_size=18, color=ManimColor("#e74c3c"),
        ).next_to(danger_zone, UP, buff=0.15)

        self.play(FadeIn(danger_zone), FadeIn(danger_label), run_time=1.0)

        # Show diverging classical formula
        classical = classical_doppler_beta().scale(0.8)
        classical.move_to(DOWN * 2.5)
        diverge_note = Text(
            "\u2192 \u221e  as  \u03b2 \u2192 1",
            font_size=22, color=ManimColor("#e74c3c"),
        ).next_to(classical, RIGHT, buff=0.3)

        self.play(Write(classical), FadeIn(diverge_note), run_time=1.5)

        self.wait(0.5)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
