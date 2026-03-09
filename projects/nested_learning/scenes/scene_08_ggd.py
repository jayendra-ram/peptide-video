"""Scene 8: Generalized Gradient Descent — ~40s. Definition 5, Eqs. 59-60."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    MathTex,
    RoundedRectangle,
    Arrow,
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
    ManimColor,
    SurroundingRectangle,
)
from src.manim.scene_base import ExplainerSceneBase


class GGDScene(ExplainerSceneBase):
    """~40-second scene: GGD — self-referential learning (Def. 5, Eqs. 59-60)."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")
        RED = ManimColor("#e74c3c")
        PURPLE = ManimColor("#6c5ce7")

        # ── Phase 1 (0-8s): Standard Backprop with External Targets ──────
        title1 = Text(
            "Standard Backprop: External Targets",
            font_size=26,
            color=GREY_A,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title1), run_time=1.0)

        # Data box
        data_box = RoundedRectangle(
            width=1.2, height=0.7, corner_radius=0.08,
            fill_color=ORANGE, fill_opacity=0.25,
            stroke_color=ORANGE, stroke_width=2,
        ).move_to([-4.5, 0, 0])
        data_label = Text("x", font_size=22, color=ORANGE).move_to(data_box)

        # Model box
        model_box = RoundedRectangle(
            width=1.8, height=0.9, corner_radius=0.1,
            fill_color=BLUE, fill_opacity=0.25,
            stroke_color=BLUE, stroke_width=2,
        ).move_to([-1.5, 0, 0])
        model_label = Text("Model", font_size=18, color=BLUE).move_to(model_box)

        # Output box
        output_box = RoundedRectangle(
            width=1.2, height=0.7, corner_radius=0.08,
            fill_color=GREEN, fill_opacity=0.25,
            stroke_color=GREEN, stroke_width=2,
        ).move_to([1.5, 0, 0])
        output_label = Text("\u0177", font_size=22, color=GREEN).move_to(output_box)

        # External target box
        target_box = RoundedRectangle(
            width=1.2, height=0.7, corner_radius=0.08,
            fill_color=RED, fill_opacity=0.25,
            stroke_color=RED, stroke_width=2,
        ).move_to([4.0, 0, 0])
        target_label = Text("y*", font_size=22, color=RED).move_to(target_box)
        ext_label = Text("(external)", font_size=12, color=RED)
        ext_label.next_to(target_box, DOWN, buff=0.1)

        # Arrows: forward path
        arr1 = Arrow(data_box.get_right(), model_box.get_left(),
                     buff=0.1, color=GREY_A, stroke_width=2)
        arr2 = Arrow(model_box.get_right(), output_box.get_left(),
                     buff=0.1, color=GREY_A, stroke_width=2)
        arr3 = Arrow(output_box.get_right(), target_box.get_left(),
                     buff=0.1, color=GREY_A, stroke_width=2)

        # Gradient arrow
        grad_arr = Arrow(
            target_box.get_bottom() + np.array([0, -0.3, 0]),
            model_box.get_bottom() + np.array([0, -0.3, 0]),
            buff=0.1, color=YELLOW, stroke_width=2.5,
        ).shift(DOWN * 0.4)
        grad_label = Text("\u2207W", font_size=16, color=YELLOW)
        grad_label.next_to(grad_arr, DOWN, buff=0.08)

        # Update W label
        update_label = Text("update W", font_size=12, color=YELLOW)
        update_label.next_to(model_box, DOWN, buff=0.55)

        standard_flow = VGroup(
            data_box, data_label, model_box, model_label,
            output_box, output_label, target_box, target_label, ext_label,
            arr1, arr2, arr3, grad_arr, grad_label, update_label,
        )

        self.play(FadeIn(standard_flow), run_time=2.5)

        # ── Phase 2 (8-14s): Hold the standard backprop diagram ─────────
        self.wait(5.5)

        # ── Phase 3 (14-18s): Fade out, new GGD title ───────────────────
        self.play(FadeOut(standard_flow), FadeOut(title1), run_time=1.0)

        title2 = Text(
            "GGD (Def. 5): Self-Referential Learning",
            font_size=26,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title2), run_time=1.2)
        self.wait(1.8)

        # ── Phase 4 (18-26s): Display Eq. 59 and Eq. 60 ─────────────────
        eq59 = MathTex(
            r"W_{t+1} = \operatorname*{argmin}_W \;"
            r"\mathcal{L}(x_t,\, u_t) + \text{Ret}(W_t \mid W_{t-1},\ldots,W_{t-s})",
            font_size=24,
        ).next_to(title2, DOWN, buff=0.4)

        eq59_label = Text("Eq. 59:", font_size=14, color=GREY_A).next_to(
            eq59, LEFT, buff=0.2
        )

        self.play(Write(eq59_label), Write(eq59), run_time=2.0)
        self.wait(1.0)

        eq60 = MathTex(
            r"u_t = f_{W_t}(x_t) \quad \text{(self-generated value)}",
            font_size=26,
        ).next_to(eq59, DOWN, buff=0.35)

        eq60_label = Text("Eq. 60:", font_size=14, color=GREY_A).next_to(
            eq60, LEFT, buff=0.2
        )

        self.play(Write(eq60_label), Write(eq60), run_time=1.5)
        self.wait(3.5)

        # ── Phase 5 (26-34s): Self-referential diagram ───────────────────
        model_box2 = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.12,
            fill_color=BLUE, fill_opacity=0.2,
            stroke_color=BLUE, stroke_width=2.5,
        ).move_to([0, -1.5, 0])
        model_label2 = MathTex(r"f_{W_t}", font_size=28, color=BLUE).move_to(model_box2)

        data_in = MathTex(r"x_t", font_size=24, color=ORANGE).move_to([-3.5, -1.5, 0])
        arr_in = Arrow(data_in.get_right(), model_box2.get_left(),
                       buff=0.15, color=GREY_A, stroke_width=2)

        output_dot = MathTex(r"u_t", font_size=24, color=GREEN).move_to([3.5, -1.5, 0])
        arr_out = Arrow(model_box2.get_right(), output_dot.get_left(),
                        buff=0.15, color=GREEN, stroke_width=2)

        # Self-referential loop: output curves back to input
        self_loop = CurvedArrow(
            output_dot.get_top() + np.array([0, 0.1, 0]),
            data_in.get_top() + np.array([0, 0.1, 0]),
            color=PURPLE, stroke_width=3, angle=-1.2,
        )
        loop_label = Text("self-referential", font_size=14, color=PURPLE)
        loop_label.next_to(self_loop, UP, buff=0.08)

        self.play(
            FadeIn(model_box2), Write(model_label2),
            FadeIn(data_in), Create(arr_in),
            FadeIn(output_dot), Create(arr_out),
            run_time=2.0,
        )
        self.play(Create(self_loop), Write(loop_label), run_time=1.5)
        self.wait(4.5)

        # ── Phase 6 (34-38s): Highlight box ──────────────────────────────
        box_text = Text(
            "Backpropagation is a self-referential process",
            font_size=18,
            color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        box_rect = SurroundingRectangle(
            box_text, color=YELLOW, buff=0.12, stroke_width=1.5
        )

        self.play(Write(box_text), Create(box_rect), run_time=1.5)
        self.wait(2.5)

        # ── Phase 7: Fade out ────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        self.pad_to_duration()
