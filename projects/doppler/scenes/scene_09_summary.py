"""Scene 9: Summary — three key equations.

Classical, relativistic, and transverse Doppler formulas stacked vertically.
"""

from __future__ import annotations

from manim import (
    Circle,
    Create,
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
from data.equations import (
    classical_doppler,
    relativistic_doppler_approach,
    transverse_doppler,
)


class SummaryScene(ExplainerSceneBase):
    """10-second summary: three key equations + wavefront fade."""

    def construct(self) -> None:
        # ── Title ─────────────────────────────────────────────────────
        title = Text(
            "Key Equations",
            font_size=36, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.6)

        # ── Equation 1: Classical ─────────────────────────────────────
        label1 = Text(
            "Classical:", font_size=22, color=ManimColor("#7f8c8d"),
        ).move_to(UP * 1.8 + LEFT * 4.0)
        eq1 = classical_doppler().scale(0.75)
        eq1.next_to(label1, RIGHT, buff=0.3)

        self.play(FadeIn(label1), Write(eq1), run_time=1.2)

        # ── Equation 2: Relativistic ──────────────────────────────────
        label2 = Text(
            "Relativistic:", font_size=22, color=ManimColor("#f1c40f"),
        ).move_to(UP * 0.3 + LEFT * 4.0)
        eq2 = relativistic_doppler_approach().scale(0.75)
        eq2.next_to(label2, RIGHT, buff=0.3)

        self.play(FadeIn(label2), Write(eq2), run_time=1.2)

        # Highlight the relativistic formula
        box = SurroundingRectangle(
            VGroup(label2, eq2),
            color=ManimColor("#f1c40f"),
            buff=0.15, stroke_width=2,
        )
        self.play(Create(box), run_time=0.5)

        # ── Equation 3: Transverse ────────────────────────────────────
        label3 = Text(
            "Transverse:", font_size=22, color=ManimColor("#e74c3c"),
        ).move_to(DOWN * 1.2 + LEFT * 4.0)
        eq3 = transverse_doppler().scale(0.75)
        eq3.next_to(label3, RIGHT, buff=0.3)

        self.play(FadeIn(label3), Write(eq3), run_time=1.2)

        # ── Background wavefront fade ─────────────────────────────────
        wavefronts = VGroup()
        for i in range(5):
            ring = Circle(
                radius=0.5 + i * 1.0,
                stroke_color=ManimColor("#5dade2"),
                stroke_width=1, stroke_opacity=0.15,
            )
            wavefronts.add(ring)
        # Send to back
        self.add(wavefronts)
        for m in [title, label1, eq1, label2, eq2, box, label3, eq3]:
            self.bring_to_front(m)

        self.play(FadeIn(wavefronts), run_time=0.5)

        self.wait(1.8)

        # ── Fade out everything ───────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
