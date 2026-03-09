"""Scene 1: Intro — ~20s hook. Flat deep network transforms into nested view."""

from __future__ import annotations

from manim import (
    VGroup,
    Text,
    RoundedRectangle,
    Arrow,
    FadeIn,
    FadeOut,
    Write,
    Create,
    Transform,
    ReplacementTransform,
    WHITE,
    GREY,
    GREY_A,
    UP,
    DOWN,
    ORIGIN,
    ManimColor,
)
from src.manim.scene_base import ExplainerSceneBase


class IntroScene(ExplainerSceneBase):
    """~20s hook: flat deep network transforms into nested concentric view."""

    def construct(self) -> None:
        # Color palettes
        layer_colors = ["#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#e74c3c"]

        # ===== Phase 1 (0-6s): Flat network — 5 layers stacked vertically =====
        title_flat = Text(
            "The Deep Learning View",
            font_size=32,
            color=GREY_A,
        ).to_edge(UP, buff=0.4)

        layers = VGroup()
        arrows = VGroup()
        for i in range(5):
            rect = RoundedRectangle(
                width=3.0,
                height=0.5,
                corner_radius=0.1,
                fill_color=ManimColor(layer_colors[i]),
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=1.5,
            )
            label = Text(f"Layer {i + 1}", font_size=18, color=WHITE)
            label.move_to(rect.get_center())
            block = VGroup(rect, label)
            block.move_to([0, 2.0 - i * 1.0, 0])
            layers.add(block)

        for i in range(4):
            arr = Arrow(
                layers[i].get_bottom(),
                layers[i + 1].get_top(),
                buff=0.08,
                color=GREY,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(arr)

        flat_network = VGroup(layers, arrows)
        flat_network.move_to(ORIGIN)

        self.play(Write(title_flat), run_time=1.0)
        self.play(FadeIn(flat_network), run_time=2.0)
        self.wait(3.0)  # Hold until ~6s

        # ===== Phase 2 (6-14s): Transform into nested concentric rectangles =====
        title_nested = Text(
            "The Nested Learning View",
            font_size=32,
            color=ManimColor("#f1c40f"),
        ).to_edge(UP, buff=0.4)

        level_configs = [
            ("#e74c3c", 6.0, 4.0, "Level 1: Fast"),
            ("#f39c12", 4.5, 3.0, "Level 2: Medium"),
            ("#3498db", 3.0, 2.0, "Level 3: Slow"),
        ]

        nested = VGroup()
        nested_labels = VGroup()
        for color, w, h, label_text in level_configs:
            rect = RoundedRectangle(
                width=w,
                height=h,
                corner_radius=0.15,
                fill_color=ManimColor(color),
                fill_opacity=0.15,
                stroke_color=ManimColor(color),
                stroke_width=2.5,
            )
            rect.move_to([0, -0.2, 0])
            nested.add(rect)
            label = Text(label_text, font_size=16, color=ManimColor(color))
            label.next_to(rect, DOWN, buff=0.05)
            nested_labels.add(label)

        # Fade out arrows first, then transform layers into nested rectangles
        self.play(FadeOut(arrows), run_time=0.5)
        self.play(
            ReplacementTransform(title_flat, title_nested),
            ReplacementTransform(layers, nested),
            run_time=2.5,
        )
        self.play(
            *[FadeIn(lbl) for lbl in nested_labels],
            run_time=1.5,
        )
        self.wait(3.5)  # Hold until ~14s

        # ===== Phase 3 (14-18s): Paper title =====
        paper_title = Text(
            "Nested Learning",
            font_size=48,
            color=ManimColor("#f1c40f"),
            weight="BOLD",
        ).to_edge(DOWN, buff=0.6)

        self.play(Write(paper_title), run_time=2.0)
        self.wait(2.0)  # Hold until ~18s

        # Fade everything out
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.5,
        )

        self.pad_to_duration()
