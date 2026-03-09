"""Scene 1: Introduction — wavefronts from a moving source.

A dot source emits expanding circles. First stationary (symmetric rings),
then moving right so rings compress ahead and stretch behind.
Title fades in at the end.
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
    Text,
    VGroup,
    Write,
    np,
)

from src.manim.scene_base import ExplainerSceneBase


class IntroScene(ExplainerSceneBase):
    """12-second intro: wavefronts + title."""

    def construct(self) -> None:
        # ── Source dot ──────────────────────────────────────────────────
        source = Dot(color=ManimColor("#3498db"), radius=0.12)
        source.move_to(LEFT * 2)
        self.add(source)

        wavefronts = VGroup()

        # ── Phase 1: stationary source, 3 symmetric rings (3s) ────────
        for i in range(3):
            ring = Circle(
                radius=0.01, stroke_color=ManimColor("#5dade2"),
                stroke_width=2, stroke_opacity=0.7,
            ).move_to(source.get_center())
            wavefronts.add(ring)
            self.play(
                ring.animate.scale_to_fit_width((i + 1) * 2.0),
                run_time=1.0,
            )

        # ── Phase 2: source moves right, emitting compressed/stretched rings (5s)
        self.play(FadeOut(wavefronts), run_time=0.3)
        wavefronts = VGroup()

        emit_interval = 0.7
        n_moving_rings = 6
        total_move = 4.0  # source travels 4 units right
        move_duration = n_moving_rings * emit_interval

        # Create all rings at once, animate them with updaters
        ring_origins = []
        for i in range(n_moving_rings):
            # Source position at emit time
            t_frac = i / n_moving_rings
            src_x = -2.0 + total_move * t_frac
            ring = Circle(
                radius=0.01, stroke_color=ManimColor("#5dade2"),
                stroke_width=2, stroke_opacity=0.6,
            ).move_to([src_x, 0, 0])
            ring_origins.append(src_x)
            wavefronts.add(ring)

        self.add(wavefronts)

        # Animate source moving + rings growing
        from manim import AnimationGroup, MoveAlongPath, Line

        target_pos = RIGHT * 2
        self.play(
            source.animate.move_to(target_pos),
            *[
                wavefronts[i].animate.scale_to_fit_width(
                    (n_moving_rings - i) * 1.2
                )
                for i in range(n_moving_rings)
            ],
            run_time=move_duration,
        )

        # ── Phase 3: Title fade in (2s) ───────────────────────────────
        title = Text(
            "The Relativistic Doppler Effect",
            font_size=48,
            color=ManimColor("#ecf0f1"),
            weight="BOLD",
        ).to_edge(DOWN, buff=1.5)
        self.play(FadeIn(title), run_time=2.0)

        # ── Hold + fade out (remaining ~1.5s) ─────────────────────────
        self.wait(0.5)
        self.play(
            FadeOut(wavefronts), FadeOut(source), FadeOut(title),
            run_time=1.0,
        )
