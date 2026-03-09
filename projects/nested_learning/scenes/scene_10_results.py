"""Scene 10: Results & Big Picture — ~35s. Charts and concluding message."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    RoundedRectangle,
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
    ManimColor,
    Axes,
    Rectangle,
    Line,
    DashedLine,
)
from src.manim.scene_base import ExplainerSceneBase


class ResultsScene(ExplainerSceneBase):
    """~35-second scene: Key experimental results and concluding message."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")

        # ── Phase 1 (0-6s): Left panel — Continual Learning bar chart ────
        cl_title = Text(
            "Continual Learning",
            font_size=20, color=YELLOW,
        ).move_to([-3.5, 3.0, 0])

        bar_data = [
            ("Transformer", 0.45, BLUE),
            ("Mamba", 0.52, GREEN),
            ("HOPE", 0.78, YELLOW),
        ]

        bars = VGroup()
        bar_labels = VGroup()
        bar_values = VGroup()

        for i, (name, height, color) in enumerate(bar_data):
            x = -4.5 + i * 1.2
            bar = Rectangle(
                width=0.8, height=height * 4,
                fill_color=color, fill_opacity=0.6,
                stroke_color=color, stroke_width=1.5,
            )
            bar.move_to([x, -0.5 + height * 2, 0])

            label = Text(name, font_size=11, color=GREY_A)
            label.next_to(bar, DOWN, buff=0.1)

            val = Text(f"{height:.0%}", font_size=12, color=WHITE)
            val.next_to(bar, UP, buff=0.05)

            bars.add(bar)
            bar_labels.add(label)
            bar_values.add(val)

        bar_y_axis = Line(
            [-5.0, -0.5, 0], [-5.0, 3.0, 0],
            color=GREY, stroke_width=1.5,
        )

        y_axis_label = Text("Accuracy", font_size=11, color=GREY_A)
        y_axis_label.next_to(bar_y_axis, LEFT, buff=0.1).shift(UP * 0.5)

        # Animate left panel
        self.play(
            Write(cl_title),
            FadeIn(bar_y_axis),
            Write(y_axis_label),
            run_time=1.0,
        )
        self.play(
            *[FadeIn(b) for b in bars],
            *[Write(l) for l in bar_labels],
            *[Write(v) for v in bar_values],
            run_time=2.5,
        )
        self.wait(2.5)

        # ── Phase 2 (6-12s): Right panel — Long-Context line chart ───────
        divider = DashedLine(
            [0, -1.5, 0], [0, 3.5, 0],
            color=GREY, stroke_width=1,
        )
        self.play(Create(divider), run_time=0.5)

        lc_title = Text(
            "Long-Context Understanding",
            font_size=20, color=YELLOW,
        ).move_to([3.0, 3.0, 0])

        axes = Axes(
            x_range=[0, 256, 64],
            y_range=[0.3, 0.9, 0.1],
            x_length=4.5, y_length=3.0,
            axis_config={"color": GREY, "include_numbers": False},
            tips=False,
        ).move_to([3.5, 0.8, 0])

        axes_x_label = Text("Context Length (K tokens)", font_size=12, color=GREY_A)
        axes_x_label.next_to(axes, DOWN, buff=0.2)
        axes_y_label = Text("Accuracy", font_size=11, color=GREY_A)
        axes_y_label.next_to(axes, LEFT, buff=0.15).shift(UP * 0.3)

        self.play(
            Write(lc_title), FadeIn(axes),
            Write(axes_x_label), Write(axes_y_label),
            run_time=1.5,
        )

        # Transformer curve drops
        transformer_curve = axes.plot(
            lambda x: max(0.3, 0.85 - 0.003 * x),
            x_range=[0, 256],
            color=BLUE, stroke_width=2,
        )
        t_label = Text("Transformer", font_size=11, color=BLUE).move_to([5.5, 1.8, 0])

        # HOPE curve stays high
        hope_curve = axes.plot(
            lambda x: max(0.3, 0.82 - 0.0005 * x),
            x_range=[0, 256],
            color=YELLOW, stroke_width=2.5,
        )
        h_label = Text("HOPE", font_size=11, color=YELLOW).move_to([5.5, 2.2, 0])

        self.play(
            Create(transformer_curve), Write(t_label),
            run_time=1.5,
        )
        self.play(
            Create(hope_curve), Write(h_label),
            run_time=1.5,
        )

        # ── Phase 3 (12-18s): Hold both charts ──────────────────────────
        self.wait(6.0)

        # ── Phase 4 (18-22s): Fade charts, show final title ─────────────
        all_charts = VGroup(
            cl_title, bar_y_axis, y_axis_label, bars, bar_labels, bar_values,
            lc_title, axes, axes_x_label, axes_y_label,
            transformer_curve, hope_curve,
            t_label, h_label, divider,
        )
        self.play(FadeOut(all_charts), run_time=1.0)

        final_title = Text(
            "Nested Learning",
            font_size=44,
            color=YELLOW,
            weight="BOLD",
        ).move_to([0, 1.0, 0])

        subtitle = Text(
            "The Illusion of Deep Learning Architecture",
            font_size=24,
            color=WHITE,
        ).next_to(final_title, DOWN, buff=0.3)

        authors = Text(
            "Behrouz, Razaviyayn, Zhong & Mirrokni",
            font_size=18,
            color=GREY_A,
        ).next_to(subtitle, DOWN, buff=0.3)

        self.play(Write(final_title), Write(subtitle), run_time=2.0)
        self.play(Write(authors), run_time=1.0)

        # ── Phase 5 (22-30s): Tagline ───────────────────────────────────
        tagline = Text(
            "True depth is not layers \u2014 it is nested optimization at multiple timescales",
            font_size=16,
            color=ManimColor("#f39c12"),
        ).next_to(authors, DOWN, buff=0.5)

        self.play(Write(tagline), run_time=2.0)
        self.wait(6.0)

        # ── Phase 6 (30-33s): Fade out ──────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

        self.pad_to_duration()
