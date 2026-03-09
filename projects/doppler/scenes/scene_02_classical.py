"""Scene 2: Classical Doppler effect.

Moving source emitting wavefront rings + classical formula.
"""

from __future__ import annotations

from manim import (
    Circle,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    ManimColor,
    RIGHT,
    SurroundingRectangle,
    Text,
    UP,
    VGroup,
    Write,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import classical_doppler


class ClassicalScene(ExplainerSceneBase):
    """13-second scene: classical Doppler formula + wavefronts."""

    def construct(self) -> None:
        # ── Title ───────────────────────────────────────────────────────
        title = Text(
            "Classical Doppler Effect",
            font_size=36, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Moving source with wavefronts (top half) ──────────────────
        source = Dot(
            color=ManimColor("#e74c3c"), radius=0.12,
        ).move_to(LEFT * 4 + UP * 1.5)
        source_label = Text(
            "Source", font_size=22, color=ManimColor("#ecf0f1"),
        ).next_to(source, UP, buff=0.15)

        self.play(FadeIn(source), FadeIn(source_label), run_time=0.5)

        # Emit rings while source moves right
        wavefronts = VGroup()
        n_rings = 5
        total_move = 6.0
        for i in range(n_rings):
            frac = i / n_rings
            src_x = -4.0 + total_move * frac
            ring = Circle(
                radius=0.01, stroke_color=ManimColor("#5dade2"),
                stroke_width=1.5, stroke_opacity=0.5,
            ).move_to([src_x, 1.5, 0])
            wavefronts.add(ring)

        self.add(wavefronts)
        target_pos = RIGHT * 2 + UP * 1.5
        self.play(
            source.animate.move_to(target_pos),
            source_label.animate.move_to(target_pos + UP * 0.35),
            *[
                wavefronts[i].animate.scale_to_fit_width((n_rings - i) * 1.6)
                for i in range(n_rings)
            ],
            run_time=3.5,
        )

        # ── Classical formula (bottom half) ────────────────────────────
        formula = classical_doppler().scale(0.9)
        formula.move_to(DOWN * 1.5)

        self.play(Write(formula), run_time=2.0)

        # Highlight box
        box = SurroundingRectangle(
            formula, color=ManimColor("#f1c40f"),
            buff=0.2, stroke_width=2,
        )
        self.play(Create(box), run_time=0.8)

        # ── Labels ────────────────────────────────────────────────────
        compressed_label = Text(
            "Compressed", font_size=18, color=ManimColor("#3498db"),
        ).move_to(RIGHT * 4.5 + UP * 1.5)
        stretched_label = Text(
            "Stretched", font_size=18, color=ManimColor("#e74c3c"),
        ).move_to(LEFT * 5 + UP * 1.5)

        self.play(
            FadeIn(compressed_label), FadeIn(stretched_label),
            run_time=0.8,
        )

        self.wait(3.6)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in [
                title, source, source_label, wavefronts,
                formula, box, compressed_label, stretched_label,
            ]],
            run_time=1.0,
        )
