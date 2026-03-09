"""Scene 5: Knowledge Transfer Between Levels — ~40s. Eqs. 26-28."""

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
    DashedLine,
)
from src.manim.scene_base import ExplainerSceneBase


class KnowledgeTransferScene(ExplainerSceneBase):
    """~40-second scene: Three knowledge transfer mechanisms (Eqs. 26-28)."""

    def construct(self) -> None:
        BLUE = ManimColor("#3498db")
        ORANGE = ManimColor("#f39c12")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")
        RED = ManimColor("#e74c3c")
        PURPLE = ManimColor("#6c5ce7")

        # ── Phase 1 (0-8s): Title ─────────────────────────────────────
        title = Text(
            "Knowledge Transfer Between Levels",
            font_size=28,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.5)
        self.wait(6.5)

        # ── Helper: build a panel with Fast/Slow boxes ────────────────
        panel_x = [-4.0, 0.0, 4.0]

        def _make_boxes(x: float) -> tuple:
            fast_box = RoundedRectangle(
                width=2.0, height=0.8, corner_radius=0.1,
                fill_color=RED, fill_opacity=0.2,
                stroke_color=RED, stroke_width=2,
            ).move_to([x, 0.6, 0])
            fast_label = Text("Fast (L1)", font_size=14, color=RED)
            fast_label.move_to(fast_box.get_center())

            slow_box = RoundedRectangle(
                width=2.0, height=0.8, corner_radius=0.1,
                fill_color=BLUE, fill_opacity=0.2,
                stroke_color=BLUE, stroke_width=2,
            ).move_to([x, -0.8, 0])
            slow_label = Text("Slow (L2)", font_size=14, color=BLUE)
            slow_label.move_to(slow_box.get_center())

            return fast_box, fast_label, slow_box, slow_label

        # DashedLine dividers
        div1 = DashedLine(
            [-2.0, 2.5, 0], [-2.0, -2.8, 0],
            color=GREY, stroke_width=1,
        )
        div2 = DashedLine(
            [2.0, 2.5, 0], [2.0, -2.8, 0],
            color=GREY, stroke_width=1,
        )

        # ── Phase 2 (8-16s): Panel 1 — Direct Connection ─────────────
        fast1, fl1, slow1, sl1 = _make_boxes(panel_x[0])

        p1_title = Text("1. Direct Connection", font_size=16, color=GREEN)
        p1_title.move_to([panel_x[0], 2.0, 0])

        fwd_arrow = Arrow(
            slow1.get_top(), fast1.get_bottom(),
            buff=0.1, color=GREEN, stroke_width=2.5,
        )
        fwd_label = Text("output", font_size=12, color=GREEN)
        fwd_label.next_to(fwd_arrow, RIGHT, buff=0.1)

        eq1 = MathTex(
            r"M^{(1)}\!\left(\cdot\,;\, M^{(2)}(\cdot)\right)",
            font_size=22,
        ).move_to([panel_x[0], -2.0, 0])

        panel1 = VGroup(
            fast1, fl1, slow1, sl1, p1_title,
            fwd_arrow, fwd_label, eq1,
        )

        self.play(FadeIn(panel1), Create(div1), run_time=2.0)
        self.wait(6.0)

        # ── Phase 3 (16-24s): Panel 2 — Backpropagation ──────────────
        fast2, fl2, slow2, sl2 = _make_boxes(panel_x[1])

        p2_title = Text("2. Backpropagation", font_size=16, color=ORANGE)
        p2_title.move_to([panel_x[1], 2.0, 0])

        grad_arrow = Arrow(
            fast2.get_bottom(), slow2.get_top(),
            buff=0.1, color=ORANGE, stroke_width=2.5,
        )
        grad_label = Text("\u2207", font_size=20, color=ORANGE)
        grad_label.next_to(grad_arrow, LEFT, buff=0.1)

        eq2 = MathTex(
            r"\nabla_{\theta^{(1)}} \ell^{(2)}",
            font_size=22,
        ).move_to([panel_x[1], -2.0, 0])

        panel2 = VGroup(
            fast2, fl2, slow2, sl2, p2_title,
            grad_arrow, grad_label, eq2,
        )

        self.play(FadeIn(panel2), Create(div2), run_time=2.0)
        self.wait(6.0)

        # ── Phase 4 (24-32s): Panel 3 — Meta-Learning (MAML) ─────────
        fast3, fl3, slow3, sl3 = _make_boxes(panel_x[2])

        p3_title = Text("3. Meta-Learning", font_size=16, color=PURPLE)
        p3_title.move_to([panel_x[2], 2.0, 0])

        meta_arrow = CurvedArrow(
            slow3.get_right() + np.array([0.0, 0.2, 0.0]),
            fast3.get_right() + np.array([0.0, -0.2, 0.0]),
            color=PURPLE, stroke_width=2.5, angle=-1.2,
        )
        meta_label = Text("\u03b8\u2080", font_size=18, color=PURPLE)
        meta_label.next_to(meta_arrow, RIGHT, buff=0.1)

        eq3 = MathTex(
            r"\theta_0^{(1)} = \operatorname*{argmin} \; "
            r"\mathbb{E}_{T}\!\left[\mathcal{L}\right]",
            font_size=20,
        ).move_to([panel_x[2], -2.0, 0])

        panel3 = VGroup(
            fast3, fl3, slow3, sl3, p3_title,
            meta_arrow, meta_label, eq3,
        )

        self.play(FadeIn(panel3), run_time=2.0)
        self.wait(6.0)

        # ── Phase 5 (32-37s): Examples mapping ────────────────────────
        examples = Text(
            "Transformers \u2192 Direct  |  MAML \u2192 Meta-Learning  |  Fine-tuning \u2192 Backprop",
            font_size=16,
            color=GREY_A,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(examples), run_time=1.5)
        self.wait(3.5)

        # ── Phase 6: Fade out ─────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

        self.pad_to_duration()
