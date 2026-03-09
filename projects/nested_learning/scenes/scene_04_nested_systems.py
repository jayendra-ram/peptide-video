"""Scene 4: Nested Systems — ~45s. Definition 3, Eq. 19."""

from __future__ import annotations

import numpy as np
from manim import (
    VGroup,
    Text,
    MathTex,
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
    SurroundingRectangle,
)
from src.manim.scene_base import ExplainerSceneBase


class NestedSystemsScene(ExplainerSceneBase):
    """~45-second scene: Definition 3 — Nested systems with K ordered levels."""

    def construct(self) -> None:
        RED = ManimColor("#e74c3c")
        ORANGE = ManimColor("#f39c12")
        BLUE = ManimColor("#3498db")
        YELLOW = ManimColor("#f1c40f")
        GREEN = ManimColor("#2ecc71")

        # ── Phase 1 (0-8s): Title + intuition ────────────────────────
        title = Text(
            "Definition 3: Nested System",
            font_size=28,
            color=YELLOW,
        ).to_edge(UP, buff=0.35)

        self.play(Write(title), run_time=1.5)

        intuition = Text(
            "Intuition: different parts of the brain learn at different speeds.\n"
            "Synapses adjust quickly; structural wiring changes slowly.",
            font_size=18,
            color=GREY_A,
            line_spacing=1.3,
        ).next_to(title, DOWN, buff=0.4)

        self.play(FadeIn(intuition), run_time=1.5)
        self.wait(5.0)

        # ── Phase 2 (8-18s): Concentric rounded rectangles ───────────
        self.play(FadeOut(intuition), run_time=0.8)

        level_configs = [
            (RED, 9.5, 3.8, "Level 1 (f\u2081 = high)"),
            (ORANGE, 7.0, 2.8, "Level 2 (f\u2082 = med)"),
            (BLUE, 4.5, 1.8, "Level 3 (f\u2083 = low)"),
        ]

        center = np.array([0.0, -1.0, 0.0])

        levels_group = VGroup()
        level_labels = VGroup()

        for color, w, h, label_text in level_configs:
            rect = RoundedRectangle(
                width=w, height=h, corner_radius=0.25,
                fill_color=color, fill_opacity=0.1,
                stroke_color=color, stroke_width=2.5,
            ).move_to(center)
            levels_group.add(rect)

            label = Text(label_text, font_size=14, color=color)
            label.next_to(rect, DOWN, buff=0.05)
            level_labels.add(label)

        inner = RoundedRectangle(
            width=2.5, height=0.9, corner_radius=0.1,
            fill_color=GREEN, fill_opacity=0.2,
            stroke_color=GREEN, stroke_width=2,
        ).move_to(center)

        inner_label = Text(
            "\u03b8\u2096, \u2113\u2096, C\u2096, f\u2096",
            font_size=24,
            color=WHITE,
        ).move_to(inner.get_center())

        # Animate levels one by one for clarity
        self.play(Create(levels_group[0]), Write(level_labels[0]), run_time=1.5)
        self.play(Create(levels_group[1]), Write(level_labels[1]), run_time=1.5)
        self.play(Create(levels_group[2]), Write(level_labels[2]), run_time=1.5)
        self.play(FadeIn(inner), Write(inner_label), run_time=1.2)

        self.wait(3.5)

        # ── Phase 3 (18-28s): Eq. 19 with MathTex ────────────────────
        eq19_label = Text("Eq. 19:", font_size=16, color=GREY_A)
        eq19 = MathTex(
            r"\theta_k^{(t+1)} = \operatorname*{argmin}_{\theta_k} "
            r"\ell_k\!\left(\theta_k;\, X,\, \theta_{\uparrow k},\, "
            r"\theta_{\downarrow k}\right) + \frac{1}{2\eta_k}"
            r"\|\theta_k - \theta_k^{(t)}\|^2",
            font_size=24,
        )
        eq19_group = VGroup(eq19_label, eq19).arrange(RIGHT, buff=0.25)
        eq19_group.next_to(title, DOWN, buff=0.3)

        self.play(Write(eq19_label), run_time=0.5)
        self.play(Write(eq19), run_time=2.5)

        self.wait(6.5)

        # ── Phase 4 (28-38s): Transformer decomposition labels ───────
        transformer_labels_data = [
            ("Attention / In-context", RED, levels_group[0]),
            ("MLP weights", ORANGE, levels_group[1]),
            ("Embeddings", BLUE, levels_group[2]),
        ]

        transformer_labels = VGroup()
        for text, color, rect in transformer_labels_data:
            lbl = Text(text, font_size=14, color=color)
            lbl.move_to(rect.get_center() + np.array([0.0, rect.height / 2 - 0.2, 0.0]))
            transformer_labels.add(lbl)

        self.play(*[Write(lbl) for lbl in transformer_labels], run_time=2.0)

        annotation_text = Text(
            "Transformer as a 3-level nested system",
            font_size=16,
            color=WHITE,
        ).move_to([0.0, -3.2, 0.0])

        annotation_box = SurroundingRectangle(
            annotation_text, color=ORANGE, buff=0.12, stroke_width=1.5,
        )

        self.play(Write(annotation_text), Create(annotation_box), run_time=1.5)

        self.wait(6.5)

        # ── Phase 5 (38-42s): Highlight persistence principle ─────────
        self.play(
            FadeOut(annotation_text), FadeOut(annotation_box),
            FadeOut(eq19_group),
            run_time=0.8,
        )

        highlight = Text(
            "Higher level \u2192 lower frequency \u2192 more persistent",
            font_size=20,
            color=WHITE,
        ).to_edge(DOWN, buff=0.5)

        h_box = SurroundingRectangle(
            highlight, color=YELLOW, buff=0.12, stroke_width=2.0,
        )

        self.play(Write(highlight), Create(h_box), run_time=1.5)
        self.wait(2.0)

        # ── Phase 6: Fade out ─────────────────────────────────────────
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)

        self.pad_to_duration()
