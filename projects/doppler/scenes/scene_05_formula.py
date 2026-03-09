"""Scene 5: Deriving the relativistic Doppler formula.

Three-step derivation:
  1. Classical: f_obs = f_s / (1 - beta)
  2. Multiply by 1/gamma
  3. Simplify to sqrt form
"""

from __future__ import annotations

from manim import (
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    ManimColor,
    ReplacementTransform,
    SurroundingRectangle,
    Text,
    UP,
    Write,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import (
    classical_doppler_beta,
    relativistic_doppler_step1,
    relativistic_doppler_approach,
)


class FormulaScene(ExplainerSceneBase):
    """14-second scene: three-step derivation."""

    def construct(self) -> None:
        # ── Title ─────────────────────────────────────────────────────
        title = Text(
            "Deriving the Relativistic Formula",
            font_size=32, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Step 1: Classical formula ─────────────────────────────────
        step1_label = Text(
            "Step 1: Classical Doppler",
            font_size=22, color=ManimColor("#7f8c8d"),
        ).move_to(UP * 2.0)
        eq1 = classical_doppler_beta().scale(0.9)
        eq1.move_to(UP * 1.0)

        self.play(FadeIn(step1_label), run_time=0.3)
        self.play(Write(eq1), run_time=1.5)
        self.wait(0.5)

        # ── Step 2: Multiply by 1/gamma ───────────────────────────────
        step2_label = Text(
            "Step 2: Multiply by 1/γ for time dilation",
            font_size=22, color=ManimColor("#7f8c8d"),
        ).move_to(UP * 2.0)
        eq2 = relativistic_doppler_step1().scale(0.9)
        eq2.move_to(UP * 1.0)

        self.play(
            FadeOut(step1_label), FadeIn(step2_label),
            ReplacementTransform(eq1, eq2),
            run_time=2.0,
        )
        self.wait(0.5)

        # ── Step 3: Simplify ──────────────────────────────────────────
        step3_label = Text(
            "Step 3: Simplify",
            font_size=22, color=ManimColor("#7f8c8d"),
        ).move_to(UP * 2.0)
        eq3 = relativistic_doppler_approach().scale(1.0)
        eq3.move_to(UP * 1.0)

        self.play(
            FadeOut(step2_label), FadeIn(step3_label),
            ReplacementTransform(eq2, eq3),
            run_time=2.0,
        )

        # ── Highlight the final result ────────────────────────────────
        box = SurroundingRectangle(
            eq3, color=ManimColor("#f1c40f"),
            buff=0.25, stroke_width=3,
        )
        self.play(Create(box), run_time=0.8)

        # Final note
        note = Text(
            "Flip β sign for recession",
            font_size=20, color=ManimColor("#7f8c8d"),
        ).next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(note), run_time=0.5)

        self.wait(3.1)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
