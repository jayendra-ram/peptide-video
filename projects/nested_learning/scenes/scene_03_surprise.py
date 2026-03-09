"""Scene 3: Backprop as Surprise Memory — ~40s. Eqs. 7-9."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    MathTex,
    RoundedRectangle,
    Rectangle,
    Arrow,
    FadeIn,
    FadeOut,
    Write,
    Create,
    Transform,
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
)
from src.manim.scene_base import ExplainerSceneBase


class SurpriseMemoryScene(ExplainerSceneBase):
    """~40s scene: Backprop reformulated as surprise-based memory (Eqs. 7-9)."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")
        RED = ManimColor("#e74c3c")

        # ===== Phase 1 (0-8s): Title and Eq. 7 =====
        title = Text(
            "Backprop = Surprise-Based Memory",
            font_size=30,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.5)

        eq7_label = Text("Eq. 7:", font_size=18, color=GREY_A)
        eq7 = MathTex(
            r"W^* = \operatorname*{argmin}_W \;\mathcal{L}(W;\, \mathcal{D}_{\text{train}})",
            font_size=30,
        )
        eq7_group = VGroup(eq7_label, eq7).arrange(RIGHT, buff=0.3)
        eq7_group.next_to(title, DOWN, buff=0.5)

        self.play(Write(eq7_label), run_time=0.5)
        self.play(Write(eq7), run_time=2.5)
        self.wait(3.5)  # Hold until ~8s

        # ===== Phase 2 (8-16s): Single layer diagram =====
        # Shift equation up
        self.play(eq7_group.animate.shift(UP * 0.3), run_time=0.5)

        # Input x
        input_label = Text("x", font_size=28, color=ORANGE).move_to([-5.0, -0.3, 0])

        # W box
        w_box = RoundedRectangle(
            width=2.0, height=1.4, corner_radius=0.1,
            fill_color=ManimColor("#3498db"), fill_opacity=0.3,
            stroke_color=BLUE, stroke_width=2,
        ).move_to([-2.0, -0.3, 0])
        w_label = Text("W", font_size=30, color=BLUE).move_to(w_box.get_center())

        # Output y-hat
        output_label = Text("\u0177", font_size=28, color=GREEN).move_to([1.0, -0.3, 0])

        # Surprise bar
        surprise_bar = Rectangle(
            width=0.5, height=1.8,
            fill_color=ManimColor("#e74c3c"), fill_opacity=0.7,
            stroke_color=RED, stroke_width=1.5,
        ).move_to([3.5, -0.3, 0])
        surprise_label = Text(
            "Surprise",
            font_size=18, color=RED,
        ).next_to(surprise_bar, UP, buff=0.12)

        # Arrows
        arr_in = Arrow(
            input_label.get_right(), w_box.get_left(),
            buff=0.15, color=GREY_A, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        arr_out = Arrow(
            w_box.get_right(), output_label.get_left(),
            buff=0.15, color=GREY_A, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        arr_surprise = Arrow(
            output_label.get_right(), surprise_bar.get_left(),
            buff=0.15, color=RED, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        # Gradient arrow flowing back from surprise to W
        grad_arrow = Arrow(
            surprise_bar.get_bottom() + np.array([0, -0.3, 0]),
            w_box.get_bottom() + np.array([0, -0.3, 0]),
            buff=0.1, color=YELLOW, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.12,
        ).shift(DOWN * 0.4)
        grad_label = Text(
            "\u2207 \u2113",
            font_size=22, color=YELLOW,
        ).next_to(grad_arrow, DOWN, buff=0.1)

        layer_group = VGroup(
            input_label, w_box, w_label, output_label,
            arr_in, arr_out, arr_surprise,
        )

        self.play(FadeIn(layer_group), run_time=2.0)
        self.play(
            FadeIn(surprise_bar), Write(surprise_label),
            run_time=1.5,
        )
        self.play(
            Create(grad_arrow), Write(grad_label),
            run_time=1.5,
        )
        self.wait(2.5)  # Hold until ~16s

        # ===== Phase 3 (16-24s): Surprise = gradient concept, key-value mapping =====
        # Fade the layer diagram partially and show the key-value interpretation
        full_diagram = VGroup(
            layer_group, surprise_bar, surprise_label,
            grad_arrow, grad_label,
        )
        self.play(full_diagram.animate.shift(UP * 0.5).scale(0.8), run_time=1.0)

        # Key-value mapping text
        kv_title = Text(
            "Surprise = Gradient of the loss",
            font_size=24, color=YELLOW,
        ).move_to([0, -1.2, 0])

        kv_mapping = Text(
            "Key: x\u209c     Value: \u2207\u0177 \u2113",
            font_size=22, color=WHITE,
        ).next_to(kv_title, DOWN, buff=0.4)

        # Color the key and value portions
        kv_key_label = Text("Key:", font_size=22, color=GREY_A).move_to([-2.5, -2.0, 0])
        kv_key_val = Text("x\u209c", font_size=26, color=ORANGE).next_to(kv_key_label, RIGHT, buff=0.2)
        kv_arrow = Arrow(
            [-0.8, -2.0, 0], [0.8, -2.0, 0],
            buff=0.1, color=GREY_A, stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        kv_val_label = Text("Value:", font_size=22, color=GREY_A).move_to([1.5, -2.0, 0])
        kv_val_val = Text("\u2207\u0177 \u2113", font_size=26, color=YELLOW).next_to(kv_val_label, RIGHT, buff=0.2)

        kv_row = VGroup(kv_key_label, kv_key_val, kv_arrow, kv_val_label, kv_val_val)

        self.play(Write(kv_title), run_time=1.5)
        self.play(FadeIn(kv_row), run_time=2.0)
        self.wait(3.5)  # Hold until ~24s

        # ===== Phase 4 (24-32s): Display Eq. 9 =====
        # Clear the key-value row and title
        self.play(FadeOut(kv_title), FadeOut(kv_row), run_time=0.8)

        eq9_label = Text("Eq. 9:", font_size=18, color=GREY_A)
        eq9 = MathTex(
            r"W_{t+1} = \operatorname*{argmin}_W \langle \nabla_{\hat{y}}\mathcal{L},\, Wx \rangle + \frac{1}{2\eta}\|W - W_t\|^2",
            font_size=26,
        )
        eq9_group = VGroup(eq9_label, eq9).arrange(RIGHT, buff=0.3)
        eq9_group.move_to([0, -1.5, 0])

        self.play(Write(eq9_label), run_time=0.5)
        self.play(Write(eq9), run_time=3.5)
        self.wait(3.2)  # Hold until ~32s

        # ===== Phase 5 (32-37s): Highlight box with takeaway =====
        highlight_text = Text(
            "Backpropagation is memorizing surprises",
            font_size=24,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)

        highlight_box = SurroundingRectangle(
            highlight_text,
            color=YELLOW,
            buff=0.15,
            stroke_width=2,
        )

        self.play(
            Write(highlight_text),
            Create(highlight_box),
            run_time=2.0,
        )
        self.wait(3.0)  # Hold until ~37s

        # ===== Phase 6 (37-38s): Fade out =====
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5,
        )

        self.pad_to_duration()
