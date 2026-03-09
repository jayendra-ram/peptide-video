"""Scene 9: HOPE Architecture — ~40s. Three-step architecture build."""

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
    Brace,
)
from src.manim.scene_base import ExplainerSceneBase


class HOPEScene(ExplainerSceneBase):
    """~40-second scene: HOPE architecture — self-modifying Titans + CMS."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")
        RED = ManimColor("#e74c3c")
        PURPLE = ManimColor("#6c5ce7")

        # ── Phase 1 (0-4s): Title ────────────────────────────────────────
        title = Text(
            "HOPE: Self-Referential Learning + Continuum Memory",
            font_size=24,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.5)
        self.wait(2.5)

        # ── Phase 2 (4-14s): Step 1 — Self-Modifying Titans ─────────────
        step1_label = Text(
            "Step 1: Self-Modifying Titans",
            font_size=18,
            color=GREY_A,
        ).next_to(title, DOWN, buff=0.25)

        self.play(Write(step1_label), run_time=0.8)

        # Blue base box
        base_box = RoundedRectangle(
            width=3.0, height=1.8, corner_radius=0.15,
            fill_color=BLUE, fill_opacity=0.2,
            stroke_color=BLUE, stroke_width=2.5,
        ).move_to([-3.0, -0.5, 0])

        # Inner boxes
        attn_box = RoundedRectangle(
            width=2.4, height=0.5, corner_radius=0.08,
            fill_color=PURPLE, fill_opacity=0.3,
            stroke_color=PURPLE, stroke_width=1.5,
        ).move_to([-3.0, 0.05, 0])
        attn_label = Text("Attention + Memory", font_size=12, color=PURPLE)
        attn_label.move_to(attn_box)

        mlp_box = RoundedRectangle(
            width=2.4, height=0.5, corner_radius=0.08,
            fill_color=GREEN, fill_opacity=0.3,
            stroke_color=GREEN, stroke_width=1.5,
        ).move_to([-3.0, -0.7, 0])
        mlp_label = Text("MLP + Local Objective", font_size=12, color=GREEN)
        mlp_label.move_to(mlp_box)

        # CurvedArrow self-loop on right side
        self_loop = CurvedArrow(
            base_box.get_right() + np.array([0, 0.5, 0]),
            base_box.get_right() + np.array([0, -0.5, 0]),
            color=YELLOW, stroke_width=2.5, angle=-2.5,
        )
        loop_label = Text("self-modify", font_size=12, color=YELLOW)
        loop_label.next_to(self_loop, RIGHT, buff=0.08)

        self.play(
            FadeIn(base_box),
            FadeIn(attn_box), Write(attn_label),
            FadeIn(mlp_box), Write(mlp_label),
            run_time=2.0,
        )
        self.play(Create(self_loop), Write(loop_label), run_time=1.5)

        base_label = Text("Titan Block", font_size=14, color=BLUE)
        base_label.next_to(base_box, DOWN, buff=0.15)
        self.play(Write(base_label), run_time=0.7)

        self.wait(3.0)

        # ── Phase 3 (14-26s): Step 2 — Add CMS ──────────────────────────
        step2_label = Text(
            "Step 2: Add CMS",
            font_size=18,
            color=GREY_A,
        ).next_to(title, DOWN, buff=0.25)

        self.play(FadeOut(step1_label), run_time=0.3)
        self.play(Write(step2_label), run_time=0.8)

        # Three CMS blocks at different frequencies
        cms_blocks = VGroup()
        cms_colors = [RED, ORANGE, BLUE]
        cms_labels_text = [
            "Block 1\nf = high",
            "Block 2\nf = med",
            "Block 3\nf = low",
        ]

        cms_rects: list = []
        for i in range(3):
            color = cms_colors[i]
            rect = RoundedRectangle(
                width=1.8, height=1.2, corner_radius=0.1,
                fill_color=color, fill_opacity=0.15,
                stroke_color=color, stroke_width=2,
            ).move_to([1.5 + i * 2.3, -0.5, 0])

            label = Text(cms_labels_text[i], font_size=12, color=color)
            label.move_to(rect.get_center())

            cms_blocks.add(VGroup(rect, label))
            cms_rects.append(rect)

        # Arrows between CMS blocks
        cms_arrows = VGroup()
        for i in range(2):
            arr = Arrow(
                cms_rects[i].get_right(), cms_rects[i + 1].get_left(),
                buff=0.1, color=GREY_A, stroke_width=1.5,
            )
            cms_arrows.add(arr)

        # Connect base box to first CMS block
        connect_arr = Arrow(
            base_box.get_right() + np.array([0.3, 0, 0]),
            cms_rects[0].get_left(),
            buff=0.15, color=GREY_A, stroke_width=2,
        )

        # Brace below CMS blocks
        cms_rect_group = VGroup(*cms_rects)
        cms_brace = Brace(cms_rect_group, DOWN, color=GREY_A)
        cms_brace_label = Text("Continuum Memory System", font_size=14, color=YELLOW)
        cms_brace_label.next_to(cms_brace, DOWN, buff=0.1)

        self.play(
            *[FadeIn(b) for b in cms_blocks],
            *[Create(a) for a in cms_arrows],
            Create(connect_arr),
            run_time=2.5,
        )
        self.play(Create(cms_brace), Write(cms_brace_label), run_time=1.5)
        self.wait(5.0)

        # Frequency annotations
        freq_fast = Text("updates every token", font_size=10, color=RED)
        freq_fast.next_to(cms_rects[0], UP, buff=0.1)
        freq_med = Text("updates every C tokens", font_size=10, color=ORANGE)
        freq_med.next_to(cms_rects[1], UP, buff=0.1)
        freq_slow = Text("updates every C\u00b2 tokens", font_size=10, color=BLUE)
        freq_slow.next_to(cms_rects[2], UP, buff=0.1)

        self.play(
            Write(freq_fast), Write(freq_med), Write(freq_slow),
            run_time=1.5,
        )
        self.wait(1.5)

        # ── Phase 4 (26-34s): Step 3 — Parallelizable Training + Eq. ────
        step3_label = Text(
            "Step 3: Parallelizable Training",
            font_size=18,
            color=GREY_A,
        ).next_to(title, DOWN, buff=0.25)

        self.play(FadeOut(step2_label), run_time=0.3)
        self.play(Write(step3_label), run_time=0.8)

        arch_eq = MathTex(
            r"M_t = M_{t-1} - \eta\,\nabla\mathcal{L}\!\left("
            r"M_t,\, f(\theta)\!\left(\frac{\partial g}{\partial k}\right)\right)",
            font_size=22,
        ).to_edge(DOWN, buff=1.5)

        self.play(Write(arch_eq), run_time=2.0)

        chunk_text = Text(
            "Input \u2192 chunks \u2192 blocks update independently \u2192 state transfers between chunks",
            font_size=14,
            color=WHITE,
        ).to_edge(DOWN, buff=0.6)

        self.play(Write(chunk_text), run_time=1.5)
        self.wait(3.4)

        # ── Phase 5 (34-38s): Hold with all elements visible ────────────
        self.wait(4.0)

        # ── Phase 6: Fade out ────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        self.pad_to_duration()
