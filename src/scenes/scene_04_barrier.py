"""Scene 4: free-energy barrier.

Reaction coordinate energy diagram with animated pointer and thermodynamic equations.
"""

from __future__ import annotations

import sys
from pathlib import Path

from manim import (
    DOWN,
    FadeIn,
    FadeOut,
    MathTex,
    Text,
    UP,
    WHITE,
    Write,
    np,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_04_barrier"

from src.manim.scene_base import PeptideSceneBase
from src.manim.energy_diagram import ReactionCoordinatePlot
from src.manim.equation_helpers import gibbs_equation, arrhenius_equation
from src.chemistry.reaction_coordinate import (
    ReactionCoordinate,
    ReactionCoordinatePoint,
)


class BarrierScene(PeptideSceneBase):
    """12-second scene: reaction coordinate diagram with thermodynamic annotations."""

    def construct(self) -> None:
        # ── Build energy profile ──────────────────────────────────────────
        coordinate = ReactionCoordinate(
            points=[
                ReactionCoordinatePoint(progress=0.0, free_energy=1.0),
                ReactionCoordinatePoint(progress=0.2, free_energy=2.0),
                ReactionCoordinatePoint(progress=0.4, free_energy=6.5),
                ReactionCoordinatePoint(progress=0.5, free_energy=7.0),
                ReactionCoordinatePoint(progress=0.6, free_energy=6.5),
                ReactionCoordinatePoint(progress=0.8, free_energy=1.5),
                ReactionCoordinatePoint(progress=1.0, free_energy=0.0),
            ]
        )

        plot = ReactionCoordinatePlot(
            coordinate,
            energy_color=self.ENERGY_COLOR,
            x_length=8.0,
            y_length=4.5,
        )
        plot.move_to(UP * 0.3)

        # ── Step 1: Show axes + curve (2s) ────────────────────────────────
        self.play(FadeIn(plot), run_time=2.0)

        # ── Step 2: Animate pointer along curve (3s) ──────────────────────
        self.play(plot.get_pointer_animation(run_time=3.0))

        # ── Step 3: Write barrier annotation (1.5s) ───────────────────────
        barrier_label = MathTex(
            r"\Delta G^{\ddagger} \approx 80 \;\text{kJ/mol}",
            font_size=26,
            color=self.ENERGY_COLOR,
        )
        # Place near the top of the barrier (TS region)
        ts_point = plot.axes.c2p(0.5, 7.0)
        barrier_label.next_to(ts_point, UP + np.array([1.0, 0, 0]), buff=0.3)
        self.play(Write(barrier_label), run_time=1.5)

        # ── Step 4: Write Gibbs equation (1.5s) ───────────────────────────
        gibbs_eq = gibbs_equation(font_size=28, color=WHITE)
        gibbs_eq.to_edge(DOWN, buff=1.2)
        self.play(Write(gibbs_eq), run_time=1.5)

        # ── Step 5: Write Arrhenius equation (1.5s) ───────────────────────
        arr_eq = arrhenius_equation(font_size=28, color=WHITE)
        arr_eq.next_to(gibbs_eq, DOWN, buff=0.3)
        self.play(Write(arr_eq), run_time=1.5)

        # ── Step 6: Wait remaining ────────────────────────────────────────
        # Total so far: 2.0 + 3.0 + 1.5 + 1.5 + 1.5 = 9.5s
        # Need 12s total, minus 1s for fade out = 1.5s remaining
        self.wait(1.5)

        # ── Step 7: FadeOut (1s) ──────────────────────────────────────────
        self.play(
            FadeOut(plot),
            FadeOut(barrier_label),
            FadeOut(gibbs_eq),
            FadeOut(arr_eq),
            run_time=1.0,
        )
