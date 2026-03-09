"""Scene 2: Associative Memory — ~35s. Definition 1, Eq. 6."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    MathTex,
    RoundedRectangle,
    Arrow,
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
)
from src.manim.scene_base import ExplainerSceneBase


class AssocMemoryScene(ExplainerSceneBase):
    """~35s scene: Definition 1 — Associative Memory (Eq. 6)."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")

        # ===== Phase 1 (0-8s): Title and intuitive key-value analogy =====
        title = Text(
            "Definition 1: Associative Memory",
            font_size=30,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.5)

        # Intuitive analogy: key-value pairs fade in one by one
        analogy_pairs = [
            ("Phone number", "Person's name"),
            ("Word in English", "Word in French"),
            ("Face", "Identity"),
            ("Input pattern", "Stored response"),
        ]

        pair_mobjects = VGroup()
        for i, (k, v) in enumerate(analogy_pairs):
            y_pos = 1.8 - i * 0.7
            key_text = Text(k, font_size=20, color=ORANGE).move_to([-3.0, y_pos, 0])
            arrow = Arrow(
                [-1.5, y_pos, 0], [1.0, y_pos, 0],
                buff=0.1, color=GREY_A, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.15,
            )
            val_text = Text(v, font_size=20, color=GREEN).move_to([3.0, y_pos, 0])
            pair_group = VGroup(key_text, arrow, val_text)
            pair_mobjects.add(pair_group)

        for pair in pair_mobjects:
            self.play(FadeIn(pair), run_time=1.0)
        self.wait(1.5)  # Hold until ~8s

        # ===== Phase 2 (8-16s): Central M box with key-value arrows =====
        # Fade out analogy
        self.play(FadeOut(pair_mobjects), run_time=0.8)

        # Build the M diagram
        m_box = RoundedRectangle(
            width=1.8,
            height=2.4,
            corner_radius=0.12,
            fill_color=ManimColor("#3498db"),
            fill_opacity=0.3,
            stroke_color=BLUE,
            stroke_width=2,
        ).move_to(ORIGIN + DOWN * 0.3)
        m_label = Text("M", font_size=36, color=BLUE).move_to(m_box.get_center())

        keys_header = Text("Keys", font_size=22, color=ORANGE).move_to([-4.0, 1.5, 0])
        values_header = Text("Values", font_size=22, color=GREEN).move_to([4.0, 1.5, 0])

        key_items = VGroup()
        value_items = VGroup()
        arrows_in = VGroup()
        arrows_out = VGroup()
        subscripts = ["\u2081", "\u2082", "\u2083", "\u2084"]

        for i in range(4):
            y_pos = 0.8 - i * 0.6
            k = Text(f"k{subscripts[i]}", font_size=24, color=ORANGE)
            k.move_to([-4.0, y_pos, 0])
            key_items.add(k)

            v = Text(f"v{subscripts[i]}", font_size=24, color=GREEN)
            v.move_to([4.0, y_pos, 0])
            value_items.add(v)

            arr_in = Arrow(
                k.get_right(), m_box.get_left() + np.array([0, y_pos - m_box.get_center()[1], 0]),
                buff=0.15, color=GREY_A, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows_in.add(arr_in)

            arr_out = Arrow(
                m_box.get_right() + np.array([0, y_pos - m_box.get_center()[1], 0]), v.get_left(),
                buff=0.15, color=GREY_A, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.15,
            )
            arrows_out.add(arr_out)

        self.play(
            FadeIn(m_box), FadeIn(m_label),
            FadeIn(keys_header), FadeIn(values_header),
            run_time=1.5,
        )
        self.play(
            *[FadeIn(k) for k in key_items],
            *[FadeIn(v) for v in value_items],
            run_time=1.5,
        )
        self.play(
            *[Create(a) for a in arrows_in],
            *[Create(a) for a in arrows_out],
            run_time=2.0,
        )
        self.wait(3.0)  # Hold until ~16s

        # ===== Phase 3 (16-22s): Display Eq. 6 using MathTex =====
        # Shift the diagram up to make room
        diagram_group = VGroup(
            m_box, m_label, keys_header, values_header,
            key_items, value_items, arrows_in, arrows_out,
        )
        self.play(diagram_group.animate.shift(UP * 0.5), run_time=0.8)

        eq_label = Text("Eq. 6:", font_size=20, color=GREY_A)
        eq6 = MathTex(
            r"M^* = \operatorname*{argmin}_M \sum_i \mathcal{L}\big(M(k_i),\, v_i\big)",
            font_size=36,
        )
        eq_group = VGroup(eq_label, eq6).arrange(RIGHT, buff=0.3)
        eq_group.to_edge(DOWN, buff=1.2)

        self.play(Write(eq_label), run_time=0.5)
        self.play(Write(eq6), run_time=2.5)
        self.wait(2.2)  # Hold until ~22s

        # ===== Phase 4 (22-30s): Highlight box with takeaway =====
        highlight_text = Text(
            "Any learning process solving this optimization\nis building an associative memory",
            font_size=22,
            color=WHITE,
        ).to_edge(DOWN, buff=0.4)

        highlight_box = SurroundingRectangle(
            highlight_text,
            color=YELLOW,
            buff=0.15,
            stroke_width=2,
        )

        self.play(
            FadeOut(eq_group),
            run_time=0.8,
        )
        self.play(
            Write(highlight_text),
            Create(highlight_box),
            run_time=2.0,
        )
        self.wait(5.2)  # Hold until ~30s

        # ===== Phase 5 (30-33s): Fade out =====
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=2.0,
        )
        self.wait(1.0)

        self.pad_to_duration()
