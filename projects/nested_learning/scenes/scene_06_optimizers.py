"""Scene 6: Optimizers as Associative Memories — ~45s. Eqs. 46-50."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    MathTex,
    RoundedRectangle,
    CurvedArrow,
    FadeIn,
    FadeOut,
    Write,
    Create,
    WHITE,
    GREY,
    GREY_A,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ORIGIN,
    ManimColor,
    SurroundingRectangle,
    Axes,
    DashedLine,
)
from src.manim.scene_base import ExplainerSceneBase


class OptimizersScene(ExplainerSceneBase):
    """~45-second scene: Momentum and Adam as associative memories, Delta GD."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        RED = ManimColor("#e74c3c")
        PURPLE = ManimColor("#6c5ce7")

        # ── Phase 1 (0-4s): Title ─────────────────────────────────────
        title1 = Text(
            "Momentum as Associative Memory (Eq. 46)",
            font_size=26,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title1), run_time=1.5)
        self.wait(2.5)

        # ── Phase 2 (4-10s): Eq. 46 ──────────────────────────────────
        eq46_label = Text("Eq. 46:", font_size=16, color=GREY_A)
        eq46 = MathTex(
            r"\min_m \; \ell\!\left(m,\, \nabla\mathcal{L}(W_t, x_t)^\top,"
            r"\, P_t\right)",
            font_size=28,
        )
        eq46_group = VGroup(eq46_label, eq46).arrange(RIGHT, buff=0.25)
        eq46_group.next_to(title1, DOWN, buff=0.35)

        self.play(Write(eq46_label), run_time=0.5)
        self.play(Write(eq46), run_time=2.0)
        self.wait(3.5)

        # ── Phase 3 (10-18s): Exponential decay plot ──────────────────
        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 1.0, 0.2],
            x_length=5.0,
            y_length=2.5,
            axis_config={"color": GREY, "include_numbers": False},
            tips=False,
        ).move_to([0.0, -0.8, 0.0])

        x_label = Text("Steps ago (t\u2212i)", font_size=14, color=GREY_A)
        x_label.next_to(axes, DOWN, buff=0.2)
        y_label = Text("Weight", font_size=14, color=GREY_A)
        y_label.next_to(axes, LEFT, buff=0.2)

        beta = 0.9
        decay_curve = axes.plot(
            lambda x: beta ** x,
            x_range=[0, 99],
            color=ORANGE,
            stroke_width=2.5,
        )

        # Threshold line at x=43
        x_43_bottom = axes.c2p(43, 0)
        x_43_top = axes.c2p(43, beta ** 43)
        threshold_line = DashedLine(
            x_43_bottom,
            [x_43_top[0], x_43_top[1] + 0.3, 0.0],
            color=RED, stroke_width=1.5,
        )
        threshold_label = Text(
            "~43 steps:\n>50% of state",
            font_size=12,
            color=RED,
        ).next_to(threshold_line, UP, buff=0.1)

        self.play(FadeIn(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(decay_curve), run_time=2.0)
        self.play(Create(threshold_line), Write(threshold_label), run_time=1.5)

        self.wait(3.5)

        # ── Phase 4 (18-22s): Transition to Delta GD ─────────────────
        decay_elements = VGroup(
            axes, x_label, y_label, decay_curve,
            threshold_line, threshold_label,
            eq46_group,
        )
        self.play(FadeOut(decay_elements), run_time=0.8)

        title2 = Text(
            "Delta Gradient Descent (Eq. 50)",
            font_size=26,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(FadeOut(title1), FadeIn(title2), run_time=0.8)
        self.wait(2.4)

        # ── Phase 5 (22-32s): Side-by-side standard vs Delta ─────────
        # Left: Standard momentum
        std_heading = Text("Standard Momentum:", font_size=18, color=GREY_A)
        std_heading.move_to([-3.0, 1.8, 0.0])

        std_eq = MathTex(
            r"m_{t+1} = \beta\, m_t - \eta\, \nabla\mathcal{L}",
            font_size=26,
        ).next_to(std_heading, DOWN, buff=0.25)

        std_box = RoundedRectangle(
            width=2.8, height=1.2, corner_radius=0.1,
            fill_color=ORANGE, fill_opacity=0.15,
            stroke_color=ORANGE, stroke_width=2,
        ).move_to([-3.0, -0.8, 0.0])
        std_inner = Text("Weighted\nSum", font_size=16, color=ORANGE)
        std_inner.move_to(std_box.get_center())

        # Right: Delta momentum
        delta_heading = Text("Delta Momentum:", font_size=18, color=GREY_A)
        delta_heading.move_to([3.0, 1.8, 0.0])

        delta_eq = MathTex(
            r"m_{t+1} = \alpha\, m_t - \eta\, "
            r"\nabla\mathcal{L}^{(2)}(m_t,\, u_t,\, k_t)",
            font_size=24,
        ).next_to(delta_heading, DOWN, buff=0.25)

        delta_box = RoundedRectangle(
            width=2.8, height=1.2, corner_radius=0.1,
            fill_color=PURPLE, fill_opacity=0.15,
            stroke_color=PURPLE, stroke_width=2,
        ).move_to([3.0, -0.8, 0.0])
        delta_inner = Text("Self-Referential\nMemory", font_size=16, color=PURPLE)
        delta_inner.move_to(delta_box.get_center())

        loop_arr = CurvedArrow(
            delta_box.get_right() + np.array([0.0, 0.3, 0.0]),
            delta_box.get_right() + np.array([0.0, -0.3, 0.0]),
            color=PURPLE, stroke_width=2, angle=-2.0,
        )

        self.play(Write(std_heading), Write(std_eq), run_time=1.5)
        self.play(FadeIn(std_box), Write(std_inner), run_time=1.0)
        self.wait(1.0)

        self.play(Write(delta_heading), Write(delta_eq), run_time=1.5)
        self.play(
            FadeIn(delta_box), Write(delta_inner),
            Create(loop_arr),
            run_time=1.5,
        )

        self.wait(3.5)

        # ── Phase 6 (32-40s): Highlight box ──────────────────────────
        highlight = Text(
            "Delta GD: momentum generates its own learning signal",
            font_size=18,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)

        h_box = SurroundingRectangle(
            highlight, color=YELLOW, buff=0.12, stroke_width=2.0,
        )

        self.play(Write(highlight), Create(h_box), run_time=1.5)
        self.wait(6.5)

        # ── Phase 7: Fade out ─────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

        self.pad_to_duration()
