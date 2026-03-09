"""Scene 6: Blueshift and redshift visualization.

Visible spectrum bar, approaching/receding sources with colored wavefronts.
"""

from __future__ import annotations

from manim import (
    Arrow,
    Circle,
    Create,
    DOWN,
    Dot,
    FadeIn,
    FadeOut,
    LEFT,
    ManimColor,
    Rectangle,
    RIGHT,
    Text,
    UP,
    VGroup,
    Write,
    color_gradient,
    BLUE,
    RED,
)

from src.manim.scene_base import ExplainerSceneBase
from data.equations import wavelength_ratio


class SpectrumScene(ExplainerSceneBase):
    """12-second scene: blueshift and redshift with spectrum bar."""

    def construct(self) -> None:
        # ── Title ─────────────────────────────────────────────────────
        title = Text(
            "Blueshift & Redshift",
            font_size=36, color=ManimColor("#ecf0f1"), weight="BOLD",
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=0.8)

        # ── Spectrum bar (center) ─────────────────────────────────────
        spectrum_colors = [
            "#8b00ff", "#4b0082", "#0000ff", "#00ff00",
            "#ffff00", "#ff7f00", "#ff0000",
        ]
        n_bars = 40
        bar_width = 8.0 / n_bars
        spectrum = VGroup()
        for i in range(n_bars):
            frac = i / (n_bars - 1)
            # Interpolate through spectrum colors
            idx = frac * (len(spectrum_colors) - 1)
            lo = int(idx)
            hi = min(lo + 1, len(spectrum_colors) - 1)
            color = spectrum_colors[lo] if lo == hi else spectrum_colors[hi]
            rect = Rectangle(
                width=bar_width, height=0.5,
                fill_color=ManimColor(spectrum_colors[min(lo, len(spectrum_colors) - 1)]),
                fill_opacity=0.8,
                stroke_width=0,
            ).move_to([i * bar_width - 4.0 + bar_width / 2, 0, 0])
            spectrum.add(rect)

        violet_label = Text("Violet", font_size=16, color=ManimColor("#8b00ff"))
        violet_label.next_to(spectrum, LEFT, buff=0.15).shift(DOWN * 0)
        red_label = Text("Red", font_size=16, color=ManimColor("#ff0000"))
        red_label.next_to(spectrum, RIGHT, buff=0.15)

        self.play(FadeIn(spectrum), FadeIn(violet_label), FadeIn(red_label), run_time=1.0)

        # ── Approaching source (top) — blueshift ──────────────────────
        approach_label = Text(
            "Approaching → Blueshift",
            font_size=22, color=ManimColor("#3498db"),
        ).move_to(UP * 2.0)

        approach_source = Dot(
            color=ManimColor("#3498db"), radius=0.1,
        ).move_to(RIGHT * 3 + UP * 1.2)
        approach_arrow = Arrow(
            start=RIGHT * 3 + UP * 1.2,
            end=LEFT * 1 + UP * 1.2,
            color=ManimColor("#3498db"),
            stroke_width=2,
        )

        # Compressed wavefronts (blue circles, small gaps)
        blue_waves = VGroup()
        for i in range(4):
            ring = Circle(
                radius=0.3 + i * 0.25,
                stroke_color=ManimColor("#3498db"),
                stroke_width=1.5, stroke_opacity=0.6,
            ).move_to(RIGHT * 1 + UP * 1.2)
            blue_waves.add(ring)

        self.play(
            FadeIn(approach_label), FadeIn(approach_source),
            Create(approach_arrow), FadeIn(blue_waves),
            run_time=1.5,
        )

        # ── Receding source (bottom) — redshift ───────────────────────
        recede_label = Text(
            "Receding → Redshift",
            font_size=22, color=ManimColor("#e74c3c"),
        ).move_to(DOWN * 2.0)

        recede_source = Dot(
            color=ManimColor("#e74c3c"), radius=0.1,
        ).move_to(LEFT * 3 + DOWN * 1.2)
        recede_arrow = Arrow(
            start=LEFT * 3 + DOWN * 1.2,
            end=RIGHT * 1 + DOWN * 1.2,
            color=ManimColor("#e74c3c"),
            stroke_width=2,
        )

        # Stretched wavefronts (red circles, wide gaps)
        red_waves = VGroup()
        for i in range(3):
            ring = Circle(
                radius=0.5 + i * 0.6,
                stroke_color=ManimColor("#e74c3c"),
                stroke_width=1.5, stroke_opacity=0.5,
            ).move_to(LEFT * 1 + DOWN * 1.2)
            red_waves.add(ring)

        self.play(
            FadeIn(recede_label), FadeIn(recede_source),
            Create(recede_arrow), FadeIn(red_waves),
            run_time=1.5,
        )

        # ── Wavelength ratio formula ──────────────────────────────────
        ratio = wavelength_ratio().scale(0.7)
        ratio.move_to(DOWN * 3.0)
        self.play(Write(ratio), run_time=1.5)

        self.wait(3.7)

        # ── Fade out ──────────────────────────────────────────────────
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )
