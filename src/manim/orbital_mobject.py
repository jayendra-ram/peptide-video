"""Orbital lobe and energy level diagram mobjects."""

from __future__ import annotations

from typing import List, Optional, Tuple

from manim import (
    VGroup,
    Ellipse,
    Line,
    DashedLine,
    Arrow,
    Dot,
    Text,
    MathTex,
    WHITE,
    GREY,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ManimColor,
    np,
)


class OrbitalLobe(VGroup):
    """Coloured ellipse representing an orbital lobe (HOMO or LUMO)."""

    def __init__(
        self,
        center: np.ndarray,
        width: float = 0.6,
        height: float = 0.9,
        color: ManimColor | str = "#6c5ce7",
        opacity: float = 0.35,
        label: Optional[str] = None,
    ) -> None:
        super().__init__()
        center = np.array(center, dtype=float)
        ellipse = Ellipse(width=width, height=height)
        ellipse.set_fill(ManimColor(color), opacity=opacity)
        ellipse.set_stroke(ManimColor(color), width=2, opacity=0.8)
        ellipse.move_to(center)
        self.ellipse = ellipse
        self.add(ellipse)

        if label:
            txt = Text(label, font_size=18, color=WHITE)
            txt.next_to(ellipse, UP, buff=0.1)
            self.label_text = txt
            self.add(txt)


class EnergyLevelDiagram(VGroup):
    """HOMO/LUMO energy level diagram with horizontal lines, electron dots,
    and connecting arrows.

    Parameters
    ----------
    levels : list of (name, energy, color, n_electrons)
        Each level is drawn as a horizontal line at a relative y-position
        proportional to *energy*. *n_electrons* dots are placed on the line.
    width : float
        Width of each energy level line.
    height : float
        Total height of the diagram.
    show_arrow : bool
        If True, draw a dashed arrow between the two levels labelled ``delta_e``.
    """

    def __init__(
        self,
        levels: List[Tuple[str, float, str, int]],
        width: float = 2.5,
        height: float = 3.0,
        show_arrow: bool = True,
    ) -> None:
        super().__init__()

        if not levels:
            return

        energies = [e for _, e, _, _ in levels]
        e_min, e_max = min(energies), max(energies)
        e_range = e_max - e_min or 1.0

        self.level_lines = {}

        for name, energy, color, n_electrons in levels:
            y = ((energy - e_min) / e_range - 0.5) * height
            line = Line(
                LEFT * width / 2 + UP * y,
                RIGHT * width / 2 + UP * y,
                stroke_width=3,
                color=ManimColor(color),
            )
            self.level_lines[name] = line
            self.add(line)

            # Label
            label = Text(name, font_size=16, color=ManimColor(color))
            label.next_to(line, RIGHT, buff=0.2)
            self.add(label)

            # Electron dots
            spacing = 0.2
            start_x = -spacing * (n_electrons - 1) / 2
            for i in range(n_electrons):
                dot = Dot(
                    point=line.get_center() + np.array([start_x + i * spacing, 0.1, 0]),
                    radius=0.06,
                    color=WHITE,
                )
                self.add(dot)

        # Arrow between first and last level
        if show_arrow and len(levels) >= 2:
            low_line = self.level_lines[levels[0][0]]
            high_line = self.level_lines[levels[-1][0]]
            arrow = DashedLine(
                low_line.get_center() + LEFT * (width / 2 + 0.3),
                high_line.get_center() + LEFT * (width / 2 + 0.3),
                stroke_width=2,
                color=GREY,
                dash_length=0.08,
            )
            self.add(arrow)

            delta_label = MathTex(r"\Delta E", font_size=24, color=WHITE)
            delta_label.next_to(arrow, LEFT, buff=0.1)
            self.add(delta_label)
