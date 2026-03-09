"""Scene 7: Transverse Doppler effect.

Source moves perpendicular to observer — pure time-dilation redshift.
"""

from __future__ import annotations

from manim import (
    Arrow,
    Circle,
    Create,
    DashedLine,
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
from data.equations import transverse_doppler


class TransverseScene(ExplainerSceneBase):
    """12-second scene: transverse Doppler geometry + formula."""

    def construct(self) -> None:
        # ── Title ─────────────────────────────────────────────────────
        title = Text(
            "Transverse Doppler Effect",
            font_size=36, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Observer ──────────────────────────────────────────────────
        observer = Dot(
            color=ManimColor("#2ecc71"), radius=0.12,
        ).move_to(DOWN * 1.5)
        obs_label = Text(
            "Observer", font_size=20, color=ManimColor("#2ecc71"),
        ).next_to(observer, DOWN, buff=0.15)

        self.play(FadeIn(observer), FadeIn(obs_label), run_time=0.5)

        # ── Source moving horizontally ────────────────────────────────
        source = Dot(
            color=ManimColor("#e67e22"), radius=0.12,
        ).move_to(LEFT * 4 + UP * 1.0)
        src_label = Text(
            "Source", font_size=20, color=ManimColor("#e67e22"),
        ).next_to(source, UP, buff=0.15)

        # Velocity arrow
        vel_arrow = Arrow(
            start=LEFT * 0.5, end=RIGHT * 1.5,
            color=ManimColor("#e67e22"), stroke_width=3,
        ).next_to(source, RIGHT, buff=0.1).shift(UP * 0.0)
        vel_label = Text(
            "v", font_size=20, color=ManimColor("#e67e22"),
        ).next_to(vel_arrow, UP, buff=0.1)

        self.play(
            FadeIn(source), FadeIn(src_label),
            Create(vel_arrow), FadeIn(vel_label),
            run_time=0.8,
        )

        # ── Animate source moving across ──────────────────────────────
        target_x = RIGHT * 4 + UP * 1.0
        self.play(
            source.animate.move_to(target_x),
            src_label.animate.move_to(target_x + UP * 0.35),
            vel_arrow.animate.move_to(target_x + RIGHT * 1.2),
            vel_label.animate.move_to(target_x + RIGHT * 1.2 + UP * 0.3),
            run_time=3.0,
        )

        # ── Perpendicular dashed line at closest approach ─────────────
        closest = UP * 1.0  # directly above observer
        perp_line = DashedLine(
            start=observer.get_center(),
            end=closest,
            color=ManimColor("#7f8c8d"),
            stroke_width=2,
        )
        perp_label = Text(
            "90°", font_size=18, color=ManimColor("#7f8c8d"),
        ).next_to(perp_line, RIGHT, buff=0.15)

        self.play(Create(perp_line), FadeIn(perp_label), run_time=0.8)

        # ── Redshifted wavefronts arriving at observer ────────────────
        waves = VGroup()
        for i in range(3):
            ring = Circle(
                radius=0.4 + i * 0.5,
                stroke_color=ManimColor("#e74c3c"),
                stroke_width=1.5, stroke_opacity=0.5,
            ).move_to(observer.get_center())
            waves.add(ring)
        redshift_note = Text(
            "Always a redshift — pure time dilation",
            font_size=20, color=ManimColor("#e74c3c"),
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(waves), FadeIn(redshift_note), run_time=0.8)

        # ── Formula ───────────────────────────────────────────────────
        formula = transverse_doppler().scale(0.85)
        formula.move_to(DOWN * 0.5 + RIGHT * 0)
        box = SurroundingRectangle(
            formula, color=ManimColor("#f1c40f"),
            buff=0.2, stroke_width=2,
        )

        self.play(Write(formula), run_time=1.5)
        self.play(Create(box), run_time=0.5)

        self.wait(1.3)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
