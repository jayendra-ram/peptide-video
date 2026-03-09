"""Reaction coordinate energy diagram with thermodynamic annotations."""

from __future__ import annotations

from typing import List, Tuple

from manim import (
    VGroup,
    Axes,
    Dot,
    DashedLine,
    DoubleArrow,
    Text,
    WHITE,
    GREY,
    YELLOW,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ManimColor,
    np,
)

from src.chemistry.reaction_coordinate import ReactionCoordinate


class ReactionCoordinatePlot(VGroup):
    """Publication-quality reaction coordinate diagram.

    Features:
    - Smooth energy curve plotted on labelled axes
    - Animated pointer dot that traverses the curve
    - Annotations for activation energy (DeltaG-double-dagger) and
      overall free energy change (DeltaG-naught)
    - State labels (Reactants, TS, Products)
    """

    def __init__(
        self,
        coordinate: ReactionCoordinate,
        energy_color: ManimColor | str = "#f1c40f",
        x_length: float = 8.0,
        y_length: float = 4.5,
        x_label: str = "Reaction Coordinate",
        y_label: str = "\u0394G (kJ/mol)",
    ) -> None:
        super().__init__()
        self.coordinate = coordinate
        energy_color = ManimColor(energy_color)

        # Determine y range from data
        samples = [coordinate.sample(p / 50).free_energy for p in range(51)]
        y_min = min(samples) - 1
        y_max = max(samples) + 1

        self.axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[y_min, y_max, 2],
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": GREY, "include_numbers": False},
            tips=False,
        )
        self.add(self.axes)

        # Axis labels
        x_lab = Text(x_label, font_size=28, color=WHITE)
        x_lab.next_to(self.axes.x_axis, DOWN, buff=0.3)
        self.add(x_lab)

        y_lab = Text(y_label, font_size=28, color=WHITE)
        y_lab.next_to(self.axes.y_axis, LEFT, buff=0.3)
        y_lab.rotate(np.pi / 2)
        self.add(y_lab)

        # Energy curve
        self.curve = self.axes.plot(
            lambda x: coordinate.sample(x).free_energy,
            x_range=[0, 1],
            color=energy_color,
            stroke_width=3,
        )
        self.add(self.curve)

        # Find key energies
        reactant_e = coordinate.sample(0.0).free_energy
        product_e = coordinate.sample(1.0).free_energy
        ts_progress = max(
            (p / 50 for p in range(51)),
            key=lambda p: coordinate.sample(p).free_energy,
        )
        ts_e = coordinate.sample(ts_progress).free_energy

        # State labels
        r_label = Text("Reactants", font_size=20, color=WHITE)
        r_label.next_to(self.axes.c2p(0.05, reactant_e), UP + LEFT, buff=0.15)
        self.add(r_label)

        ts_label = Text("TS", font_size=20, color=WHITE)
        ts_label.next_to(self.axes.c2p(ts_progress, ts_e), UP, buff=0.2)
        self.add(ts_label)

        p_label = Text("Products", font_size=20, color=WHITE)
        p_label.next_to(self.axes.c2p(0.95, product_e), UP + RIGHT, buff=0.15)
        self.add(p_label)

        # DeltaG-double-dagger annotation
        r_point = self.axes.c2p(0.25, reactant_e)
        ts_point = self.axes.c2p(0.25, ts_e)
        dg_dagger_arrow = DoubleArrow(
            r_point, ts_point, buff=0, color=YELLOW, stroke_width=2,
            tip_length=0.15,
        )
        self.add(dg_dagger_arrow)

        dg_dagger_label = Text(
            "\u0394G\u2021", font_size=24, color=YELLOW,
        )
        dg_dagger_label.next_to(dg_dagger_arrow, LEFT, buff=0.1)
        self.add(dg_dagger_label)

        # DeltaG-naught annotation
        r2_point = self.axes.c2p(0.85, reactant_e)
        p_point = self.axes.c2p(0.85, product_e)
        dg_naught_arrow = DoubleArrow(
            r2_point, p_point, buff=0, color=WHITE, stroke_width=2,
            tip_length=0.12,
        )
        self.add(dg_naught_arrow)

        dg_naught_label = Text(
            "\u0394G\u00b0", font_size=24, color=WHITE,
        )
        dg_naught_label.next_to(dg_naught_arrow, RIGHT, buff=0.1)
        self.add(dg_naught_label)

        # Dashed reference lines
        r_ref = DashedLine(
            self.axes.c2p(0, reactant_e),
            self.axes.c2p(1, reactant_e),
            stroke_width=1,
            color=GREY,
            dash_length=0.08,
        )
        self.add(r_ref)

        p_ref = DashedLine(
            self.axes.c2p(0, product_e),
            self.axes.c2p(1, product_e),
            stroke_width=1,
            color=GREY,
            dash_length=0.08,
        )
        self.add(p_ref)

        # Pointer dot (for animation)
        self.pointer = Dot(
            self.axes.c2p(0, reactant_e),
            radius=0.08,
            color=energy_color,
        )
        self.add(self.pointer)

    def get_pointer_animation(self, run_time: float = 4.0):
        """Return an animation that moves the pointer along the curve."""
        from manim import MoveAlongPath
        return MoveAlongPath(self.pointer, self.curve, run_time=run_time)
