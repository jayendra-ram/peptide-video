"""Scene 4: Time dilation — clocks and the Lorentz factor.

Two clocks ticking at different rates + gamma vs beta curve.
"""

from __future__ import annotations

import numpy as np

from manim import (
    Axes,
    Circle,
    Create,
    DOWN,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    ManimColor,
    RIGHT,
    Rotate,
    Text,
    UP,
    VGroup,
    Write,
    TAU,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import lorentz_factor


class TimeDilationScene(ExplainerSceneBase):
    """13-second scene: two clocks + gamma curve."""

    def _make_clock(self, label: str, position, color: str) -> VGroup:
        """Create a simple clock face with a hand."""
        face = Circle(
            radius=0.8, stroke_color=ManimColor(color),
            stroke_width=2, fill_opacity=0,
        )
        # Tick marks at 12, 3, 6, 9
        ticks = VGroup()
        for angle in [0, TAU / 4, TAU / 2, 3 * TAU / 4]:
            tick = Line(
                start=face.point_at_angle(angle),
                end=face.point_at_angle(angle) * 0.85 + face.get_center() * 0.15,
                stroke_width=2, color=ManimColor(color),
            )
            ticks.add(tick)

        hand = Line(
            start=face.get_center(),
            end=face.get_center() + UP * 0.65,
            stroke_width=3, color=ManimColor("#ecf0f1"),
        )
        clock_label = Text(
            label, font_size=20, color=ManimColor("#ecf0f1"),
        ).next_to(face, DOWN, buff=0.2)

        clock = VGroup(face, ticks, hand, clock_label)
        clock.move_to(position)
        return clock

    def construct(self) -> None:
        # ── Title labels ──────────────────────────────────────────────
        rest_label = Text(
            "Rest Frame", font_size=24, color=ManimColor("#2ecc71"),
        ).move_to(LEFT * 3.5 + UP * 3.0)
        moving_label = Text(
            "Moving Frame", font_size=24, color=ManimColor("#e67e22"),
        ).move_to(RIGHT * 3.5 + UP * 3.0)

        self.play(FadeIn(rest_label), FadeIn(moving_label), run_time=0.5)

        # ── Clocks ────────────────────────────────────────────────────
        rest_clock = self._make_clock("t", LEFT * 3.5 + UP * 1.0, "#2ecc71")
        moving_clock = self._make_clock("t'", RIGHT * 3.5 + UP * 1.0, "#e67e22")

        self.play(FadeIn(rest_clock), FadeIn(moving_clock), run_time=0.5)

        # Animate clocks: rest hand does full rotation, moving hand does 0.6 rotation
        rest_hand = rest_clock[2]
        moving_hand = moving_clock[2]

        self.play(
            Rotate(rest_hand, angle=-TAU, about_point=rest_clock[0].get_center()),
            Rotate(moving_hand, angle=-TAU * 0.6, about_point=moving_clock[0].get_center()),
            run_time=3.0,
        )

        # ── Lorentz factor equation ───────────────────────────────────
        gamma_eq = lorentz_factor().scale(0.85)
        gamma_eq.move_to(DOWN * 0.3)
        self.play(Write(gamma_eq), run_time=1.5)

        # ── Gamma vs beta plot ────────────────────────────────────────
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[1, 8, 1],
            x_length=5,
            y_length=2.5,
            axis_config={"color": ManimColor("#7f8c8d"), "font_size": 20},
            tips=False,
        ).move_to(DOWN * 2.3)

        x_label = Text("β", font_size=22, color=ManimColor("#7f8c8d"))
        x_label.next_to(axes.x_axis, RIGHT, buff=0.1)
        y_label = Text("γ", font_size=22, color=ManimColor("#7f8c8d"))
        y_label.next_to(axes.y_axis, UP, buff=0.1)

        # gamma curve: 1/sqrt(1 - beta^2), clamped to avoid infinity
        gamma_curve = axes.plot(
            lambda x: 1 / np.sqrt(1 - min(x, 0.98) ** 2),
            x_range=[0, 0.98, 0.01],
            color=ManimColor("#f1c40f"),
            stroke_width=3,
        )

        self.play(
            Create(axes), FadeIn(x_label), FadeIn(y_label),
            run_time=1.0,
        )
        self.play(Create(gamma_curve), run_time=2.0)

        # ── Annotation: gamma shoots up near beta=1 ──────────────────
        shoot_label = Text(
            "γ → ∞", font_size=20, color=ManimColor("#e74c3c"),
        ).next_to(axes.c2p(0.95, 7), RIGHT, buff=0.15)
        self.play(FadeIn(shoot_label), run_time=0.5)

        self.wait(2.5)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
