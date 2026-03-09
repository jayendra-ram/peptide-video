"""Scene 7: Continuum Memory System — ~40s. Eqs. 70-71."""

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
    Flash,
)
from src.manim.scene_base import ExplainerSceneBase


class CMSScene(ExplainerSceneBase):
    """~40-second scene: Continuum Memory System with multi-frequency MLP chain."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        RED = ManimColor("#e74c3c")

        # ── Phase 1 (0-6s): Title + RAM vs hard-drive intuition ──────────
        title = Text(
            "Continuum Memory System (CMS)",
            font_size=28,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.2)

        intuition = Text(
            "Intuition: RAM is fast but small; a hard drive is slow but vast.\n"
            "CMS stacks layers at different update frequencies — the same idea.",
            font_size=16,
            color=GREY_A,
            line_spacing=1.3,
        ).next_to(title, DOWN, buff=0.35)

        self.play(FadeIn(intuition), run_time=1.5)
        self.wait(3.3)

        # ── Phase 2 (6-14s): Build horizontal chain of 4 MLP blocks ─────
        self.play(FadeOut(intuition), run_time=0.8)

        n_blocks = 4
        block_colors_hex = ["#e74c3c", "#e67e22", "#f39c12", "#3498db"]
        block_labels_text = [
            "MLP\u00b9\nf = 1",
            "MLP\u00b2\nf = 1/C",
            "MLP\u00b3\nf = 1/C\u00b2",
            "MLP\u2074\nf = 1/C\u00b3",
        ]

        blocks = VGroup()
        block_rects: list = []
        chain_arrows = VGroup()

        start_x = -4.5
        spacing = 2.8

        for i in range(n_blocks):
            color = ManimColor(block_colors_hex[i])
            rect = RoundedRectangle(
                width=2.0, height=1.4, corner_radius=0.12,
                fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2.5,
            )
            x_pos = start_x + i * spacing
            rect.move_to([x_pos, -0.3, 0])

            label = Text(block_labels_text[i], font_size=14, color=color)
            label.move_to(rect.get_center())

            block_group = VGroup(rect, label)
            blocks.add(block_group)
            block_rects.append(rect)

        for i in range(n_blocks - 1):
            arr = Arrow(
                block_rects[i].get_right(), block_rects[i + 1].get_left(),
                buff=0.1, color=GREY_A, stroke_width=2,
            )
            chain_arrows.add(arr)

        # Input x_t on right, output y_t on left
        input_label = Text("x\u209c", font_size=24, color=WHITE)
        input_label.move_to([start_x + (n_blocks - 1) * spacing + 1.8, -0.3, 0])
        input_arr = Arrow(
            input_label.get_left(), block_rects[-1].get_right(),
            buff=0.15, color=WHITE, stroke_width=2,
        )

        output_label = Text("y\u209c", font_size=24, color=WHITE)
        output_label.move_to([start_x - 1.8, -0.3, 0])
        output_arr = Arrow(
            block_rects[0].get_left(), output_label.get_right(),
            buff=0.15, color=WHITE, stroke_width=2,
        )

        # Speed labels below blocks
        speed_labels_text = ["fastest", "fast", "slow", "slowest"]
        speed_labels = VGroup()
        for i in range(n_blocks):
            sl = Text(speed_labels_text[i], font_size=11, color=GREY_A)
            sl.next_to(block_rects[i], DOWN, buff=0.15)
            speed_labels.add(sl)

        self.play(*[FadeIn(b) for b in blocks], run_time=2.0)
        self.play(
            *[Create(a) for a in chain_arrows],
            FadeIn(input_label), Create(input_arr),
            FadeIn(output_label), Create(output_arr),
            *[Write(sl) for sl in speed_labels],
            run_time=2.0,
        )

        self.wait(2.0)

        # ── Phase 3 (14-20s): Display Eq. 70 ────────────────────────────
        eq70 = MathTex(
            r"y_t = \text{MLP}^{(1)}\!\left(\text{MLP}^{(2)}\!\left("
            r"\cdots \text{MLP}^{(K)}(x_t)\cdots\right)\right)",
            font_size=24,
        ).to_edge(DOWN, buff=1.4)

        eq70_label = Text("Eq. 70:", font_size=14, color=GREY_A).next_to(
            eq70, LEFT, buff=0.2
        )

        self.play(Write(eq70_label), Write(eq70), run_time=2.0)
        self.wait(4.0)

        # ── Phase 4 (20-28s): Flash animations for update cadences ───────
        # Block 1 flashes every round; block 4 almost never.
        for _ in range(3):
            self.play(
                Flash(block_rects[0], color=RED, flash_radius=0.45, run_time=0.5),
                run_time=0.5,
            )
            self.wait(0.3)

        # Second burst — blocks 1+2 flash
        self.play(
            Flash(block_rects[0], color=RED, flash_radius=0.45, run_time=0.5),
            Flash(block_rects[1], color=ManimColor("#e67e22"), flash_radius=0.45, run_time=0.5),
            run_time=0.5,
        )
        self.wait(0.3)

        # Third burst — blocks 1+2+3
        self.play(
            Flash(block_rects[0], color=RED, flash_radius=0.45, run_time=0.5),
            Flash(block_rects[1], color=ManimColor("#e67e22"), flash_radius=0.45, run_time=0.5),
            Flash(block_rects[2], color=ORANGE, flash_radius=0.45, run_time=0.5),
            run_time=0.5,
        )
        self.wait(0.3)

        # Rare full update — all four
        self.play(
            Flash(block_rects[0], color=RED, flash_radius=0.45, run_time=0.7),
            Flash(block_rects[1], color=ManimColor("#e67e22"), flash_radius=0.45, run_time=0.7),
            Flash(block_rects[2], color=ORANGE, flash_radius=0.45, run_time=0.7),
            Flash(block_rects[3], color=BLUE, flash_radius=0.45, run_time=0.7),
            run_time=0.7,
        )
        self.wait(1.2)

        # ── Phase 5 (28-34s): Display Eq. 71 ────────────────────────────
        self.play(FadeOut(eq70), FadeOut(eq70_label), run_time=0.6)

        eq71 = MathTex(
            r"\theta_i^{(t)} = \begin{cases}"
            r" \text{update}(\theta_i, x) & \text{if } t \equiv 0 \pmod{C^{(i)}} \\"
            r" \theta_i^{(t-1)} & \text{otherwise}"
            r" \end{cases}",
            font_size=22,
        ).to_edge(DOWN, buff=1.0)

        eq71_label = Text("Eq. 71:", font_size=14, color=GREY_A).next_to(
            eq71, LEFT, buff=0.2
        )

        self.play(Write(eq71_label), Write(eq71), run_time=2.0)
        self.wait(4.0)

        # ── Phase 6 (34-38s): Consolidation highlight ───────────────────
        self.play(FadeOut(eq71), FadeOut(eq71_label), run_time=0.5)

        consolidation = Text(
            "Fast \u2192 Slow: knowledge consolidation across timescales",
            font_size=18,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)
        c_box = SurroundingRectangle(
            consolidation, color=YELLOW, buff=0.12, stroke_width=1.5
        )

        self.play(Write(consolidation), Create(c_box), run_time=1.5)
        self.wait(2.0)

        # ── Phase 7: Fade out ────────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)

        self.pad_to_duration()
